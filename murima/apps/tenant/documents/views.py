from rest_framework import generics, permissions, filters, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.http import FileResponse, Http404
from django.contrib.auth import get_user_model
from .models import (
    Document, DocumentType, DocumentVersion,
    DocumentAccessLog, DocumentShareLink,
    DocumentPreview, DocumentTemplate
)
from .serializers import (
    DocumentSerializer, DocumentUploadSerializer,
    DocumentTypeSerializer, DocumentVersionSerializer,
    DocumentAccessLogSerializer, DocumentShareLinkSerializer,
    DocumentPreviewSerializer, DocumentTemplateSerializer,
    DocumentSearchSerializer, DocumentBulkUpdateSerializer
)
from apps.shared.core.permissions import (
    IsTenantUser, IsTenantAdmin,
    HasDocumentPermission
)
from apps.shared.core.pagination import StandardResultsSetPagination
from apps.tenant.cases.models import Case
from apps.tenant.contacts.models import Contact
from apps.tenant.tasks.models import Task

User = get_user_model()

class DocumentTypeListCreateView(generics.ListCreateAPIView):
    queryset = DocumentType.objects.all()
    serializer_class = DocumentTypeSerializer
    permission_classes = [permissions.IsAuthenticated, IsTenantAdmin]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']

    def get_queryset(self):
        return self.queryset.filter(tenant=self.request.tenant)

    def perform_create(self, serializer):
        serializer.save(tenant=self.request.tenant)

class DocumentTypeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DocumentType.objects.all()
    serializer_class = DocumentTypeSerializer
    permission_classes = [permissions.IsAuthenticated, IsTenantAdmin]
    lookup_field = 'pk'

    def get_queryset(self):
        return self.queryset.filter(tenant=self.request.tenant)

class DocumentListCreateView(generics.ListCreateAPIView):
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated, IsTenantUser]
    pagination_class = StandardResultsSetPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = {
        'document_type': ['exact'],
        'category': ['exact'],
        'permission_level': ['exact'],
        'created_at': ['gte', 'lte', 'exact'],
        'case': ['exact', 'isnull'],
        'contact': ['exact', 'isnull'],
        'task': ['exact', 'isnull'],
    }
    search_fields = [
        'title', 'description',
        'case__title', 'contact__first_name',
        'contact__last_name', 'task__title'
    ]
    ordering_fields = [
        'title', 'created_at', 'file_size',
        'permission_level', 'category'
    ]

    def get_queryset(self):
        queryset = Document.objects.filter(
            tenant=self.request.tenant
        ).select_related(
            'document_type', 'case', 'contact', 'task', 'created_by'
        ).prefetch_related('versions', 'access_logs')

        # Apply additional permission filtering
        if not self.request.user.is_superuser:
            queryset = queryset.filter(
                permission_level__lte=Document.DocumentPermissionLevel.INTERNAL.value
            )
        return queryset

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return DocumentUploadSerializer
        return DocumentSerializer

    def perform_create(self, serializer):
        serializer.save(
            tenant=self.request.tenant,
            created_by=self.request.user
        )

class DocumentSearchView(generics.ListAPIView):
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated, IsTenantUser]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        serializer = DocumentSearchSerializer(data=self.request.query_params)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        queryset = Document.objects.filter(
            tenant=self.request.tenant
        ).select_related(
            'document_type', 'case', 'contact', 'task'
        )

        # Apply filters
        if data.get('query'):
            queryset = queryset.filter(
                models.Q(title__icontains=data['query']) |
                models.Q(description__icontains=data['query'])
            )
        if data.get('category'):
            queryset = queryset.filter(category=data['category'])
        if data.get('document_type'):
            queryset = queryset.filter(document_type=data['document_type'])
        if data.get('case_id'):
            queryset = queryset.filter(case=data['case_id'])
        if data.get('contact_id'):
            queryset = queryset.filter(contact=data['contact_id'])
        if data.get('task_id'):
            queryset = queryset.filter(task=data['task_id'])
        if data.get('tags'):
            queryset = queryset.filter(tags__overlap=data['tags'])
        if data.get('uploaded_after'):
            queryset = queryset.filter(created_at__gte=data['uploaded_after'])
        if data.get('uploaded_before'):
            queryset = queryset.filter(created_at__lte=data['uploaded_before'])

        # Apply sorting
        sort_by = data.get('sort_by', 'created_at')
        sort_order = data.get('sort_order', 'desc')
        if sort_order == 'desc':
            sort_by = f'-{sort_by}'
        queryset = queryset.order_by(sort_by)

        return queryset

class DocumentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated, HasDocumentPermission]
    lookup_field = 'pk'

    def get_queryset(self):
        return self.queryset.filter(
            tenant=self.request.tenant
        ).select_related(
            'document_type', 'case', 'contact', 'task', 'created_by'
        ).prefetch_related('versions', 'access_logs')

    def perform_update(self, serializer):
        serializer.save(last_modified_by=self.request.user)

    def perform_destroy(self, instance):
        # Log the deletion
        DocumentAccessLog.objects.create(
            document=instance,
            access_type='delete',
            user=self.request.user,
            tenant=self.request.tenant,
            ip_address=self.request.META.get('REMOTE_ADDR'),
            user_agent=self.request.META.get('HTTP_USER_AGENT', '')
        )
        instance.delete()

class DocumentDownloadView(generics.RetrieveAPIView):
    queryset = Document.objects.all()
    permission_classes = [permissions.IsAuthenticated, HasDocumentPermission]

    def get(self, request, *args, **kwargs):
        document = self.get_object()
        
        # Log the download
        DocumentAccessLog.objects.create(
            document=document,
            access_type='download',
            user=request.user,
            tenant=request.tenant,
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )

        try:
            response = FileResponse(
                document.file.open('rb'),
                as_attachment=True,
                filename=document.file.name.split('/')[-1]
            )
            response['Content-Length'] = document.file_size
            return response
        except FileNotFoundError:
            raise Http404("File not found")

class DocumentVersionListView(generics.ListAPIView):
    serializer_class = DocumentVersionSerializer
    permission_classes = [permissions.IsAuthenticated, HasDocumentPermission]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        document = get_object_or_404(
            Document,
            pk=self.kwargs['pk'],
            tenant=self.request.tenant
        )
        return DocumentVersion.objects.filter(
            document=document
        ).order_by('-version')

class DocumentVersionDownloadView(generics.RetrieveAPIView):
    queryset = DocumentVersion.objects.all()
    permission_classes = [permissions.IsAuthenticated, HasDocumentPermission]

    def get_object(self):
        document = get_object_or_404(
            Document,
            pk=self.kwargs['document_pk'],
            tenant=self.request.tenant
        )
        return get_object_or_404(
            DocumentVersion,
            document=document,
            version=self.kwargs['version']
        )

    def get(self, request, *args, **kwargs):
        version = self.get_object()
        
        # Log the access
        DocumentAccessLog.objects.create(
            document=version.document,
            access_type='version_download',
            user=request.user,
            tenant=request.tenant,
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )

        try:
            response = FileResponse(
                version.file.open('rb'),
                as_attachment=True,
                filename=f"v{version.version}_{version.file.name.split('/')[-1]}"
            )
            response['Content-Length'] = version.file_size
            return response
        except FileNotFoundError:
            raise Http404("File not found")

class DocumentAccessLogListView(generics.ListAPIView):
    serializer_class = DocumentAccessLogSerializer
    permission_classes = [permissions.IsAuthenticated, IsTenantAdmin]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = {
        'document': ['exact'],
        'access_type': ['exact'],
        'created_at': ['gte', 'lte', 'exact'],
        'user': ['exact']
    }
    ordering_fields = ['-created_at']

    def get_queryset(self):
        document_id = self.kwargs.get('document_pk')
        queryset = DocumentAccessLog.objects.filter(
            tenant=self.request.tenant
        ).select_related('document', 'user')

        if document_id:
            queryset = queryset.filter(document_id=document_id)
        
        return queryset

class DocumentShareLinkCreateView(generics.CreateAPIView):
    serializer_class = DocumentShareLinkSerializer
    permission_classes = [permissions.IsAuthenticated, IsTenantUser]

    def perform_create(self, serializer):
        document = get_object_or_404(
            Document,
            pk=self.kwargs['document_pk'],
            tenant=self.request.tenant
        )
        serializer.save(
            document=document,
            created_by=self.request.user,
            tenant=self.request.tenant
        )

