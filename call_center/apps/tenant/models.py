# apps/tenant/models.py
from django.db import models
from django_tenants.models import TenantMixin, DomainMixin
from django.utils.translation import gettext_lazy as _


class Tenant(TenantMixin):
    """
    Tenant model for multi-tenancy support.
    Each tenant represents a separate organization using the call center system.
    """
    # Basic Information
    name = models.CharField(
        max_length=100, 
        verbose_name=_("Organization Name"),
        help_text=_("Name of the organization")
    )
    description = models.TextField(
        blank=True, 
        verbose_name=_("Description"),
        help_text=_("Brief description of the organization")
    )
    
    # Contact Information
    contact_email = models.EmailField(
        blank=True,
        verbose_name=_("Contact Email"),
        help_text=_("Primary contact email for the organization")
    )
    contact_phone = models.CharField(
        max_length=20, 
        blank=True,
        verbose_name=_("Contact Phone"),
        help_text=_("Primary contact phone number")
    )
    contact_person = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Contact Person"),
        help_text=_("Primary contact person name")
    )
    
    # Address Information
    address_line1 = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Address Line 1")
    )
    address_line2 = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Address Line 2")
    )
    city = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("City")
    )
    state = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("State/Province")
    )
    postal_code = models.CharField(
        max_length=20,
        blank=True,
        verbose_name=_("Postal Code")
    )
    country = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Country")
    )
    
    # Configuration Settings
    timezone = models.CharField(
        max_length=50, 
        default='UTC',
        verbose_name=_("Timezone"),
        help_text=_("Default timezone for the organization")
    )
    language = models.CharField(
        max_length=10, 
        default='en',
        verbose_name=_("Language"),
        help_text=_("Default language for the organization")
    )
    currency = models.CharField(
        max_length=3,
        default='USD',
        verbose_name=_("Currency"),
        help_text=_("Default currency (ISO 4217 code)")
    )
    
    # Subscription and Limits
    subscription_plan = models.CharField(
        max_length=50,
        default='basic',
        verbose_name=_("Subscription Plan"),
        choices=[
            ('basic', _('Basic')),
            ('professional', _('Professional')),
            ('enterprise', _('Enterprise')),
            ('custom', _('Custom')),
        ]
    )
    max_users = models.PositiveIntegerField(
        default=10,
        verbose_name=_("Maximum Users"),
        help_text=_("Maximum number of users allowed")
    )
    max_contacts = models.PositiveIntegerField(
        default=1000,
        verbose_name=_("Maximum Contacts"),
        help_text=_("Maximum number of contacts allowed")
    )
    max_campaigns = models.PositiveIntegerField(
        default=5,
        verbose_name=_("Maximum Campaigns"),
        help_text=_("Maximum number of active campaigns")
    )
    storage_limit_gb = models.PositiveIntegerField(
        default=1,
        verbose_name=_("Storage Limit (GB)"),
        help_text=_("Storage limit in gigabytes")
    )
    
    # Billing Information
    billing_email = models.EmailField(
        blank=True,
        verbose_name=_("Billing Email")
    )
    billing_contact = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Billing Contact")
    )
    
    # Features Enabled
    features = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("Enabled Features"),
        help_text=_("JSON object containing enabled features")
    )
    
    # Status and Dates
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Is Active"),
        help_text=_("Whether the tenant is currently active")
    )
    is_trial = models.BooleanField(
        default=False,
        verbose_name=_("Is Trial"),
        help_text=_("Whether this is a trial account")
    )
    trial_end_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Trial End Date")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created At")
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated At")
    )
    
    # Settings for django-tenants
    auto_create_schema = True
    auto_drop_schema = True
    
    class Meta:
        verbose_name = _("Tenant")
        verbose_name_plural = _("Tenants")
        ordering = ['name']
        indexes = [
            models.Index(fields=['schema_name']),
            models.Index(fields=['is_active', 'created_at']),
            models.Index(fields=['subscription_plan']),
        ]
    
    def __str__(self):
        return self.name
    
    @property
    def is_trial_expired(self):
        """Check if trial has expired"""
        if not self.is_trial or not self.trial_end_date:
            return False
        from django.utils import timezone
        return timezone.now() > self.trial_end_date
    
    @property
    def days_until_trial_expiry(self):
        """Get days until trial expires"""
        if not self.is_trial or not self.trial_end_date:
            return None
        from django.utils import timezone
        delta = self.trial_end_date - timezone.now()
        return max(0, delta.days)
    
    def get_feature(self, feature_name, default=False):
        """Get a specific feature setting"""
        return self.features.get(feature_name, default)
    
    def set_feature(self, feature_name, value):
        """Set a specific feature setting"""
        if not self.features:
            self.features = {}
        self.features[feature_name] = value
        self.save(update_fields=['features'])
    
    def get_usage_stats(self):
        """Get current usage statistics"""
        # This will be implemented later when we have the related models
        return {
            'users_count': 0,  # User.objects.count() when available
            'contacts_count': 0,  # Contact.objects.count() when available
            'campaigns_count': 0,  # Campaign.objects.count() when available
            'storage_used_gb': 0,  # Calculate storage usage
        }


class Domain(DomainMixin):
    """
    Domain model for tenant routing.
    Each tenant can have multiple domains pointing to it.
    """
    
    class Meta:
        verbose_name = _("Domain")
        verbose_name_plural = _("Domains")
    
    def __str__(self):
        return self.domain


class TenantSetting(models.Model):
    """
    Tenant-specific settings that can be customized per tenant.
    """
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name='settings',
        verbose_name=_("Tenant")
    )
    key = models.CharField(
        max_length=100,
        verbose_name=_("Setting Key")
    )
    value = models.TextField(
        verbose_name=_("Setting Value")
    )
    value_type = models.CharField(
        max_length=20,
        default='string',
        choices=[
            ('string', _('String')),
            ('integer', _('Integer')),
            ('float', _('Float')),
            ('boolean', _('Boolean')),
            ('json', _('JSON')),
        ],
        verbose_name=_("Value Type")
    )
    description = models.TextField(
        blank=True,
        verbose_name=_("Description")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created At")
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated At")
    )
    
    class Meta:
        verbose_name = _("Tenant Setting")
        verbose_name_plural = _("Tenant Settings")
        unique_together = ['tenant', 'key']
        indexes = [
            models.Index(fields=['tenant', 'key']),
        ]
    
    def __str__(self):
        return f"{self.tenant.name} - {self.key}"
    
    def get_value(self):
        """Get the properly typed value"""
        if self.value_type == 'integer':
            return int(self.value)
        elif self.value_type == 'float':
            return float(self.value)
        elif self.value_type == 'boolean':
            return self.value.lower() in ('true', '1', 'yes', 'on')
        elif self.value_type == 'json':
            import json
            return json.loads(self.value)
        return self.value
    
    def set_value(self, value):
        """Set the value with proper type conversion"""
        if self.value_type == 'json':
            import json
            self.value = json.dumps(value)
        else:
            self.value = str(value)