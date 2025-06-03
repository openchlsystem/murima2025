# core/models.py
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
from django_tenants.models import TenantMixin
from core.models import BaseModel

class Channel(BaseModel):
    CHANNEL_TYPES = [
        ('CALL', 'Voice Call'),
        ('SMS', 'SMS'),
        ('WHATSAPP', 'WhatsApp'),
        ('EMAIL', 'Email'),
        ('SOCIAL', 'Social Media'),
    ]
    
    tenant = models.ForeignKey('tenants.Tenant', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    channel_type = models.CharField(max_length=20, choices=CHANNEL_TYPES)
    is_active = models.BooleanField(default=True)
    config = models.JSONField(default=dict)  # Stores API keys, webhook URLs, etc.

    def __str__(self):
        return f"{self.name} ({self.channel_type})"

class Message(BaseModel):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    external_id = models.CharField(max_length=100)  # ID from Twilio/WhatsApp/etc.
    direction = models.CharField(max_length=10, choices=[('IN', 'Inbound'), ('OUT', 'Outbound')])
    content = models.TextField()
    status = models.CharField(max_length=20)  # e.g., "delivered", "failed"
    metadata = models.JSONField(default=dict)  # Raw payload from provider

    class Meta:
        ordering = ['-created_at']