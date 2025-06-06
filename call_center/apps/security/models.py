# apps/security/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import TimeStampedModel


class SecurityEvent(TimeStampedModel):
    """Track security-related events"""
    
    EVENT_TYPES = [
        ('login_success', _('Login Success')),
        ('login_failed', _('Login Failed')),
        ('logout', _('Logout')),
        ('password_change', _('Password Change')),
        ('suspicious_activity', _('Suspicious Activity')),
        ('access_denied', _('Access Denied')),
    ]
    
    SEVERITY_LEVELS = [
        ('low', _('Low')),
        ('medium', _('Medium')),
        ('high', _('High')),
        ('critical', _('Critical')),
    ]
    
    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='security_events',
        verbose_name=_("User")
    )
    event_type = models.CharField(
        max_length=50,
        choices=EVENT_TYPES,
        verbose_name=_("Event Type")
    )
    severity = models.CharField(
        max_length=20,
        choices=SEVERITY_LEVELS,
        default='low',
        verbose_name=_("Severity")
    )
    ip_address = models.GenericIPAddressField(
        verbose_name=_("IP Address")
    )
    user_agent = models.TextField(
        blank=True,
        verbose_name=_("User Agent")
    )
    description = models.TextField(
        verbose_name=_("Description")
    )
    additional_data = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("Additional Data")
    )
    
    class Meta:
        verbose_name = _("Security Event")
        verbose_name_plural = _("Security Events")
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['event_type', '-created_at']),
            models.Index(fields=['severity', '-created_at']),
            models.Index(fields=['ip_address']),
        ]
    
    def __str__(self):
        username = self.user.username if self.user else 'Anonymous'
        return f"{self.get_event_type_display()} - {username} - {self.created_at}"