from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone
from tenants.models import Tenant

User = get_user_model()


# 🔁 Common Mixin for timestamps
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# ⚙️ System Configuration (Singleton)
class SystemConfiguration(TimeStampedModel):
    maintenance_mode = models.BooleanField(default=False, help_text="Only admins can access when enabled")
    allow_new_signups = models.BooleanField(default=True, help_text="Allow new user registrations")
    
    default_ai_provider = models.CharField(
        max_length=50,
        choices=[
            ('OPENAI', 'OpenAI'),
            ('HUGGINGFACE', 'Hugging Face'),
            ('ANTHROPIC', 'Anthropic'),
            ('LOCAL', 'Local Model'),
        ],
        default='OPENAI'
    )

    ai_provider_settings = models.JSONField(default=dict, blank=True, help_text="Provider-specific config")

    case_number_prefix = models.CharField(max_length=10, default='CASE')
    case_number_counter = models.PositiveIntegerField(default=1)
    
    default_case_priority = models.CharField(
        max_length=20,
        choices=[
            ('LOW', 'Low'),
            ('MEDIUM', 'Medium'),
            ('HIGH', 'High'),
            ('CRITICAL', 'Critical')
        ],
        default='MEDIUM'
    )

    class Meta:
        verbose_name = "System Configuration"

    def save(self, *args, **kwargs):
        if not self.pk and SystemConfiguration.objects.exists():
            raise ValidationError("Only one SystemConfiguration instance allowed.")
        super().save(*args, **kwargs)

    def __str__(self):
        return "System Configuration"

    @classmethod
    def get_solo(cls):
        return cls.objects.first()

    def generate_case_number(self):
        case_number = f"{self.case_number_prefix}{self.case_number_counter:06}"
        self.case_number_counter += 1
        self.save(update_fields=['case_number_counter'])
        return case_number


# 🏢 Per-Tenant Configuration
class TenantConfiguration(TimeStampedModel):
    tenant = models.OneToOneField(Tenant, on_delete=models.CASCADE, related_name='configuration')
    custom_domain = models.CharField(max_length=255, blank=True)
    enabled_modules = models.JSONField(default=list)
    custom_categories = models.JSONField(default=dict, blank=True)
    case_workflow = models.JSONField(default=list)
    default_assignee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"TenantConfig: {self.tenant.name}"


# 🔍 Audit Trail
class AuditLog(TimeStampedModel):
    ACTION_CHOICES = [
        ('CREATE', 'Create'),
        ('UPDATE', 'Update'),
        ('DELETE', 'Delete'),
        ('LOGIN', 'Login'),
        ('LOGOUT', 'Logout'),
        ('ACCESS', 'Access'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    model_name = models.CharField(max_length=50, db_index=True)
    object_id = models.CharField(max_length=36, db_index=True, blank=True, null=True)
    metadata = models.JSONField(default=dict)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['model_name', 'object_id']),
            models.Index(fields=['action', 'timestamp']),
        ]

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_action_display()} by {self.user} on {self.model_name}"


# 🏷️ Category Typing System
class CategoryType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    tenant_specific = models.BooleanField(default=False)
    system_managed = models.BooleanField(default=False)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Category(models.Model):
    category_type = models.ForeignKey(CategoryType, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)
    metadata = models.JSONField(default=dict, blank=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['category_type', 'sort_order', 'name']
        unique_together = ('category_type', 'name')
        constraints = [
            models.CheckConstraint(check=~models.Q(parent=models.F('id')), name='no_self_parent')
        ]

    def clean(self):
        if self.parent and self.parent.category_type != self.category_type:
            raise ValidationError("Parent category must be of the same type.")

    def __str__(self):
        return f"{self.category_type.name}: {self.name}"


# 🔔 System Notifications
class SystemNotification(TimeStampedModel):
    SEVERITY_CHOICES = [
        ('INFO', 'Information'),
        ('WARNING', 'Warning'),
        ('ERROR', 'Error'),
        ('CRITICAL', 'Critical'),
    ]

    title = models.CharField(max_length=200)
    message = models.TextField()
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default='INFO')
    is_active = models.BooleanField(default=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    affected_tenants = models.ManyToManyField(Tenant, blank=True)

    class Meta:
        ordering = ['-start_date']

    def clean(self):
        if self.end_date and self.end_date <= self.start_date:
            raise ValidationError("End date must be after start date.")

    def __str__(self):
        return f"{self.get_severity_display()}: {self.title}"
