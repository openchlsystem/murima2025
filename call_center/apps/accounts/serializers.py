# apps/accounts/serializers.py
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone as django_timezone
from datetime import datetime, timedelta
from .models import User, UserProfile, AgentShift, UserSession


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for UserProfile model"""
    
    class Meta:
        model = UserProfile
        fields = [
            'avatar', 'date_of_birth', 'emergency_contact_name', 
            'emergency_contact_phone', 'email_notifications', 
            'browser_notifications', 'sms_notifications', 'skills', 
            'certifications', 'languages_spoken', 'call_queue_limit', 
            'auto_answer_calls', 'wrap_up_time_seconds'
        ]
        extra_kwargs = {
            'avatar': {'required': False},
            'date_of_birth': {'required': False},
        }
    
    def validate_call_queue_limit(self, value):
        """Validate call queue limit"""
        if value < 1 or value > 20:
            raise serializers.ValidationError(
                _("Call queue limit must be between 1 and 20")
            )
        return value
    
    def validate_wrap_up_time_seconds(self, value):
        """Validate wrap-up time"""
        if value < 0 or value > 300:
            raise serializers.ValidationError(
                _("Wrap-up time must be between 0 and 300 seconds")
            )
        return value


class AgentShiftSerializer(serializers.ModelSerializer):
    """Serializer for AgentShift model"""
    
    day_name = serializers.CharField(source='get_day_of_week_display', read_only=True)
    duration_hours = serializers.ReadOnlyField()
    is_current = serializers.ReadOnlyField()
    
    class Meta:
        model = AgentShift
        fields = [
            'id', 'day_of_week', 'day_name', 'start_time', 'end_time',
            'break_duration_minutes', 'timezone', 'effective_from',
            'effective_to', 'duration_hours', 'is_current', 'is_active'
        ]
        extra_kwargs = {
            'effective_from': {'required': False},
            'effective_to': {'required': False},
        }
    
    def validate(self, data):
        """Validate shift data"""
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        effective_from = data.get('effective_from')
        effective_to = data.get('effective_to')
        
        if start_time and end_time and start_time >= end_time:
            raise serializers.ValidationError({
                'end_time': _("End time must be after start time")
            })
        
        if effective_from and effective_to and effective_from >= effective_to:
            raise serializers.ValidationError({
                'effective_to': _("Effective to date must be after effective from date")
            })
        
        return data


class UserSessionSerializer(serializers.ModelSerializer):
    """Serializer for UserSession model"""
    
    duration = serializers.ReadOnlyField()
    duration_formatted = serializers.SerializerMethodField()
    
    class Meta:
        model = UserSession
        fields = [
            'id', 'session_key', 'ip_address', 'user_agent',
            'login_time', 'logout_time', 'is_active', 'duration',
            'duration_formatted'
        ]
        read_only_fields = [
            'session_key', 'ip_address', 'user_agent', 'login_time',
            'logout_time', 'duration'
        ]
    
    def get_duration_formatted(self, obj):
        """Get formatted duration string"""
        if not obj.duration:
            return None
        
        total_seconds = int(obj.duration.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        
        if hours > 0:
            return f"{hours}h {minutes}m {seconds}s"
        elif minutes > 0:
            return f"{minutes}m {seconds}s"
        else:
            return f"{seconds}s"


class UserListSerializer(serializers.ModelSerializer):
    """Minimal serializer for user listings"""
    
    full_name = serializers.ReadOnlyField(source='get_full_name')
    role_display = serializers.ReadOnlyField(source='get_role_display')
    status_display = serializers.ReadOnlyField(source='get_status_display')
    agent_status_display = serializers.ReadOnlyField(source='get_agent_status_display')
    manager_name = serializers.CharField(source='manager.get_full_name', read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'employee_id', 'full_name',
            'role', 'role_display', 'status', 'status_display',
            'agent_status', 'agent_status_display', 'department',
            'manager_name', 'extension', 'agent_number', 'is_online',
            'last_activity', 'is_active'
        ]


class UserDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for user details"""
    
    full_name = serializers.ReadOnlyField(source='get_full_name')
    display_name = serializers.ReadOnlyField(source='get_display_name')
    role_display = serializers.ReadOnlyField(source='get_role_display')
    status_display = serializers.ReadOnlyField(source='get_status_display')
    agent_status_display = serializers.ReadOnlyField(source='get_agent_status_display')
    
    # Related data
    profile = UserProfileSerializer(read_only=True)
    shifts = AgentShiftSerializer(many=True, read_only=True)
    manager_name = serializers.CharField(source='manager.get_full_name', read_only=True)
    subordinates_count = serializers.SerializerMethodField()
    
    # Computed properties
    is_agent = serializers.ReadOnlyField()
    is_supervisor = serializers.ReadOnlyField()
    is_manager = serializers.ReadOnlyField()
    is_admin = serializers.ReadOnlyField()
    can_supervise = serializers.ReadOnlyField()
    is_available_for_calls = serializers.ReadOnlyField()
    is_on_break = serializers.ReadOnlyField()
    
    class Meta:
        model = User
        fields = [
            # Basic info
            'id', 'username', 'email', 'employee_id', 'first_name', 'last_name',
            'full_name', 'display_name', 'phone',
            
            # Work info
            'role', 'role_display', 'department', 'manager', 'manager_name',
            'extension', 'agent_number',
            
            # Status
            'status', 'status_display', 'agent_status', 'agent_status_display',
            'is_online', 'is_active', 'last_activity',
            
            # Break and time tracking
            'last_break_type', 'last_break_time', 'break_start_time',
            'shift_start_time',
            
            # Contact info
            'last_login_ip', 'timezone', 'language',
            
            # Dates
            'date_joined', 'date_terminated', 'last_login',
            
            # Related data
            'profile', 'shifts', 'subordinates_count',
            
            # Computed properties
            'is_agent', 'is_supervisor', 'is_manager', 'is_admin',
            'can_supervise', 'is_available_for_calls', 'is_on_break'
        ]
        read_only_fields = [
            'id', 'last_login', 'date_joined', 'last_login_ip',
            'last_activity', 'is_online'
        ]
    
    def get_subordinates_count(self, obj):
        """Get count of subordinates"""
        return obj.get_subordinates().count()


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new users"""
    
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        help_text=_("User's password")
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        help_text=_("Confirm password")
    )
    profile = UserProfileSerializer(required=False)
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'employee_id', 'first_name', 'last_name',
            'phone', 'role', 'department', 'manager', 'extension',
            'agent_number', 'status', 'timezone', 'language',
            'password', 'password_confirm', 'profile'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'password_confirm': {'write_only': True},
        }
    
    def validate_password(self, value):
        """Validate password strength"""
        try:
            validate_password(value)
        except DjangoValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return value
    
    def validate(self, data):
        """Validate passwords match"""
        password = data.get('password')
        password_confirm = data.get('password_confirm')
        
        if password != password_confirm:
            raise serializers.ValidationError({
                'password_confirm': _("Passwords do not match")
            })
        
        return data
    
    def create(self, validated_data):
        """Create user with password and profile"""
        profile_data = validated_data.pop('profile', {})
        validated_data.pop('password_confirm', None)
        password = validated_data.pop('password')
        
        user = User.objects.create_user(
            password=password,
            **validated_data
        )
        
        # Create profile if data provided
        if profile_data:
            UserProfile.objects.create(user=user, **profile_data)
        
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating users"""
    
    profile = UserProfileSerializer(required=False)
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'employee_id', 'first_name', 'last_name',
            'phone', 'role', 'department', 'manager', 'extension',
            'agent_number', 'status', 'timezone', 'language', 'profile'
        ]
    
    def update(self, instance, validated_data):
        """Update user and profile"""
        profile_data = validated_data.pop('profile', None)
        
        # Update user fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update or create profile
        if profile_data is not None:
            profile, created = UserProfile.objects.get_or_create(user=instance)
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()
        
        return instance


