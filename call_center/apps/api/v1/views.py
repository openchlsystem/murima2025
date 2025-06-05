# # apps/api/v1/views.py
# from rest_framework import viewsets, status
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from django.shortcuts import get_object_or_404

# from apps.api.pagination import StandardResultsSetPagination
# from apps.api.permissions import IsOwnerOrStaff, HasCasePermission
# from apps.cases.models import Case
# from apps.contacts.models import Contact
# from apps.calls.models import Call
# from apps.campaigns.models import Campaign
# from apps.accounts.models import User
# from apps.notifications.models import Notification
# from apps.core.models import ReferenceData

# from apps.cases.services import CaseService # type: ignore
# from apps.ai.services.case_service import CaseAIService

# from . import serializers

# class CaseViewSet(viewsets.ModelViewSet):
#     """ViewSet for cases."""
#     serializer_class = serializers.CaseSerializer
#     permission_classes = [IsAuthenticated, HasCasePermission]
#     pagination_class = StandardResultsSetPagination
#     filterset_fields = ['status', 'priority', 'assigned_to', 'created_by', 'is_gbv_related']
#     search_fields = ['case_number', 'narrative', 'reporter__full_name', 'reporter__phone']
#     ordering_fields = ['created_at', 'updated_at', 'closed_at', 'priority']
    
#     def get_queryset(self):
#         """Filter cases based on permissions."""
#         user = self.request.user
        
#         # Admins and managers see all cases
#         if user.is_staff or user.role in ['admin', 'manager']:
#             return Case.objects.all()
            
#         # Supervisors see all cases they supervise plus their own
#         if user.role == 'supervisor':
#             supervised_users = User.objects.filter(
#                 created_by=user
#             ).values_list('id', flat=True)
            
#             return Case.objects.filter(
#                 # Cases created by supervisor or their team
#                 created_by__in=list(supervised_users) + [user.id]
#             )
            
#         # Regular users see only their cases
#         return Case.objects.filter(
#             created_by=user
#         )
    
#     def get_serializer_class(self):
#         """Return different serializers for different actions."""
#         if self.action == 'list':
#             return serializers.CaseListSerializer
#         elif self.action == 'retrieve':
#             return serializers.CaseDetailSerializer
#         return serializers.CaseSerializer
    
#     def perform_create(self, serializer):
#         """Set created_by when creating cases."""
#         serializer.save(created_by=self.request.user)
    
#     @action(detail=True, methods=['post'])
#     def close(self, request, pk=None):
#         """Close a case."""
#         case = self.get_object()
#         status_id = request.data.get('status_id')
#         comments = request.data.get('comments')
        
#         try:
#             updated_case = CaseService.close_case(
#                 case_id=case.id,
#                 user=request.user,
#                 status_id=status_id,
#                 comments=comments
#             )
            
#             serializer = self.get_serializer(updated_case)
#             return Response(serializer.data)
            
#         except Exception as e:
#             return Response(
#                 {'error': str(e)},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
    
#     @action(detail=True, methods=['post'])
#     def escalate(self, request, pk=None):
#         """Escalate a case to another user."""
#         case = self.get_object()
#         escalated_to_id = request.data.get('escalated_to_id')
#         comments = request.data.get('comments')
        
#         try:
#             from apps.accounts.models import User
#             escalated_to = User.objects.get(id=escalated_to_id)
            
#             updated_case = CaseService.escalate_case(
#                 case_id=case.id,
#                 escalated_to=escalated_to,
#                 escalated_by=request.user,
#                 comments=comments
#             )
            
#             serializer = self.get_serializer(updated_case)
#             return Response(serializer.data)
            
#         except User.DoesNotExist:
#             return Response(
#                 {'error': 'User not found'},
#                 status=status.HTTP_404_NOT_FOUND
#             )
#         except Exception as e:
#             return Response(
#                 {'error': str(e)},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
    
