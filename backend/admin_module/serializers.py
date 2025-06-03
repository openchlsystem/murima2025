from rest_framework import serializers
from .models import SystemConfiguration, TenantConfiguration, AuditLog

class SystemConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemConfiguration
        fields = '__all__'
        read_only_fields = ('id',)

class TenantConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantConfiguration
        fields = '__all__'

class AuditLogSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = AuditLog
        fields = ['id', 'user_email', 'action', 'model_name', 'timestamp', 'metadata']