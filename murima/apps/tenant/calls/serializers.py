from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.conf import settings
from .models import Extension, CallLog

User = get_user_model()


class ExtensionSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Extension
        fields = ['id', 'username', 'password', 'user_id', 'user_username', 'is_active', 'created_at']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user_id = validated_data.pop('user_id')
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise serializers.ValidationError({"user_id": "User does not exist"})
        
        # Check if user already has an extension
        if Extension.objects.filter(user=user).exists():
            raise serializers.ValidationError({"user_id": "User already has an extension"})
        
        validated_data['user'] = user
        return super().create(validated_data)


class ExtensionRetrieveSerializer(serializers.ModelSerializer):
    """Serializer for retrieving extension with password for WebRTC registration"""
    class Meta:
        model = Extension
        fields = ['id', 'username', 'password', 'user_id', 'is_active']


class CallLogSerializer(serializers.ModelSerializer):
    caller_username = serializers.CharField(source='caller_extension.username', read_only=True)
    callee_username = serializers.CharField(source='callee_extension.username', read_only=True)
    caller_user_id = serializers.IntegerField(source='caller_extension.user.id', read_only=True)
    callee_user_id = serializers.IntegerField(source='callee_extension.user.id', read_only=True)

    class Meta:
        model = CallLog
        fields = [
            'id',
            'caller_username',
            'callee_username', 
            'caller_user_id',
            'callee_user_id',
            'start_time',
            'end_time',
            'duration',
            'call_status',
            'asterisk_call_id',
            'created_at'
        ]


class CallLogCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating call logs from ARI events"""
    caller_username = serializers.CharField(write_only=True)
    callee_username = serializers.CharField(write_only=True)

    class Meta:
        model = CallLog
        fields = [
            'caller_username',
            'callee_username',
            'start_time',
            'end_time',
            'call_status',
            'asterisk_call_id'
        ]

    def create(self, validated_data):
        caller_username = validated_data.pop('caller_username')
        callee_username = validated_data.pop('callee_username')
        
        try:
            caller_extension = Extension.objects.get(username=caller_username)
            callee_extension = Extension.objects.get(username=callee_username)
        except Extension.DoesNotExist:
            raise serializers.ValidationError("Extension not found")
        
        validated_data['caller_extension'] = caller_extension
        validated_data['callee_extension'] = callee_extension
        
        return super().create(validated_data)