class PasswordChangeSerializer(serializers.Serializer):
    """Serializer for password change"""
    
    old_password = serializers.CharField(
        required=True,
        style={'input_type': 'password'}
    )
    new_password = serializers.CharField(
        required=True,
        style={'input_type': 'password'}
    )
    new_password_confirm = serializers.CharField(
        required=True,
        style={'input_type': 'password'}
    )
    
    def validate_old_password(self, value):
        """Validate current password"""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(_("Current password is incorrect"))
        return value
    
    def validate_new_password(self, value):
        """Validate new password strength"""
        try:
            validate_password(value, user=self.context['request'].user)
        except DjangoValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return value
    
    def validate(self, data):
        """Validate new passwords match"""
        new_password = data.get('new_password')
        new_password_confirm = data.get('new_password_confirm')
        
        if new_password != new_password_confirm:
            raise serializers.ValidationError({
                'new_password_confirm': _("New passwords do not match")
            })
        
        return data


class AgentStatusSerializer(serializers.Serializer):
    """Serializer for changing agent status"""
    
    status = serializers.ChoiceField(
        choices=User.AGENT_STATUS_CHOICES,
        required=True
    )
    break_type = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=32
    )
    
    def validate(self, data):
        """Validate status change"""
        status = data.get('status')
        break_type = data.get('break_type')
        
        if status == 'on_break' and not break_type:
            raise serializers.ValidationError({
                'break_type': _("Break type is required when status is 'on_break'")
            })
        
        return data


