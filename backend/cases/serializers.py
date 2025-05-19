from rest_framework import serializers
from .models import Case
from users.models import User

class CaseSerializer(serializers.ModelSerializer):
    assigned_to = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), 
        required=False, 
        allow_null=True
    )

    class Meta:
        model = Case
        fields = [
            'id', 'title', 'description', 'status', 
            'assigned_to', 'tenant', 'created_at', 
            'updated_at', 'created_by', 'updated_by'
        ]
        read_only_fields = ['tenant', 'created_by', 'updated_by']

    def create(self, validated_data):
        # Auto-set tenant and creator from request
        request = self.context.get('request')
        validated_data['tenant'] = request.user.tenant
        validated_data['created_by'] = request.user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Auto-set updater from request
        request = self.context.get('request')
        validated_data['updated_by'] = request.user
        return super().update(instance, validated_data)