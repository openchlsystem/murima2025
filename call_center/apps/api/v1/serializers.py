# apps/api/v1/serializers.py
from rest_framework import serializers
from apps.cases.models import Case, CaseActivity, CaseClient, CasePerpetrator, CaseService, CaseReferral
from apps.contacts.models import Contact, Location
from apps.calls.models import Call, CallEvent
from apps.campaigns.models import Campaign, WorkingHour
from apps.accounts.models import User
from apps.notifications.models import Notification
from apps.core.models import ReferenceData

class UserSerializer(serializers.ModelSerializer):
    """Serializer for users."""
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 
                 'full_name', 'role', 'extension', 'is_active', 'date_joined']
        read_only_fields = fields
    
    def get_full_name(self, obj):
        return obj.get_full_name()

class LocationSerializer(serializers.ModelSerializer):
    """Serializer for locations."""
    class Meta:
        model = Location
        fields = ['id', 'name', 'type', 'parent', 'code']

class ContactListSerializer(serializers.ModelSerializer):
    """Serializer for contact listing."""
    class Meta:
        model = Contact
        fields = ['id', 'full_name', 'phone', 'email', 'age', 'sex']

class ContactSerializer(serializers.ModelSerializer):
    """Detailed serializer for contacts."""
    sex_display = serializers.SerializerMethodField()
    age_group_display = serializers.SerializerMethodField()
    
    class Meta:
        model = Contact
        fields = ['id', 'full_name', 'first_name', 'last_name', 'email', 'phone', 
                 'phone2', 'birth_date', 'age', 'age_group', 'age_group_display',
                 'sex', 'sex_display', 'national_id', 'national_id_type',
                 'address', 'residence', 'location', 'nationality', 'tribe',
                 'language', 'landmark', 'created_at', 'updated_at']
    
    def get_sex_display(self, obj):
        return obj.sex.name if obj.sex else None
    
    def get_age_group_display(self, obj):
        return obj.age_group.name if obj.age_group else None

class CaseListSerializer(serializers.ModelSerializer):
    """Serializer for case listing."""
    reporter_name = serializers.SerializerMethodField()
    status_display = serializers.SerializerMethodField()
    priority_display = serializers.SerializerMethodField()
    assigned_to_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Case
        fields = ['id', 'case_number', 'reporter_name', 'status', 'status_display', 
                 'priority', 'priority_display', 'assigned_to', 'assigned_to_name',
                 'created_at', 'closed_at']
    
    def get_reporter_name(self, obj):
        return obj.reporter.full_name if obj.reporter else None
    
    def get_status_display(self, obj):
        return obj.status.name if obj.status else None
    
    def get_priority_display(self, obj):
        return obj.priority.name if obj.priority else None
    
    def get_assigned_to_name(self, obj):
        return obj.assigned_to.get_full_name() if obj.assigned_to else None

class CaseClientSerializer(serializers.ModelSerializer):
    """Serializer for case clients."""
    contact = ContactSerializer()
    
    class Meta:
        model = CaseClient
        fields = ['id', 'contact', 'relationship', 'is_disabled', 'disability', 
                 'health_status', 'hiv_status', 'in_school', 'school_type',
                 'school_level', 'school_attendance', 'school_name', 'marital_status',
                 'notes']

class CasePerpetratorSerializer(serializers.ModelSerializer):
    """Serializer for case perpetrators."""
    contact = ContactSerializer()
    
    class Meta:
        model = CasePerpetrator
        fields = ['id', 'contact', 'relationship', 'shares_home', 'marital_status',
                 'health_status', 'employment_status', 'notes']

class CaseActivitySerializer(serializers.ModelSerializer):
    """Serializer for case activities."""
    user_name = serializers.SerializerMethodField()
    
    class Meta:
        model = CaseActivity
        fields = ['id', 'activity_type', 'user', 'user_name', 'details', 
                 'changes', 'created_at']
    
    def get_user_name(self, obj):
        return obj.user.get_full_name() if obj.user else None

class CaseDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for cases."""
    reporter = ContactSerializer()
    status_display = serializers.SerializerMethodField()
    priority_display = serializers.SerializerMethodField()
    category_display = serializers.SerializerMethodField()
    assigned_to_detail = UserSerializer(source='assigned_to', read_only=True)
    escalated_to_detail = UserSerializer(source='escalated_to', read_only=True)
    escalated_by_detail = UserSerializer(source='escalated_by', read_only=True)
    created_by_detail = UserSerializer(source='created_by', read_only=True)
    clients = CaseClientSerializer(many=True, read_only=True)
    perpetrators = CasePerpetratorSerializer(many=True, read_only=True)
    services = serializers.SerializerMethodField()
    referrals = serializers.SerializerMethodField()
    
    class Meta:
        model = Case
        fields = ['id', 'uuid', 'case_number', 'reporter', 'status', 'status_display', 
                 'priority', 'priority_display', 'category', 'category_display',
                 'assigned_to', 'assigned_to_detail', 'escalated_to', 'escalated_to_detail',
                 'escalated_by', 'escalated_by_detail', 'escalated_at', 'source',
                 'narrative', 'action_plan', 'is_gbv_related', 'created_at', 
                 'updated_at', 'closed_at', 'created_by', 'created_by_detail',
                 'clients', 'perpetrators', 'services', 'referrals']
    
    def get_status_display(self, obj):
        return obj.status.name if obj.status else None
    
    def get_priority_display(self, obj):
        return obj.priority.name if obj.priority else None
    
    def get_category_display(self, obj):
        return obj.category.name if obj.category else None
    
    def get_services(self, obj):
        services = obj.case_services.all()
        return [
            {
                'id': service.id,
                'service_id': service.service.id,
                'name': service.service.name,
                'details': service.details
            }
            for service in services
        ]
    
    def get_referrals(self, obj):
        referrals = obj.case_referrals.all()
        return [
            {
                'id': referral.id,
                'referral_id': referral.referral.id,
                'name': referral.referral.name,
                'details': referral.details
            }
            for referral in referrals
        ]

class CaseSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating cases."""
    class Meta:
        model = Case
        fields = ['id', 'case_number', 'reporter', 'status', 'priority', 'category',
                 'assigned_to', 'narrative', 'action_plan', 'is_gbv_related', 
                 'created_at', 'updated_at', 'closed_at']
        read_only_fields = ['id', 'case_number', 'created_at', 'updated_at', 'closed_at']

