# apps/admin_config/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import TimeStampedModel


class AdminConfiguration(TimeStampedModel):
    """Configuration settings for admin interface"""
    
    key = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_("Configuration Key")
    )
    value = models.TextField(
        verbose_name=_("Value")
    )
    description = models.TextField(
        blank=True,
        verbose_name=_("Description")
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Is Active")
    )
    
    class Meta:
        verbose_name = _("Admin Configuration")
        verbose_name_plural = _("Admin Configurations")
        ordering = ['key']
    
    def __str__(self):
        return self.key