# analytics/serializers.py
from rest_framework import serializers
from .models import Dashboard, Widget
from tenants.serializers import TenantSerializer

class WidgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Widget
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'created_by', 'updated_by')

class DashboardSerializer(serializers.ModelSerializer):
    widgets = WidgetSerializer(many=True, read_only=True)
    tenant = TenantSerializer(read_only=True)

    class Meta:
        model = Dashboard
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'created_by', 'updated_by')