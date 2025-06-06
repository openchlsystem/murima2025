# apps/cases/services.py
from django.db import transaction
from django.utils import timezone
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models import Count, Q, Avg, Sum, F
from django.core.cache import cache
from typing import Dict, List, Optional, Any, Tuple
from datetime import timedelta, datetime
import logging
import json
from decimal import Decimal

from .models import (
    Case, CaseActivity, CaseService, CaseReferral, 
    CaseNote, CaseAttachment, CaseUpdate, CaseCategory
)
from apps.core.models import ReferenceData
from apps.contacts.models import Contact, ContactRole
from apps.accounts.models import User
from apps.campaigns.models import Campaign

logger = logging.getLogger(__name__)


class CaseBusinessLogic:
    """Core business logic for case management operations"""
    
    @staticmethod
    def create_case(
        reporter: Contact,
        narrative: str,
        created_by: User,
        case_type: Optional[ReferenceData] = None,
        status: Optional[ReferenceData] = None,
        priority: Optional[ReferenceData] = None,
        **kwargs
    ) -> Case:
        """
        Create a new case with proper validation and initialization.
        
        Args:
            reporter: Reporter contact
            narrative: Case description
            created_by: User creating the case
            case_type: Case type (auto-determined if not provided)
            status: Case status (defaults to 'open')
            priority: Case priority (defaults to 'medium')
            **kwargs: Additional case fields
            
        Returns:
            Created Case instance
            
        Raises:
            ValidationError: If validation fails
        """
        try:
            with transaction.atomic():
                # Auto-determine case type if not provided
                if not case_type:
                    case_type = CaseBusinessLogic._determine_case_type(narrative, kwargs)
                
                # Set default status and priority
                if not status:
                    status = ReferenceData.objects.filter(
                        category='case_status', 
                        name__icontains='open',
                        is_active=True
                    ).first()
                    
                if not priority:
                    priority = ReferenceData.objects.filter(
                        category='case_priority', 
                        name__icontains='medium',
                        is_active=True
                    ).first()
                
                # Validate required reference data
                if not case_type:
                    raise ValidationError("Case type is required and could not be determined")
                if not status:
                    raise ValidationError("Valid case status not found")
                if not priority:
                    raise ValidationError("Valid case priority not found")
                
                # Calculate due date based on priority if not provided
                if 'due_date' not in kwargs or not kwargs['due_date']:
                    kwargs['due_date'] = CaseBusinessLogic._calculate_due_date(priority)
                
                # Auto-generate title if not provided
                if 'title' not in kwargs or not kwargs['title']:
                    kwargs['title'] = CaseBusinessLogic._generate_title(narrative, case_type)
                
                # Create the case
                case = Case.objects.create(
                    case_type=case_type,
                    reporter=reporter,
                    narrative=narrative,
                    status=status,
                    priority=priority,
                    created_by=created_by,
                    updated_by=created_by,
                    **kwargs
                )
                
                # Create reporter role entry
                ContactRole.objects.create(
                    contact=reporter,
                    case=case,
                    role='reporter',
                    is_primary=True,
                    role_data={
                        'is_afflicted': kwargs.get('reporter_is_afflicted', False),
                        'knows_about_116': str(kwargs.get('knows_about_116', ''))
                    }
                )
                
                # Log case creation
                CaseActivity.objects.create(
                    case=case,
                    activity_type='created',
                    user=created_by,
                    title='Case Created',
                    description=f"Case {case.case_number} created",
                    data={
                        'case_type': case_type.name,
                        'priority': priority.name,
                        'status': status.name,
                        'initial_narrative_length': len(narrative)
                    }
                )
                
                # Trigger AI analysis if enabled
                if getattr(settings, 'ENABLE_AI_ANALYSIS', True):
                    CaseAIService.queue_analysis(case)
                
                logger.info(f"Case {case.case_number} created by {created_by.username}")
                return case
                
        except Exception as e:
            logger.error(f"Error creating case: {str(e)}")
            raise ValidationError(f"Failed to create case: {str(e)}")
    
    @staticmethod
    def _determine_case_type(narrative: str, case_data: Dict) -> Optional[ReferenceData]:
        """Auto-determine case type based on content and flags"""
        # Check for GBV indicators
        if case_data.get('is_gbv_related'):
            gbv_type = ReferenceData.objects.filter(
                category='case_type', 
                name__icontains='gbv',
                is_active=True
            ).first()
            if gbv_type:
                return gbv_type
        
        # Check narrative for keywords
        narrative_lower = narrative.lower()
        
        # Violence indicators
        violence_keywords = ['violence', 'abuse', 'assault', 'rape', 'sexual', 'domestic']
        if any(keyword in narrative_lower for keyword in violence_keywords):
            gbv_type = ReferenceData.objects.filter(
                category='case_type',
                name__icontains='gbv',
                is_active=True
            ).first()
            if gbv_type:
                return gbv_type
        
        # Child protection indicators
        child_keywords = ['child', 'minor', 'underage', 'school', 'orphan']
        if any(keyword in narrative_lower for keyword in child_keywords):
            child_type = ReferenceData.objects.filter(
                category='case_type',
                name__icontains='child',
                is_active=True
            ).first()
            if child_type:
                return child_type
        
        # Default to general case type
        return ReferenceData.objects.filter(
            category='case_type',
            name__icontains='general',
            is_active=True
        ).first()
    
    @staticmethod
    def _calculate_due_date(priority: ReferenceData) -> datetime:
        """Calculate due date based on priority"""
        now = timezone.now()
        priority_name = priority.name.lower()
        
        if 'critical' in priority_name:
            return now + timedelta(hours=4)  # 4 hours for critical
        elif 'high' in priority_name:
            return now + timedelta(days=1)   # 1 day for high
        elif 'medium' in priority_name:
            return now + timedelta(days=3)   # 3 days for medium
        elif 'low' in priority_name:
            return now + timedelta(days=7)   # 1 week for low
        else:
            return now + timedelta(days=5)   # Default 5 days
    
    @staticmethod
    def _generate_title(narrative: str, case_type: ReferenceData) -> str:
        """Generate appropriate case title"""
        if len(narrative) <= 50:
            return narrative
        
        # Extract first sentence or 50 characters
        sentences = narrative.split('.')
        first_sentence = sentences[0].strip()
        
        if len(first_sentence) <= 50:
            return first_sentence
        
        # Truncate to 47 chars and add ellipsis
        return narrative[:47].strip() + "..."
    
    @staticmethod
    def assign_case(case: Case, assigned_to: User, assigned_by: User, reason: str = '') -> bool:
        """
        Assign a case to a user with validation and logging.
        
        Args:
            case: Case to assign
            assigned_to: User to assign to
            assigned_by: User making the assignment
            reason: Optional reason for assignment
            
        Returns:
            True if successful
            
        Raises:
            ValidationError: If assignment is invalid
        """
        try:
            with transaction.atomic():
                # Validate assignment
                if not CaseBusinessLogic._can_user_handle_cases(assigned_to):
                    raise ValidationError(f"User {assigned_to.username} cannot handle cases")
                
                if case.assigned_to == assigned_to:
                    raise ValidationError("Case is already assigned to this user")
                
                # Check workload
                if not CaseBusinessLogic._check_user_workload(assigned_to):
                    logger.warning(f"User {assigned_to.username} has high case workload")
                
                old_assignee = case.assigned_to
                old_assignee_name = old_assignee.get_full_name() if old_assignee else 'Unassigned'
                
                # Update case
                case.assigned_to = assigned_to
                case.updated_by = assigned_by
                case.save(update_fields=['assigned_to', 'updated_by', 'updated_at'])
                
                # Log activity
                CaseActivity.objects.create(
                    case=case,
                    activity_type='assigned',
                    user=assigned_by,
                    title='Case Assigned',
                    description=f"Case assigned from {old_assignee_name} to {assigned_to.get_full_name()}",
                    data={
                        'assigned_to': assigned_to.id,
                        'assigned_to_name': assigned_to.get_full_name(),
                        'previous_assignee': old_assignee.id if old_assignee else None,
                        'previous_assignee_name': old_assignee_name,
                        'reason': reason
                    }
                )
                
                # Send notification
                CaseNotificationService.send_assignment_notification(case, assigned_to, assigned_by)
                
                logger.info(f"Case {case.case_number} assigned to {assigned_to.username} by {assigned_by.username}")
                return True
                
        except Exception as e:
            logger.error(f"Error assigning case {case.case_number}: {str(e)}")
            raise ValidationError(str(e))
    
    @staticmethod
    def escalate_case(
        case: Case, 
        escalated_to: User, 
        escalated_by: User, 
        reason: str,
        urgency_level: str = 'normal'
    ) -> bool:
        """
        Escalate a case to a supervisor with proper validation.
        
        Args:
            case: Case to escalate
            escalated_to: User to escalate to
            escalated_by: User escalating the case
            reason: Reason for escalation (required)
            urgency_level: Urgency of escalation
            
        Returns:
            True if successful
        """
        try:
            with transaction.atomic():
                # Validate escalation
                if not reason.strip():
                    raise ValidationError("Escalation reason is required")
                
                if not CaseBusinessLogic._can_user_handle_escalations(escalated_to):
                    raise ValidationError(f"User {escalated_to.username} cannot handle escalations")
                
                if case.escalated_to == escalated_to:
                    raise ValidationError("Case is already escalated to this user")
                
                # Update case
                previous_escalated_to = case.escalated_to
                case.escalated_to = escalated_to
                case.escalated_by = escalated_by
                case.escalation_date = timezone.now()
                case.updated_by = escalated_by
                
                # Auto-assign if not assigned or assigned to someone without escalation rights
                if not case.assigned_to or not CaseBusinessLogic._can_user_handle_escalations(case.assigned_to):
                    case.assigned_to = escalated_to
                
                case.save(update_fields=[
                    'escalated_to', 'escalated_by', 'escalation_date', 
                    'assigned_to', 'updated_by', 'updated_at'
                ])
                
                # Log activity
                CaseActivity.objects.create(
                    case=case,
                    activity_type='escalated',
                    user=escalated_by,
                    title='Case Escalated',
                    description=f"Case escalated to {escalated_to.get_full_name()}",
                    data={
                        'escalated_to': escalated_to.id,
                        'escalated_to_name': escalated_to.get_full_name(),
                        'previous_escalated_to': previous_escalated_to.id if previous_escalated_to else None,
                        'reason': reason,
                        'urgency_level': urgency_level
                    },
                    is_important=True
                )
                
                # Add escalation note
                CaseNote.objects.create(
                    case=case,
                    note_type='supervisor',
                    author=escalated_by,
                    title='Escalation Notice',
                    content=f"Case escalated to {escalated_to.get_full_name()}.\n\nReason: {reason}",
                    is_important=True,
                    is_private=False
                )
                
                # Send notifications
                CaseNotificationService.send_escalation_notification(case, escalated_to, escalated_by, reason)
                
                logger.info(f"Case {case.case_number} escalated to {escalated_to.username} by {escalated_by.username}")
                return True
                
        except Exception as e:
            logger.error(f"Error escalating case {case.case_number}: {str(e)}")
            raise ValidationError(str(e))
    
    @staticmethod
    def update_case_status(
        case: Case, 
        new_status: ReferenceData, 
        updated_by: User,
        notes: str = '',
        auto_actions: bool = True
    ) -> bool:
        """
        Update case status with automated actions and validation.
        
        Args:
            case: Case to update
            new_status: New status reference data
            updated_by: User making the change
            notes: Optional notes about the status change
            auto_actions: Whether to perform automated actions
            
        Returns:
            True if successful
        """
        try:
            with transaction.atomic():
                old_status = case.status
                
                # Validate status transition
                if not CaseBusinessLogic._is_valid_status_transition(old_status, new_status):
                    raise ValidationError(f"Invalid status transition from {old_status.name} to {new_status.name}")
                
                # Update case
                case.status = new_status
                case.updated_by = updated_by
                
                # Handle status-specific actions
                if auto_actions:
                    CaseBusinessLogic._handle_status_change_actions(case, old_status, new_status, updated_by)
                
                case.save(update_fields=['status', 'closed_date', 'updated_by', 'updated_at'])
                
                # Log activity
                CaseActivity.objects.create(
                    case=case,
                    activity_type='status_changed',
                    user=updated_by,
                    title='Status Changed',
                    description=f"Status changed from {old_status.name} to {new_status.name}",
                    data={
                        'old_status': old_status.name,
                        'new_status': new_status.name,
                        'notes': notes,
                        'auto_actions': auto_actions
                    }
                )
                
                # Add note if provided
                if notes:
                    CaseNote.objects.create(
                        case=case,
                        note_type='update',
                        author=updated_by,
                        title=f'Status Update: {new_status.name}',
                        content=notes,
                        is_important=True
                    )
                
                # Send notifications
                CaseNotificationService.send_status_change_notification(case, old_status, new_status, updated_by)
                
                logger.info(f"Case {case.case_number} status changed to {new_status.name} by {updated_by.username}")
                return True
                
        except Exception as e:
            logger.error(f"Error updating case {case.case_number} status: {str(e)}")
            raise ValidationError(str(e))
    
    @staticmethod
    def _is_valid_status_transition(old_status: ReferenceData, new_status: ReferenceData) -> bool:
        """Validate if status transition is allowed"""
        # Define valid transitions
        transitions = {
            'open': ['in_progress', 'pending', 'escalated', 'closed', 'cancelled'],
            'in_progress': ['pending', 'escalated', 'resolved', 'closed', 'on_hold'],
            'pending': ['in_progress', 'escalated', 'closed', 'cancelled'],
            'escalated': ['in_progress', 'resolved', 'closed'],
            'on_hold': ['in_progress', 'pending', 'closed'],
            'resolved': ['closed', 'in_progress'],  # Can reopen if needed
            'closed': ['in_progress'],  # Can reopen closed cases
            'cancelled': []  # Cannot change from cancelled
        }
        
        old_name = old_status.name.lower().replace(' ', '_')
        new_name = new_status.name.lower().replace(' ', '_')
        
        allowed_transitions = transitions.get(old_name, [])
        return new_name in allowed_transitions or old_name == new_name
    
    @staticmethod
    def _handle_status_change_actions(case: Case, old_status: ReferenceData, new_status: ReferenceData, user: User):
        """Handle automated actions when status changes"""
        new_status_name = new_status.name.lower()
        
        # Closing actions
        if new_status_name in ['closed', 'resolved']:
            if not case.closed_date:
                case.closed_date = timezone.now()
            
            # Auto-generate resolution summary if empty
            if not case.resolution_summary:
                case.resolution_summary = f"Case {new_status.name.lower()} on {timezone.now().strftime('%Y-%m-%d')}"
        
        # Reopening actions
        elif old_status.name.lower() in ['closed', 'resolved'] and new_status_name in ['open', 'in_progress']:
            case.closed_date = None
            case.resolution_summary = ''
        
        # Escalation status actions
        elif new_status_name == 'escalated' and not case.escalated_to:
            # Find a supervisor to escalate to
            supervisor = User.objects.filter(
                role__in=['supervisor', 'manager'],
                is_active=True
            ).first()
            if supervisor:
                case.escalated_to = supervisor
                case.escalated_by = user
                case.escalation_date = timezone.now()
    
    @staticmethod
    def _can_user_handle_cases(user: User) -> bool:
        """Check if user can handle cases"""
        return user.is_active and user.role in ['agent', 'supervisor', 'manager', 'admin']
    
    @staticmethod
    def _can_user_handle_escalations(user: User) -> bool:
        """Check if user can handle escalations"""
        return user.is_active and user.role in ['supervisor', 'manager', 'admin']
    
    @staticmethod
    def _check_user_workload(user: User) -> bool:
        """Check if user workload is reasonable"""
        active_cases = Case.objects.filter(
            assigned_to=user,
            status__name__in=['open', 'in_progress', 'pending', 'escalated'],
            is_active=True
        ).count()
        
        # Define workload limits by role
        limits = {
            'agent': 20,
            'supervisor': 30,
            'manager': 50,
            'admin': 100
        }
        
        limit = limits.get(user.role, 20)
        return active_cases < limit


