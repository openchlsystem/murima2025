# apps/cases/views.py
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
import logging

from .models import (
    Case, CaseActivity, CaseService, CaseReferral, 
    CaseNote, CaseAttachment, CaseUpdate, CaseCategory
)
from .serializers import (
    CaseSerializer, CaseDetailSerializer, CaseActivitySerializer,
    CaseServiceSerializer, CaseReferralSerializer, CaseNoteSerializer,
    CaseAttachmentSerializer, CaseUpdateSerializer, CaseCategorySerializer
)
from .services import CaseService as CaseServiceLogic, CaseSearchService, CaseAnalyticsService
from .filters import CaseFilter, CaseActivityFilter
from apps.core.permissions import IsAuthenticated

logger = logging.getLogger(__name__)


class CaseViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Case model with full CRUD operations.
    """
    queryset = Case.objects.select_related(
        'case_type', 'status', 'priority', 'reporter', 
        'assigned_to', 'escalated_to', 'source_channel'
    ).prefetch_related('categories', 'contact_roles')
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = CaseFilter
    search_fields = ['case_number', 'title', 'narrative', 'reporter__full_name']
    ordering_fields = ['created_at', 'due_date', 'case_number', 'priority']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """Use detailed serializer for retrieve and list actions"""
        if self.action in ['retrieve', 'list']:
            return CaseDetailSerializer
        return CaseSerializer
    
    def get_queryset(self):
        """Filter queryset based on user permissions"""
        queryset = super().get_queryset()
        user = self.request.user
        
        # If user is not admin/supervisor, only show assigned cases or cases they created
        if not user.is_staff and user.role not in ['admin', 'supervisor']:
            queryset = queryset.filter(
                Q(assigned_to=user) | Q(created_by=user)
            )
        
        return queryset.filter(is_active=True)
    
    def perform_create(self, serializer):
        """Set created_by when creating a case"""
        serializer.save(created_by=self.request.user)
    
    def perform_update(self, serializer):
        """Set updated_by when updating a case"""
        serializer.save(updated_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def assign(self, request, pk=None):
        """Assign case to a user"""
        case = self.get_object()
        assigned_to_id = request.data.get('assigned_to')
        
        if not assigned_to_id:
            return Response(
                {'error': 'assigned_to is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            from apps.accounts.models import User
            assigned_to = User.objects.get(id=assigned_to_id)
            CaseServiceLogic.assign_case(case, assigned_to, request.user)
            
            return Response({'message': f'Case assigned to {assigned_to.get_full_name()}'})
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'])
    def escalate(self, request, pk=None):
        """Escalate case to a supervisor"""
        case = self.get_object()
        escalated_to_id = request.data.get('escalated_to')
        reason = request.data.get('reason', '')
        
        if not escalated_to_id:
            return Response(
                {'error': 'escalated_to is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            from apps.accounts.models import User
            escalated_to = User.objects.get(id=escalated_to_id)
            CaseServiceLogic.escalate_case(case, escalated_to, request.user, reason)
            
            return Response({'message': f'Case escalated to {escalated_to.get_full_name()}'})
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'])
    def close(self, request, pk=None):
        """Close a case"""
        case = self.get_object()
        resolution_summary = request.data.get('resolution_summary', '')
        
        try:
            CaseServiceLogic.close_case(case, request.user, resolution_summary)
            return Response({'message': 'Case closed successfully'})
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        """Get case statistics"""
        case = self.get_object()
        stats = CaseServiceLogic.get_case_statistics(case)
        return Response(stats)


class CaseActivityViewSet(viewsets.ModelViewSet):
    """ViewSet for Case Activities"""
    serializer_class = CaseActivitySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = CaseActivityFilter
    search_fields = ['description', 'title']
    ordering_fields = ['created_at', 'activity_type']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return CaseActivity.objects.select_related('case', 'user').all()
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CaseServiceViewSet(viewsets.ModelViewSet):
    """ViewSet for Case Services"""
    serializer_class = CaseServiceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['service_date', 'created_at']
    ordering = ['-service_date']
    
    def get_queryset(self):
        return CaseService.objects.select_related('case', 'service', 'provided_by').all()
    
    def perform_create(self, serializer):
        serializer.save(provided_by=self.request.user)


class CaseReferralViewSet(viewsets.ModelViewSet):
    """ViewSet for Case Referrals"""
    serializer_class = CaseReferralSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['referral_date', 'follow_up_date']
    ordering = ['-referral_date']
    
    def get_queryset(self):
        return CaseReferral.objects.select_related(
            'case', 'referral_type', 'urgency', 'referred_by'
        ).all()
    
    def perform_create(self, serializer):
        serializer.save(referred_by=self.request.user)


class CaseNoteViewSet(viewsets.ModelViewSet):
    """ViewSet for Case Notes"""
    serializer_class = CaseNoteSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'note_type']
    ordering = ['-created_at']
    
    def get_queryset(self):
        queryset = CaseNote.objects.select_related('case', 'author').all()
        
        # Filter private notes based on user permissions
        user = self.request.user
        if not user.is_staff and user.role not in ['admin', 'supervisor']:
            queryset = queryset.filter(
                Q(is_private=False) | Q(author=user)
            )
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CaseAttachmentViewSet(viewsets.ModelViewSet):
    """ViewSet for Case Attachments"""
    serializer_class = CaseAttachmentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['created_at', 'attachment_type']
    ordering = ['-created_at']
    
    def get_queryset(self):
        queryset = CaseAttachment.objects.select_related('case', 'uploaded_by').all()
        
        # Filter confidential attachments based on user permissions
        user = self.request.user
        if not user.is_staff and user.role not in ['admin', 'supervisor']:
            queryset = queryset.filter(
                Q(is_confidential=False) | Q(uploaded_by=user)
            )
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)


class CaseUpdateViewSet(viewsets.ModelViewSet):
    """ViewSet for Case Updates"""
    serializer_class = CaseUpdateSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['created_at', 'next_update_due']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return CaseUpdate.objects.select_related(
            'case', 'updated_by', 'status_at_update', 'priority_at_update'
        ).all()
    
    def perform_create(self, serializer):
        serializer.save(updated_by=self.request.user)


class CaseCategoryViewSet(viewsets.ModelViewSet):
    """ViewSet for Case Categories"""
    serializer_class = CaseCategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    
    def get_queryset(self):
        return CaseCategory.objects.select_related('case', 'category', 'added_by').all()
    
    def perform_create(self, serializer):
        serializer.save(added_by=self.request.user)


# Custom API Views
class AssignCaseView(APIView):
    """API view to assign a case to a user"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request, case_id):
        case = get_object_or_404(Case, id=case_id)
        assigned_to_id = request.data.get('assigned_to')
        
        if not assigned_to_id:
            return Response(
                {'error': 'assigned_to is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            from apps.accounts.models import User
            assigned_to = User.objects.get(id=assigned_to_id)
            CaseServiceLogic.assign_case(case, assigned_to, request.user)
            
            return Response({
                'message': f'Case {case.case_number} assigned to {assigned_to.get_full_name()}'
            })
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )


class EscalateCaseView(APIView):
    """API view to escalate a case"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request, case_id):
        case = get_object_or_404(Case, id=case_id)
        escalated_to_id = request.data.get('escalated_to')
        reason = request.data.get('reason', '')
        
        if not escalated_to_id:
            return Response(
                {'error': 'escalated_to is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            from apps.accounts.models import User
            escalated_to = User.objects.get(id=escalated_to_id)
            CaseServiceLogic.escalate_case(case, escalated_to, request.user, reason)
            
            return Response({
                'message': f'Case {case.case_number} escalated to {escalated_to.get_full_name()}'
            })
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )


class CloseCaseView(APIView):
    """API view to close a case"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request, case_id):
        case = get_object_or_404(Case, id=case_id)
        resolution_summary = request.data.get('resolution_summary', '')
        
        try:
            CaseServiceLogic.close_case(case, request.user, resolution_summary)
            return Response({
                'message': f'Case {case.case_number} closed successfully'
            })
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )


