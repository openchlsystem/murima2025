# workflows/serializers.py
from rest_framework import serializers
from .models import Workflow, Step
from tenants.serializers import TenantSerializer

class StepSerializer(serializers.ModelSerializer):
    class Meta:
        model = Step
        fields = ['id', 'name', 'order', 'action', 'created_at', 'updated_at']

class WorkflowSerializer(serializers.ModelSerializer):
    steps = StepSerializer(many=True, read_only=True)
    tenant = TenantSerializer(read_only=True)  # Nested tenant data

    class Meta:
        model = Workflow
        fields = [
            'id', 'name', 'description', 'is_active', 
            'tenant', 'steps', 'created_at', 'updated_at'
        ]