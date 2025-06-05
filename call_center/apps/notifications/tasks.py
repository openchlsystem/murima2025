# apps/notifications/tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from django.conf import settings

@shared_task
def send_email_notification(notification_id):
    """
    Send email notification.
    
    Args:
        notification_id: ID of the notification to send
    """
    from .models import Notification
    
    try:
        notification = Notification.objects.select_related('user', 'content_type').get(id=notification_id)
        user = notification.user
        
        # Skip if user has no email
        if not user.email:
            return {'success': False, 'reason': 'no_email'}
        
        # Determine template based on notification type
        template_name = f"notifications/email/{notification.notification_type}.html"
        
        try:
            # Get the related object if any
            related_object = notification.content_object
            
            # Render email content
            context = {
                'user': user,
                'notification': notification,
                'related_object': related_object,
                'site_url': settings.SITE_URL
            }
            
            html_message = render_to_string(template_name, context)
            
            # Send the email
            send_mail(
                subject=notification.title,
                message=notification.message,  # Plain text version
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                html_message=html_message
            )
            
            # Update notification status
            notification.email_sent = True
            notification.email_sent_at = timezone.now()
            notification.save(update_fields=['email_sent', 'email_sent_at'])
            
            return {'success': True}
            
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Failed to send email notification {notification_id}: {str(e)}")
            return {'success': False, 'error': str(e)}
            
    except Notification.DoesNotExist:
        return {'success': False, 'reason': 'notification_not_found'}

@shared_task
def send_sms_notification(notification_id):
    """
    Send SMS notification.
    
    Args:
        notification_id: ID of the notification to send
    """
    from .models import Notification
    
    try:
        notification = Notification.objects.select_related('user').get(id=notification_id)
        user = notification.user
        
        # Skip if user has no phone
        if not hasattr(user, 'contact') or not user.contact or not user.contact.phone:
            return {'success': False, 'reason': 'no_phone'}
        
        phone = user.contact.phone
        
        # Here you would integrate with your SMS provider
        # For example, using Twilio:
        try:
            # Pseudo-code for SMS sending
            # from twilio.rest import Client
            # client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            # client.messages.create(
            #     body=notification.message,
            #     from_=settings.TWILIO_PHONE_NUMBER,
            #     to=phone
            # )
            
            # For now, just log that we would send SMS
            import logging
            logger = logging.getLogger(__name__)
            logger.info(f"Would send SMS to {phone}: {notification.message}")
            
            # Update notification status
            notification.sms_sent = True
            notification.sms_sent_at = timezone.now()
            notification.save(update_fields=['sms_sent', 'sms_sent_at'])
            
            return {'success': True}
            
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Failed to send SMS notification {notification_id}: {str(e)}")
            return {'success': False, 'error': str(e)}
            
    except Notification.DoesNotExist:
        return {'success': False, 'reason': 'notification_not_found'}

@shared_task
def send_daily_summary_emails():
    """
    Send daily summary emails to users who have opted in.
    """
    from apps.accounts.models import User
    from .models import NotificationPreference
    
    # Get users who want daily summaries
    users = User.objects.filter(
        is_active=True,
        notification_preferences__email_enabled=True,
        notification_preferences__email_daily_summary=True
    ).select_related('notification_preferences')
    
    for user in users:
        try:
            # Generate user's daily summary
            from apps.analytics.services import ReportingService # type: ignore
            summary = ReportingService.generate_user_daily_summary(user)
            
            # Send summary email
            context = {
                'user': user,
                'summary': summary,
                'date': timezone.now().strftime('%Y-%m-%d'),
                'site_url': settings.SITE_URL
            }
            
            html_message = render_to_string('notifications/email/daily_summary.html', context)
            
            send_mail(
                subject=f"Daily Summary - {timezone.now().strftime('%Y-%m-%d')}",
                message=f"Your daily summary for {timezone.now().strftime('%Y-%m-%d')}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                html_message=html_message
            )
            
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Failed to send daily summary to user {user.id}: {str(e)}")