class CaseDataService:
    """Service for case data operations and queries"""
    
    @staticmethod
    def get_case_statistics(case: Case) -> Dict[str, Any]:
        """Get comprehensive statistics for a case"""
        try:
            # Basic info
            stats = {
                'basic_info': {
                    'case_number': case.case_number,
                    'case_id': case.id,
                    'age_in_days': case.age_in_days,
                    'status': case.status.name if case.status else None,
                    'priority': case.priority.name if case.priority else None,
                    'case_type': case.case_type.name if case.case_type else None,
                    'is_overdue': case.is_overdue,
                    'is_escalated': case.is_escalated,
                    'is_gbv_related': case.is_gbv_related,
                },
                'timing': {
                    'created_at': case.created_at,
                    'due_date': case.due_date,
                    'closed_date': case.closed_date,
                    'escalation_date': case.escalation_date,
                    'time_to_resolution': case.time_to_resolution,
                    'days_overdue': (timezone.now() - case.due_date).days if case.due_date and case.is_overdue else 0,
                },
                'contacts': {
                    'reporter': {
                        'name': case.reporter.full_name if case.reporter else None,
                        'phone': case.reporter.primary_phone if case.reporter else None,
                        'is_afflicted': case.reporter_is_afflicted
                    },
                    'client_count': case.client_count,
                    'perpetrator_count': case.perpetrator_count,
                    'total_contacts': case.contact_roles.count() if hasattr(case, 'contact_roles') else 0,
                },
                'activities': {
                    'total_activities': case.activities.count(),
                    'notes_count': case.notes.count(),
                    'services_count': case.services.count(),
                    'referrals_count': case.referrals.count(),
                    'attachments_count': case.attachments.count(),
                    'last_activity': case.activities.first().created_at if case.activities.exists() else None,
                    'recent_activity_types': list(
                        case.activities.order_by('-created_at')[:5].values_list('activity_type', flat=True)
                    )
                },
                'assignment': {
                    'assigned_to': case.assigned_to.get_full_name() if case.assigned_to else None,
                    'assigned_to_id': case.assigned_to.id if case.assigned_to else None,
                    'escalated_to': case.escalated_to.get_full_name() if case.escalated_to else None,
                    'escalated_to_id': case.escalated_to.id if case.escalated_to else None,
                    'created_by': case.created_by.get_full_name() if case.created_by else None,
                },
                'ai_analysis': {
                    'risk_score': case.ai_risk_score,
                    'urgency_score': case.ai_urgency_score,
                    'sentiment_score': case.ai_sentiment_score,
                    'analysis_completed': case.ai_analysis_completed,
                    'analysis_date': case.ai_analysis_date,
                    'suggested_category': case.ai_suggested_category.name if case.ai_suggested_category else None,
                    'suggested_priority': case.ai_suggested_priority.name if case.ai_suggested_priority else None,
                    'keywords': case.ai_keywords[:10] if case.ai_keywords else [],  # Top 10 keywords
                }
            }
            
            # Calculate progress percentage
            if case.status:
                status_progress = {
                    'open': 10,
                    'in_progress': 50,
                    'pending': 40,
                    'escalated': 60,
                    'resolved': 90,
                    'closed': 100,
                    'cancelled': 0
                }
                stats['basic_info']['progress_percentage'] = status_progress.get(
                    case.status.name.lower().replace(' ', '_'), 0
                )
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting case statistics for {case.case_number}: {str(e)}")
            return {'error': str(e)}
    
    @staticmethod
    def get_overdue_cases(
        assigned_to: Optional[User] = None,
        limit: int = 50
    ) -> List[Case]:
        """Get list of overdue cases with caching"""
        cache_key = f"overdue_cases_{assigned_to.id if assigned_to else 'all'}_{limit}"
        
        cached_result = cache.get(cache_key)
        if cached_result:
            return cached_result
        
        try:
            queryset = Case.objects.filter(
                due_date__lt=timezone.now(),
                status__name__in=['open', 'in_progress', 'pending', 'escalated'],
                is_active=True
            ).select_related(
                'status', 'priority', 'assigned_to', 'case_type', 'reporter'
            ).prefetch_related('activities')
            
            if assigned_to:
                queryset = queryset.filter(assigned_to=assigned_to)
            
            cases = list(queryset.order_by('due_date')[:limit])
            
            # Cache for 5 minutes
            cache.set(cache_key, cases, 300)
            
            return cases
            
        except Exception as e:
            logger.error(f"Error getting overdue cases: {str(e)}")
            return []
    
    @staticmethod
    def get_dashboard_metrics(user: Optional[User] = None) -> Dict[str, Any]:
        """Get dashboard metrics for a user or system-wide"""
        try:
            # Base queryset
            base_qs = Case.objects.filter(is_active=True)
            if user and user.role in ['agent', 'supervisor']:
                base_qs = base_qs.filter(
                    Q(assigned_to=user) | Q(created_by=user) | Q(escalated_to=user)
                )
            
            # Current date calculations
            now = timezone.now()
            today = now.date()
            week_ago = now - timedelta(days=7)
            month_ago = now - timedelta(days=30)
            
            # Basic counts
            total_cases = base_qs.count()
            open_cases = base_qs.filter(status__name__in=['open', 'in_progress', 'pending']).count()
            closed_cases = base_qs.filter(status__name__in=['closed', 'resolved']).count()
            overdue_cases = base_qs.filter(
                due_date__lt=now,
                status__name__in=['open', 'in_progress', 'pending', 'escalated']
            ).count()
            
            # Recent activity
            cases_today = base_qs.filter(created_at__date=today).count()
            cases_this_week = base_qs.filter(created_at__gte=week_ago).count()
            cases_this_month = base_qs.filter(created_at__gte=month_ago).count()
            
            # Priority distribution
            priority_dist = base_qs.values('priority__name').annotate(
                count=Count('id')
            ).order_by('-count')
            
            # Status distribution
            status_dist = base_qs.values('status__name').annotate(
                count=Count('id')
            ).order_by('-count')
            
            # GBV statistics
            gbv_cases = base_qs.filter(is_gbv_related=True).count()
            
            # Escalation statistics
            escalated_cases = base_qs.filter(escalated_to__isnull=False).count()
            
            # Performance metrics
            closed_this_month = base_qs.filter(
                closed_date__gte=month_ago,
                status__name__in=['closed', 'resolved']
            )
            
            avg_resolution_time = None
            if closed_this_month.exists():
                resolution_times = []
                for case in closed_this_month:
                    if case.time_to_resolution:
                        resolution_times.append(case.time_to_resolution.total_seconds() / 86400)  # Days
                
                if resolution_times:
                    avg_resolution_time = sum(resolution_times) / len(resolution_times)
            
            return {
                'summary': {
                    'total_cases': total_cases,
                    'open_cases': open_cases,
                    'closed_cases': closed_cases,
                    'overdue_cases': overdue_cases,
                    'escalated_cases': escalated_cases,
                    'gbv_cases': gbv_cases,
                    'closure_rate': round((closed_cases / total_cases * 100), 2) if total_cases > 0 else 0,
                    'overdue_rate': round((overdue_cases / total_cases * 100), 2) if total_cases > 0 else 0,
                    'escalation_rate': round((escalated_cases / total_cases * 100), 2) if total_cases > 0 else 0,
                    'gbv_rate': round((gbv_cases / total_cases * 100), 2) if total_cases > 0 else 0,
                },
                'recent_activity': {
                    'cases_today': cases_today,
                    'cases_this_week': cases_this_week,
                    'cases_this_month': cases_this_month,
                },
                'distributions': {
                    'priority': [
                        {'name': item['priority__name'] or 'Unknown', 'count': item['count']}
                        for item in priority_dist
                    ],
                    'status': [
                        {'name': item['status__name'] or 'Unknown', 'count': item['count']}
                        for item in status_dist
                    ],
                },
                'performance': {
                    'avg_resolution_days': round(avg_resolution_time, 2) if avg_resolution_time else None,
                    'closed_this_month': closed_this_month.count(),
                },
                'timestamp': now,
                'user_filter': user.username if user else None,
            }
            
        except Exception as e:
            logger.error(f"Error getting dashboard metrics: {str(e)}")
            return {'error': str(e)}


