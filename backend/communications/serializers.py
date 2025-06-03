from rest_framework import serializers
from .models import Channel, Message
from tenants.models import Tenant

class ChannelSerializer(serializers.ModelSerializer):
    tenant_name = serializers.CharField(source='tenant.name', read_only=True)
    
    class Meta:
        model = Channel
        fields = ['id', 'name', 'channel_type', 'is_active', 'config', 'tenant', 'tenant_name']
        extra_kwargs = {
            'tenant': {'write_only': True}  # Hide tenant ID in output (show name instead)
        }

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']