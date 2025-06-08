from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    Case, CaseType, CaseStatus, CaseStatusTransition,
    RelatedCase, CaseNote, CaseAttachment,
    CaseWorkflow, CaseSLA, CaseEventLog
)
from apps.tenant.contacts.serializers import ContactSerializer
from apps.tenant.documents.serializers import DocumentSerializer
from apps.accounts.serializers import UserSerializer, TeamSerializer
from enum import Enum

User = get_user_model()

class CasePrioritySerializer(serializers.Serializer):
    """Serializer for the CasePriority enum"""
    id = serializers.IntegerField()
    name = serializers.CharField()

    @classmethod
    def get_values(cls):
        return [{'id': priority.value, 'name': priority.name} 
               for priority in CasePriority]

class CaseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseType
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'tenant')

    def validate(self, data):
        """Validate form_schema and workflow_definition"""
        # Add JSON schema validation here if needed
        return data

class CaseStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseStatus
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'tenant')

class CaseStatusTransitionSerializer(serializers.ModelSerializer):
    from_status = CaseStatusSerializer(read_only=True)
    to_status = CaseStatusSerializer(read_only=True)
    from_status_id = serializers.PrimaryKeyRelatedField(
        queryset=CaseStatus.objects.all(),
        source='from_status',
        write_only=True
    )
    to_status_id = serializers.PrimaryKeyRelatedField(
        queryset=CaseStatus.objects.all(),
        source='to_status',
        write_only=True
    )

    class Meta:
        model = CaseStatusTransition
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'tenant')

class RelatedCaseSerializer(serializers.ModelSerializer):
    related_case = serializers.PrimaryKeyRelatedField(
        queryset=Case.objects.all()
    )
    related_case_details = serializers.SerializerMethodField()

    class Meta:
        model = RelatedCase
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

    def get_related_case_details(self, obj):
        """Nested serialization of related case"""
        from .serializers import CaseListSerializer  # Avoid circular import
        return CaseListSerializer(obj.related_case).data

    def validate(self, data):
        """Prevent circular references"""
        if data['primary_case'] == data['related_case']:
            raise serializers.ValidationError("A case cannot be related to itself")
        return data

class CaseNoteSerializer(serializers.ModelSerializer):
    document = DocumentSerializer(read_only=True)
    document_id = serializers.PrimaryKeyRelatedField(
        queryset=Document.objects.all(),
        source='document',
        write_only=True,
        required=False,
        allow_null=True
    )
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = CaseNote
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'tenant', 'case')

class CaseAttachmentSerializer(serializers.ModelSerializer):
    document = DocumentSerializer(read_only=True)
    document_id = serializers.PrimaryKeyRelatedField(
        queryset=Document.objects.all(),
        source='document',
        write_only=True
    )

    class Meta:
        model = CaseAttachment
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'tenant', 'case')

class CaseWorkflowSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseWorkflow
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'tenant')

    def validate_condition(self, value):
        """Validate workflow condition JSON"""
        # Add specific validation logic for conditions
        return value

    def validate_actions(self, value):
        """Validate workflow actions JSON"""
        # Add specific validation logic for actions
        return value

class CaseSLASerializer(serializers.ModelSerializer):
    case_type = CaseTypeSerializer(read_only=True)
    case_type_id = serializers.PrimaryKeyRelatedField(
        queryset=CaseType.objects.all(),
        source='case_type',
        write_only=True
    )

    class Meta:
        model = CaseSLA
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'tenant')

class CaseEventLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseEventLog
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'tenant')

class CaseListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for case listings"""
    status = CaseStatusSerializer(read_only=True)
    assigned_to = UserSerializer(read_only=True)
    contact = ContactSerializer(read_only=True)
    priority_display = serializers.SerializerMethodField()
    days_open = serializers.SerializerMethodField()

    class Meta:
        model = Case
        fields = [
            'id', 'case_number', 'title', 'status', 
            'priority', 'priority_display', 'assigned_to',
            'contact', 'opened_date', 'due_date', 'days_open',
            'sla_breached', 'is_escalated'
        ]

    def get_priority_display(self, obj):
        return CasePriority(obj.priority).name

    def get_days_open(self, obj):
        from django.utils.timezone import now
        if obj.opened_date:
            return (now() - obj.opened_date).days
        return None

class CaseDetailSerializer(serializers.ModelSerializer):
    """Comprehensive serializer for case details"""
    case_type = CaseTypeSerializer(read_only=True)
    case_type_id = serializers.PrimaryKeyRelatedField(
        queryset=CaseType.objects.all(),
        source='case_type',
        write_only=True
    )
    status = CaseStatusSerializer(read_only=True)
    status_id = serializers.PrimaryKeyRelatedField(
        queryset=CaseStatus.objects.all(),
        source='status',
        write_only=True
    )
    assigned_to = UserSerializer(read_only=True)
    assigned_to_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='assigned_to',
        write_only=True,
        required=False,
        allow_null=True
    )
    assigned_team = TeamSerializer(read_only=True)
    assigned_team_id = serializers.PrimaryKeyRelatedField(
        queryset=Team.objects.all(),
        source='assigned_team',
        write_only=True,
        required=False,
        allow_null=True
    )
    contact = ContactSerializer(read_only=True)
    contact_id = serializers.PrimaryKeyRelatedField(
        queryset=Contact.objects.all(),
        source='contact',
        write_only=True,
        required=False,
        allow_null=True
    )
    related_cases = RelatedCaseSerializer(
        source='primary_relations',
        many=True,
        read_only=True
    )
    notes = CaseNoteSerializer(many=True, read_only=True)
    attachments = CaseAttachmentSerializer(many=True, read_only=True)
    event_logs = CaseEventLogSerializer(many=True, read_only=True)
    priority_display = serializers.SerializerMethodField()
    allowed_transitions = serializers.SerializerMethodField()

    class Meta:
        model = Case
        fields = '__all__'
        read_only_fields = (
            'created_at', 'updated_at', 'tenant', 
            'case_number', 'opened_date', 'sla_breached',
            'event_logs'
        )

    def get_priority_display(self, obj):
        return CasePriority(obj.priority).name

    def get_allowed_transitions(self, obj):
        """Get allowed status transitions for the current case"""
        transitions = obj.status.from_transitions.all()
        return CaseStatusTransitionSerializer(transitions, many=True).data

    def validate(self, data):
        """Validate case data and transitions"""
        # Check if status transition is allowed
        if 'status_id' in data and self.instance:
            new_status = data['status_id']
            if not self.instance.status.from_transitions.filter(to_status=new_status).exists():
                raise serializers.ValidationError(
                    f"Invalid status transition from {self.instance.status} to {new_status}"
                )
        
        # Validate SLA dates
        if 'due_date' in data and 'sla_due_date' in data:
            if data['due_date'] and data['sla_due_date']:
                if data['due_date'] > data['sla_due_date']:
                    raise serializers.ValidationError(
                        "Due date cannot be after SLA due date"
                    )
        
        return data

    def create(self, validated_data):
        """Handle case creation with automatic numbering"""
        # Set initial status based on case type
        case_type = validated_data.get('case_type')
        if case_type and not validated_data.get('status_id'):
            initial_status = CaseStatus.objects.filter(
                tenant=self.context['request'].tenant,
                is_initial=True
            ).first()
            if initial_status:
                validated_data['status_id'] = initial_status
        
        case = super().create(validated_data)
        
        # Log creation event
        CaseEventLog.objects.create(
            case=case,
            event_type='status_change',
            new_value={'status': str(case.status)},
            tenant=self.context['request'].tenant
        )
        
        return case

    def update(self, instance, validated_data):
        """Handle case updates with audit logging"""
        # Track changes for audit log
        changes = {}
        for field, value in validated_data.items():
            if field in ['status_id', 'assigned_to_id', 'assigned_team_id']:
                field_name = field.replace('_id', '')
                old_value = getattr(instance, field_name)
                if str(old_value.id) != str(value.id):
                    changes[field_name] = {
                        'from': str(old_value),
                        'to': str(value)
                    }
        
        case = super().update(instance, validated_data)
        
        # Create audit logs for changes
        if changes:
            for field, change in changes.items():
                CaseEventLog.objects.create(
                    case=case,
                    event_type=f"{field}_change",
                    previous_value=change['from'],
                    new_value=change['to'],
                    tenant=self.context['request'].tenant
                )
        
        return case

class CaseBulkUpdateSerializer(serializers.Serializer):
    """Serializer for bulk case updates"""
    case_ids = serializers.ListField(
        child=serializers.IntegerField(),
        min_length=1
    )
    status_id = serializers.PrimaryKeyRelatedField(
        queryset=CaseStatus.objects.all(),
        required=False
    )
    assigned_to_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False,
        allow_null=True
    )
    priority = serializers.IntegerField(
        required=False,
        min_value=1,
        max_value=4
    )

    def validate(self, data):
        """Validate bulk update data"""
        if not any([field in data for field in ['status_id', 'assigned_to_id', 'priority']]):
            raise serializers.ValidationError(
                "At least one update field (status_id, assigned_to_id, or priority) is required"
            )
        return data