class CaseNotificationService:
    """Service for case-related notifications"""
    
    @staticmethod
    def send_assignment_notification(case: Case, assigned_to: User, assigned_by: User):
        """Send notification when case is assigned"""
        try:
            from apps.notifications.models import Notification
            
            Notification.objects.create(
                user=assigned_to,
                title=f'Case Assigned: {case.case_number}',
                content=f'Case {case.case_number} has been assigned to you by {assigned_by.get_full_name()}.',
                notification_type='case_assignment',
                data={
                    'case_id': case.id,
                    'case_number': case.case_number,
                    'assigned_by': assigned_by.id,
                    'priority': case.priority.name if case.priority else None,
                    'due_date': case.due_date.isoformat() if case.due_date else None,
                }
            )
            
        except Exception as e:
            logger.error(f"Error sending assignment notification: {str(e)}")
    
    @staticmethod
    def send_escalation_notification(case: Case, escalated_to: User, escalated_by: User, reason: str):
        """Send notification when case is escalated"""
        try:
            from apps.notifications.models import Notification
            
            Notification.objects.create(
                user=escalated_to,
                title=f'Case Escalated: {case.case_number}',
                content=f'Case {case.case_number} has been escalated to you by {escalated_by.get_full_name()}.\n\nReason: {reason}',
                notification_type='case_escalation',
                priority='high',
                data={
                    'case_id': case.id,
                    'case_number': case.case_number,
                    'escalated_by': escalated_by.id,
                    'reason': reason,
                    'original_assignee': case.assigned_to.id if case.assigned_to else None,
                }
            )
            
        except Exception as e:
            logger.error(f"Error sending escalation notification: {str(e)}")
    
    @staticmethod
    def send_status_change_notification(case: Case, old_status: ReferenceData, new_status: ReferenceData, updated_by: User):
        """Send notification when case status changes"""
        try:
            from apps.notifications.models import Notification
            
            # Notify assigned user and escalated user
            recipients = [user for user in [case.assigned_to, case.escalated_to] if user and user != updated_by]
            
            for recipient in recipients:
                Notification.objects.create(
                    user=recipient,
                    title=f'Case Status Updated: {case.case_number}',
                    content=f'Case {case.case_number} status changed from {old_status.name} to {new_status.name} by {updated_by.get_full_name()}.',
                    notification_type='case_status_change',
                    data={
                        'case_id': case.id,
                        'case_number': case.case_number,
                        'old_status': old_status.name,
                        'new_status': new_status.name,
                        'updated_by': updated_by.id,
                    }
                )
                
        except Exception as e:
            logger.error(f"Error sending status change notification: {str(e)}")
    
    @staticmethod
    def send_overdue_notification(case: Case):
        """Send notification when case becomes overdue"""
        try:
            from apps.notifications.models import Notification
            
            # Notify assigned user and escalated user
            recipients = [user for user in [case.assigned_to, case.escalated_to] if user]
            
            for recipient in recipients:
                Notification.objects.create(
                    user=recipient,
                    title=f'Overdue Case: {case.case_number}',
                    content=f'Case {case.case_number} is overdue. Due date was {case.due_date.strftime("%Y-%m-%d %H:%M")}.',
                    notification_type='case_overdue',
                    priority='high',
                    data={
                        'case_id': case.id,
                        'case_number': case.case_number,
                        'due_date': case.due_date.isoformat(),
                        'days_overdue': (timezone.now() - case.due_date).days,
                    }
                )
                
        except Exception as e:
            logger.error(f"Error sending overdue notification: {str(e)}")