#     @action(detail=True, methods=['post'])
#     def assign(self, request, pk=None):
#         """Assign a case to a user."""
#         case = self.get_object()
#         assigned_to_id = request.data.get('assigned_to_id')
#         comments = request.data.get('comments')
        
#         try:
#             from apps.accounts.models import User
#             assigned_to = User.objects.get(id=assigned_to_id)
            
#             updated_case = CaseService.assign_case(
#                 case_id=case.id,
#                 assigned_to=assigned_to,
#                 assigned_by=request.user,
#                 comments=comments
#             )
            
#             serializer = self.get_serializer(updated_case)
#             return Response(serializer.data)
            
#         except User.DoesNotExist:
#             return Response(
#                 {'error': 'User not found'},
#                 status=status.HTTP_404_NOT_FOUND
#             )
#         except Exception as e:
#             return Response(
#                 {'error': str(e)},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
    
#     @action(detail=True, methods=['get'])
#     def activities(self, request, pk=None):
#         """Get case activities."""
#         case = self.get_object()
#         activities = case.activities.all().order_by('-created_at')
        
#         page = self.paginate_queryset(activities)
#         if page is not None:
#             serializer = serializers.CaseActivitySerializer(page, many=True)
#             return self.get_paginated_response(serializer.data)
            
#         serializer = serializers.CaseActivitySerializer(activities, many=True)
#         return Response(serializer.data)
    
#     @action(detail=True, methods=['get'])
#     def ai_suggestions(self, request, pk=None):
#         """Get AI suggestions for this case."""
#         case = self.get_object()
#         suggestions = CaseAIService.get_case_suggestions(case, user=request.user)
#         return Response(suggestions)
        
#     @action(detail=True, methods=['post'])
#     def ai_categorize(self, request, pk=None):
#         """Categorize this case using AI."""
#         case = self.get_object()
#         narrative = request.data.get('narrative', case.narrative)
#         categories = CaseAIService.categorize_case(
#             case=case,
#             narrative=narrative,
#             user=request.user
#         )
#         return Response(categories)

# class ContactViewSet(viewsets.ModelViewSet):
#     """ViewSet for contacts."""
#     queryset = Contact.objects.all()
#     serializer_class = serializers.ContactSerializer
#     permission_classes = [IsAuthenticated]
#     pagination_class = StandardResultsSetPagination
#     filterset_fields = ['nationality', 'sex', 'age_group']
#     search_fields = ['full_name', 'phone', 'email', 'address']
#     ordering_fields = ['full_name', 'created_at']
    
#     def get_serializer_class(self):
#         """Return different serializers for different actions."""
#         if self.action == 'list':
#             return serializers.ContactListSerializer
#         return serializers.ContactSerializer

# class CallViewSet(viewsets.ModelViewSet):
#     """ViewSet for calls."""
#     queryset = Call.objects.all()
#     serializer_class = serializers.CallSerializer
#     permission_classes = [IsAuthenticated]
#     pagination_class = StandardResultsSetPagination
#     filterset_fields = ['direction', 'status', 'agent', 'campaign']
#     search_fields = ['caller_number', 'caller_name', 'agent__username']
#     ordering_fields = ['start_time', 'duration_seconds']
    
#     def get_serializer_class(self):
#         """Return different serializers for different actions."""
#         if self.action == 'list':
#             return serializers.CallListSerializer
#         return serializers.CallSerializer

# class CampaignViewSet(viewsets.ModelViewSet):
#     """ViewSet for campaigns."""
#     queryset = Campaign.objects.all()
#     serializer_class = serializers.CampaignSerializer
#     permission_classes = [IsAuthenticated]
#     pagination_class = StandardResultsSetPagination
#     filterset_fields = ['campaign_type', 'is_active']
#     search_fields = ['name', 'description']
#     ordering_fields = ['name', 'created_at']

