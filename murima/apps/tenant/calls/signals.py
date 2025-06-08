# asterisk_app/signals.py
import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import transaction
from .models import AsteriskExtension
from .services.ari_service import AsteriskARIService

logger = logging.getLogger(__name__)


@receiver(post_save, sender='users.TenantMembership')  # Adjust app name as needed
def handle_tenant_membership_created(sender, instance, created, **kwargs):
    """
    Handle TenantMembership creation/update.
    Create Asterisk extension if role has asterisk=True.
    """
    try:
        # Check if the role has asterisk permission
        if not hasattr(instance, 'role') or not instance.role.asterisk:
            logger.info(f"Role {instance.role} does not have asterisk permission")
            return
        
        # Check if user already has an extension for this tenant
        existing_extension = AsteriskExtension.objects.filter(
            user=instance.user,
            tenant=instance.tenant
        ).first()
        
        if existing_extension:
            logger.info(f"User {instance.user} already has extension for tenant {instance.tenant}")
            return
        
        # Create new extension
        logger.info(f"Creating Asterisk extension for user {instance.user} in tenant {instance.tenant}")
        
        # Use transaction to ensure data consistency
        with transaction.atomic():
            # Generate extension details
            extension_number = AsteriskExtension.generate_extension_number(instance.tenant.id)
            username, password = AsteriskExtension.generate_credentials()
            
            # Create extension record
            extension = AsteriskExtension.objects.create(
                user=instance.user,
                extension_number=extension_number,
                username=username,
                password=password,
                tenant=instance.tenant,
                is_active=True
            )
            
            # Create extension in Asterisk via ARI
            ari_service = AsteriskARIService()
            success, error_message = ari_service.create_extension(extension)
            
            if success:
                extension.asterisk_created = True
                extension.save()
                logger.info(f"Successfully created Asterisk extension {extension_number} for user {instance.user}")
            else:
                extension.asterisk_created = False
                extension.asterisk_error = error_message
                extension.save()
                logger.error(f"Failed to create Asterisk extension: {error_message}")
    
    except Exception as e:
        logger.error(f"Error handling tenant membership signal: {str(e)}")


@receiver(post_delete, sender='users.TenantMembership')
def handle_tenant_membership_deleted(sender, instance, **kwargs):
    """
    Handle TenantMembership deletion.
    Remove Asterisk extension if it exists.
    """
    try:
        # Only process if role had asterisk permission
        if not hasattr(instance, 'role') or not instance.role.asterisk:
            return
        
        # Find and remove extension
        try:
            extension = AsteriskExtension.objects.get(
                user=instance.user,
                tenant=instance.tenant
            )
            
            # Remove from Asterisk via ARI
            ari_service = AsteriskARIService()
            success, error_message = ari_service.remove_extension(extension)
            
            if success:
                extension.delete()
                logger.info(f"Successfully removed Asterisk extension {extension.extension_number}")
            else:
                logger.error(f"Failed to remove Asterisk extension: {error_message}")
                # Mark as inactive but keep record for debugging
                extension.is_active = False
                extension.asterisk_error = f"Deletion failed: {error_message}"
                extension.save()
        
        except AsteriskExtension.DoesNotExist:
            logger.info(f"No Asterisk extension found for user {instance.user} in tenant {instance.tenant}")
    
    except Exception as e:
        logger.error(f"Error handling tenant membership deletion signal: {str(e)}")


@receiver(post_save, sender='users.Role')  # Optional: Handle role changes
def handle_role_updated(sender, instance, created, **kwargs):
    """
    Handle Role updates. If asterisk permission is removed, 
    deactivate all extensions for users with this role.
    """
    if created:
        return
    
    try:
        # If asterisk permission was removed
        if not instance.asterisk:
            # Find all tenant memberships with this role
            memberships = instance.tenant_memberships.all()  # Adjust field name as needed
            
            for membership in memberships:
                try:
                    extension = AsteriskExtension.objects.get(
                        user=membership.user,
                        tenant=membership.tenant
                    )
                    
                    # Deactivate extension in Asterisk
                    ari_service = AsteriskARIService()
                    success, error_message = ari_service.deactivate_extension(extension)
                    
                    if success:
                        extension.is_active = False
                        extension.save()
                        logger.info(f"Deactivated extension {extension.extension_number} due to role change")
                    else:
                        logger.error(f"Failed to deactivate extension: {error_message}")
                
                except AsteriskExtension.DoesNotExist:
                    continue
    
    except Exception as e:
        logger.error(f"Error handling role update signal: {str(e)}")