class CaseAIService:
    """Service for AI-enhanced case features"""
    
    @staticmethod
    def queue_analysis(case: Case, force: bool = False):
        """Queue case for AI analysis"""
        try:
            if case.ai_analysis_completed and not force:
                return
            
            # Mark as queued for analysis
            case.ai_analysis_completed = False
            case.save(update_fields=['ai_analysis_completed'])
            
            # In a real implementation, this would queue a background task
            # For now, we'll call the analysis directly
            CaseAIService.analyze_case(case)
            
        except Exception as e:
            logger.error(f"Error queuing AI analysis for case {case.case_number}: {str(e)}")
    
    @staticmethod
    def analyze_case(case: Case) -> Dict[str, Any]:
        """Perform AI analysis on a case (placeholder implementation)"""
        try:
            # This would integrate with actual AI services like OpenAI, Claude, etc.
            # For now, we'll provide a mock implementation
            
            analysis_results = CaseAIService._mock_ai_analysis(case)
            
            # Update case with AI results
            case.ai_risk_score = analysis_results.get('risk_score')
            case.ai_urgency_score = analysis_results.get('urgency_score')
            case.ai_sentiment_score = analysis_results.get('sentiment_score')
            case.ai_summary = analysis_results.get('summary', '')
            case.ai_keywords = analysis_results.get('keywords', [])
            case.ai_analysis_completed = True
            case.ai_analysis_date = timezone.now()
            
            # Set AI suggestions
            if analysis_results.get('suggested_category_id'):
                case.ai_suggested_category_id = analysis_results['suggested_category_id']
            if analysis_results.get('suggested_priority_id'):
                case.ai_suggested_priority_id = analysis_results['suggested_priority_id']
            
            case.save(update_fields=[
                'ai_risk_score', 'ai_urgency_score', 'ai_sentiment_score',
                'ai_summary', 'ai_keywords', 'ai_analysis_completed',
                'ai_analysis_date', 'ai_suggested_category', 'ai_suggested_priority'
            ])
            
            # Log AI analysis completion
            CaseActivity.objects.create(
                case=case,
                activity_type='ai_analysis',
                title='AI Analysis Completed',
                description='Automated AI analysis completed',
                data=analysis_results,
                is_internal=True
            )
            
            return analysis_results
            
        except Exception as e:
            logger.error(f"Error analyzing case {case.case_number}: {str(e)}")
            return {'error': str(e)}
    
    @staticmethod
    def _mock_ai_analysis(case: Case) -> Dict[str, Any]:
        """Mock AI analysis implementation"""
        narrative = case.narrative.lower()
        
        # Mock risk scoring based on keywords
        high_risk_keywords = ['violence', 'threat', 'weapon', 'injury', 'hospital', 'police', 'emergency']
        medium_risk_keywords = ['conflict', 'dispute', 'argument', 'problem', 'concern']
        
        high_risk_count = sum(1 for keyword in high_risk_keywords if keyword in narrative)
        medium_risk_count = sum(1 for keyword in medium_risk_keywords if keyword in narrative)
        
        risk_score = min(1.0, (high_risk_count * 0.3 + medium_risk_count * 0.1))
        
        # Mock urgency scoring
        urgent_keywords = ['urgent', 'immediate', 'emergency', 'asap', 'critical']
        urgency_score = min(1.0, sum(0.2 for keyword in urgent_keywords if keyword in narrative))
        
        # Mock sentiment analysis
        negative_keywords = ['sad', 'angry', 'frustrated', 'upset', 'hurt', 'pain']
        positive_keywords = ['happy', 'grateful', 'thank', 'satisfied', 'good']
        
        negative_count = sum(1 for keyword in negative_keywords if keyword in narrative)
        positive_count = sum(1 for keyword in positive_keywords if keyword in narrative)
        
        sentiment_score = max(-1.0, min(1.0, (positive_count - negative_count) * 0.2))
        
        # Extract keywords (simple word frequency)
        words = narrative.split()
        word_freq = {}
        for word in words:
            if len(word) > 3:  # Skip short words
                word_freq[word] = word_freq.get(word, 0) + 1
        
        keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
        keywords = [word for word, freq in keywords]
        
        # Generate summary
        sentences = case.narrative.split('.')
        summary = sentences[0][:200] + "..." if len(sentences[0]) > 200 else sentences[0]
        
        # Suggest category based on content
        suggested_category = None
        if case.is_gbv_related or any(word in narrative for word in ['violence', 'abuse', 'assault']):
            suggested_category = ReferenceData.objects.filter(
                category='case_category',
                name__icontains='gbv'
            ).first()
        
        # Suggest priority based on risk and urgency
        suggested_priority = None
        if risk_score > 0.7 or urgency_score > 0.7:
            suggested_priority = ReferenceData.objects.filter(
                category='case_priority',
                name__icontains='high'
            ).first()
        elif risk_score > 0.4 or urgency_score > 0.4:
            suggested_priority = ReferenceData.objects.filter(
                category='case_priority',
                name__icontains='medium'
            ).first()
        
        return {
            'risk_score': round(risk_score, 3),
            'urgency_score': round(urgency_score, 3),
            'sentiment_score': round(sentiment_score, 3),
            'summary': summary,
            'keywords': keywords,
            'suggested_category_id': suggested_category.id if suggested_category else None,
            'suggested_priority_id': suggested_priority.id if suggested_priority else None,
            'analysis_confidence': 0.75,  # Mock confidence score
            'analysis_version': '1.0',
            'timestamp': timezone.now().isoformat()
        }
    
    @staticmethod
    def get_similar_cases(case: Case, limit: int = 5) -> List[Case]:
        """Find similar cases using AI/ML techniques"""
        try:
            # Simple similarity based on keywords and case type
            # In a real implementation, this would use embeddings or ML models
            
            similar_cases = Case.objects.filter(
                case_type=case.case_type,
                is_active=True
            ).exclude(id=case.id).select_related(
                'status', 'priority', 'reporter'
            )
            
            # If GBV case, prioritize other GBV cases
            if case.is_gbv_related:
                similar_cases = similar_cases.filter(is_gbv_related=True)
            
            # Order by recent cases with similar status
            similar_cases = similar_cases.filter(
                status__name__in=['closed', 'resolved']
            ).order_by('-created_at')
            
            return list(similar_cases[:limit])
            
        except Exception as e:
            logger.error(f"Error finding similar cases for {case.case_number}: {str(e)}")
            return []
    
    @staticmethod
    def suggest_next_actions(case: Case) -> List[Dict[str, str]]:
        """Suggest next actions based on case analysis"""
        try:
            suggestions = []
            
            # Based on case status
            status_name = case.status.name.lower() if case.status else ''
            
            if 'open' in status_name:
                suggestions.append({
                    'action': 'contact_reporter',
                    'title': 'Contact Reporter',
                    'description': 'Follow up with the reporter for additional details',
                    'priority': 'high'
                })
                
                if case.is_gbv_related:
                    suggestions.append({
                        'action': 'safety_assessment',
                        'title': 'Conduct Safety Assessment',
                        'description': 'Assess immediate safety risks for the victim',
                        'priority': 'critical'
                    })
            
            elif 'in_progress' in status_name:
                suggestions.append({
                    'action': 'update_progress',
                    'title': 'Update Case Progress',
                    'description': 'Document current investigation progress',
                    'priority': 'medium'
                })
            
            # Based on overdue status
            if case.is_overdue:
                suggestions.append({
                    'action': 'escalate_case',
                    'title': 'Consider Escalation',
                    'description': 'Case is overdue - consider escalating to supervisor',
                    'priority': 'high'
                })
            
            # Based on AI analysis
            if case.ai_risk_score and case.ai_risk_score > 0.7:
                suggestions.append({
                    'action': 'risk_mitigation',
                    'title': 'Risk Mitigation',
                    'description': 'High risk detected - implement mitigation measures',
                    'priority': 'critical'
                })
            
            # Based on case age
            if case.age_in_days > 30 and case.status.name.lower() not in ['closed', 'resolved']:
                suggestions.append({
                    'action': 'review_case',
                    'title': 'Case Review',
                    'description': 'Case is over 30 days old - conduct comprehensive review',
                    'priority': 'medium'
                })
            
            # Missing services/referrals
            if case.services.count() == 0:
                suggestions.append({
                    'action': 'assess_services',
                    'title': 'Assess Service Needs',
                    'description': 'Evaluate what services the client might need',
                    'priority': 'medium'
                })
            
            return suggestions[:5]  # Return top 5 suggestions
            
        except Exception as e:
            logger.error(f"Error generating suggestions for case {case.case_number}: {str(e)}")
            return []


