# apps/notifications/serializers.py
from rest_framework import serializers
from .models import Notification, NotificationPreference

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

class NotificationPreferenceSerializer(serializers.ModelSerializer):
    """Serializer for notification preferences."""
    class Meta:
        model = NotificationPreference
        exclude = ['user', 'created_at', 'updated_at']