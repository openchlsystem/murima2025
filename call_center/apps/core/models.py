# apps/core/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth import get_user_model
import uuid


class TimeStampedModel(models.Model):
    """Base model with created and updated timestamps."""
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))
    
    class Meta:
        abstract = True


class UserStampedModel(TimeStampedModel):
    """Base model with created by user and updated by user tracking."""
    created_by = models.ForeignKey(
        'accounts.User', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name="%(class)s_created",
        verbose_name=_("Created by")
    )
    updated_by = models.ForeignKey(
        'accounts.User', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name="%(class)s_updated",
        verbose_name=_("Updated by")
    )
    
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """Override save to automatically set updated_by"""
        user = kwargs.pop('user', None)
        if user:
            if not self.pk:  # New object
                self.created_by = user
            self.updated_by = user
        super().save(*args, **kwargs)


class ActiveManager(models.Manager):
    """Manager that returns only active records"""
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class SoftDeleteManager(models.Manager):
    """Manager that includes soft-deleted records"""
    def get_queryset(self):
        return super().get_queryset()

    def active(self):
        """Return only active records"""
        return self.get_queryset().filter(is_active=True, deleted_at__isnull=True)

    def deleted(self):
        """Return only soft-deleted records"""
        return self.get_queryset().filter(is_active=False, deleted_at__isnull=False)


class SoftDeleteModel(UserStampedModel):
    """
    Abstract model that provides soft delete functionality
    """
    is_active = models.BooleanField(default=True, verbose_name=_("Is active"))
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name=_("Deleted at"))
    deleted_by = models.ForeignKey(
        'accounts.User', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name="%(class)s_deleted",
        verbose_name=_("Deleted by")
    )

    objects = SoftDeleteManager()  # Default manager (includes deleted)
    active_objects = ActiveManager()  # Active records only

    class Meta:
        abstract = True

    def soft_delete(self, user=None):
        """Soft delete the record"""
        self.is_active = False
        self.deleted_at = timezone.now()
        if user:
            self.deleted_by = user
        self.save()

    def restore(self, user=None):
        """Restore a soft-deleted record"""
        self.is_active = True
        self.deleted_at = None
        self.deleted_by = None
        if user:
            self.updated_by = user
        self.save()

    def delete(self, using=None, keep_parents=False, hard_delete=False):
        """Override delete to perform soft delete by default"""
        if hard_delete:
            super().delete(using=using, keep_parents=keep_parents)
        else:
            self.soft_delete()


