# core/models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
import uuid
from ipaddress import ip_address

User = get_user_model()

class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

class UUIDModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    class Meta:
        abstract = True

class UserTrackingModel(models.Model):
    created_by = models.ForeignKey(
        User, 
        on_delete=models.PROTECT, 
        related_name='%(class)s_created',
        null=True,
        blank=True
    )
    updated_by = models.ForeignKey(
        User, 
        on_delete=models.PROTECT, 
        related_name='%(class)s_updated', 
        null=True, 
        blank=True
    )
    
    class Meta:
        abstract = True

class SoftDeleteModel(models.Model):
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='%(class)s_deleted'
    )
    
    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False, user=None):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.deleted_by = user
        self.save()

class OwnedModel(models.Model):
    """For models that belong to a specific user/tenant"""
    owner = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='%(class)s_owned',
        null=True,
        blank=True
    )
    
    class Meta:
        abstract = True

class TenantModel(models.Model):
    """For multi-tenancy support"""
    tenant = models.ForeignKey(
        'tenants.Tenant',  # Assuming you have a Tenant model
        on_delete=models.CASCADE,
        related_name='%(class)s_tenant'
    )
    
    class Meta:
        abstract = True

class AuditLog(models.Model):
    """For centralized audit logging"""
    ACTION_CHOICES = [
        ('CREATE', 'Create'),
        ('READ', 'Read'),
        ('UPDATE', 'Update'),
        ('DELETE', 'Delete'),
        ('SOFT_DELETE', 'Soft Delete'),
        ('LOGIN', 'Login'),
        ('LOGOUT', 'Logout'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    object_type = models.CharField(max_length=64)
    object_id = models.CharField(max_length=255, null=True, blank=True)
    metadata = models.JSONField(default=dict)
    user_agent = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp']),
            models.Index(fields=['user']),
            models.Index(fields=['action']),
            models.Index(fields=['object_type', 'object_id']),
        ]

    def __str__(self):
        return f"{self.timestamp} - {self.user} - {self.action}"

class BaseModel(UUIDModel, TimestampedModel, UserTrackingModel, SoftDeleteModel):
    """Complete base model with all common functionality"""
    
    class Meta:
        abstract = True