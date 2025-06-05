# apps/cases/serializers.py
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.utils import timezone
from .models import (
    Case, CaseCategory, CaseActivity, CaseService, CaseReferral,
    CaseNote, CaseAttachment, CaseUpdate
)
from apps.core.serializers import ReferenceDataSerializer
from apps.contacts.serializers import ContactSerializer
from apps.accounts.serializers import UserListSerializer


class CaseCategorySerializer(serializers.ModelSerializer):
    """Serializer for Case Categories"""
    category = ReferenceDataSerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    added_by = UserListSerializer(read_only=True)
    
    class Meta:
        model = CaseCategory
        fields = [
            'id', 'case', 'category', 'category_id', 'is_primary', 
            'confidence_score', 'added_by', 'created_at'
        ]


class CaseActivitySerializer(serializers.ModelSerializer):
    """Serializer for Case Activities"""
    user = UserListSerializer(read_only=True)
    case_number = serializers.CharField(source='case.case_number', read_only=True)
    
    class Meta:
        model = CaseActivity
        fields = [
            'id', 'case', 'case_number', 'activity_type', 'user', 'title', 
            'description', 'data', 'field_changes', 'is_important', 
            'is_internal', 'source_reference', 'created_at'
        ]
        read_only_fields = ['user', 'created_at']


class CaseServiceSerializer(serializers.ModelSerializer):
    """Serializer for Case Services"""
    service = ReferenceDataSerializer(read_only=True)
    service_id = serializers.IntegerField(write_only=True)
    provided_by = UserListSerializer(read_only=True)
    case_number = serializers.CharField(source='case.case_number', read_only=True)
    
    class Meta:
        model = CaseService
        fields = [
            'id', 'case', 'case_number', 'service', 'service_id', 'provided_by',
            'service_date', 'details', 'cost', 'is_completed', 'created_at'
        ]
        read_only_fields = ['provided_by', 'created_at']


class CaseReferralSerializer(serializers.ModelSerializer):
    """Serializer for Case Referrals"""
    referral_type = ReferenceDataSerializer(read_only=True)
    referral_type_id = serializers.IntegerField(write_only=True)
    urgency = ReferenceDataSerializer(read_only=True)
    urgency_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    referred_by = UserListSerializer(read_only=True)
    case_number = serializers.CharField(source='case.case_number', read_only=True)
    is_overdue = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = CaseReferral
        fields = [
            'id', 'case', 'case_number', 'referral_type', 'referral_type_id',
            'organization', 'contact_person', 'contact_phone', 'contact_email',
            'reason', 'urgency', 'urgency_id', 'status', 'referred_by',
            'referral_date', 'follow_up_date', 'outcome', 'notes',
            'attachments', 'is_overdue', 'created_at'
        ]
        read_only_fields = ['referred_by', 'referral_date', 'created_at', 'is_overdue']


class CaseNoteSerializer(serializers.ModelSerializer):
    """Serializer for Case Notes"""
    author = UserListSerializer(read_only=True)
    case_number = serializers.CharField(source='case.case_number', read_only=True)
    
    class Meta:
        model = CaseNote
        fields = [
            'id', 'case', 'case_number', 'note_type', 'author', 'title', 
            'content', 'is_private', 'is_important', 'visible_to_client',
            'attachments', 'created_at', 'updated_at'
        ]
        read_only_fields = ['author', 'created_at', 'updated_at']


class CaseAttachmentSerializer(serializers.ModelSerializer):
    """Serializer for Case Attachments"""
    uploaded_by = UserListSerializer(read_only=True)
    case_number = serializers.CharField(source='case.case_number', read_only=True)
    file_size_human = serializers.CharField(read_only=True)
    
    class Meta:
        model = CaseAttachment
        fields = [
            'id', 'case', 'case_number', 'attachment_type', 'file_name',
            'file_path', 'file_size', 'file_size_human', 'mime_type',
            'title', 'description', 'uploaded_by', 'is_confidential',
            'access_level', 'checksum', 'created_at'
        ]
        read_only_fields = ['uploaded_by', 'file_size_human', 'checksum', 'created_at']