class LoginSerializer(serializers.Serializer):
    """Serializer for user login"""
    
    username = serializers.CharField(required=True)
    password = serializers.CharField(
        required=True,
        style={'input_type': 'password'}
    )
    
    def validate(self, data):
        """Validate credentials"""
        username = data.get('username')
        password = data.get('password')
        
        if username and password:
            user = authenticate(
                request=self.context.get('request'),
                username=username,
                password=password
            )
            
            if not user:
                raise serializers.ValidationError(
                    _("Invalid username or password")
                )
            
            if not user.is_active:
                raise serializers.ValidationError(
                    _("User account is disabled")
                )
            
            data['user'] = user
        else:
            raise serializers.ValidationError(
                _("Username and password are required")
            )
        
        return data


class UserStatsSerializer(serializers.Serializer):
    """Serializer for user statistics"""
    
    total_calls_today = serializers.IntegerField(read_only=True)
    total_talk_time_today = serializers.DurationField(read_only=True)
    average_call_time = serializers.DurationField(read_only=True)
    cases_handled_today = serializers.IntegerField(read_only=True)
    break_time_today = serializers.DurationField(read_only=True)
    login_time_today = serializers.DateTimeField(read_only=True)
    shift_duration = serializers.DurationField(read_only=True)
    
    # Performance metrics
    call_resolution_rate = serializers.FloatField(read_only=True)
    customer_satisfaction_score = serializers.FloatField(read_only=True)
    quality_score = serializers.FloatField(read_only=True)


class TeamStatsSerializer(serializers.Serializer):
    """Serializer for team statistics"""
    
    team_members = UserListSerializer(many=True, read_only=True)
    total_agents_online = serializers.IntegerField(read_only=True)
    total_agents_available = serializers.IntegerField(read_only=True)
    total_agents_on_call = serializers.IntegerField(read_only=True)
    total_agents_on_break = serializers.IntegerField(read_only=True)
    team_call_volume_today = serializers.IntegerField(read_only=True)
    team_average_handle_time = serializers.DurationField(read_only=True)


class UserPreferencesSerializer(serializers.ModelSerializer):
    """Serializer for user preferences"""
    
    class Meta:
        model = User
        fields = ['timezone', 'language']
    
    def update(self, instance, validated_data):
        """Update user preferences"""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save(update_fields=validated_data.keys())
        return instance