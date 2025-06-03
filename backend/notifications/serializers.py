from rest_framework import serializers
from .models import Notification
from users.serializers import UserSerializer  # Assume this exists

class NotificationSerializer(serializers.ModelSerializer):
    recipient = UserSerializer(read_only=True)
    recipient_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), 
        source='recipient', 
        write_only=True
    )

    class Meta:
        model = Notification
        fields = [
            'id', 'title', 'message', 'is_read', 
            'channel', 'sent_at', 'recipient', 
            'recipient_id', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'sent_at']