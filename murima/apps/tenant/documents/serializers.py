from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from .models import (
    Document, DocumentType, DocumentVersion,
    DocumentAccessLog, DocumentShareLink,
    DocumentPreview, DocumentTemplate,
    DocumentPermissionLevel
)
from apps.tenant.cases.models import Case
from apps.tenant.contacts.models import Contact
from apps.tenant.tasks.models import Task
from apps.shared.core.models import (
    BaseModel,
    TenantModel
)
import hashlib
import uuid

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = fields

class TimestampedModelSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        abstract = True

class UUIDModelSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        abstract = True

class UserTrackingModelSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    updated_by = UserSerializer(read_only=True)

    class Meta:
        abstract = True

class SoftDeleteModelSerializer(serializers.ModelSerializer):
    is_deleted = serializers.BooleanField(read_only=True)
    deleted_at = serializers.DateTimeField(read_only=True)
    deleted_by = UserSerializer(read_only=True)

    class Meta:
        abstract = True

class OwnedModelSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        abstract = True

class BaseModelSerializer(
    UUIDModelSerializer,
    TimestampedModelSerializer,
    UserTrackingModelSerializer,
    SoftDeleteModelSerializer
):
    """
    Base serializer that includes all common functionality
    """
    class Meta:
        abstract = True

class DocumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentType
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'tenant')

class DocumentPermissionLevelSerializer(serializers.Serializer):
    """Serializer for the DocumentPermissionLevel enum"""
    id = serializers.IntegerField()
    name = serializers.CharField()

    @classmethod
    def get_values(cls):
        return [{'id': level.value, 'name': level.name} 
               for level in DocumentPermissionLevel]

class DocumentVersionSerializer(serializers.ModelSerializer):
    modified_by = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )
    download_url = serializers.SerializerMethodField()

    class Meta:
        model = DocumentVersion
        fields = '__all__'
        read_only_fields = (
            'created_at', 'updated_at', 'tenant',
            'file_size', 'file_hash', 'version'
        )

    def get_download_url(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.file.url)
        return obj.file.url

class DocumentSerializer(BaseModelSerializer, serializers.ModelSerializer):
    document_type = DocumentTypeSerializer(read_only=True)
    document_type_id = serializers.PrimaryKeyRelatedField(
        queryset=DocumentType.objects.all(),
        source='document_type',
        write_only=True
    )
    case = serializers.PrimaryKeyRelatedField(
        queryset=Case.objects.all(),
        required=False,
        allow_null=True
    )
    contact = serializers.PrimaryKeyRelatedField(
        queryset=Contact.objects.all(),
        required=False,
        allow_null=True
    )
    task = serializers.PrimaryKeyRelatedField(
        queryset=Task.objects.all(),
        required=False,
        allow_null=True
    )
    versions = DocumentVersionSerializer(many=True, read_only=True)
    download_url = serializers.SerializerMethodField()
    preview_url = serializers.SerializerMethodField()
    permission_level_display = serializers.SerializerMethodField()
    created_by = serializers.PrimaryKeyRelatedField(
        default=serializers.CurrentUserDefault(),
        queryset=User.objects.all()
    )

    class Meta:
        model = Document
        fields = '__all__'
        read_only_fields = (
            'created_at', 'updated_at', 'tenant',
            'file_size', 'file_hash', 'version',
            'parent_version', 'versions'
        )

    def get_download_url(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.file.url)
        return obj.file.url

    def get_preview_url(self, obj):
        if hasattr(obj, 'preview') and obj.preview.status == 'ready':
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.preview.thumbnail.url)
            return obj.preview.thumbnail.url
        return None

    def get_permission_level_display(self, obj):
        return DocumentPermissionLevel(obj.permission_level).name

    def validate_file(self, value):
        """Validate file size and type"""
        max_size = 50 * 1024 * 1024  # 50MB
        if value.size > max_size:
            raise serializers.ValidationError(
                f"File size exceeds maximum allowed size of {max_size/1024/1024}MB"
            )
        
        # Validate extension against document type
        if hasattr(self, 'initial_data') and 'document_type_id' in self.initial_data:
            doc_type = DocumentType.objects.get(pk=self.initial_data['document_type_id'])
            ext = value.name.split('.')[-1].lower()
            if doc_type.allowed_extensions and ext not in doc_type.allowed_extensions:
                raise serializers.ValidationError(
                    f"File type not allowed. Allowed types: {', '.join(doc_type.allowed_extensions)}"
                )
        
        return value

    def create(self, validated_data):
        """Handle document creation with versioning"""
        file = validated_data.pop('file', None)
        document = Document(**validated_data)
        
        # Calculate file hash
        file_hash = hashlib.sha256(file.read()).hexdigest()
        file.seek(0)  # Reset file pointer after reading
        
        document.file = file
        document.file_hash = file_hash
        document.file_size = file.size
        document.save()
        
        # Create initial version
        DocumentVersion.objects.create(
            document=document,
            version=1,
            file=file,
            file_size=file.size,
            file_hash=file_hash,
            modified_by=validated_data.get('created_by'),
            tenant=document.tenant
        )
        
        return document

    def update(self, instance, validated_data):
        """Handle document updates with versioning"""
        file = validated_data.pop('file', None)
        user = self.context['request'].user
        
        if file:
            # Create new version
            file_hash = hashlib.sha256(file.read()).hexdigest()
            file.seek(0)  # Reset file pointer
            
            # Save current version as historical record
            DocumentVersion.objects.create(
                document=instance,
                version=instance.version,
                file=instance.file,
                file_size=instance.file_size,
                file_hash=instance.file_hash,
                modified_by=user,
                tenant=instance.tenant
            )
            
            # Update document with new file
            instance.file = file
            instance.file_hash = file_hash
            instance.file_size = file.size
            instance.version += 1
            instance.parent_version_id = instance.pk
        
        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance

