from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils import timezone


class Extension(models.Model):
    username = models.CharField(max_length=50, unique=True, help_text="SIP extension number")
    password = models.CharField(max_length=100, help_text="SIP password")
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='extension')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'extensions'
        ordering = ['-created_at']

    def __str__(self):
        return f"Extension {self.username} - User: {self.user.username}"


class CallLog(models.Model):
    CALL_STATUS_CHOICES = [
        ('answered', 'Answered'),
        ('busy', 'Busy'),
        ('no_answer', 'No Answer'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]

    caller_extension = models.ForeignKey(
        Extension, 
        on_delete=models.CASCADE, 
        related_name='outgoing_calls',
        help_text="Extension that initiated the call"
    )
    callee_extension = models.ForeignKey(
        Extension, 
        on_delete=models.CASCADE, 
        related_name='incoming_calls',
        help_text="Extension that received the call"
    )
    start_time = models.DateTimeField(help_text="When the call started")
    end_time = models.DateTimeField(null=True, blank=True, help_text="When the call ended")
    duration = models.IntegerField(default=0, help_text="Call duration in seconds")
    call_status = models.CharField(max_length=20, choices=CALL_STATUS_CHOICES, default='failed')
    asterisk_call_id = models.CharField(max_length=255, unique=True, help_text="Unique call ID from Asterisk")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'call_logs'
        ordering = ['-start_time']

    def __str__(self):
        return f"Call from {self.caller_extension.username} to {self.callee_extension.username} - {self.call_status}"

    def save(self, *args, **kwargs):
        if self.end_time and self.start_time:
            self.duration = int((self.end_time - self.start_time).total_seconds())
        super().save(*args, **kwargs)