class CaseBulkOperationsService:
    """Service for bulk operations on multiple cases"""
    
    @staticmethod
    def bulk_assign_cases(case_ids: List[int], assigned_to: User, assigned_by: User) -> Dict[str, Any]:
        """Assign multiple cases to a user"""
        try:
            results = {
                'success_count': 0,
                'error_count': 0,
                'errors': [],
                'processed_cases': []
            }
            
            cases = Case.objects.filter(id__in=case_ids, is_active=True)
            
            for case in cases:
                try:
                    CaseBusinessLogic.assign_case(case, assigned_to, assigned_by)
                    results['success_count'] += 1
                    results['processed_cases'].append({
                        'case_id': case.id,
                        'case_number': case.case_number,
                        'status': 'success'
                    })
                except Exception as e:
                    results['error_count'] += 1
                    results['errors'].append({
                        'case_id': case.id,
                        'case_number': case.case_number,
                        'error': str(e)
                    })
                    results['processed_cases'].append({
                        'case_id': case.id,
                        'case_number': case.case_number,
                        'status': 'error',
                        'error': str(e)
                    })
            
            return results
            
        except Exception as e:
            logger.error(f"Error in bulk assign operation: {str(e)}")
            return {'error': str(e)}
    
    @staticmethod
    def bulk_update_status(case_ids: List[int], new_status: ReferenceData, updated_by: User) -> Dict[str, Any]:
        """Update status for multiple cases"""
        try:
            results = {
                'success_count': 0,
                'error_count': 0,
                'errors': [],
                'processed_cases': []
            }
            
            cases = Case.objects.filter(id__in=case_ids, is_active=True)
            
            for case in cases:
                try:
                    CaseBusinessLogic.update_case_status(case, new_status, updated_by)
                    results['success_count'] += 1
                    results['processed_cases'].append({
                        'case_id': case.id,
                        'case_number': case.case_number,
                        'status': 'success'
                    })
                except Exception as e:
                    results['error_count'] += 1
                    results['errors'].append({
                        'case_id': case.id,
                        'case_number': case.case_number,
                        'error': str(e)
                    })
                    results['processed_cases'].append({
                        'case_id': case.id,
                        'case_number': case.case_number,
                        'status': 'error',
                        'error': str(e)
                    })
            
            return results
            
        except Exception as e:
            logger.error(f"Error in bulk status update: {str(e)}")
            return {'error': str(e)}
    
    @staticmethod
    def bulk_close_cases(
        case_ids: List[int], 
        closed_by: User, 
        resolution_summary: str = "Bulk closure"
    ) -> Dict[str, Any]:
        """Close multiple cases"""
        try:
            # Get closed status
            closed_status = ReferenceData.objects.filter(
                category='case_status',
                name__icontains='closed',
                is_active=True
            ).first()
            
            if not closed_status:
                return {'error': 'Closed status not found in reference data'}
            
            return CaseBulkOperationsService.bulk_update_status(case_ids, closed_status, closed_by)
            
        except Exception as e:
            logger.error(f"Error in bulk close operation: {str(e)}")
            return {'error': str(e)}