# class UserViewSet(viewsets.ReadOnlyModelViewSet):
#     """ViewSet for users, read-only."""
#     queryset = User.objects.filter(is_active=True)
#     serializer_class = serializers.UserSerializer
#     permission_classes = [IsAuthenticated]
#     pagination_class = StandardResultsSetPagination
#     filterset_fields = ['role']
#     search_fields = ['username', 'first_name', 'last_name', 'email']
#     ordering_fields = ['username', 'date_joined']

# class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
#     """ViewSet for notifications."""
#     serializer_class = serializers.NotificationSerializer
#     permission_classes = [IsAuthenticated]
#     pagination_class = StandardResultsSetPagination
    
#     def get_queryset(self):
#         """Return only the user's notifications."""
#         return Notification.objects.filter(
#             user=self.request.user
#         ).order_by('-created_at')
    
#     @action(detail=False, methods=['get'])
#     def unread(self, request):
#         """Get unread notifications."""
#         from apps.notifications.services import NotificationService
#         notifications = NotificationService.get_unread_notifications(request.user)
        
#         page = self.paginate_queryset(notifications)
#         if page is not None:
#             serializer = self.get_serializer(page, many=True)
#             return self.get_paginated_response(serializer.data)
            
#         serializer = self.get_serializer(notifications, many=True)
#         return Response(serializer.data)
    
#     @action(detail=True, methods=['post'])
#     def mark_read(self, request, pk=None):
#         """Mark a notification as read."""
#         notification = self.get_object()
#         notification.mark_as_read()
#         serializer = self.get_serializer(notification)
#         return Response(serializer.data)
    
#     @action(detail=False, methods=['post'])
#     def mark_all_read(self, request):
#         """Mark all notifications as read."""
#         from apps.notifications.services import NotificationService
#         count = NotificationService.mark_all_as_read(request.user)
#         return Response({'marked_read': count})

# class ReferenceDataViewSet(viewsets.ReadOnlyModelViewSet):
#     """ViewSet for reference data."""
#     queryset = ReferenceData.objects.filter(is_active=True)
#     serializer_class = serializers.ReferenceDataSerializer
#     permission_classes = [IsAuthenticated]
#     filterset_fields = ['category', 'level']
#     search_fields = ['name', 'code']
#     ordering_fields = ['category', 'level', 'name']
    
#     @action(detail=False, methods=['get'])
#     def by_category(self, request):
#         """Get reference data by category."""
#         category = request.query_params.get('category')
#         if not category:
#             return Response(
#                 {'error': 'Category parameter is required'},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
            
#         data = ReferenceData.objects.filter(
#             category=category,
#             is_active=True
#         ).order_by('level', 'name')
        
#         serializer = self.get_serializer(data, many=True)
#         return Response(serializer.data)

# class AIViewSet(viewsets.ViewSet):
#     """ViewSet for AI operations."""
#     permission_classes = [IsAuthenticated]
    
#     @action(detail=True, methods=['get'], url_path='case-suggestions')
#     def case_suggestions(self, request, pk=None):
#         """Get AI suggestions for a case."""
#         case = get_object_or_404(Case, pk=pk)
        
#         # Check permissions
#         if not request.user.has_perm('cases.view_case'):
#             return Response(
#                 {"error": "You don't have permission to access this case"},
#                 status=status.HTTP_403_FORBIDDEN
#             )
        
#         suggestions = CaseAIService.get_case_suggestions(case, user=request.user)
#         return Response(suggestions)
    
#     @action(detail=True, methods=['post'], url_path='categorize-case')
#     def categorize_case(self, request, pk=None):
#         """Categorize a case using AI."""
#         case = get_object_or_404(Case, pk=pk)
        
#         # Check permissions
#         if not request.user.has_perm('cases.change_case'):
#             return Response(
#                 {"error": "You don't have permission to modify this case"},
#                 status=status.HTTP_403_FORBIDDEN
#             )
        
#         # Get narrative from request or use case narrative
#         narrative = request.data.get('narrative', case.narrative)
        
#         categories = CaseAIService.categorize_case(
#             case=case,
#             narrative=narrative,
#             user=request.user
#         )
        
#         return Response(categories)