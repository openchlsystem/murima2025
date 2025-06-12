from rest_framework import serializers
from django.contrib.auth import get_user_model
from apps.shared.core.models import AuditLog
from apps.shared.core.serializers import BaseModelSerializer, UserBasicSerializer
from .models import (
    CaseType, CaseStatus, Case, CaseDocument, CaseNote,
    CaseHistory, CaseLink, CaseTemplate, SLA, WorkflowRule
)
# from apps.shared.accounts.models import Team
# from apps.shared.accounts.serializers import TeamSerializer

User = get_user_model()

class CaseTypeSerializer(BaseModelSerializer):
    class Meta:
        model = CaseType
        fields = BaseModelSerializer.Meta.fields + [
            'name', 'code', 'description', 'is_active', 'icon', 'color',
            'default_priority', 'default_sla_hours', 'metadata'
        ]

    def validate_code(self, value):
        if not value.isidentifier():
            raise serializers.ValidationError("Code must be a valid identifier (letters, numbers, underscores)")
        return value.lower()


class CaseStatusSerializer(BaseModelSerializer):
    allowed_next_statuses = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=CaseStatus.objects.all(),
        required=False
    )

    class Meta:
        model = CaseStatus
        fields = BaseModelSerializer.Meta.fields + [
            'name', 'code', 'description', 'is_active', 'is_closed',
            'is_default', 'color', 'order', 'allowed_next_statuses'
        ]

    def validate(self, data):
        if data.get('is_default') and CaseStatus.objects.filter(is_default=True).exists():
            if not self.instance or not self.instance.is_default:
                raise serializers.ValidationError("There can only be one default status")
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
            raise serializers.ValidationError("Invalid priority value")


class CaseSerializer(BaseModelSerializer):
    priority = CasePriorityField()
    assigned_to = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(is_active=True),
        allow_null=True
    )
    # assigned_team = serializers.PrimaryKeyRelatedField(
    #     queryset=Team.objects.all(),
    #     allow_null=Truex
    # )
    
    resolved_by = serializers.PrimaryKeyRelatedField(
        read_only=True,
        allow_null=True
    )    
    created_by = UserBasicSerializer(read_only=True)
    updated_by = UserBasicSerializer(read_only=True)
    time_to_resolution = serializers.DurationField(read_only=True)
    is_overdue = serializers.BooleanField(read_only=True)
    url = serializers.SerializerMethodField()

    class Meta:
        model = Case
        fields = BaseModelSerializer.Meta.fields + [
            'case_number', 'case_type', 'title', 'description', 'status',
            'priority', 'assigned_to', 'assigned_team', 'due_date', 'resolved_at',
            'resolved_by', 'sla_expires_at', 'is_high_priority', 'is_confidential',
            'source_channel', 'reference_id', 'custom_fields', 'tags',
            'time_to_resolution', 'is_overdue', 'url'
        ]
        read_only_fields = BaseModelSerializer.Meta.read_only_fields + [
            'case_number', 'resolved_by', 'resolved_at', 'time_to_resolution',
            'is_overdue', 'sla_expires_at'
        ]

    def get_url(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.get_absolute_url())
        return obj.get_absolute_url()

    def validate(self, data):
        case_type = data.get('case_type', getattr(self.instance, 'case_type', None))
        status = data.get('status', getattr(self.instance, 'status', None))
        
        if case_type and status:
            pass

        assigned_to = data.get('assigned_to')
        # assigned_team = data.get('assigned_team')
        
        if assigned_to and assigned_team:
            raise serializers.ValidationError("Case can be assigned to a user OR a team, not both")

        return data

    def update(self, instance, validated_data):
        new_status = validated_data.get('status')
        if new_status and new_status != instance.status:
            instance.update_status(
                new_status=new_status,
                changed_by=self.context['request'].user,
                comment="Status changed via API"
            )
            validated_data.pop('status')
        
        return super().update(instance, validated_data)


class CaseDocumentSerializer(BaseModelSerializer):
    file = serializers.FileField(required=True)
    uploaded_by = UserBasicSerializer(read_only=True)
    case = serializers.PrimaryKeyRelatedField(
        queryset=Case.objects.all(),
        write_only=True
    )
    download_url = serializers.SerializerMethodField()
    preview_url = serializers.SerializerMethodField()

    class Meta:
        model = CaseDocument
        fields = BaseModelSerializer.Meta.fields + [
            'case', 'file', 'description', 'uploaded_by', 'file_type',
            'file_size', 'version', 'is_current', 'metadata',
            'download_url', 'preview_url'
        ]
        read_only_fields = BaseModelSerializer.Meta.read_only_fields + [
            'uploaded_by', 'file_type', 'file_size', 'version'
        ]

    def get_download_url(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.file.url)
        return obj.file.url

    def get_preview_url(self, obj):
        return None


