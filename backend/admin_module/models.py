from django.db import models
from tenants.models import Tenant
from django.contrib.auth import get_user_model

User = get_user_model()

class SystemConfiguration(models.Model):
    """Global system settings"""
    maintenance_mode = models.BooleanField(default=False)
    allow_new_signups = models.BooleanField(default=True)
    default_ai_provider = models.CharField(
        max_length=50,
        choices=[('OPENAI', 'OpenAI'), ('HUGGINGFACE', 'Hugging Face')],
        default='OPENAI'
    )

class TenantConfiguration(models.Model):
    """Tenant-specific overrides"""
    tenant = models.OneToOneField(Tenant, on_delete=models.CASCADE)
    custom_domain = models.CharField(max_length=255, blank=True)
    enabled_modules = models.JSONField(
        default=list,
        help_text="List of enabled module IDs (e.g., ['ai_chatbot', 'advanced_analytics'])"
    )

class AuditLog(models.Model):
    """Track admin actions"""
    ACTION_CHOICES = [
        ('CREATE', 'Create'),
        ('UPDATE', 'Update'),
        ('DELETE', 'Delete')
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    model_name = models.CharField(max_length=50)
    object_id = models.CharField(max_length=36)
    timestamp = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(default=dict)