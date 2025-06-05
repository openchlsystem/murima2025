# apps/ai/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from apps.cases.models import Case
from apps.calls.models import Call
from .services.case_service import CaseAIService
from .services.call_service import CallAIService  # type: ignore # You would implement this too

class AIViewSet(viewsets.ViewSet):
    """ViewSet for AI operations."""
    permission_classes = [IsAuthenticated]
    
    @action(detail=True, methods=['get'], url_path='case-suggestions')
    def case_suggestions(self, request, pk=None):
        """Get AI suggestions for a case."""
        case = get_object_or_404(Case, pk=pk)
        
        # Check permissions
        if not request.user.has_perm('cases.view_case'):
            return Response(
                {"error": "You don't have permission to access this case"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        suggestions = CaseAIService.get_case_suggestions(case, user=request.user)
        return Response(suggestions)
    
    @action(detail=True, methods=['post'], url_path='categorize-case')
    def categorize_case(self, request, pk=None):
        """Categorize a case using AI."""
        case = get_object_or_404(Case, pk=pk)
        
        # Check permissions
        if not request.user.has_perm('cases.change_case'):
            return Response(
                {"error": "You don't have permission to modify this case"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Get narrative from request or use case narrative
        narrative = request.data.get('narrative', case.narrative)
        
        categories = CaseAIService.categorize_case(
            case=case,
            narrative=narrative,
            user=request.user
        )
        
        # Optionally update the case with the suggested category
        auto_categorize = request.data.get('auto_categorize', False)
        if auto_categorize and categories.get('success', False):
            from apps.core.models import ReferenceData
            primary_category = categories['categories'].get('primary_category')
            if primary_category:
                category = ReferenceData.objects.filter(
                    category='case_category',
                    name=primary_category
                ).first()
                
                if category:
                    case.category = category
                    case.save(update_fields=['category'])
        
        return Response(categories)
    
    @action(detail=True, methods=['get'], url_path='summarize-call')
    def summarize_call(self, request, pk=None):
        """Get AI summary of a call."""
        call = get_object_or_404(Call, pk=pk)
        
        # Check permissions
        if not request.user.has_perm('calls.view_call'):
            return Response(
                {"error": "You don't have permission to access this call"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        summary = CallAIService.summarize_call(call, user=request.user)
        return Response(summary)