class DocumentUploadSerializer(serializers.Serializer):
    """Specialized serializer for file uploads"""
    file = serializers.FileField(required=True)
    title = serializers.CharField(max_length=255)
    description = serializers.CharField(required=False, allow_blank=True)
    document_type_id = serializers.PrimaryKeyRelatedField(
        queryset=DocumentType.objects.all()
    )
    category = serializers.ChoiceField(
        choices=Document.DOCUMENT_CATEGORIES,
        default='general'
    )
    case_id = serializers.PrimaryKeyRelatedField(
        queryset=Case.objects.all(),
        required=False,
        allow_null=True
    )
    contact_id = serializers.PrimaryKeyRelatedField(
        queryset=Contact.objects.all(),
        required=False,
        allow_null=True
    )
    task_id = serializers.PrimaryKeyRelatedField(
        queryset=Task.objects.all(),
        required=False,
        allow_null=True
    )
    tags = serializers.ListField(
        child=serializers.CharField(max_length=50),
        required=False,
        default=list
    )

    def create(self, validated_data):
        request = self.context.get('request')
        document_serializer = DocumentSerializer(
            data=validated_data,
            context={'request': request}
        )
        document_serializer.is_valid(raise_exception=True)
        return document_serializer.save(
            created_by=request.user,
            tenant=request.tenant
        )

class DocumentAccessLogSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )
    document_title = serializers.CharField(
        source='document.title',
        read_only=True
    )

    class Meta:
        model = DocumentAccessLog
        fields = '__all__'
        read_only_fields = (
            'created_at', 'updated_at', 'tenant',
            'ip_address', 'user_agent'
        )

class DocumentShareLinkSerializer(serializers.ModelSerializer):
    document_title = serializers.CharField(
        source='document.title',
        read_only=True
    )
    created_by_email = serializers.EmailField(
        source='created_by.email',
        read_only=True
    )
    is_expired = serializers.SerializerMethodField()
    share_url = serializers.SerializerMethodField()

    class Meta:
        model = DocumentShareLink
        fields = '__all__'
        read_only_fields = (
            'created_at', 'updated_at', 'tenant',
            'token', 'created_by'
        )

    def get_is_expired(self, obj):
        from django.utils.timezone import now
        return obj.expiration < now() if obj.expiration else False

    def get_share_url(self, obj):
        request = self.context.get('request')
        if request:
            return f"{request.build_absolute_uri('/')}api/documents/share/{obj.token}/"
        return f"/api/documents/share/{obj.token}/"

    def create(self, validated_data):
        """Set created_by and tenant automatically"""
        request = self.context.get('request')
        validated_data['created_by'] = request.user
        validated_data['tenant'] = request.tenant
        return super().create(validated_data)

class DocumentPreviewSerializer(serializers.ModelSerializer):
    thumbnail_url = serializers.SerializerMethodField()
    preview_url = serializers.SerializerMethodField()

    class Meta:
        model = DocumentPreview
        fields = '__all__'
        read_only_fields = (
            'created_at', 'updated_at', 'tenant',
            'status', 'metadata'
        )

    def get_thumbnail_url(self, obj):
        request = self.context.get('request')
        if obj.thumbnail and request:
            return request.build_absolute_uri(obj.thumbnail.url)
        return obj.thumbnail.url if obj.thumbnail else None

    def get_preview_url(self, obj):
        request = self.context.get('request')
        if obj.preview_file and request:
            return request.build_absolute_uri(obj.preview_file.url)
        return obj.preview_file.url if obj.preview_file else None

class DocumentTemplateSerializer(serializers.ModelSerializer):
    download_url = serializers.SerializerMethodField()
    variables = serializers.JSONField()

    class Meta:
        model = DocumentTemplate
        fields = '__all__'
        read_only_fields = (
            'created_at', 'updated_at', 'tenant',
            'is_system'
        )

    def get_download_url(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.file.url)
        return obj.file.url

class DocumentSearchSerializer(serializers.Serializer):
    """Serializer for document search parameters"""
    query = serializers.CharField(required=False)
    category = serializers.ChoiceField(
        choices=Document.DOCUMENT_CATEGORIES,
        required=False
    )
    document_type = serializers.PrimaryKeyRelatedField(
        queryset=DocumentType.objects.all(),
        required=False
    )
    case_id = serializers.PrimaryKeyRelatedField(
        queryset=Case.objects.all(),
        required=False
    )
    contact_id = serializers.PrimaryKeyRelatedField(
        queryset=Contact.objects.all(),
        required=False
    )
    task_id = serializers.PrimaryKeyRelatedField(
        queryset=Task.objects.all(),
        required=False
    )
    tags = serializers.ListField(
        child=serializers.CharField(max_length=50),
        required=False
    )
    uploaded_after = serializers.DateField(required=False)
    uploaded_before = serializers.DateField(required=False)
    sort_by = serializers.ChoiceField(
        choices=[
            ('title', 'Title'),
            ('created_at', 'Upload Date'),
            ('file_size', 'File Size')
        ],
        default='created_at'
    )
    sort_order = serializers.ChoiceField(
        choices=[('asc', 'Ascending'), ('desc', 'Descending')],
        default='desc'
    )

class DocumentBulkUpdateSerializer(serializers.Serializer):
    """Serializer for bulk document updates"""
    document_ids = serializers.ListField(
        child=serializers.PrimaryKeyRelatedField(queryset=Document.objects.all()),
        min_length=1
    )
    permission_level = serializers.IntegerField(
        min_value=1,
        max_value=4,
        required=False
    )
    tags = serializers.ListField(
        child=serializers.CharField(max_length=50),
        required=False
    )