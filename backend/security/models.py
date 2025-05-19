from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='%(class)s_created'
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='%(class)s_updated'
    )

    class Meta:
        abstract = True  # Makes this a reusable base class
        

from django.db import models
from core.models import BaseModel

class AuditLog(BaseModel):
    ACTION_CHOICES = [
        ('CREATE', 'Create'),
        ('READ', 'Read'),
        ('UPDATE', 'Update'),
        ('DELETE', 'Delete'),
        ('LOGIN', 'Login'),
        ('LOGOUT', 'Logout'),
    ]
    
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    model_name = models.CharField(max_length=100)  # e.g., "Case", "User"
    object_id = models.CharField(max_length=100)  # ID of the affected object
    details = models.JSONField(default=dict)  # Flexible field for changes
    ip_address = models.GenericIPAddressField(null=True)

    def __str__(self):
        return f"{self.action} on {self.model_name} ({self.object_id})"

class EncryptionKey(BaseModel):
    tenant = models.ForeignKey('tenants.Tenant', on_delete=models.CASCADE)
    key_name = models.CharField(max_length=100)
    encrypted_key = models.TextField()  # Store encrypted keys
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ['tenant', 'key_name']