from django.db import models
from django.core.cache import cache
from django.core.validators import validate_slug
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
import json
import uuid
from jsonschema import validate as jsonschema_validate
from apps.shared.core.models import BaseModel



class ReferenceDataType(BaseModel):
    """
    Master table of all reference data types available in the system.
    Defines the types of reference data that can be created.
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text=_("Unique name identifier for this reference data type (e.g., 'product_categories')")
    )
    description = models.TextField(
        blank=True,
        help_text=_("Description of what this reference data type represents")
    )
    is_tenant_specific = models.BooleanField(
        default=True,
        help_text=_("Whether this data type can have tenant-specific values")
    )
    is_system_managed = models.BooleanField(
        default=False,
        help_text=_("If True, this type is managed by the system and cannot be modified via API")
    )
    allowed_metadata_keys = ArrayField(
        models.CharField(max_length=50),
        blank=True,
        null=True,
        help_text=_("List of allowed keys in the metadata JSON field")
    )
    validation_schema = models.JSONField(
        blank=True,
        null=True,
        help_text=_("JSON schema for validating the metadata field")
    )

    class Meta:
        verbose_name = _("Reference Data Type")
        verbose_name_plural = _("Reference Data Types")
        ordering = ['name']

    def __str__(self):
        return self.name

    def clean(self):
        """Validate that system-managed types aren't tenant-specific"""
        if self.is_system_managed and self.is_tenant_specific:
            raise ValidationError(_("System-managed types cannot be tenant-specific"))

class ReferenceData(BaseModel):
    """
    Base model for all tenant-specific reference data entries.
    Represents individual values within a reference data type.
    """
    tenant = models.ForeignKey(
        'tenants.Tenant',
        on_delete=models.CASCADE,
        related_name='reference_data'
    )
    data_type = models.ForeignKey(
        ReferenceDataType,
        on_delete=models.PROTECT,
        related_name='entries',
        help_text=_("Type of reference data this entry belongs to")
    )
    code = models.CharField(
        max_length=50,
        help_text=_("Unique code identifier within this data type and tenant")
    )
    display_value = models.CharField(
        max_length=255,
        help_text=_("Human-readable display value")
    )
    description = models.TextField(
        blank=True,
        help_text=_("Detailed description of this entry")
    )
    is_active = models.BooleanField(
        default=True,
        help_text=_("Whether this entry is active and available for use")
    )
    sort_order = models.IntegerField(
        default=0,
        help_text=_("Sort order for display purposes")
    )
    metadata = models.JSONField(
        default=dict,
        blank=True,
        help_text=_("Additional attributes specific to this entry")
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='children',
        help_text=_("Parent entry for hierarchical data")
    )
    version = models.PositiveIntegerField(
        default=1,
        help_text=_("Version number for optimistic concurrency control")
    )

    class Meta:
        verbose_name = _("Reference Data")
        verbose_name_plural = _("Reference Data")
        unique_together = [['tenant', 'data_type', 'code']]
        ordering = ['data_type', 'sort_order', 'display_value']
        indexes = [
            models.Index(fields=['tenant', 'data_type', 'is_active']),
            models.Index(fields=['tenant', 'data_type', 'code']),
        ]

    def __str__(self):
        return f"{self.data_type.name}: {self.display_value} ({self.code})"

    def clean(self):
        """Validate the reference data entry"""
        # Validate metadata against allowed keys and schema
        if self.data_type.allowed_metadata_keys:
            for key in self.metadata.keys():
                if key not in self.data_type.allowed_metadata_keys:
                    raise ValidationError(
                        _("Metadata key '%(key)s' is not allowed for this data type"),
                        params={'key': key}
                    )
        
        if self.data_type.validation_schema:
            try:
                jsonschema_validate(self.metadata, self.data_type.validation_schema)
            except Exception as e:
                raise ValidationError(_(f"Metadata validation error: {str(e)}"))

        # Validate tenant-specific constraint
        if not self.data_type.is_tenant_specific and self.tenant != get_public_tenant():
            raise ValidationError(
                _("This data type is not tenant-specific and can only be created for the public tenant")
            )

    def save(self, *args, **kwargs):
        """Override save to handle versioning and cache invalidation"""
        if self.pk:
            self.version += 1
        
        self.full_clean()
        super().save(*args, **kwargs)
        
        # Invalidate cache for this data type
        # cache_key = f"ref_data_{self.tenant.id}_{self.data_type.name}"
        cache.delete(cache_key)

    def delete(self, *args, **kwargs):
        """Override delete to handle cache invalidation"""
        # cache_key = f"ref_data_{self.tenant.id}_{self.data_type.name}"
        cache.delete(cache_key)
        super().delete(*args, **kwargs)

class ReferenceDataHistory(BaseModel):
    """
    Audit history for reference data changes.
    Tracks all modifications to reference data entries.
    """
    reference_data = models.ForeignKey(
        ReferenceData,
        on_delete=models.CASCADE,
        related_name='history'
    )
    version = models.PositiveIntegerField()
    change_reason = models.CharField(
        max_length=255,
        blank=True,
        help_text=_("Reason for the change")
    )
    changed_fields = models.JSONField()
    previous_state = models.JSONField()

    class Meta:
        verbose_name = _("Reference Data History")
        verbose_name_plural = _("Reference Data Histories")
        ordering = ['-created_at']
        get_latest_by = 'created_at'

    def __str__(self):
        return f"{self.reference_data} - v{self.version}"

def get_public_tenant():
    """Helper function to get the public tenant"""
    # return Tenant.objects.filter(schema_name='public').first()