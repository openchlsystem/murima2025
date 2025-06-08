from apps.shared.accounts.models import Team
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model
from apps.shared.core.models import AuditLog
from .models import (
    CaseType, CaseStatus, Case, CaseDocument, CaseNote,
    CaseHistory, CaseLink, CaseTemplate, SLA, WorkflowRule
)
from apps.shared.accounts.serializers import UserSerializer, TeamSerializer

User = get_user_model()

class CaseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseType
        fields = [
            'id', 'name', 'code', 'description', 'is_active', 'icon', 'color',
            'default_priority', 'default_sla_hours', 'metadata', 'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_code(self, value):
        if not value.isidentifier():
            raise ValidationError("Code must be a valid identifier (letters, numbers, underscores)")
        return value.lower()


class CaseStatusSerializer(serializers.ModelSerializer):
    allowed_next_statuses = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=CaseStatus.objects.all(),
        required=False
    )

    class Meta:
        model = CaseStatus
        fields = [
            'id', 'name', 'code', 'description', 'is_active', 'is_closed',
            'is_default', 'color', 'order', 'allowed_next_statuses', 'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, data):
        if data.get('is_default') and CaseStatus.objects.filter(is_default=True).exists():
            if not self.instance or not self.instance.is_default:
                raise ValidationError("There can only be one default status")
        return data


class CasePriorityField(serializers.Field):
    def to_representation(self, value):
        return {
            'value': value,
            'label': Case.get_priority_display(value)
        }

    def to_internal_value(self, data):
        try:
            priority = int(data)
            if priority not in dict(Case.PRIORITY_CHOICES):
                raise ValueError
            return priority
        except (ValueError, TypeError):
            raise ValidationError("Invalid priority value")


class CaseSerializer(serializers.ModelSerializer):
    # case_type = serializers.PrimaryKeyRelatedField(queryset=CaseType.objects.filter(is_active=True))
    # status = serializers.PrimaryKeyRelatedField(queryset=CaseStatus.objects.filter(is_active=True))
    priority = CasePriorityField()
    assigned_to = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(is_active=True),
        allow_null=True
    )
    assigned_team = serializers.PrimaryKeyRelatedField(
        queryset=Team.objects.all(),
        allow_null=True
    )
    resolved_by = serializers.PrimaryKeyRelatedField(
        read_only=True,
        allow_null=True
    )    
    created_by = UserSerializer(read_only=True)
    updated_by = UserSerializer(read_only=True)
    time_to_resolution = serializers.DurationField(read_only=True)
    is_overdue = serializers.BooleanField(read_only=True)
    url = serializers.SerializerMethodField()

    class Meta:
        model = Case
        fields = [
            'id', 'case_number', 'case_type', 'title', 'description', 'status',
            'priority', 'assigned_to', 'assigned_team', 'due_date', 'resolved_at',
            'resolved_by', 'sla_expires_at', 'is_high_priority', 'is_confidential',
            'source_channel', 'reference_id', 'custom_fields', 'tags', 'created_at',
            'updated_at', 'created_by', 'updated_by', 'time_to_resolution',
            'is_overdue', 'url'
        ]
        read_only_fields = [
            'id', 'case_number', 'created_at', 'updated_at', 'created_by',
            'updated_by', 'resolved_by', 'resolved_at', 'time_to_resolution',
            'is_overdue', 'sla_expires_at'
        ]

    def get_url(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.get_absolute_url())
        return obj.get_absolute_url()

    def validate(self, data):
        # Validate case type and status compatibility
        case_type = data.get('case_type', getattr(self.instance, 'case_type', None))
        status = data.get('status', getattr(self.instance, 'status', None))
        
        if case_type and status:
            # Add any custom validation for case type and status here
            pass

        # Validate that either assigned_to or assigned_team is set, not both
        assigned_to = data.get('assigned_to')
        assigned_team = data.get('assigned_team')
        
        if assigned_to and assigned_team:
            raise ValidationError("Case can be assigned to a user OR a team, not both")

        return data

    def create(self, validated_data):
        # Set created_by from request user
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Set updated_by from request user
        validated_data['updated_by'] = self.context['request'].user
        
        # Handle status changes
        new_status = validated_data.get('status')
        if new_status and new_status != instance.status:
            # This could be enhanced with workflow validation
            instance.update_status(
                new_status=new_status,
                changed_by=self.context['request'].user,
                comment="Status changed via API"
            )
            validated_data.pop('status')  # Already handled by update_status
        
        return super().update(instance, validated_data)


class CaseDocumentSerializer(serializers.ModelSerializer):
    file = serializers.FileField(required=True)
    uploaded_by = UserSerializer(read_only=True)
    case = serializers.PrimaryKeyRelatedField(
        queryset=Case.objects.all(),
        write_only=True
    )
    download_url = serializers.SerializerMethodField()
    preview_url = serializers.SerializerMethodField()

    class Meta:
        model = CaseDocument
        fields = [
            'id', 'case', 'file', 'description', 'uploaded_by', 'file_type',
            'file_size', 'version', 'is_current', 'metadata', 'created_at',
            'updated_at', 'download_url', 'preview_url'
        ]
        read_only_fields = [
            'id', 'uploaded_by', 'file_type', 'file_size', 'version',
            'created_at', 'updated_at'
        ]

    def get_download_url(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.file.url)
        return obj.file.url

    def get_preview_url(self, obj):
        # This could be enhanced to return preview URLs for supported file types
        return None

    def create(self, validated_data):
        validated_data['uploaded_by'] = self.context['request'].user
        return super().create(validated_data)


class CaseNoteSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    case = serializers.PrimaryKeyRelatedField(
        queryset=Case.objects.all(),
        write_only=True
    )
    reply_to = serializers.PrimaryKeyRelatedField(
        queryset=CaseNote.objects.all(),
        allow_null=True,
        required=False
    )

    class Meta:
        model = CaseNote
        fields = [
            'id', 'case', 'content', 'is_internal', 'pinned', 'reply_to',
            'metadata', 'created_at', 'updated_at', 'created_by'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by']

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class CaseHistorySerializer(serializers.ModelSerializer):
    changed_by = UserSerializer(read_only=True)
    from_status = CaseStatusSerializer(read_only=True)
    to_status = CaseStatusSerializer(read_only=True)
    from_priority = CasePriorityField(read_only=True)
    to_priority = CasePriorityField(read_only=True)
    from_assignment = UserSerializer(read_only=True)
    to_assignment = UserSerializer(read_only=True)
    related_note = serializers.PrimaryKeyRelatedField(
        queryset=CaseNote.objects.all(),
        allow_null=True,
        required=False
    )
    related_document = serializers.PrimaryKeyRelatedField(
        queryset=CaseDocument.objects.all(),
        allow_null=True,
        required=False
    )

    class Meta:
        model = CaseHistory
        fields = [
            'id', 'case', 'action', 'changed_by', 'from_status', 'to_status',
            'from_priority', 'to_priority', 'from_assignment', 'to_assignment',
            'related_note', 'related_document', 'comment', 'changes',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class CaseLinkSerializer(serializers.ModelSerializer):
    source_case = serializers.PrimaryKeyRelatedField(queryset=Case.objects.all())
    target_case = serializers.PrimaryKeyRelatedField(queryset=Case.objects.all())

    class Meta:
        model = CaseLink
        fields = [
            'id', 'source_case', 'target_case', 'relationship_type',
            'description', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, data):
        source_case = data.get('source_case')
        target_case = data.get('target_case')
        
        if source_case and target_case and source_case == target_case:
            raise ValidationError("A case cannot be linked to itself")
        
        return data


class CaseTemplateSerializer(serializers.ModelSerializer):
    case_type = serializers.PrimaryKeyRelatedField(queryset=CaseType.objects.all())
    default_status = serializers.PrimaryKeyRelatedField(
        queryset=CaseStatus.objects.all())
    default_assignee = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        allow_null=True
    )
    default_team = serializers.PrimaryKeyRelatedField(
        queryset=Team.objects.all(),
        allow_null=True
    )
    default_priority = CasePriorityField()

    class Meta:
        model = CaseTemplate
        fields = [
            'id', 'name', 'case_type', 'description', 'default_priority',
            'default_status', 'default_assignee', 'default_team',
            'default_sla_hours', 'content', 'custom_fields', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class SLASerializer(serializers.ModelSerializer):
    case_type = serializers.PrimaryKeyRelatedField(
        queryset=CaseType.objects.filter(is_active=True),
        allow_null=True
    )
    priority = CasePriorityField(allow_null=True)

    class Meta:
        model = SLA
        fields = [
            'id', 'name', 'case_type', 'priority', 'response_time_hours',
            'resolution_time_hours', 'business_hours_only', 'is_active',
            'description', 'escalation_path', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class WorkflowRuleSerializer(serializers.ModelSerializer):
    case_type = serializers.PrimaryKeyRelatedField(
        queryset=CaseType.objects.filter(is_active=True),
        allow_null=True
    )
    priority = CasePriorityField(allow_null=True)

    class Meta:
        model = WorkflowRule
        fields = [
            'id', 'name', 'description', 'case_type', 'priority',
            'trigger_condition', 'condition_expression', 'action_type',
            'action_parameters', 'is_active', 'order', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_condition_expression(self, value):
        # Add validation for condition expression structure
        if not isinstance(value, dict):
            raise ValidationError("Condition expression must be a JSON object")
        return value

    def validate_action_parameters(self, value):
        # Add validation for action parameters based on action_type
        action_type = self.initial_data.get('action_type')
        
        if action_type == 'CHANGE_STATUS' and 'status_id' not in value:
            raise ValidationError("Status change requires status_id parameter")
            
        # Add more validations for other action types
        
        return value


# Special serializers for nested representations
class CaseWithRelatedSerializer(CaseSerializer):
    case_type = CaseTypeSerializer(read_only=True)
    status = CaseStatusSerializer(read_only=True)
    assigned_to = UserSerializer(read_only=True)
    assigned_team = TeamSerializer(read_only=True)
    documents = CaseDocumentSerializer(many=True, read_only=True)
    notes = CaseNoteSerializer(many=True, read_only=True)
    history = CaseHistorySerializer(many=True, read_only=True)
    linked_cases = serializers.SerializerMethodField()

    class Meta(CaseSerializer.Meta):
        fields = CaseSerializer.Meta.fields + [
            'documents', 'notes', 'history', 'linked_cases'
        ]

    def get_linked_cases(self, obj):
        links = CaseLink.objects.filter(source_case=obj)
        return CaseLinkSerializer(links, many=True, context=self.context).data


class AuditLogSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    object_type = serializers.CharField(source='object_type.model')
    
    class Meta:
        model = AuditLog
        fields = [
            'id', 'user', 'action', 'object_type', 'object_id',
            'object_repr', 'changes', 'ip_address', 'user_agent',
            'description', 'metadata', 'created_at'
        ]
        read_only_fields = fields