class DocumentShareLinkRetrieveView(generics.RetrieveAPIView):
    queryset = DocumentShareLink.objects.all()
    serializer_class = DocumentShareLinkSerializer
    permission_classes = [permissions.IsAuthenticated, IsTenantUser]
    lookup_field = 'token'

    def get_object(self):
        return get_object_or_404(
            DocumentShareLink,
            token=self.kwargs['token'],
            is_active=True,
            tenant=self.request.tenant
        )

class DocumentShareLinkDownloadView(generics.RetrieveAPIView):
    queryset = DocumentShareLink.objects.all()
    permission_classes = [permissions.AllowAny]  # Public access with token

    def get_object(self):
        share_link = get_object_or_404(
            DocumentShareLink,
            token=self.kwargs['token'],
            is_active=True
        )
        
        # Check expiration
        from django.utils.timezone import now
        if share_link.expiration and share_link.expiration < now():
            raise Http404("Share link has expired")
        
        # Check download limit
        if share_link.max_downloads:
            downloads = DocumentAccessLog.objects.filter(
                document=share_link.document,
                access_type='share_download'
            ).count()
            if downloads >= share_link.max_downloads:
                raise Http404("Download limit reached")
        
        return share_link

    def get(self, request, *args, **kwargs):
        share_link = self.get_object()
        
        # Log the download
        DocumentAccessLog.objects.create(
            document=share_link.document,
            access_type='share_download',
            tenant=share_link.tenant,
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            metadata={'share_link': str(share_link.token)}
        )

        try:
            response = FileResponse(
                share_link.document.file.open('rb'),
                as_attachment=True,
                filename=share_link.document.file.name.split('/')[-1]
            )
            response['Content-Length'] = share_link.document.file_size
            return response
        except FileNotFoundError:
            raise Http404("File not found")

class DocumentBulkUpdateView(generics.GenericAPIView):
    serializer_class = DocumentBulkUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsTenantAdmin]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        documents = Document.objects.filter(
            id__in=data['document_ids'],
            tenant=request.tenant
        )

        update_fields = {}
        if 'permission_level' in data:
            update_fields['permission_level'] = data['permission_level']
        if 'tags' in data:
            update_fields['tags'] = data['tags']

        updated_count = documents.update(**update_fields)

        # Handle add/remove tags
        if 'add_tags' in data or 'remove_tags' in data:
            for document in documents:
                current_tags = set(document.tags)
                if 'add_tags' in data:
                    current_tags.update(data['add_tags'])
                if 'remove_tags' in data:
                    current_tags.difference_update(data['remove_tags'])
                document.tags = list(current_tags)
                document.save()

        return Response({
            'message': f'Successfully updated {updated_count} documents',
            'updated_fields': list(update_fields.keys()) + 
                             (['tags'] if 'tags' in data or 'add_tags' in data or 'remove_tags' in data else [])
        }, status=status.HTTP_200_OK)

class DocumentTemplateListCreateView(generics.ListCreateAPIView):
    queryset = DocumentTemplate.objects.all()
    serializer_class = DocumentTemplateSerializer
    permission_classes = [permissions.IsAuthenticated, IsTenantAdmin]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']

    def get_queryset(self):
        return self.queryset.filter(tenant=self.request.tenant)

    def perform_create(self, serializer):
        serializer.save(tenant=self.request.tenant)

class DocumentTemplateRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DocumentTemplate.objects.all()
    serializer_class = DocumentTemplateSerializer
    permission_classes = [permissions.IsAuthenticated, IsTenantAdmin]
    lookup_field = 'pk'

    def get_queryset(self):
        return self.queryset.filter(tenant=self.request.tenant)

class DocumentPreviewRetrieveView(generics.RetrieveAPIView):
    queryset = DocumentPreview.objects.all()
    serializer_class = DocumentPreviewSerializer
    permission_classes = [permissions.IsAuthenticated, IsTenantUser]
    lookup_field = 'document_id'

    def get_queryset(self):
        return self.queryset.filter(
            document__tenant=self.request.tenant
        )