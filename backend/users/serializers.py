from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework_simplejwt.tokens import RefreshToken
from .models import OTP

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'tenant', 'is_verified']


class UserWithTokensSerializer(UserSerializer):
    access = serializers.SerializerMethodField()
    refresh = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ['access', 'refresh']

    def get_access(self, obj):
        return str(RefreshToken.for_user(obj).access_token)

    def get_refresh(self, obj):
        return str(RefreshToken.for_user(obj))


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
    access = serializers.SerializerMethodField(read_only=True)
    refresh = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'tenant', 'password', 'access', 'refresh']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data.get('username'),
            email=validated_data.get('email'),
            phone=validated_data.get('phone'),
            tenant=validated_data.get('tenant'),
            password=validated_data.get('password')
        )
        return user

    def get_access(self, obj):
        return str(RefreshToken.for_user(obj).access_token)

    def get_refresh(self, obj):
        return str(RefreshToken.for_user(obj))


class RequestOTPSerializer(serializers.Serializer):
    contact = serializers.CharField()  # phone or email
    method = serializers.ChoiceField(choices=OTP.DeliveryMethods.choices)

    def validate_contact(self, value):
        # Check if contact exists as email or phone for any user
        if '@' in value:
            if not User.objects.filter(email=value).exists():
                raise serializers.ValidationError("No user with this email exists.")
        else:
            if not User.objects.filter(phone=value).exists():
                raise serializers.ValidationError("No user with this phone number exists.")
        return value


class VerifyOTPSerializer(serializers.Serializer):
    contact = serializers.CharField()
    code = serializers.CharField(max_length=6)
    method = serializers.ChoiceField(choices=OTP.DeliveryMethods.choices)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    user = UserSerializer(read_only=True)

    def validate(self, attrs):
        contact = attrs['contact']
        code = attrs['code']
        method = attrs['method']

        try:
            if '@' in contact:
                user = User.objects.get(email=contact)
            else:
                user = User.objects.get(phone=contact)
        except User.DoesNotExist:
            raise serializers.ValidationError({"contact": "User not found."})

        if not OTP.verify_otp(user, code, method):
            raise serializers.ValidationError({"code": "Invalid OTP or OTP expired."})

        # Generate tokens
        refresh = RefreshToken.for_user(user)
        attrs['user'] = user
        attrs['access'] = str(refresh.access_token)
        attrs['refresh'] = str(refresh)
        
        return attrs