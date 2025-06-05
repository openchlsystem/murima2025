from rest_framework import serializers
from .models import (
    SystemConfiguration,
    TenantConfiguration,
    AuditLog,
    CategoryType,
    Category,
    SystemNotification
)
from tenants.models import Tenant
from django.contrib.auth import get_user_model

User = get_user_model()


# 🔧 System Configuration Serializer
class SystemConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemConfiguration
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


# 🏢 Tenant Configuration Serializer
class TenantConfigurationSerializer(serializers.ModelSerializer):
    tenant_name = serializers.CharField(source='tenant.name', read_only=True)
    default_assignee_name = serializers.CharField(source='default_assignee.get_full_name', read_only=True)

    class Meta:
        model = TenantConfiguration
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


# 🕵️ Audit Log Serializer
class AuditLogSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email', read_only=True)
    action_display = serializers.CharField(source='get_action_display', read_only=True)

    class Meta:
        model = AuditLog
        fields = '__all__'
        read_only_fields = ['id', 'timestamp', 'user_email', 'action_display']


# 📁 Category Type Serializer
class CategoryTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryType
        fields = '__all__'


# 📂 Category Serializer
class CategorySerializer(serializers.ModelSerializer):
    category_type_name = serializers.CharField(source='category_type.name', read_only=True)
    parent_name = serializers.CharField(source='parent.name', read_only=True)

    class Meta:
        model = Category
        fields = '__all__'


# 🔔 System Notification Serializer
class SystemNotificationSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    tenant_ids = serializers.PrimaryKeyRelatedField(
        source='affected_tenants',
        many=True,
        queryset=Tenant.objects.all()
    )

    class Meta:
        model = SystemNotification
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by_name']