class CaseUpdateSerializer(serializers.ModelSerializer):
    """Serializer for Case Updates"""
    updated_by = UserListSerializer(read_only=True)
    status_at_update = ReferenceDataSerializer(read_only=True)
    status_at_update_id = serializers.IntegerField(write_only=True)
    priority_at_update = ReferenceDataSerializer(read_only=True)
    priority_at_update_id = serializers.IntegerField(write_only=True)
    case_number = serializers.CharField(source='case.case_number', read_only=True)
    
    class Meta:
        model = CaseUpdate
        fields = [
            'id', 'case', 'case_number', 'updated_by', 'summary', 'details',
            'status_at_update', 'status_at_update_id', 'priority_at_update',
            'priority_at_update_id', 'progress_percentage', 'next_actions',
            'next_update_due', 'changes_made', 'created_at'
        ]
        read_only_fields = ['updated_by', 'created_at']


class CaseSerializer(serializers.ModelSerializer):
    """Basic Case serializer for list/create operations"""
    case_type = ReferenceDataSerializer(read_only=True)
    case_type_id = serializers.IntegerField(write_only=True)
    status = ReferenceDataSerializer(read_only=True)
    status_id = serializers.IntegerField(write_only=True)
    priority = ReferenceDataSerializer(read_only=True)
    priority_id = serializers.IntegerField(write_only=True)
    reporter = ContactSerializer(read_only=True)
    reporter_id = serializers.IntegerField(write_only=True)
    assigned_to = UserListSerializer(read_only=True)
    assigned_to_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    escalated_to = UserListSerializer(read_only=True)
    source_channel = serializers.StringRelatedField(read_only=True)
    source_channel_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    knows_about_116 = ReferenceDataSerializer(read_only=True)
    knows_about_116_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    ai_suggested_category = ReferenceDataSerializer(read_only=True)
    ai_suggested_priority = ReferenceDataSerializer(read_only=True)
    
    # Computed fields
    age_in_days = serializers.IntegerField(read_only=True)
    is_overdue = serializers.BooleanField(read_only=True)
    is_escalated = serializers.BooleanField(read_only=True)
    time_to_resolution = serializers.DurationField(read_only=True)
    
    class Meta:
        model = Case
        fields = [
            'id', 'uuid', 'case_number', 'case_type', 'case_type_id',
            'status', 'status_id', 'priority', 'priority_id', 'reporter',
            'reporter_id', 'reporter_is_afflicted', 'knows_about_116',
            'knows_about_116_id', 'assigned_to', 'assigned_to_id',
            'escalated_to', 'escalated_by', 'escalation_date', 'title',
            'narrative', 'action_plan', 'incident_date', 'incident_location',
            'report_location', 'source_type', 'source_reference',
            'source_channel', 'source_channel_id', 'is_gbv_related',
            'medical_exam_done', 'incident_reported_to_police',
            'police_ob_number', 'hiv_tested', 'hiv_test_result',
            'pep_given', 'art_given', 'ecp_given', 'counselling_given',
            'counselling_organization', 'due_date', 'closed_date',
            'resolution_summary', 'client_count', 'perpetrator_count',
            'incident_reference_number', 'ai_risk_score', 'ai_urgency_score',
            'ai_suggested_category', 'ai_suggested_priority', 'ai_summary',
            'ai_sentiment_score', 'ai_analysis_completed', 'ai_analysis_date',
            'age_in_days', 'is_overdue', 'is_escalated', 'time_to_resolution',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'uuid', 'case_number', 'escalated_by', 'escalation_date',
            'closed_date', 'client_count', 'perpetrator_count',
            'ai_analysis_completed', 'ai_analysis_date', 'age_in_days',
            'is_overdue', 'is_escalated', 'time_to_resolution',
            'created_at', 'updated_at'
        ]


