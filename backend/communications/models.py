# core/models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinLengthValidator
from django_tenants.models import TenantMixin

User = get_user_model()

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='%(class)s_created'
    )
    updated_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='%(class)s_updated'
    )

    class Meta:
        abstract = True

class Channel(BaseModel):
    class ChannelType(models.TextChoices):
        ASTERISK = 'ASTERISK', _('Asterisk Call')
        WHATSAPP = 'WHATSAPP', _('WhatsApp')
        SMS = 'SMS', _('SMS')
        FACEBOOK = 'FACEBOOK', _('Facebook Messenger')
        EMAIL = 'EMAIL', _('Email')
        TELEGRAM = 'TELEGRAM', _('Telegram')
        OTHER = 'OTHER', _('Other')
    
    class ChannelStatus(models.TextChoices):
        ACTIVE = 'ACTIVE', _('Active')
        INACTIVE = 'INACTIVE', _('Inactive')
        MAINTENANCE = 'MAINTENANCE', _('Under Maintenance')
    
    tenant = models.ForeignKey('tenants.Tenant', on_delete=models.CASCADE)
    name = models.CharField(max_length=50, validators=[MinLengthValidator(2)])
    channel_type = models.CharField(
        max_length=20, 
        choices=ChannelType.choices,
        default=ChannelType.OTHER
    )
    status = models.CharField(
        max_length=15,
        choices=ChannelStatus.choices,
        default=ChannelStatus.ACTIVE
    )
    config = models.JSONField(default=dict)  # Stores API keys, webhook URLs, etc.
    priority = models.PositiveSmallIntegerField(default=1)  # For routing priority
    rate_limit = models.PositiveIntegerField(default=100, help_text="Messages per hour")
    
    def __str__(self):
        return f"{self.name} ({self.get_channel_type_display()})"

class Contact(BaseModel):
    tenant = models.ForeignKey('tenants.Tenant', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    whatsapp_id = models.CharField(max_length=50, blank=True, null=True)
    facebook_id = models.CharField(max_length=50, blank=True, null=True)
    other_identifiers = models.JSONField(default=dict)
    is_blocked = models.BooleanField(default=False)
    metadata = models.JSONField(default=dict)
    
    class Meta:
        unique_together = ('tenant', 'phone')
    
    def __str__(self):
        return f"{self.name} ({self.phone or self.email})"

class Message(BaseModel):
    class Direction(models.TextChoices):
        INBOUND = 'IN', _('Inbound')
        OUTBOUND = 'OUT', _('Outbound')
    
    class MessageStatus(models.TextChoices):
        QUEUED = 'QUEUED', _('Queued')
        SENT = 'SENT', _('Sent')
        DELIVERED = 'DELIVERED', _('Delivered')
        READ = 'READ', _('Read')
        FAILED = 'FAILED', _('Failed')
    
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, null=True, blank=True)
    external_id = models.CharField(max_length=100)  # ID from provider
    direction = models.CharField(
        max_length=3, 
        choices=Direction.choices
    )
    content = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=MessageStatus.choices,
        default=MessageStatus.QUEUED
    )
    status_updated_at = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(default=dict)  # Raw payload from provider
    error_reason = models.TextField(blank=True, null=True)
    
    # For calls
    call_duration = models.PositiveIntegerField(null=True, blank=True)  # in seconds
    call_record_url = models.URLField(blank=True, null=True)
    
    # For media messages
    media_url = models.URLField(blank=True, null=True)
    media_type = models.CharField(max_length=50, blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['external_id', 'channel']),
            models.Index(fields=['contact']),
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.get_direction_display()} message via {self.channel}"

class Conversation(BaseModel):
    tenant = models.ForeignKey('tenants.Tenant', on_delete=models.CASCADE)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    is_open = models.BooleanField(default=True)
    last_message = models.ForeignKey(
        'Message',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    tags = models.ManyToManyField('Tag', blank=True)
    
    class Meta:
        unique_together = ('tenant', 'contact', 'channel')
    
    def __str__(self):
        return f"Conversation with {self.contact} on {self.channel}"

class Tag(BaseModel):
    tenant = models.ForeignKey('tenants.Tenant', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=7, default='#3498db')  # Hex color
    
    def __str__(self):
        return self.name

class CallLog(BaseModel):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True, blank=True)
    from_number = models.CharField(max_length=20)
    to_number = models.CharField(max_length=20)
    call_sid = models.CharField(max_length=100)  # Provider's call ID
    direction = models.CharField(max_length=3, choices=Message.Direction.choices)
    status = models.CharField(max_length=20)  # e.g., completed, failed, busy
    duration = models.PositiveIntegerField()  # in seconds
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    recording_url = models.URLField(blank=True, null=True)
    metadata = models.JSONField(default=dict)
    
    class Meta:
        ordering = ['-start_time']
    
    def __str__(self):
        return f"Call from {self.from_number} to {self.to_number} ({self.status})"

class Template(BaseModel):
    class TemplateType(models.TextChoices):
        TEXT = 'TEXT', _('Text')
        MEDIA = 'MEDIA', _('Media')
        INTERACTIVE = 'INTERACTIVE', _('Interactive')
    
    tenant = models.ForeignKey('tenants.Tenant', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    content = models.TextField()
    template_type = models.CharField(
        max_length=20,
        choices=TemplateType.choices,
        default=TemplateType.TEXT
    )
    channel_types = models.CharField(max_length=200)  # Comma-separated channel types
    variables = models.JSONField(default=list)  # List of template variables
    
    def __str__(self):
        return self.name