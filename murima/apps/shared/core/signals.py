from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from core.utils import log_action
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save)
def log_save(sender, instance, created, **kwargs):
    if sender._meta.app_label == 'core' and sender.__name__ == 'AuditLog':
        return
    action = 'CREATE' if created else 'UPDATE'
    log_action(action, obj=instance)

@receiver(post_delete)
def log_delete(sender, instance, **kwargs):
    if sender._meta.app_label == 'core' and sender.__name__ == 'AuditLog':
        return
    log_action('DELETE', obj=instance)