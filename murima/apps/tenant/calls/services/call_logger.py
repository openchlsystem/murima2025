import logging
from datetime import datetime
from django.utils import timezone
from django.db import transaction
from ..models import Extension, CallLog
from ..serializers import CallLogCreateSerializer

logger = logging.getLogger(__name__)


class CallLoggerService:
    """
    Service for handling call logging business logic
    """
    
    @staticmethod
    def create_call_log(caller_username, callee_username, asterisk_call_id, start_time=None, end_time=None, call_status='failed'):
        """
        Create a call log entry
        """
        try:
            with transaction.atomic():
                # Use current time if start_time not provided
                if start_time is None:
                    start_time = timezone.now()
                
                call_log_data = {
                    'caller_username': caller_username,
                    'callee_username': callee_username,
                    'start_time': start_time,
                    'end_time': end_time,
                    'call_status': call_status,
                    'asterisk_call_id': asterisk_call_id
                }
                
                serializer = CallLogCreateSerializer(data=call_log_data)
                
                if serializer.is_valid():
                    call_log = serializer.save()
                    logger.info(f"Call log created successfully: {call_log.id}")
                    return call_log
                else:
                    logger.error(f"Call log creation failed: {serializer.errors}")
                    return None
                    
        except Exception as e:
            logger.error(f"Error creating call log: {str(e)}")
            return None

    @staticmethod
    def update_call_log(asterisk_call_id, end_time=None, call_status=None):
        """
        Update an existing call log (typically when call ends)
        """
        try:
            with transaction.atomic():
                call_log = CallLog.objects.select_for_update().get(asterisk_call_id=asterisk_call_id)
                
                if end_time:
                    call_log.end_time = end_time
                
                if call_status:
                    call_log.call_status = call_status
                
                # Calculate duration if both start and end times are available
                if call_log.start_time and call_log.end_time:
                    call_log.duration = int((call_log.end_time - call_log.start_time).total_seconds())
                
                call_log.save()
                logger.info(f"Call log updated: {call_log.id}")
                return call_log
                
        except CallLog.DoesNotExist:
            logger.error(f"Call log not found for asterisk_call_id: {asterisk_call_id}")
            return None
        except Exception as e:
            logger.error(f"Error updating call log: {str(e)}")
            return None

    @staticmethod
    def get_user_call_statistics(user_id):
        """
        Get call statistics for a user
        """
        try:
            from django.contrib.auth import get_user_model
            from django.db.models import Count, Q, Avg, Sum
            
            User = get_user_model()
            user = User.objects.get(id=user_id)
            extension = Extension.objects.get(user=user)
            
            # Get all call logs for this user
            call_logs = CallLog.objects.filter(
                Q(caller_extension=extension) | Q(callee_extension=extension)
            )
            
            # Calculate statistics
            total_calls = call_logs.count()
            outgoing_calls = call_logs.filter(caller_extension=extension).count()
            incoming_calls = call_logs.filter(callee_extension=extension).count()
            
            answered_calls = call_logs.filter(call_status='answered').count()
            missed_calls = call_logs.filter(
                callee_extension=extension,
                call_status__in=['no_answer', 'busy']
            ).count()
            
            # Average call duration for answered calls
            avg_duration = call_logs.filter(call_status='answered').aggregate(
                Avg('duration')
            )['duration__avg'] or 0
            
            # Total talk time
            total_talk_time = call_logs.filter(call_status='answered').aggregate(
                Sum('duration')
            )['duration__sum'] or 0
            
            return {
                'total_calls': total_calls,
                'outgoing_calls': outgoing_calls,
                'incoming_calls': incoming_calls,
                'answered_calls': answered_calls,
                'missed_calls': missed_calls,
                'answer_rate': round((answered_calls / total_calls * 100) if total_calls > 0 else 0, 2),
                'average_duration': round(avg_duration, 2),
                'total_talk_time': total_talk_time
            }
            
        except Exception as e:
            logger.error(f"Error getting call statistics for user {user_id}: {str(e)}")
            return None

    @staticmethod
    def get_recent_calls(user_id, limit=10):
        """
        Get recent calls for a user
        """
        try:
            from django.contrib.auth import get_user_model
            from django.db.models import Q
            
            User = get_user_model()
            user = User.objects.get(id=user_id)
            extension = Extension.objects.get(user=user)
            
            recent_calls = CallLog.objects.filter(
                Q(caller_extension=extension) | Q(callee_extension=extension)
            ).select_related(
                'caller_extension', 'callee_extension',
                'caller_extension__user', 'callee_extension__user'
            ).order_by('-start_time')[:limit]
            
            return recent_calls
            
        except Exception as e:
            logger.error(f"Error getting recent calls for user {user_id}: {str(e)}")
            return []

    @staticmethod
    def cleanup_old_call_logs(days_to_keep=90):
        """
        Clean up old call logs (useful for scheduled cleanup)
        """
        try:
            from datetime import timedelta
            
            cutoff_date = timezone.now() - timedelta(days=days_to_keep)
            
            deleted_count = CallLog.objects.filter(
                created_at__lt=cutoff_date
            ).delete()[0]
            
            logger.info(f"Cleaned up {deleted_count} old call logs")
            return deleted_count
            
        except Exception as e:
            logger.error(f"Error cleaning up old call logs: {str(e)}")
            return 0

    @staticmethod
    def export_call_logs_to_csv(user_id, start_date=None, end_date=None):
        """
        Export call logs to CSV format
        """
        try:
            import csv
            import io
            from django.contrib.auth import get_user_model
            from django.db.models import Q
            
            User = get_user_model()
            user = User.objects.get(id=user_id)
            extension = Extension.objects.get(user=user)
            
            # Build query
            query = Q(caller_extension=extension) | Q(callee_extension=extension)
            
            if start_date:
                query &= Q(start_time__gte=start_date)
            if end_date:
                query &= Q(start_time__lte=end_date)
            
            call_logs = CallLog.objects.filter(query).select_related(
                'caller_extension', 'callee_extension'
            ).order_by('-start_time')
            
            # Create CSV
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Write header
            writer.writerow([
                'Date', 'Time', 'Caller', 'Callee', 'Duration (seconds)', 
                'Status', 'Call Type'
            ])
            
            # Write data
            for log in call_logs:
                call_type = 'Outgoing' if log.caller_extension == extension else 'Incoming'
                
                writer.writerow([
                    log.start_time.strftime('%Y-%m-%d'),
                    log.start_time.strftime('%H:%M:%S'),
                    log.caller_extension.username,
                    log.callee_extension.username,
                    log.duration,
                    log.call_status,
                    call_type
                ])
            
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"Error exporting call logs to CSV: {str(e)}")
            return None