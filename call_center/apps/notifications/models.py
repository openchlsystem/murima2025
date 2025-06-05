# apps/notifications/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from apps.core.models import TimeStampedModel


class Notification(TimeStampedModel):
    """System notifications for users"""
    
    NOTIFICATION_TYPES = [
        ('info', _('Information')),
        ('success', _('Success')),
        ('warning', _('Warning')),
        ('error', _('Error')),
        ('case_assigned', _('Case Assigned')),
        ('case_escalated', _('Case Escalated')),
        ('call_missed', _('Call Missed')),
        ('system', _('System')),
    ]
    
    PRIORITY_LEVELS = [
        ('low', _('Low')),
        ('normal', _('Normal')),
        ('high', _('High')),
        ('urgent', _('Urgent')),
    ]
    
    recipient = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name=_("Recipient")
    )
    sender = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sent_notifications',
        verbose_name=_("Sender")
    )
    
    notification_type = models.CharField(
        max_length=20,
        choices=NOTIFICATION_TYPES,
        default='info',
        verbose_name=_("Type")
    )
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_LEVELS,
        default='normal',
        verbose_name=_("Priority")
    )
    
    title = models.CharField(
        max_length=255,
        verbose_name=_("Title")
    )
    message = models.TextField(
        verbose_name=_("Message")
    )
    
    # Generic foreign key to link to any model
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    
    # Status tracking
    is_read = models.BooleanField(
        default=False,
        verbose_name=_("Is Read")
    )
    read_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Read At")
    )
    
    # Delivery tracking
    email_sent = models.BooleanField(
        default=False,
        verbose_name=_("Email Sent")
    )
    email_sent_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Email Sent At")
    )
    
    # Additional data
    data = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("Additional Data")
    )
    
    # Auto-delete after certain time
    expires_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Expires At"),
        help_text=_("Notification will be auto-deleted after this date")
    )
    
    class Meta:
        verbose_name = _("Notification")
        verbose_name_plural = _("Notifications")
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', '-created_at']),
            models.Index(fields=['recipient', 'is_read']),
            models.Index(fields=['notification_type', '-created_at']),
            models.Index(fields=['priority', '-created_at']),
            models.Index(fields=['expires_at']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.recipient.username}"
    
    def mark_as_read(self):
        """Mark notification as read"""
        if not self.is_read:
            from django.utils import timezone
            self.is_read = True
            self.read_at = timezone.now()
            self.save(update_fields=['is_read', 'read_at'])


class NotificationTemplate(TimeStampedModel):
    """Templates for different types of notifications"""
    
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_("Name")
    )
    notification_type = models.CharField(
        max_length=20,
        choices=Notification.NOTIFICATION_TYPES,
        verbose_name=_("Type")
    )
    title_template = models.CharField(
        max_length=255,
        verbose_name=_("Title Template"),
        help_text=_("Template with placeholders like {variable_name}")
    )
    message_template = models.TextField(
        verbose_name=_("Message Template"),
        help_text=_("Template with placeholders like {variable_name}")
    )
    email_template = models.TextField(
        blank=True,
        verbose_name=_("Email Template"),
        help_text=_("HTML email template (optional)")
    )
    default_priority = models.CharField(
        max_length=10,
        choices=Notification.PRIORITY_LEVELS,
        default='normal',
        verbose_name=_("Default Priority")
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Is Active")
    )
    
    class Meta:
        verbose_name = _("Notification Template")
        verbose_name_plural = _("Notification Templates")
        ordering = ['name']
    
    def __str__(self):
        return self.name


class NotificationPreference(TimeStampedModel):
    """User preferences for notifications"""
    
    user = models.OneToOneField(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='notification_preferences',
        verbose_name=_("User")
    )
    
    # Email preferences
    email_enabled = models.BooleanField(
        default=True,
        verbose_name=_("Email Notifications")
    )
    email_digest = models.BooleanField(
        default=False,
        verbose_name=_("Email Digest"),
        help_text=_("Receive summary emails instead of individual notifications")
    )
    
    # Browser preferences
    browser_enabled = models.BooleanField(
        default=True,
        verbose_name=_("Browser Notifications")
    )
    sound_enabled = models.BooleanField(
        default=True,
        verbose_name=_("Sound Notifications")
    )
    
    # SMS preferences
    sms_enabled = models.BooleanField(
        default=False,
        verbose_name=_("SMS Notifications")
    )
    sms_urgent_only = models.BooleanField(
        default=True,
        verbose_name=_("SMS for Urgent Only")
    )
    
    # Specific notification type preferences
    notification_types = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("Notification Type Preferences"),
        help_text=_("Preferences for specific notification types")
    )
    
    class Meta:
        verbose_name = _("Notification Preference")
        verbose_name_plural = _("Notification Preferences")
    
    def __str__(self):
        return f"Preferences for {self.user.username}"