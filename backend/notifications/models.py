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
        related_name="%(class)s_created"
    )
    updated_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name="%(class)s_updated"
    )

    class Meta:
        abstract = True  # Marks this as an abstract base class
        
        
from django.db import models
from core.models import BaseModel
from tenants.models import Tenant

class Notification(BaseModel):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)  # Tenant-specific
    recipient = models.ForeignKey(
        'users.User', 
        on_delete=models.CASCADE, 
        related_name='notifications'
    )
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    channel = models.CharField(  # e.g., "email", "sms", "whatsapp"
        max_length=20, 
        choices=[
            ('email', 'Email'),
            ('sms', 'SMS'),
            ('whatsapp', 'WhatsApp'),
            ('in_app', 'In-App')
        ]
    )
    sent_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} (to {self.recipient.email})"