from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from .models import OTP

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'tenant', 'is_verified']


class UserManagementSerializer(serializers.ModelSerializer):
    groups = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Group.objects.all(),
        required=False
    )

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'phone', 'tenant', 'is_verified', 'is_active', 'groups'
        ]
        read_only_fields = ['id']

    def update(self, instance, validated_data):
        groups = validated_data.pop('groups', None)
        if groups is not None:
            instance.groups.set(groups)
        return super().update(instance, validated_data)


class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'tenant', 'password']

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data.get('username'),
            email=validated_data.get('email'),
            phone=validated_data.get('phone'),
            tenant=validated_data.get('tenant'),
            password=validated_data.get('password')
        )


class RequestOTPSerializer(serializers.Serializer):
    contact = serializers.CharField()  # phone or email
    method = serializers.ChoiceField(choices=OTP.DeliveryMethods.choices)


class VerifyOTPSerializer(serializers.Serializer):
    contact = serializers.CharField()
    code = serializers.CharField(max_length=6)
    method = serializers.ChoiceField(choices=OTP.DeliveryMethods.choices)