class ReopenCaseView(APIView):
    """API view to reopen a case"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request, case_id):
        case = get_object_or_404(Case, id=case_id)
        reason = request.data.get('reason', '')
        
        try:
            CaseServiceLogic.reopen_case(case, request.user, reason)
            return Response({
                'message': f'Case {case.case_number} reopened successfully'
            })
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )


class AddCaseContactView(APIView):
    """API view to add a contact to a case"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request, case_id):
        case = get_object_or_404(Case, id=case_id)
        contact_id = request.data.get('contact_id')
        role = request.data.get('role')
        is_primary = request.data.get('is_primary', False)
        relationship_id = request.data.get('relationship_id')
        
        if not contact_id or not role:
            return Response(
                {'error': 'contact_id and role are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            from apps.contacts.models import Contact
            from apps.core.models import ReferenceData
            
            contact = Contact.objects.get(id=contact_id)
            relationship = None
            if relationship_id:
                relationship = ReferenceData.objects.get(id=relationship_id)
            
            contact_role = CaseServiceLogic.add_case_contact(
                case=case,
                contact=contact,
                role=role,
                is_primary=is_primary,
                relationship=relationship,
                added_by=request.user
            )
            
            return Response({
                'message': f'Contact {contact.full_name} added to case as {role}',
                'contact_role_id': contact_role.id
            })
        except Contact.DoesNotExist:
            return Response(
                {'error': 'Contact not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )


class CaseStatisticsView(APIView):
    """API view to get case statistics"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, case_id):
        case = get_object_or_404(Case, id=case_id)
        stats = CaseServiceLogic.get_case_statistics(case)
        return Response(stats)


class CaseSearchView(APIView):
    """API view for advanced case search"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        search_params = {
            'query': request.query_params.get('q', ''),
            'status': request.query_params.get('status'),
            'priority': request.query_params.get('priority'),
            'case_type': request.query_params.get('case_type'),
            'assigned_to': request.query_params.get('assigned_to'),
            'is_gbv': request.query_params.get('is_gbv'),
            'is_escalated': request.query_params.get('is_escalated'),
            'is_overdue': request.query_params.get('is_overdue'),
            'page': int(request.query_params.get('page', 1)),
            'page_size': int(request.query_params.get('page_size', 20)),
        }
        
        # Parse date filters
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')
        
        if date_from:
            search_params['date_from'] = timezone.datetime.fromisoformat(date_from)
        if date_to:
            search_params['date_to'] = timezone.datetime.fromisoformat(date_to)
        
        # Parse boolean filters
        for bool_field in ['is_gbv', 'is_escalated', 'is_overdue']:
            value = search_params.get(bool_field)
            if value is not None:
                search_params[bool_field] = value.lower() in ['true', '1', 'yes']
        
        results = CaseSearchService.search_cases(**search_params)
        
        # Serialize the cases
        serializer = CaseDetailSerializer(results['cases'], many=True)
        
        return Response({
            'results': serializer.data,
            'pagination': {
                'total_count': results['total_count'],
                'page_count': results['page_count'],
                'current_page': results['current_page'],
                'has_next': results['has_next'],
                'has_previous': results['has_previous'],
                'next_page': results['next_page'],
                'previous_page': results['previous_page'],
            }
        })


class OverdueCasesView(APIView):
    """API view to get overdue cases"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        assigned_to_id = request.query_params.get('assigned_to')
        assigned_to = None
        
        if assigned_to_id:
            try:
                from apps.accounts.models import User
                assigned_to = User.objects.get(id=assigned_to_id)
            except User.DoesNotExist:
                return Response(
                    {'error': 'User not found'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
        
        overdue_cases = CaseServiceLogic.get_overdue_cases(assigned_to)
        serializer = CaseDetailSerializer(overdue_cases, many=True)
        
        return Response({
            'overdue_cases': serializer.data,
            'count': len(overdue_cases)
        })


class FollowUpCasesView(APIView):
    """API view to get cases requiring follow-up"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        follow_up_cases = CaseServiceLogic.get_cases_requiring_follow_up()
        serializer = CaseDetailSerializer(follow_up_cases, many=True)
        
        return Response({
            'follow_up_cases': serializer.data,
            'count': len(follow_up_cases)
        })


class CaseMetricsView(APIView):
    """API view to get case metrics and analytics"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Parse date range
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')
        assigned_to_id = request.query_params.get('assigned_to')
        
        date_from_parsed = None
        date_to_parsed = None
        assigned_to = None
        
        if date_from:
            date_from_parsed = timezone.datetime.fromisoformat(date_from)
        if date_to:
            date_to_parsed = timezone.datetime.fromisoformat(date_to)
        if assigned_to_id:
            try:
                from apps.accounts.models import User
                assigned_to = User.objects.get(id=assigned_to_id)
            except User.DoesNotExist:
                return Response(
                    {'error': 'User not found'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
        
        metrics = CaseAnalyticsService.get_case_metrics(
            date_from=date_from_parsed,
            date_to=date_to_parsed,
            assigned_to=assigned_to
        )
        
        return Response(metrics)


class BulkAssignCasesView(APIView):
    """API view for bulk case assignment"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        case_ids = request.data.get('case_ids', [])
        assigned_to_id = request.data.get('assigned_to')
        
        if not case_ids or not assigned_to_id:
            return Response(
                {'error': 'case_ids and assigned_to are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            from apps.accounts.models import User
            assigned_to = User.objects.get(id=assigned_to_id)
            
            success_count = 0
            errors = []
            
            for case_id in case_ids:
                try:
                    case = Case.objects.get(id=case_id)
                    CaseServiceLogic.assign_case(case, assigned_to, request.user)
                    success_count += 1
                except Case.DoesNotExist:
                    errors.append(f'Case {case_id} not found')
                except Exception as e:
                    errors.append(f'Error assigning case {case_id}: {str(e)}')
            
            return Response({
                'message': f'{success_count} cases assigned successfully',
                'success_count': success_count,
                'errors': errors
            })
            
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )


class BulkCloseCasesView(APIView):
    """API view for bulk case closure"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        case_ids = request.data.get('case_ids', [])
        resolution_summary = request.data.get('resolution_summary', 'Bulk closure')
        
        if not case_ids:
            return Response(
                {'error': 'case_ids is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        success_count = 0
        errors = []
        
        for case_id in case_ids:
            try:
                case = Case.objects.get(id=case_id)
                CaseServiceLogic.close_case(case, request.user, resolution_summary)
                success_count += 1
            except Case.DoesNotExist:
                errors.append(f'Case {case_id} not found')
            except Exception as e:
                errors.append(f'Error closing case {case_id}: {str(e)}')
        
        return Response({
            'message': f'{success_count} cases closed successfully',
            'success_count': success_count,
            'errors': errors
        })


class ExportCasesView(APIView):
    """API view to export cases to CSV/Excel"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # This would implement case export functionality
        # For now, return a placeholder response
        return Response({
            'message': 'Export functionality to be implemented',
            'formats': ['csv', 'excel', 'pdf']
        })


class CaseAIAnalysisView(APIView):
    """API view to trigger AI analysis for a case"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request, case_id):
        case = get_object_or_404(Case, id=case_id)
        
        # Mark case for AI analysis
        case.ai_analysis_completed = False
        case.save(update_fields=['ai_analysis_completed'])
        
        # Here you would trigger the actual AI analysis
        # For now, return a placeholder response
        return Response({
            'message': f'AI analysis queued for case {case.case_number}',
            'case_id': case.id
        })


class CaseAISuggestionsView(APIView):
    """API view to get AI suggestions for a case"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, case_id):
        case = get_object_or_404(Case, id=case_id)
        
        # Return AI suggestions if available
        suggestions = {
            'suggested_category': case.ai_suggested_category.name if case.ai_suggested_category else None,
            'suggested_priority': case.ai_suggested_priority.name if case.ai_suggested_priority else None,
            'risk_score': case.ai_risk_score,
            'urgency_score': case.ai_urgency_score,
            'sentiment_score': case.ai_sentiment_score,
            'summary': case.ai_summary,
            'keywords': case.ai_keywords,
            'analysis_completed': case.ai_analysis_completed,
            'analysis_date': case.ai_analysis_date
        }
        
        return Response(suggestions)