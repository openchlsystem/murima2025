from rest_framework import serializers
from .models import Tenant, Domain

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User  # Ensure you import your User model
        fields = ['id', 'username', 'email']

class DomainSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    updated_by = UserSerializer(read_only=True)
    
    class Meta:
        model = Domain
        fields = ['id', 'domain', 'is_primary', 'created_at', 'updated_at', 'created_by', 'updated_by']

class TenantSerializer(serializers.ModelSerializer):
    domains = DomainSerializer(many=True, read_only=True)
    created_by = UserSerializer(read_only=True)
    updated_by = UserSerializer(read_only=True)
    
    class Meta:
        model = Tenant
        fields = [
            'id', 'name', 'paid_until', 'on_trial', 
            'enable_ai', 'enable_analytics', 'domains',
            'created_at', 'updated_at', 'created_by', 'updated_by'
        ]