class CaseNoteSerializer(BaseModelSerializer):
    created_by = UserBasicSerializer(read_only=True)
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
        fields = BaseModelSerializer.Meta.fields + [
            'case', 'content', 'is_internal', 'pinned', 'reply_to',
            'metadata'
        ]


class CaseHistorySerializer(BaseModelSerializer):
    changed_by = UserBasicSerializer(read_only=True)
    from_status = CaseStatusSerializer(read_only=True)
    to_status = CaseStatusSerializer(read_only=True)
    from_priority = CasePriorityField(read_only=True)
    to_priority = CasePriorityField(read_only=True)
    from_assignment = UserBasicSerializer(read_only=True)
    to_assignment = UserBasicSerializer(read_only=True)
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
        fields = BaseModelSerializer.Meta.fields + [
            'case', 'action', 'changed_by', 'from_status', 'to_status',
            'from_priority', 'to_priority', 'from_assignment', 'to_assignment',
            'related_note', 'related_document', 'comment', 'changes'
        ]


class CaseLinkSerializer(BaseModelSerializer):
    source_case = serializers.PrimaryKeyRelatedField(queryset=Case.objects.all())
    target_case = serializers.PrimaryKeyRelatedField(queryset=Case.objects.all())

    class Meta:
        model = CaseLink
        fields = BaseModelSerializer.Meta.fields + [
            'source_case', 'target_case', 'relationship_type',
            'description'
        ]

    def validate(self, data):
        source_case = data.get('source_case')
        target_case = data.get('target_case')
        
        if source_case and target_case and source_case == target_case:
            raise serializers.ValidationError("A case cannot be linked to itself")
        
        return data


class CaseTemplateSerializer(BaseModelSerializer):
    case_type = serializers.PrimaryKeyRelatedField(queryset=CaseType.objects.all())
    default_status = serializers.PrimaryKeyRelatedField(
        queryset=CaseStatus.objects.all())
    default_assignee = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        allow_null=True
    )
    # default_team = serializers.PrimaryKeyRelatedField(
    #     queryset=Team.objects.all(),
    #     allow_null=True
    # )
    default_priority = CasePriorityField()

    class Meta:
        model = CaseTemplate
        fields = BaseModelSerializer.Meta.fields + [
            'name', 'case_type', 'description', 'default_priority',
            'default_status', 'default_assignee', 'default_team',
            'default_sla_hours', 'content', 'custom_fields', 'is_active'
        ]


class SLASerializer(BaseModelSerializer):
    case_type = serializers.PrimaryKeyRelatedField(
        queryset=CaseType.objects.filter(is_active=True),
        allow_null=True
    )
    priority = CasePriorityField(allow_null=True)

    class Meta:
        model = SLA
        fields = BaseModelSerializer.Meta.fields + [
            'name', 'case_type', 'priority', 'response_time_hours',
            'resolution_time_hours', 'business_hours_only', 'is_active',
            'description', 'escalation_path'
        ]


class WorkflowRuleSerializer(BaseModelSerializer):
    case_type = serializers.PrimaryKeyRelatedField(
        queryset=CaseType.objects.filter(is_active=True),
        allow_null=True
    )
    priority = CasePriorityField(allow_null=True)

    class Meta:
        model = WorkflowRule
        fields = BaseModelSerializer.Meta.fields + [
            'name', 'description', 'case_type', 'priority',
            'trigger_condition', 'condition_expression', 'action_type',
            'action_parameters', 'is_active', 'order'
        ]

    def validate_condition_expression(self, value):
        if not isinstance(value, dict):
            raise serializers.ValidationError("Condition expression must be a JSON object")
        return value

    def validate_action_parameters(self, value):
        action_type = self.initial_data.get('action_type')
        
        if action_type == 'CHANGE_STATUS' and 'status_id' not in value:
            raise serializers.ValidationError("Status change requires status_id parameter")
            
        return value


class CaseWithRelatedSerializer(CaseSerializer):
    case_type = CaseTypeSerializer(read_only=True)
    status = CaseStatusSerializer(read_only=True)
    assigned_to = UserBasicSerializer(read_only=True)
    # assigned_team = TeamSerializer(read_only=True)
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
    class Meta:
        model = AuditLog  # Make sure this model is defined/imported too
        fields = '__all__'