class UUIDModel(models.Model):
    """Base model with UUID primary key"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    class Meta:
        abstract = True


class ReferenceDataManager(ActiveManager):
    """Custom manager for reference data"""
    
    def by_category(self, category):
        """Get all active reference data by category"""
        return self.get_queryset().filter(category=category)
    
    def root_items(self, category=None):
        """Get root level items (no parent)"""
        qs = self.get_queryset().filter(parent__isnull=True)
        if category:
            qs = qs.filter(category=category)
        return qs
    
    def children_of(self, parent_id):
        """Get children of a specific parent"""
        return self.get_queryset().filter(parent_id=parent_id)


class ReferenceData(SoftDeleteModel):
    """Model for all reference/lookup data."""
    category = models.CharField(
        max_length=50, 
        verbose_name=_("Category"),
        help_text=_("Category this reference data belongs to")
    )
    code = models.CharField(
        max_length=50, 
        blank=True, 
        null=True, 
        verbose_name=_("Code"),
        help_text=_("Unique code for this reference item")
    )
    name = models.CharField(
        max_length=255, 
        verbose_name=_("Name"),
        help_text=_("Display name for this reference item")
    )
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name="children",
        verbose_name=_("Parent"),
        help_text=_("Parent reference data for hierarchical structure")
    )
    level = models.IntegerField(
        default=0, 
        verbose_name=_("Level"),
        help_text=_("Hierarchy level (0 = root)")
    )
    sort_order = models.IntegerField(
        default=0,
        verbose_name=_("Sort Order"),
        help_text=_("Order for displaying items")
    )
    description = models.TextField(
        blank=True, 
        null=True, 
        verbose_name=_("Description"),
        help_text=_("Additional description or notes")
    )
    
    # Additional metadata
    metadata = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("Metadata"),
        help_text=_("Additional data stored as JSON")
    )
    
    objects = ReferenceDataManager()
    
    class Meta:
        verbose_name = _("Reference Data")
        verbose_name_plural = _("Reference Data")
        ordering = ['category', 'level', 'sort_order', 'name']
        indexes = [
            models.Index(fields=['category', 'is_active']),
            models.Index(fields=['category', 'parent']),
            models.Index(fields=['category', 'code']),
            models.Index(fields=['level', 'sort_order']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['category', 'code'],
                condition=models.Q(code__isnull=False, is_active=True),
                name='unique_active_category_code'
            )
        ]
    
    def __str__(self):
        return f"{self.category}: {self.name}"
    
    def clean(self):
        """Validate the model"""
        if self.parent and self.parent.category != self.category:
            raise ValidationError(_("Parent must be from the same category"))
        
        if self.parent == self:
            raise ValidationError(_("An item cannot be its own parent"))
    
    def save(self, *args, **kwargs):
        """Override save to calculate level automatically"""
        if self.parent:
            self.level = self.parent.level + 1
        else:
            self.level = 0
        
        self.full_clean()
        super().save(*args, **kwargs)
    
    @property
    def full_path(self):
        """Get the full hierarchical path"""
        if self.parent:
            return f"{self.parent.full_path} > {self.name}"
        return self.name
    
    @property
    def has_children(self):
        """Check if this item has children"""
        return self.children.filter(is_active=True).exists()
    
    def get_descendants(self, include_self=False):
        """Get all descendants of this item"""
        descendants = []
        if include_self:
            descendants.append(self)
        
        for child in self.children.filter(is_active=True):
            descendants.extend(child.get_descendants(include_self=True))
        
        return descendants
    
    def get_ancestors(self, include_self=False):
        """Get all ancestors of this item"""
        ancestors = []
        if include_self:
            ancestors.append(self)
        
        if self.parent:
            ancestors.extend(self.parent.get_ancestors(include_self=True))
        
        return ancestors


class AuditLog(TimeStampedModel):
    """Model for tracking changes to important data"""
    
    ACTION_CHOICES = [
        ('create', _('Create')),
        ('update', _('Update')),
        ('delete', _('Delete')),
        ('restore', _('Restore')),
        ('login', _('Login')),
        ('logout', _('Logout')),
        ('access', _('Access')),
        ('export', _('Export')),
        ('import', _('Import')),
    ]
    
    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("User")
    )
    action = models.CharField(
        max_length=20,
        choices=ACTION_CHOICES,
        verbose_name=_("Action")
    )
    content_type = models.ForeignKey(
        'contenttypes.ContentType',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_("Content Type")
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    object_repr = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Object Representation")
    )
    changes = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("Changes"),
        help_text=_("JSON representation of what changed")
    )
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name=_("IP Address")
    )
    user_agent = models.TextField(
        blank=True,
        verbose_name=_("User Agent")
    )
    additional_info = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("Additional Info")
    )
    
    class Meta:
        verbose_name = _("Audit Log")
        verbose_name_plural = _("Audit Logs")
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['action', '-created_at']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return f"{self.user} {self.action} {self.object_repr} at {self.created_at}"


class Setting(SoftDeleteModel):
    """Model for storing application settings"""
    
    SETTING_TYPES = [
        ('string', _('String')),
        ('integer', _('Integer')),
        ('float', _('Float')),
        ('boolean', _('Boolean')),
        ('json', _('JSON')),
        ('text', _('Text')),
    ]
    
    key = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_("Key"),
        help_text=_("Unique identifier for this setting")
    )
    value = models.TextField(
        verbose_name=_("Value"),
        help_text=_("The setting value")
    )
    setting_type = models.CharField(
        max_length=20,
        choices=SETTING_TYPES,
        default='string',
        verbose_name=_("Type")
    )
    category = models.CharField(
        max_length=50,
        default='general',
        verbose_name=_("Category")
    )
    description = models.TextField(
        blank=True,
        verbose_name=_("Description")
    )
    is_sensitive = models.BooleanField(
        default=False,
        verbose_name=_("Is Sensitive"),
        help_text=_("Whether this setting contains sensitive information")
    )
    
    class Meta:
        verbose_name = _("Setting")
        verbose_name_plural = _("Settings")
        ordering = ['category', 'key']
        indexes = [
            models.Index(fields=['category', 'is_active']),
            models.Index(fields=['key']),
        ]
    
    def __str__(self):
        return f"{self.category}.{self.key}"
    
    def get_value(self):
        """Get the properly typed value"""
        if self.setting_type == 'integer':
            return int(self.value)
        elif self.setting_type == 'float':
            return float(self.value)
        elif self.setting_type == 'boolean':
            return self.value.lower() in ('true', '1', 'yes', 'on')
        elif self.setting_type == 'json':
            import json
            return json.loads(self.value)
        return self.value
    
    def set_value(self, value):
        """Set the value with proper type conversion"""
        if self.setting_type == 'json':
            import json
            self.value = json.dumps(value)
        else:
            self.value = str(value)


class Country(SoftDeleteModel):
    """Country reference data"""
    name = models.CharField(max_length=100, unique=True, verbose_name=_("Name"))
    code = models.CharField(max_length=2, unique=True, verbose_name=_("ISO Code"))
    code3 = models.CharField(max_length=3, unique=True, verbose_name=_("ISO3 Code"))
    phone_code = models.CharField(max_length=10, verbose_name=_("Phone Code"))
    
    class Meta:
        verbose_name = _("Country")
        verbose_name_plural = _("Countries")
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Language(SoftDeleteModel):
    """Language reference data"""
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    code = models.CharField(max_length=5, unique=True, verbose_name=_("Code"))
    native_name = models.CharField(max_length=100, blank=True, verbose_name=_("Native Name"))
    
    class Meta:
        verbose_name = _("Language")
        verbose_name_plural = _("Languages")
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Location(SoftDeleteModel):
    """Hierarchical location model (Country > Region > District > etc.)"""
    
    LOCATION_TYPES = [
        ('country', _('Country')),
        ('region', _('Region')),
        ('district', _('District')),
        ('county', _('County')),
        ('subcounty', _('Subcounty')),
        ('parish', _('Parish')),
        ('village', _('Village')),
        ('city', _('City')),
        ('town', _('Town')),
    ]
    
    name = models.CharField(max_length=255, verbose_name=_("Name"))
    location_type = models.CharField(
        max_length=20,
        choices=LOCATION_TYPES,
        verbose_name=_("Type")
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name=_("Parent Location")
    )
    code = models.CharField(
        max_length=20,
        blank=True,
        verbose_name=_("Code")
    )
    level = models.IntegerField(default=0, verbose_name=_("Level"))
    
    class Meta:
        verbose_name = _("Location")
        verbose_name_plural = _("Locations")
        ordering = ['level', 'name']
        indexes = [
            models.Index(fields=['location_type', 'is_active']),
            models.Index(fields=['parent', 'is_active']),
            models.Index(fields=['level', 'name']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.get_location_type_display()})"
    
    def save(self, *args, **kwargs):
        """Auto-calculate level based on parent"""
        if self.parent:
            self.level = self.parent.level + 1
        else:
            self.level = 0
        super().save(*args, **kwargs)
    
    @property
    def full_path(self):
        """Get full location path"""
        if self.parent:
            return f"{self.parent.full_path} > {self.name}"
        return self.name