class CaseDetailSerializer(CaseSerializer):
    """Detailed Case serializer with related objects"""
    categories = CaseCategorySerializer(many=True, read_only=True)
    activities = serializers.SerializerMethodField()
    services = serializers.SerializerMethodField()
    referrals = serializers.SerializerMethodField()
    notes = serializers.SerializerMethodField()
    attachments = serializers.SerializerMethodField()
    contact_roles = serializers.SerializerMethodField()
    
    class Meta(CaseSerializer.Meta):
        fields = CaseSerializer.Meta.fields + [
            'categories', 'activities', 'services', 'referrals',
            'notes', 'attachments', 'contact_roles'
        ]
    
    def get_activities(self, obj):
        """Get recent activities (last 10)"""
        activities = obj.activities.order_by('-created_at')[:10]
        return CaseActivitySerializer(activities, many=True).data
    
    def get_services(self, obj):
        """Get case services"""
        services = obj.services.order_by('-service_date')
        return CaseServiceSerializer(services, many=True).data
    
    def get_referrals(self, obj):
        """Get case referrals"""
        referrals = obj.referrals.order_by('-referral_date')
        return CaseReferralSerializer(referrals, many=True).data
    
    def get_notes(self, obj):
        """Get case notes (filtered by permissions)"""
        user = self.context.get('request').user if self.context.get('request') else None
        notes = obj.notes.order_by('-created_at')
        
        # Filter private notes based on user permissions
        if user and not user.is_staff and user.role not in ['admin', 'supervisor']:
            notes = notes.filter(
                models.Q(is_private=False) | models.Q(author=user)
            )
        
        return CaseNoteSerializer(notes, many=True).data
    
    def get_attachments(self, obj):
        """Get case attachments (filtered by permissions)"""
        user = self.context.get('request').user if self.context.get('request') else None
        attachments = obj.attachments.order_by('-created_at')
        
        # Filter confidential attachments based on user permissions
        if user and not user.is_staff and user.role not in ['admin', 'supervisor']:
            attachments = attachments.filter(
                models.Q(is_confidential=False) | models.Q(uploaded_by=user)
            )
        
        return CaseAttachmentSerializer(attachments, many=True).data
    
    def get_contact_roles(self, obj):
        """Get contacts involved in the case"""
        from apps.contacts.serializers import ContactRoleSerializer
        contact_roles = obj.contact_roles.select_related('contact', 'relationship')
        return ContactRoleSerializer(contact_roles, many=True).data


class CaseCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new cases with validation"""
    case_type_id = serializers.IntegerField()
    reporter_id = serializers.IntegerField()
    status_id = serializers.IntegerField(required=False)
    priority_id = serializers.IntegerField(required=False)
    assigned_to_id = serializers.IntegerField(required=False, allow_null=True)
    source_channel_id = serializers.IntegerField(required=False, allow_null=True)
    knows_about_116_id = serializers.IntegerField(required=False, allow_null=True)
    
    # Categories to assign
    category_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        write_only=True
    )
    
    # Initial contacts to add
    contacts = serializers.ListField(
        child=serializers.DictField(),
        required=False,
        write_only=True
    )
    
    class Meta:
        model = Case
        fields = [
            'case_type_id', 'reporter_id', 'status_id', 'priority_id',
            'assigned_to_id', 'reporter_is_afflicted', 'knows_about_116_id',
            'title', 'narrative', 'action_plan', 'incident_date',
            'incident_location', 'report_location', 'source_type',
            'source_reference', 'source_channel_id', 'is_gbv_related',
            'medical_exam_done', 'incident_reported_to_police',
            'police_ob_number', 'hiv_tested', 'hiv_test_result',
            'pep_given', 'art_given', 'ecp_given', 'counselling_given',
            'counselling_organization', 'due_date', 'incident_reference_number',
            'category_ids', 'contacts'
        ]
    
    def validate_case_type_id(self, value):
        """Validate case type exists"""
        from apps.core.models import ReferenceData
        if not ReferenceData.objects.filter(
            id=value, category='case_type', is_active=True
        ).exists():
            raise serializers.ValidationError("Invalid case type")
        return value
    
    def validate_reporter_id(self, value):
        """Validate reporter exists"""
        from apps.contacts.models import Contact
        if not Contact.objects.filter(id=value, is_active=True).exists():
            raise serializers.ValidationError("Invalid reporter")
        return value
    
    def validate_assigned_to_id(self, value):
        """Validate assigned user exists and can handle cases"""
        if value:
            from apps.accounts.models import User
            try:
                user = User.objects.get(id=value)
                if user.role not in ['agent', 'supervisor', 'manager']:
                    raise serializers.ValidationError(
                        "User cannot be assigned cases"
                    )
            except User.DoesNotExist:
                raise serializers.ValidationError("Invalid assigned user")
        return value
    
    def validate(self, data):
        """Additional validation"""
        # If GBV related, certain fields should be considered
        if data.get('is_gbv_related') and not data.get('incident_date'):
            raise serializers.ValidationError(
                "Incident date is required for GBV cases"
            )
        
        # Due date should be in the future
        if data.get('due_date') and data['due_date'] < timezone.now():
            raise serializers.ValidationError(
                "Due date must be in the future"
            )
        
        return data
    
    def create(self, validated_data):
        """Create case with related objects"""
        from apps.cases.services import CaseService as CaseServiceLogic
        from apps.core.models import ReferenceData
        from apps.contacts.models import Contact
        
        # Extract related data
        category_ids = validated_data.pop('category_ids', [])
        contacts_data = validated_data.pop('contacts', [])
        
        # Get related objects
        case_type = ReferenceData.objects.get(id=validated_data.pop('case_type_id'))
        reporter = Contact.objects.get(id=validated_data.pop('reporter_id'))
        
        # Get or create default status/priority
        if 'status_id' in validated_data:
            status = ReferenceData.objects.get(id=validated_data.pop('status_id'))
            validated_data['status'] = status
        
        if 'priority_id' in validated_data:
            priority = ReferenceData.objects.get(id=validated_data.pop('priority_id'))
            validated_data['priority'] = priority
        
        # Handle optional foreign keys
        for field_name, model_field in [
            ('assigned_to_id', 'assigned_to'),
            ('source_channel_id', 'source_channel'),
            ('knows_about_116_id', 'knows_about_116')
        ]:
            if field_name in validated_data:
                field_id = validated_data.pop(field_name)
                if field_id:
                    if field_name == 'assigned_to_id':
                        from apps.accounts.models import User
                        validated_data[model_field] = User.objects.get(id=field_id)
                    elif field_name == 'source_channel_id':
                        from apps.campaigns.models import Campaign
                        validated_data[model_field] = Campaign.objects.get(id=field_id)
                    else:
                        validated_data[model_field] = ReferenceData.objects.get(id=field_id)
        
        # Create the case using service
        case = CaseServiceLogic.create_case(
            case_type=case_type,
            reporter=reporter,
            narrative=validated_data.pop('narrative'),
            created_by=self.context['request'].user,
            **validated_data
        )
        
        # Add categories
        for category_id in category_ids:
            try:
                category = ReferenceData.objects.get(
                    id=category_id, category='case_category'
                )
                CaseCategory.objects.create(
                    case=case,
                    category=category,
                    is_primary=(category_id == category_ids[0]),  # First is primary
                    added_by=self.context['request'].user
                )
            except ReferenceData.DoesNotExist:
                pass  # Skip invalid categories
        
        # Add contacts
        for contact_data in contacts_data:
            try:
                contact = Contact.objects.get(id=contact_data['contact_id'])
                relationship = None
                if contact_data.get('relationship_id'):
                    relationship = ReferenceData.objects.get(
                        id=contact_data['relationship_id']
                    )
                
                CaseServiceLogic.add_case_contact(
                    case=case,
                    contact=contact,
                    role=contact_data['role'],
                    is_primary=contact_data.get('is_primary', False),
                    relationship=relationship,
                    role_data=contact_data.get('role_data', {}),
                    added_by=self.context['request'].user
                )
            except (Contact.DoesNotExist, KeyError):
                pass  # Skip invalid contacts
        
        return case


class CaseSummarySerializer(serializers.ModelSerializer):
    """Lightweight serializer for case summaries"""
    case_type_name = serializers.CharField(source='case_type.name', read_only=True)
    status_name = serializers.CharField(source='status.name', read_only=True)
    priority_name = serializers.CharField(source='priority.name', read_only=True)
    reporter_name = serializers.CharField(source='reporter.full_name', read_only=True)
    assigned_to_name = serializers.CharField(source='assigned_to.get_full_name', read_only=True)
    age_in_days = serializers.IntegerField(read_only=True)
    is_overdue = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Case
        fields = [
            'id', 'case_number', 'title', 'case_type_name', 'status_name',
            'priority_name', 'reporter_name', 'assigned_to_name',
            'is_gbv_related', 'age_in_days', 'is_overdue', 'due_date',
            'created_at', 'updated_at'
        ]