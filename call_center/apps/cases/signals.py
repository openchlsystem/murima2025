# Import ContactRole from contacts app for case-contact relationships
from datetime import timedelta, timezone
from apps.cases.models import Case, CaseActivity, CaseAttachment, CaseNote, CaseReferral, CaseService
from apps.contacts.models import ContactRole

# Update ContactRole to include case foreign key (this will be uncommented in contacts/models.py)
# We'll handle this relationship properly when both apps are ready

# Signal handlers
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver

@receiver(post_save, sender=Case)
def case_post_save(sender, instance, created, **kwargs):
    """Handle case post-save operations"""
    if created:
        # Create initial activity
        CaseActivity.objects.create(
            case=instance,
            activity_type='created',
            user=instance.created_by,
            description=f"Case {instance.case_number} created",
            data={
                'case_type': instance.case_type.name if instance.case_type else None,
                'priority': instance.priority.name if instance.priority else None,
                'status': instance.status.name if instance.status else None,
            }
        )
        
        # Set default due date if not provided (7 days from creation)
        if not instance.due_date:
            instance.due_date = timezone.now() + timedelta(days=7)
            instance.save(update_fields=['due_date'])


@receiver(pre_save, sender=Case)
def case_pre_save(sender, instance, **kwargs):
    """Handle case pre-save operations"""
    if instance.pk:  # Existing case
        try:
            old_instance = Case.objects.get(pk=instance.pk)
            
            # Track status changes
            if old_instance.status != instance.status:
                CaseActivity.objects.create(
                    case=instance,
                    activity_type='status_changed',
                    user=instance.updated_by,
                    description=f"Status changed from {old_instance.status.name} to {instance.status.name}",
                    data={
                        'old_status': old_instance.status.name,
                        'new_status': instance.status.name,
                    }
                )
            
            # Track priority changes
            if old_instance.priority != instance.priority:
                CaseActivity.objects.create(
                    case=instance,
                    activity_type='priority_changed',
                    user=instance.updated_by,
                    description=f"Priority changed from {old_instance.priority.name} to {instance.priority.name}",
                    data={
                        'old_priority': old_instance.priority.name,
                        'new_priority': instance.priority.name,
                    }
                )
            
            # Track assignment changes
            if old_instance.assigned_to != instance.assigned_to:
                old_name = old_instance.assigned_to.get_full_name() if old_instance.assigned_to else 'Unassigned'
                new_name = instance.assigned_to.get_full_name() if instance.assigned_to else 'Unassigned'
                
                CaseActivity.objects.create(
                    case=instance,
                    activity_type='assigned',
                    user=instance.updated_by,
                    description=f"Assignment changed from {old_name} to {new_name}",
                    data={
                        'old_assignee': old_instance.assigned_to.id if old_instance.assigned_to else None,
                        'new_assignee': instance.assigned_to.id if instance.assigned_to else None,
                    }
                )
                
        except Case.DoesNotExist:
            pass  # New case, will be handled in post_save


@receiver(post_save, sender=CaseService)
def case_service_post_save(sender, instance, created, **kwargs):
    """Log service addition"""
    if created:
        CaseActivity.objects.create(
            case=instance.case,
            activity_type='service_added',
            user=instance.provided_by,
            description=f"Service added: {instance.service.name}",
            data={
                'service': instance.service.name,
                'service_date': instance.service_date.isoformat(),
                'details': instance.details,
            }
        )


@receiver(post_save, sender=CaseReferral)
def case_referral_post_save(sender, instance, created, **kwargs):
    """Log referral addition"""
    if created:
        CaseActivity.objects.create(
            case=instance.case,
            activity_type='referral_added',
            user=instance.referred_by,
            description=f"Referral made to: {instance.organization}",
            data={
                'organization': instance.organization,
                'referral_type': instance.referral_type.name,
                'reason': instance.reason,
            }
        )


@receiver(post_save, sender=CaseNote)
def case_note_post_save(sender, instance, created, **kwargs):
    """Log note addition"""
    if created:
        CaseActivity.objects.create(
            case=instance.case,
            activity_type='note_added',
            user=instance.author,
            description=f"Note added: {instance.title or instance.content[:50]}",
            data={
                'note_type': instance.note_type,
                'title': instance.title,
                'is_important': instance.is_important,
            }
        )


@receiver(post_save, sender=CaseAttachment)
def case_attachment_post_save(sender, instance, created, **kwargs):
    """Log attachment upload"""
    if created:
        CaseActivity.objects.create(
            case=instance.case,
            activity_type='document_uploaded',
            user=instance.uploaded_by,
            description=f"Document uploaded: {instance.file_name}",
            data={
                'file_name': instance.file_name,
                'attachment_type': instance.attachment_type,
                'file_size': instance.file_size,
            }
        )