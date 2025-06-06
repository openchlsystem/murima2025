# apps/ai/tasks.py
from celery import shared_task
from django.contrib.contenttypes.models import ContentType
from .services.case_service import CaseAIService

@shared_task
def analyze_case_background(case_id, user_id=None):
    """
    Analyze a case in the background.
    
    Args:
        case_id: ID of the case to analyze
        user_id: Optional user ID who requested the analysis
    """
    from apps.cases.models import Case
    from apps.accounts.models import User
    
    case = Case.objects.get(id=case_id)
    user = User.objects.get(id=user_id) if user_id else None
    
    # Perform multiple AI operations
    suggestions = CaseAIService.get_case_suggestions(case, user=user)
    categories = CaseAIService.categorize_case(case, user=user)
    
    # Create a notification when complete
    from apps.notifications.models import Notification
    if user:
        Notification.objects.create(
            user=user,
            title="Case Analysis Complete",
            message=f"AI analysis for case #{case.case_number} is now available",
            content_type=ContentType.objects.get_for_model(case),
            object_id=case.id,
            notification_type="ai_analysis"
        )
    
    return {
        'case_id': case_id,
        'suggestions': suggestions.get('success', False),
        'categories': categories.get('success', False)
    }