from rest_framework import generics, permissions, filters, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .models import (
    Case, CaseType, CaseStatus, CaseStatusTransition,
    RelatedCase, CaseNote, CaseAttachment,
    CaseWorkflow, CaseSLA, CaseEventLog
)
from .serializers import (
    CaseListSerializer, CaseDetailSerializer,
    CaseTypeSerializer, CaseStatusSerializer,
    CaseStatusTransitionSerializer, RelatedCaseSerializer,
    CaseNoteSerializer, CaseAttachmentSerializer,
    CaseWorkflowSerializer, CaseSLASerializer,
    CaseEventLogSerializer, CaseBulkUpdateSerializer
)
from apps.shared.core.permissions import IsTenantUser, IsTenantAdmin
from apps.shared.core.pagination import StandardResultsSetPagination

User = get_user_model()

class CaseTypeListCreateView(generics.ListCreateAPIView):
    queryset = CaseType.objects.all()
    serializer_class = CaseTypeSerializer
    permission_classes = [permissions.IsAuthenticated, IsTenantUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return self.queryset.filter(tenant=self.request.tenant)

    def perform_create(self, serializer):
        serializer.save(tenant=self.request.tenant)

class CaseTypeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CaseType.objects.all()
    serializer_class = CaseTypeSerializer
    permission_classes = [permissions.IsAuthenticated, IsTenantUser]
    lookup_field = 'pk'

    def get_queryset(self):
        return self.queryset.filter(tenant=self.request.tenant)

class CaseStatusListCreateView(generics.ListCreateAPIView):
    queryset = CaseStatus.objects.all()
    serializer_class = CaseStatusSerializer
    permission_classes = [permissions.IsAuthenticated, IsTenantUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'is_initial', 'is_closed']
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return self.queryset.filter(tenant=self.request.tenant)

    def perform_create(self, serializer):
        serializer.save(tenant=self.request.tenant)

class CaseStatusRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CaseStatus.objects.all()
    serializer_class = CaseStatusSerializer
    permission_classes = [permissions.IsAuthenticated, IsTenantUser]
    lookup_field = 'pk'

    def get_queryset(self):
        return self.queryset.filter(tenant=self.request.tenant)

class CaseStatusTransitionListCreateView(generics.ListCreateAPIView):
    queryset = CaseStatusTransition.objects.all()
    serializer_class = CaseStatusTransitionSerializer
    permission_classes = [permissions.IsAuthenticated, IsTenantAdmin]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['from_status', 'to_status']
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return self.queryset.filter(tenant=self.request.tenant)

    def perform_create(self, serializer):
        serializer.save(tenant=self.request.tenant)

class CaseListCreateView(generics.ListCreateAPIView):
    queryset = Case.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsTenantUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        'status': ['exact'],
        'priority': ['exact'],
        'assigned_to': ['exact', 'isnull'],
        'contact': ['exact'],
        'case_type': ['exact'],
        'opened_date': ['gte', 'lte', 'exact'],
        'due_date': ['gte', 'lte', 'exact'],
        'sla_breached': ['exact'],
        'is_escalated': ['exact'],
    }
    search_fields = [
        'case_number', 'title', 'description',
        'contact__first_name', 'contact__last_name',
        'contact__organization'
    ]
    ordering_fields = [
        'case_number', 'opened_date', 'due_date',
        'priority', 'status', 'assigned_to'
    ]
    pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CaseListSerializer
        return CaseDetailSerializer

    def get_queryset(self):
        return self.queryset.filter(
            tenant=self.request.tenant
        ).select_related(
            'status', 'case_type', 'assigned_to', 'contact'
        ).prefetch_related(
            'notes', 'attachments', 'primary_relations'
        )

    def perform_create(self, serializer):
        serializer.save(tenant=self.request.tenant, created_by=self.request.user)

class CaseRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Case.objects.all()
    serializer_class = CaseDetailSerializer
    permission_classes = [permissions.IsAuthenticated, IsTenantUser]
    lookup_field = 'pk'

    def get_queryset(self):
        return self.queryset.filter(
            tenant=self.request.tenant
        ).select_related(
            'status', 'case_type', 'assigned_to', 'contact'
        ).prefetch_related(
            'notes', 'attachments', 'primary_relations', 'event_logs'
        )

    def perform_update(self, serializer):
        serializer.save(last_modified_by=self.request.user)

