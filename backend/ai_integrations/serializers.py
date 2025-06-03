from rest_framework import serializers
from .models import AIService, AIModel
from tenants.api.serializers import TenantSerializer

class AIModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIModel
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

class AIServiceSerializer(serializers.ModelSerializer):
    models = AIModelSerializer(many=True, read_only=True)
    tenant = TenantSerializer(read_only=True)
    
    class Meta:
        model = AIService
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

    # Hide API key in responses (but allow writes)
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.pop('api_key', None)  # Remove API key from responses
        return data