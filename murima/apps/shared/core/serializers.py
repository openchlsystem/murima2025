from rest_framework import serializers
from core.models import (
    BaseModel, 
    AuditLog,
    TimestampedModel,
    UUIDModel,
    UserTrackingModel,
    SoftDeleteModel,
    OwnedModel
)
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = fields

class TimestampedModelSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        abstract = True

class UUIDModelSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        abstract = True

class UserTrackingModelSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    updated_by = UserSerializer(read_only=True)

    class Meta:
        abstract = True

class SoftDeleteModelSerializer(serializers.ModelSerializer):
    is_deleted = serializers.BooleanField(read_only=True)
    deleted_at = serializers.DateTimeField(read_only=True)
    deleted_by = UserSerializer(read_only=True)

    class Meta:
        abstract = True

class OwnedModelSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        abstract = True

class BaseModelSerializer(
    UUIDModelSerializer,
    TimestampedModelSerializer,
    UserTrackingModelSerializer,
    SoftDeleteModelSerializer
):
    """
    Base serializer that includes all common functionality
    """
    class Meta:
        abstract = True