class CaseBulkUpdateView(generics.GenericAPIView):
    serializer_class = CaseBulkUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsTenantAdmin]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        cases = Case.objects.filter(
            id__in=serializer.validated_data['case_ids'],
            tenant=request.tenant
        )
        
        update_fields = {}
        if 'status_id' in serializer.validated_data:
            update_fields['status'] = serializer.validated_data['status_id']
        if 'assigned_to_id' in serializer.validated_data:
            update_fields['assigned_to'] = serializer.validated_data['assigned_to_id']
        if 'priority' in serializer.validated_data:
            update_fields['priority'] = serializer.validated_data['priority']
        
        updated_count = cases.update(**update_fields)
        
        # Create event logs for each updated case
        for case in cases:
            CaseEventLog.objects.create(
                case=case,
                event_type='bulk_update',
                new_value=update_fields,
                tenant=request.tenant
            )
        
        return Response({
            'message': f'Successfully updated {updated_count} cases',
            'updated_fields': list(update_fields.keys())
        }, status=status.HTTP_200_OK)

class RelatedCaseListCreateView(generics.ListCreateAPIView):
    queryset = RelatedCase.objects.all()
    serializer_class = RelatedCaseSerializer
    permission_classes = [permissions.IsAuthenticated, IsTenantUser]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        case_id = self.kwargs['case_id']
        return self.queryset.filter(
            primary_case_id=case_id,
            primary_case__tenant=self.request.tenant
        ).select_related('related_case')

    def perform_create(self, serializer):
        case = get_object_or_404(
            Case,
            pk=self.kwargs['case_id'],
            tenant=self.request.tenant
        )
        serializer.save(primary_case=case)

class RelatedCaseRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    queryset = RelatedCase.objects.all()
    serializer_class = RelatedCaseSerializer
    permission_classes = [permissions.IsAuthenticated, IsTenantUser]
    lookup_field = 'pk'

    def get_queryset(self):
        return self.queryset.filter(
            primary_case__tenant=self.request.tenant
        )

class CaseNoteListCreateView(generics.ListCreateAPIView):
    queryset = CaseNote.objects.all()
    serializer_class = CaseNoteSerializer
    permission_classes = [permissions.IsAuthenticated, IsTenantUser]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at']
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        case_id = self.kwargs['case_id']
        return self.queryset.filter(
            case_id=case_id,
            case__tenant=self.request.tenant
        ).select_related('created_by', 'document')

    def perform_create(self, serializer):
        case = get_object_or_404(
            Case,
            pk=self.kwargs['case_id'],
            tenant=self.request.tenant
        )
        serializer.save(case=case, created_by=self.request.user)

class CaseNoteRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CaseNote.objects.all()
    serializer_class = CaseNoteSerializer
    permission_classes = [permissions.IsAuthenticated, IsTenantUser]
    lookup_field = 'pk'

    def get_queryset(self):
        return self.queryset.filter(
            case__tenant=self.request.tenant
        )

class CaseAttachmentListCreateView(generics.ListCreateAPIView):
    queryset = CaseAttachment.objects.all()
    serializer_class = CaseAttachmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsTenantUser]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at']
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        case_id = self.kwargs['case_id']
        return self.queryset.filter(
            case_id=case_id,
            case__tenant=self.request.tenant
        ).select_related('document')

    def perform_create(self, serializer):
        case = get_object_or_404(
            Case,
            pk=self.kwargs['case_id'],
            tenant=self.request.tenant
        )
        serializer.save(case=case)

class CaseWorkflowListCreateView(generics.ListCreateAPIView):
    queryset = CaseWorkflow.objects.all()
    serializer_class = CaseWorkflowSerializer
    permission_classes = [permissions.IsAuthenticated, IsTenantAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name', 'description', 'trigger_event']
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return self.queryset.filter(tenant=self.request.tenant)

    def perform_create(self, serializer):
        serializer.save(tenant=self.request.tenant)

class CaseWorkflowRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CaseWorkflow.objects.all()
    serializer_class = CaseWorkflowSerializer
    permission_classes = [permissions.IsAuthenticated, IsTenantAdmin]
    lookup_field = 'pk'

    def get_queryset(self):
        return self.queryset.filter(tenant=self.request.tenant)

class CaseSLAListCreateView(generics.ListCreateAPIView):
    queryset = CaseSLA.objects.all()
    serializer_class = CaseSLASerializer
    permission_classes = [permissions.IsAuthenticated, IsTenantAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name', 'description']
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return self.queryset.filter(tenant=self.request.tenant)

    def perform_create(self, serializer):
        serializer.save(tenant=self.request.tenant)

class CaseSLARetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CaseSLA.objects.all()
    serializer_class = CaseSLASerializer
    permission_classes = [permissions.IsAuthenticated, IsTenantAdmin]
    lookup_field = 'pk'

    def get_queryset(self):
        return self.queryset.filter(tenant=self.request.tenant)

class CaseEventLogListView(generics.ListAPIView):
    queryset = CaseEventLog.objects.all()
    serializer_class = CaseEventLogSerializer
    permission_classes = [permissions.IsAuthenticated, IsTenantUser]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['event_type', 'created_at']
    ordering_fields = ['-created_at']
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        case_id = self.kwargs['case_id']
        return self.queryset.filter(
            case_id=case_id,
            case__tenant=self.request.tenant
        )