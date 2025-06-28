from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Extension, CallLog
import logging

User = get_user_model()
logger = logging.getLogger(__name__)


@receiver(post_save, sender=Extension)
def extension_created(sender, instance, created, **kwargs):
    """
    Signal triggered when an extension is created
    """
    if created:
        logger.info(f"Extension created: {instance.username} for user {instance.user.username}")
        
        # You can add additional logic here, such as:
        # - Sending notifications
        # - Triggering webhooks
        # - Updating external systems
        # - Analytics tracking


@receiver(post_delete, sender=Extension)
def extension_deleted(sender, instance, **kwargs):
    """
    Signal triggered when an extension is deleted
    """
    logger.info(f"Extension deleted: {instance.username} for user {instance.user.username}")
    
    # Additional cleanup logic can be added here


@receiver(post_save, sender=CallLog)
def call_log_created(sender, instance, created, **kwargs):
    """
    Signal triggered when a call log is created or updated
    """
    if created:
        logger.info(f"Call log created: {instance.caller_extension.username} -> {instance.callee_extension.username}")
        
        # You can add logic here for:
        # - Real-time notifications to frontend via WebSocket
        # - Billing calculations
        # - Call analytics
        # - Third-party integrations (CRM updates, etc.)
        
    else:
        # Call log was updated
        logger.info(f"Call log updated: {instance.id}")


@receiver(post_save, sender=User)
def user_created(sender, instance, created, **kwargs):
    """
    Signal triggered when a user is created
    This is where you would trigger extension creation in the future
    when the tenant functionality is ready
    """
    if created:
        logger.info(f"New user created: {instance.username}")
        
        # Future implementation:
        # - Auto-generate extension for new users
        # - Create tenant-specific configurations
        # - Send welcome emails with extension details