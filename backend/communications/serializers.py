# core/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    Channel, Contact, Message, Conversation, 
    Tag, CallLog, Template
)

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = fields

class ChannelSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    channel_type_display = serializers.CharField(source='get_channel_type_display', read_only=True)
    
    class Meta:
        model = Channel
        fields = [
            'id', 'name', 'channel_type', 'channel_type_display',
            'status', 'status_display', 'config', 'priority',
            'rate_limit', 'created_at', 'updated_at'
        ]
        extra_kwargs = {
            'config': {'write_only': True}  # For security, don't expose in GET requests
        }

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = [
            'id', 'name', 'phone', 'email', 'whatsapp_id',
            'facebook_id', 'other_identifiers', 'is_blocked',
            'metadata', 'created_at', 'updated_at'
        ]

class MessageSerializer(serializers.ModelSerializer):
    direction_display = serializers.CharField(source='get_direction_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    channel_name = serializers.CharField(source='channel.name', read_only=True)
    contact_name = serializers.CharField(source='contact.name', read_only=True, allow_null=True)
    
    class Meta:
        model = Message
        fields = [
            'id', 'channel', 'channel_name', 'contact', 'contact_name',
            'external_id', 'direction', 'direction_display', 'content',
            'status', 'status_display', 'status_updated_at', 'metadata',
            'error_reason', 'call_duration', 'call_record_url', 'media_url',
            'media_type', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'status_display', 'direction_display', 'status_updated_at',
            'channel_name', 'contact_name'
        ]

class ConversationSerializer(serializers.ModelSerializer):
    last_message_content = serializers.SerializerMethodField()
    last_message_timestamp = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()
    channel_name = serializers.CharField(source='channel.name', read_only=True)
    contact_name = serializers.CharField(source='contact.name', read_only=True)
    
    class Meta:
        model = Conversation
        fields = [
            'id', 'contact', 'contact_name', 'channel', 'channel_name',
            'is_open', 'last_message', 'last_message_content',
            'last_message_timestamp', 'unread_count', 'tags',
            'created_at', 'updated_at'
        ]
    
    def get_last_message_content(self, obj):
        if obj.last_message:
            return obj.last_message.content[:100]  # Return first 100 chars
        return None
    
    def get_last_message_timestamp(self, obj):
        if obj.last_message:
            return obj.last_message.created_at
        return None
    
    def get_unread_count(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            # Implement your unread count logic here
            # Example: return Message.objects.filter(conversation=obj, status='DELIVERED', read=False).count()
            return 0
        return 0

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'color', 'created_at', 'updated_at']

class CallLogSerializer(serializers.ModelSerializer):
    direction_display = serializers.CharField(source='get_direction_display', read_only=True)
    duration_formatted = serializers.SerializerMethodField()
    channel_name = serializers.CharField(source='channel.name', read_only=True)
    contact_name = serializers.CharField(source='contact.name', read_only=True, allow_null=True)
    
    class Meta:
        model = CallLog
        fields = [
            'id', 'channel', 'channel_name', 'contact', 'contact_name',
            'from_number', 'to_number', 'call_sid', 'direction',
            'direction_display', 'status', 'duration', 'duration_formatted',
            'start_time', 'end_time', 'recording_url', 'metadata',
            'created_at', 'updated_at'
        ]
    
    def get_duration_formatted(self, obj):
        if obj.duration:
            minutes = obj.duration // 60
            seconds = obj.duration % 60
            return f"{minutes}m {seconds}s"
        return "0s"

class TemplateSerializer(serializers.ModelSerializer):
    template_type_display = serializers.CharField(source='get_template_type_display', read_only=True)
    channel_types_list = serializers.SerializerMethodField()
    
    class Meta:
        model = Template
        fields = [
            'id', 'name', 'content', 'template_type', 'template_type_display',
            'channel_types', 'channel_types_list', 'variables', 'created_at', 'updated_at'
        ]
    
    def get_channel_types_list(self, obj):
        return [ct.strip() for ct in obj.channel_types.split(',') if ct.strip()]

class MessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = [
            'channel', 'contact', 'content', 'media_url', 'media_type',
            'direction', 'status', 'metadata'
        ]
        extra_kwargs = {
            'direction': {'read_only': True},  # Typically set by the system
            'status': {'read_only': True}     # Typically starts as QUEUED
        }

class CallInitiateSerializer(serializers.Serializer):
    channel = serializers.PrimaryKeyRelatedField(queryset=Channel.objects.filter(channel_type='ASTERISK'))
    to_number = serializers.CharField(max_length=20)
    from_number = serializers.CharField(max_length=20, required=False)
    contact = serializers.PrimaryKeyRelatedField(
        queryset=Contact.objects.all(),
        required=False,
        allow_null=True
    )
    metadata = serializers.JSONField(required=False, default=dict)
    
    def validate(self, data):
        # Add any custom validation for call initiation
        return data

class WebhookPayloadSerializer(serializers.Serializer):
    """
    Generic serializer for handling incoming webhook payloads from various providers
    """
    event_type = serializers.CharField()
    payload = serializers.JSONField()
    provider = serializers.CharField()  # whatsapp, twilio, asterisk, etc.
    
    def validate_provider(self, value):
        valid_providers = ['whatsapp', 'twilio', 'asterisk', 'facebook']
        if value.lower() not in valid_providers:
            raise serializers.ValidationError(f"Provider must be one of {valid_providers}")
        return value.lower()