class CaseReportingService:
    """Service for case reporting and analytics"""
    
    @staticmethod
    def generate_case_report(
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        filters: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Generate comprehensive case report"""
        try:
            # Default to last 30 days
            if not date_to:
                date_to = timezone.now()
            if not date_from:
                date_from = date_to - timedelta(days=30)
            
            # Base queryset
            queryset = Case.objects.filter(
                created_at__range=[date_from, date_to],
                is_active=True
            )
            
            # Apply additional filters
            if filters:
                if filters.get('case_type'):
                    queryset = queryset.filter(case_type__name__icontains=filters['case_type'])
                if filters.get('status'):
                    queryset = queryset.filter(status__name__icontains=filters['status'])
                if filters.get('assigned_to'):
                    queryset = queryset.filter(assigned_to=filters['assigned_to'])
                if filters.get('is_gbv_related') is not None:
                    queryset = queryset.filter(is_gbv_related=filters['is_gbv_related'])
            
            # Calculate metrics
            total_cases = queryset.count()
            
            # Status breakdown
            status_breakdown = queryset.values('status__name').annotate(
                count=Count('id'),
                percentage=Count('id') * 100.0 / total_cases if total_cases > 0 else 0
            ).order_by('-count')
            
            # Priority breakdown
            priority_breakdown = queryset.values('priority__name').annotate(
                count=Count('id'),
                percentage=Count('id') * 100.0 / total_cases if total_cases > 0 else 0
            ).order_by('-count')
            
            # Case type breakdown
            type_breakdown = queryset.values('case_type__name').annotate(
                count=Count('id'),
                percentage=Count('id') * 100.0 / total_cases if total_cases > 0 else 0
            ).order_by('-count')
            
            # Resolution metrics
            closed_cases = queryset.filter(status__name__in=['closed', 'resolved'])
            resolution_rate = (closed_cases.count() / total_cases * 100) if total_cases > 0 else 0
            
            # Calculate average resolution time
            avg_resolution_time = None
            resolution_times = []
            for case in closed_cases:
                if case.time_to_resolution:
                    resolution_times.append(case.time_to_resolution.total_seconds() / 86400)  # Days
            
            if resolution_times:
                avg_resolution_time = sum(resolution_times) / len(resolution_times)
            
            # GBV statistics
            gbv_cases = queryset.filter(is_gbv_related=True).count()
            gbv_rate = (gbv_cases / total_cases * 100) if total_cases > 0 else 0
            
            # Overdue cases
            overdue_cases = queryset.filter(
                due_date__lt=timezone.now(),
                status__name__in=['open', 'in_progress', 'pending', 'escalated']
            ).count()
            overdue_rate = (overdue_cases / total_cases * 100) if total_cases > 0 else 0
            
            # Daily trend
            daily_trends = []
            current_date = date_from.date()
            while current_date <= date_to.date():
                day_count = queryset.filter(created_at__date=current_date).count()
                daily_trends.append({
                    'date': current_date.isoformat(),
                    'count': day_count
                })
                current_date += timedelta(days=1)
            
            # Top agents by case count
            agent_performance = queryset.filter(assigned_to__isnull=False).values(
                'assigned_to__first_name',
                'assigned_to__last_name',
                'assigned_to__username'
            ).annotate(
                case_count=Count('id'),
                closed_count=Count('id', filter=Q(status__name__in=['closed', 'resolved']))
            ).order_by('-case_count')[:10]
            
            return {
                'period': {
                    'from': date_from.isoformat(),
                    'to': date_to.isoformat(),
                    'days': (date_to - date_from).days + 1
                },
                'summary': {
                    'total_cases': total_cases,
                    'closed_cases': closed_cases.count(),
                    'open_cases': queryset.filter(status__name__in=['open', 'in_progress', 'pending']).count(),
                    'escalated_cases': queryset.filter(escalated_to__isnull=False).count(),
                    'overdue_cases': overdue_cases,
                    'gbv_cases': gbv_cases,
                    'resolution_rate': round(resolution_rate, 2),
                    'overdue_rate': round(overdue_rate, 2),
                    'gbv_rate': round(gbv_rate, 2),
                    'avg_resolution_days': round(avg_resolution_time, 2) if avg_resolution_time else None,
                },
                'breakdowns': {
                    'status': list(status_breakdown),
                    'priority': list(priority_breakdown),
                    'type': list(type_breakdown),
                },
                'trends': {
                    'daily': daily_trends,
                },
                'performance': {
                    'top_agents': list(agent_performance),
                },
                'generated_at': timezone.now().isoformat(),
                'filters_applied': filters or {},
            }
            
        except Exception as e:
            logger.error(f"Error generating case report: {str(e)}")
            return {'error': str(e)}


# Backwards compatibility aliases
CaseService = CaseBusinessLogic
CaseAnalyticsService = CaseReportingService