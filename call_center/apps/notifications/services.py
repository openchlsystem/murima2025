# apps/notifications/services.py
from django.db import transaction
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from .models import Notification, NotificationPreference
from .tasks import send_email_notification, send_sms_notification

class NotificationService:
    """Service for creating and sending notifications."""
    
    @staticmethod
    @transaction.atomic
    def create_notification(user, title, message, notification_type, 
                           content_object=None, send_email=False, send_sms=False):
        """
        Create a notification for a user.
        
        Args:
            user: User to notify
            title: Notification title
            message: Notification message
            notification_type: Type of notification
            content_object: Optional related object (case, call, etc.)
            send_email: Whether to send email notification
            send_sms: Whether to send SMS notification
            
        Returns:
            Notification: The created notification
        """
        # Check user preferences
        try:
            preferences = NotificationPreference.objects.get(user=user)
        except NotificationPreference.DoesNotExist:
            # Create default preferences if none exists
            preferences = NotificationPreference.objects.create(user=user)
        
        # Create notification object
        content_type = None
        object_id = None
        
        if content_object:
            content_type = ContentType.objects.get_for_model(content_object)
            object_id = content_object.id
        
        notification = Notification.objects.create(
            user=user,
            title=title,
            message=message,
            notification_type=notification_type,
            content_type=content_type,
            object_id=object_id
        )
        
        # Check if email should be sent
        should_send_email = send_email and preferences.email_enabled
        if notification_type == 'case_update' and not preferences.email_case_updates:
            should_send_email = False
        elif notification_type == 'case_assignment' and not preferences.email_case_assignments:
            should_send_email = False
        # Add checks for other notification types
        
        # Check if SMS should be sent
        should_send_sms = send_sms and preferences.sms_enabled
        if notification_type == 'case_escalation' and not preferences.sms_case_escalations:
            should_send_sms = False
        # Add checks for other notification types
        
        # Send notifications asynchronously
        if should_send_email:
            send_email_notification.delay(notification.id)
            
        if should_send_sms:
            send_sms_notification.delay(notification.id)
        
        return notification
    
    @staticmethod
    def notify_case_update(case, user, message=None):
        """
        Send notification about a case update.
        
        Args:
            case: The updated Case
            user: User to notify
            message: Optional custom message
        """
        if not message:
            message = f"Case #{case.case_number} has been updated."
            
        return NotificationService.create_notification(
            user=user,
            title=f"Case Update: #{case.case_number}",
            message=message,
            notification_type='case_update',
            content_object=case,
            send_email=True
        )
    
    @staticmethod
    def notify_case_assignment(case, assigned_to, assigned_by=None):
        """
        Send notification about a case assignment.
        
        Args:
            case: The Case being assigned
            assigned_to: User receiving the assignment
            assigned_by: Optional User making the assignment
        """
        assigned_by_text = f" by {assigned_by.get_full_name()}" if assigned_by else ""
        message = f"You have been assigned to Case #{case.case_number}{assigned_by_text}."
        
        return NotificationService.create_notification(
            user=assigned_to,
            title=f"Case Assignment: #{case.case_number}",
            message=message,
            notification_type='case_assignment',
            content_object=case,
            send_email=True
        )
    
    @staticmethod
    def notify_ai_insight(content_object, user, insight_type, summary):
        """
        Send notification about an AI-generated insight.
        
        Args:
            content_object: Object the insight is about (case, call, etc)
            user: User to notify
            insight_type: Type of insight (suggestion, summary, etc)
            summary: Brief summary of the insight
        """
        object_type = content_object._meta.verbose_name.title()
        object_id = getattr(content_object, 'case_number', content_object.id)
        
        return NotificationService.create_notification(
            user=user,
            title=f"AI Insight: {insight_type.title()} for {object_type} #{object_id}",
            message=f"New AI {insight_type}: {summary}",
            notification_type='ai_insight',
            content_object=content_object,
            send_email=True
        )
    
    @staticmethod
    def get_unread_notifications(user):
        """
        Get unread notifications for a user.
        
        Args:
            user: The User to get notifications for
            
        Returns:
            QuerySet: Unread notifications
        """
        return Notification.objects.filter(
            user=user,
            is_read=False
        ).select_related('content_type').order_by('-created_at')
    
    @staticmethod
    def mark_as_read(notification_id):
        """
        Mark a notification as read.
        
        Args:
            notification_id: ID of the notification
            
        Returns:
            Notification: The updated notification
        """
        notification = Notification.objects.get(id=notification_id)
        notification.mark_as_read()
        return notification
    
    @staticmethod
    def mark_all_as_read(user):
        """
        Mark all notifications for a user as read.
        
        Args:
            user: The User
            
        Returns:
            int: Number of notifications marked as read
        """
        count = Notification.objects.filter(
            user=user,
            is_read=False
        ).update(
            is_read=True,
            read_at=timezone.now()
        )
        
        return count