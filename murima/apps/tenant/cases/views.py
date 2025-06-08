from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model
from apps.shared.core.models import AuditLog
from .models import (
    CaseType, CaseStatus, Case, CaseDocument, CaseNote,
    CaseHistory, CaseLink, CaseTemplate, SLA, WorkflowRule
)
from .serializers import (
    CaseTypeSerializer, CaseStatusSerializer, CaseSerializer,
    CaseDocumentSerializer, CaseNoteSerializer, CaseHistorySerializer,
    CaseLinkSerializer, CaseTemplateSerializer, SLASerializer,
    WorkflowRuleSerializer, CaseWithRelatedSerializer, AuditLogSerializer
)
from .filters import CaseFilter, AuditLogFilter
from apps.shared.core.permissions import (
    IsCaseOwnerOrTeamMember, IsCaseTeamMember, CanEditCase,
    CanAccessCaseDocuments, CanAccessCaseNotes
)

User = get_user_model()

class CaseTypeListCreateView(generics.ListCreateAPIView):
    queryset = CaseType.objects.filter(is_active=True)
    serializer_class = CaseTypeSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'code', 'description']
    filterset_fields = ['is_active']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class CaseTypeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CaseType.objects.all()
    serializer_class = CaseTypeSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]
    lookup_field = 'pk'

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


class CaseStatusListCreateView(generics.ListCreateAPIView):
    queryset = CaseStatus.objects.filter(is_active=True)
    serializer_class = CaseStatusSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'code', 'description']
    filterset_fields = ['is_active', 'is_closed', 'is_default']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class CaseStatusRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CaseStatus.objects.all()
    serializer_class = CaseStatusSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]
    lookup_field = 'pk'

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


class CaseListCreateView(generics.ListCreateAPIView):
    serializer_class = CaseSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['case_number', 'title', 'description', 'reference_id']
    filterset_class = CaseFilter
    ordering_fields = ['created_at', 'updated_at', 'due_date', 'priority']
    ordering = ['-created_at']

    def get_queryset(self):
        user = self.request.user
        queryset = Case.objects.all()
        
        # If user doesn't have view_all permission, filter cases they have access to
        if not user.has_perm('cases.view_all_cases'):
            queryset = queryset.filter(
                models.Q(assigned_to=user) |
                models.Q(assigned_team__members=user) |
                models.Q(created_by=user)
            ).distinct()
        
        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class CaseRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Case.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsCaseOwnerOrTeamMember | permissions.DjangoModelPermissions]
    lookup_field = 'pk'

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CaseWithRelatedSerializer
        return CaseSerializer

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def perform_destroy(self, instance):
        instance.soft_delete(user=self.request.user)


class CaseDocumentListCreateView(generics.ListCreateAPIView):
    serializer_class = CaseDocumentSerializer
    permission_classes = [permissions.IsAuthenticated, CanAccessCaseDocuments]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['description', 'file_type']
    filterset_fields = ['file_type', 'is_current']

    def get_queryset(self):
        case_id = self.kwargs.get('case_pk')
        return CaseDocument.objects.filter(case_id=case_id)

    def perform_create(self, serializer):
        case = Case.objects.get(pk=self.kwargs['case_pk'])
        serializer.save(case=case, uploaded_by=self.request.user)


class CaseDocumentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CaseDocumentSerializer
    permission_classes = [permissions.IsAuthenticated, CanAccessCaseDocuments]
    lookup_field = 'pk'

    def get_queryset(self):
        case_id = self.kwargs.get('case_pk')
        return CaseDocument.objects.filter(case_id=case_id)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class CaseNoteListCreateView(generics.ListCreateAPIView):
    serializer_class = CaseNoteSerializer
    permission_classes = [permissions.IsAuthenticated, CanAccessCaseNotes]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['content']
    filterset_fields = ['is_internal', 'pinned']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-pinned', '-created_at']

    def get_queryset(self):
        case_id = self.kwargs.get('case_pk')
        user = self.request.user
        
        queryset = CaseNote.objects.filter(case_id=case_id)
        
        # Filter out internal notes if user doesn't have permission
        if not user.has_perm('cases.view_internal_notes'):
            queryset = queryset.filter(is_internal=False)
            
        return queryset

    def perform_create(self, serializer):
        case = Case.objects.get(pk=self.kwargs['case_pk'])
        serializer.save(case=case, created_by=self.request.user)


class CaseNoteRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CaseNoteSerializer
    permission_classes = [permissions.IsAuthenticated, CanAccessCaseNotes]
    lookup_field = 'pk'

    def get_queryset(self):
        case_id = self.kwargs.get('case_pk')
        user = self.request.user
        
        queryset = CaseNote.objects.filter(case_id=case_id)
        
        # Filter out internal notes if user doesn't have permission
        if not user.has_perm('cases.view_internal_notes'):
            queryset = queryset.filter(is_internal=False)
            
        return queryset

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class CaseHistoryListView(generics.ListAPIView):
    serializer_class = CaseHistorySerializer
    permission_classes = [permissions.IsAuthenticated, IsCaseOwnerOrTeamMember]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['action']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        case_id = self.kwargs.get('case_pk')
        return CaseHistory.objects.filter(case_id=case_id)


class CaseLinkListCreateView(generics.ListCreateAPIView):
    serializer_class = CaseLinkSerializer
    permission_classes = [permissions.IsAuthenticated, CanEditCase]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['relationship_type']

    def get_queryset(self):
        case_id = self.kwargs.get('case_pk')
        return CaseLink.objects.filter(source_case_id=case_id)

    def perform_create(self, serializer):
        source_case = Case.objects.get(pk=self.kwargs['case_pk'])
        serializer.save(source_case=source_case, created_by=self.request.user)


class CaseLinkRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CaseLinkSerializer
    permission_classes = [permissions.IsAuthenticated, CanEditCase]
    lookup_field = 'pk'

    def get_queryset(self):
        case_id = self.kwargs.get('case_pk')
        return CaseLink.objects.filter(source_case_id=case_id)


class CaseTemplateListCreateView(generics.ListCreateAPIView):
    queryset = CaseTemplate.objects.filter(is_active=True)
    serializer_class = CaseTemplateSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'description']
    filterset_fields = ['case_type', 'is_active']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class CaseTemplateRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CaseTemplate.objects.all()
    serializer_class = CaseTemplateSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]
    lookup_field = 'pk'

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


class SLAListCreateView(generics.ListCreateAPIView):
    queryset = SLA.objects.filter(is_active=True)
    serializer_class = SLASerializer
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['case_type', 'priority', 'is_active']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class SLARetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SLA.objects.all()
    serializer_class = SLASerializer
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]
    lookup_field = 'pk'

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


class WorkflowRuleListCreateView(generics.ListCreateAPIView):
    queryset = WorkflowRule.objects.filter(is_active=True)
    serializer_class = WorkflowRuleSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['case_type', 'priority', 'trigger_condition', 'is_active']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class WorkflowRuleRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = WorkflowRule.objects.all()
    serializer_class = WorkflowRuleSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]
    lookup_field = 'pk'

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


class AuditLogListView(generics.ListAPIView):
    serializer_class = AuditLogSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = AuditLogFilter
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        # Only show audit logs for objects the user has permission to view
        user = self.request.user
        queryset = AuditLog.objects.all()
        
        if not user.has_perm('core.view_all_auditlogs'):
            # Filter to only show logs for cases the user has access to
            accessible_case_ids = Case.objects.filter(
                models.Q(assigned_to=user) |
                models.Q(assigned_team__members=user) |
                models.Q(created_by=user)
            ).values_list('id', flat=True)
            
            case_content_type = ContentType.objects.get_for_model(Case)
            queryset = queryset.filter(
                models.Q(object_type=case_content_type, object_id__in=accessible_case_ids) |
                models.Q(user=user)
            )
        
        return queryset


class MyAssignedCasesView(generics.ListAPIView):
    serializer_class = CaseSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['case_number', 'title', 'description', 'reference_id']
    filterset_class = CaseFilter
    ordering_fields = ['created_at', 'updated_at', 'due_date', 'priority']
    ordering = ['-created_at']

    def get_queryset(self):
        user = self.request.user
        return Case.objects.filter(
            models.Q(assigned_to=user) |
            models.Q(assigned_team__members=user)
        ).distinct()


class MyTeamCasesView(generics.ListAPIView):
    serializer_class = CaseSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['case_number', 'title', 'description', 'reference_id']
    filterset_class = CaseFilter
    ordering_fields = ['created_at', 'updated_at', 'due_date', 'priority']
    ordering = ['-created_at']

    def get_queryset(self):
        user = self.request.user
        return Case.objects.filter(
            assigned_team__members=user
        ).distinct()