# apps/api/v1/serializers.py (continued)
class CallListSerializer(serializers.ModelSerializer):
    """Serializer for call listing."""
    agent_name = serializers.SerializerMethodField()
    contact_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Call
        fields = ['id', 'unique_id', 'caller_number', 'direction', 'start_time',
                 'duration_seconds', 'status', 'agent', 'agent_name', 
                 'contact', 'contact_name', 'case']
    
    def get_agent_name(self, obj):
        return obj.agent.get_full_name() if obj.agent else None
    
    def get_contact_name(self, obj):
        return obj.contact.full_name if obj.contact else None

class CallEventSerializer(serializers.ModelSerializer):
    """Serializer for call events."""
    agent_name = serializers.SerializerMethodField()
    
    class Meta:
        model = CallEvent
        fields = ['id', 'event_type', 'event_time', 'duration_seconds', 
                 'agent', 'agent_name', 'details']
    
    def get_agent_name(self, obj):
        return obj.agent.get_full_name() if obj.agent else None

class CallSerializer(serializers.ModelSerializer):
    """Detailed serializer for calls."""
    agent_detail = UserSerializer(source='agent', read_only=True)
    contact_detail = ContactSerializer(source='contact', read_only=True)
    events = CallEventSerializer(many=True, read_only=True)
    disposition_display = serializers.SerializerMethodField()
    
    class Meta:
        model = Call
        fields = ['id', 'unique_id', 'campaign', 'caller_number', 'caller_name',
                 'direction', 'agent', 'agent_detail', 'contact', 'contact_detail',
                 'start_time', 'answer_time', 'end_time', 'duration_seconds',
                 'wait_time_seconds', 'talk_time_seconds', 'hold_time_seconds',
                 'status', 'hangup_reason', 'recording_url', 'case', 
                 'disposition', 'disposition_display', 'notes', 'events']
    
    def get_disposition_display(self, obj):
        return obj.disposition.name if obj.disposition else None

class WorkingHourSerializer(serializers.ModelSerializer):
    """Serializer for working hours."""
    day_of_week_display = serializers.SerializerMethodField()
    
    class Meta:
        model = WorkingHour
        fields = ['id', 'day_of_week', 'day_of_week_display', 'start_time', 
                 'end_time', 'is_active']
    
    def get_day_of_week_display(self, obj):
        days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        return days[obj.day_of_week]

class CampaignSerializer(serializers.ModelSerializer):
    """Serializer for campaigns."""
    working_hours = WorkingHourSerializer(many=True, read_only=True)
    campaign_type_display = serializers.SerializerMethodField()
    category_display = serializers.SerializerMethodField()
    
    class Meta:
        model = Campaign
        fields = ['id', 'name', 'campaign_type', 'campaign_type_display', 
                 'caller_id', 'category', 'category_display', 'ring_strategy', 
                 'ring_timeout', 'wrapup_time', 'sla_wait_target', 
                 'sla_hold_target', 'queue_timeout', 'description', 
                 'is_active', 'working_hours']
    
    def get_campaign_type_display(self, obj):
        return dict(Campaign.CAMPAIGN_TYPE_CHOICES).get(obj.campaign_type)
    
    def get_category_display(self, obj):
        return obj.category.name if obj.category else None

class NotificationSerializer(serializers.ModelSerializer):
    """Serializer for notifications."""
    content_type_name = serializers.SerializerMethodField()
    content_object_str = serializers.SerializerMethodField()
    
    class Meta:
        model = Notification
        fields = [
            'id', 'title', 'message', 'notification_type', 
            'is_read', 'read_at', 'created_at', 'content_type_name',
            'content_object_str', 'object_id'
        ]
        read_only_fields = fields
    
    def get_content_type_name(self, obj):
        """Get the content type name."""
        if obj.content_type:
            return obj.content_type.model
        return None
    
    def get_content_object_str(self, obj):
        """Get string representation of the content object."""
        if obj.content_object:
            return str(obj.content_object)
        return None

class ReferenceDataSerializer(serializers.ModelSerializer):
    """Serializer for reference data."""
    parent_name = serializers.SerializerMethodField()
    
    class Meta:
        model = ReferenceData
        fields = ['id', 'category', 'code', 'name', 'parent', 'parent_name', 
                 'level', 'description', 'is_active']
    
    def get_parent_name(self, obj):
        return obj.parent.name if obj.parent else None