# apps/core/serializers.py
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from .models import (
    ReferenceData, AuditLog, Setting, Country, Language, Location
)


class ReferenceDataSerializer(serializers.ModelSerializer):
    """Serializer for Reference Data"""
    
    full_path = serializers.CharField(read_only=True)
    has_children = serializers.BooleanField(read_only=True)
    children = serializers.SerializerMethodField()
    parent_name = serializers.CharField(source='parent.name', read_only=True)
    
    class Meta:
        model = ReferenceData
        fields = [
            'id', 'category', 'code', 'name', 'parent', 'parent_name',
            'level', 'sort_order', 'description', 'metadata', 'full_path',
            'has_children', 'children', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['level', 'full_path', 'has_children', 'created_at', 'updated_at']
    
    def get_children(self, obj):
        """Get children if requested"""
        request = self.context.get('request')
        if request and request.query_params.get('include_children'):
            children = obj.children.filter(is_active=True).order_by('sort_order', 'name')
            return ReferenceDataSerializer(children, many=True, context=self.context).data
        return []
    
    def validate(self, data):
        """Validate reference data"""
        # Ensure parent is from same category if provided
        if data.get('parent') and data.get('category'):
            if data['parent'].category != data['category']:
                raise serializers.ValidationError(
                    _("Parent must be from the same category")
                )
        
        return data


class ReferenceDataSimpleSerializer(serializers.ModelSerializer):
    """Simplified serializer for Reference Data (for dropdowns, etc.)"""
    
    class Meta:
        model = ReferenceData
        fields = ['id', 'name', 'code', 'category']


class ReferenceDataTreeSerializer(serializers.ModelSerializer):
    """Serializer for Reference Data with tree structure"""
    
    children = serializers.SerializerMethodField()
    
    class Meta:
        model = ReferenceData
        fields = ['id', 'name', 'code', 'level', 'sort_order', 'children']
    
    def get_children(self, obj):
        """Get all children recursively"""
        children = obj.children.filter(is_active=True).order_by('sort_order', 'name')
        return ReferenceDataTreeSerializer(children, many=True).data


class CountrySerializer(serializers.ModelSerializer):
    """Serializer for Country"""
    
    class Meta:
        model = Country
        fields = ['id', 'name', 'code', 'code3', 'phone_code', 'is_active']


class LanguageSerializer(serializers.ModelSerializer):
    """Serializer for Language"""
    
    class Meta:
        model = Language
        fields = ['id', 'name', 'code', 'native_name', 'is_active']


class LocationSerializer(serializers.ModelSerializer):
    """Serializer for Location"""
    
    parent_name = serializers.CharField(source='parent.name', read_only=True)
    full_path = serializers.CharField(read_only=True)
    children = serializers.SerializerMethodField()
    
    class Meta:
        model = Location
        fields = [
            'id', 'name', 'location_type', 'parent', 'parent_name',
            'code', 'level', 'full_path', 'children', 'is_active'
        ]
        read_only_fields = ['level', 'full_path']
    
    def get_children(self, obj):
        """Get children locations if requested"""
        request = self.context.get('request')
        if request and request.query_params.get('include_children'):
            children = obj.children.filter(is_active=True).order_by('name')
            return LocationSerializer(children, many=True, context=self.context).data
        return []


class LocationSimpleSerializer(serializers.ModelSerializer):
    """Simple location serializer for dropdowns"""
    
    class Meta:
        model = Location
        fields = ['id', 'name', 'location_type', 'code']


class AuditLogSerializer(serializers.ModelSerializer):
    """Serializer for Audit Log"""
    
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    content_type_name = serializers.CharField(source='content_type.name', read_only=True)
    
    class Meta:
        model = AuditLog
        fields = [
            'id', 'user', 'user_name', 'action', 'content_type',
            'content_type_name', 'object_id', 'object_repr', 'changes',
            'ip_address', 'user_agent', 'additional_info', 'created_at'
        ]
        read_only_fields = ['created_at']


class SettingSerializer(serializers.ModelSerializer):
    """Serializer for Settings"""
    
    typed_value = serializers.SerializerMethodField()
    
    class Meta:
        model = Setting
        fields = [
            'id', 'key', 'value', 'typed_value', 'setting_type',
            'category', 'description', 'is_sensitive', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['typed_value', 'created_at', 'updated_at']
    
    def get_typed_value(self, obj):
        """Get the properly typed value"""
        if obj.is_sensitive:
            return "***HIDDEN***"
        return obj.get_value()
    
    def validate_value(self, value):
        """Validate value based on setting type"""
        setting_type = self.initial_data.get('setting_type', 'string')
        
        if setting_type == 'integer':
            try:
                int(value)
            except ValueError:
                raise serializers.ValidationError(_("Value must be a valid integer"))
        elif setting_type == 'float':
            try:
                float(value)
            except ValueError:
                raise serializers.ValidationError(_("Value must be a valid number"))
        elif setting_type == 'boolean':
            if value.lower() not in ['true', 'false', '1', '0', 'yes', 'no']:
                raise serializers.ValidationError(_("Value must be a valid boolean"))
        elif setting_type == 'json':
            try:
                import json
                json.loads(value)
            except json.JSONDecodeError:
                raise serializers.ValidationError(_("Value must be valid JSON"))
        
        return value


class ReferenceDataCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating Reference Data with validation"""
    
    class Meta:
        model = ReferenceData
        fields = [
            'category', 'code', 'name', 'parent', 'sort_order',
            'description', 'metadata'
        ]
    
    def validate_code(self, value):
        """Validate code uniqueness within category"""
        if value:
            category = self.initial_data.get('category')
            if category and ReferenceData.objects.filter(
                category=category,
                code=value,
                is_active=True
            ).exists():
                raise serializers.ValidationError(
                    _("Code already exists in this category")
                )
        return value
    
    def create(self, validated_data):
        """Create reference data with proper user tracking"""
        user = self.context['request'].user
        validated_data['created_by'] = user
        validated_data['updated_by'] = user
        return super().create(validated_data)


class CategoryOptionsSerializer(serializers.Serializer):
    """Serializer for getting category options (for form dropdowns)"""
    
    category = serializers.CharField()
    include_inactive = serializers.BooleanField(default=False)
    parent_id = serializers.IntegerField(required=False, allow_null=True)
    
    def validate_category(self, value):
        """Validate category exists"""
        if not ReferenceData.objects.filter(category=value).exists():
            raise serializers.ValidationError(_("Category does not exist"))
        return value


class BulkReferenceDataSerializer(serializers.Serializer):
    """Serializer for bulk operations on reference data"""
    
    ids = serializers.ListField(
        child=serializers.IntegerField(),
        min_length=1,
        max_length=100
    )
    action = serializers.ChoiceField(choices=[
        ('activate', 'Activate'),
        ('deactivate', 'Deactivate'),
        ('delete', 'Delete'),
        ('change_category', 'Change Category')
    ])
    new_category = serializers.CharField(required=False, allow_blank=True)
    
    def validate(self, data):
        """Validate bulk operation data"""
        if data['action'] == 'change_category' and not data.get('new_category'):
            raise serializers.ValidationError(
                _("New category is required for change_category action")
            )
        return data


# Utility serializers for common use cases
class LookupSerializer(serializers.Serializer):
    """Generic lookup serializer for ID/Name pairs"""
    id = serializers.IntegerField()
    name = serializers.CharField()


class OptionSerializer(serializers.Serializer):
    """Generic option serializer for dropdowns"""
    value = serializers.CharField()
    label = serializers.CharField()
    disabled = serializers.BooleanField(default=False)


class HierarchyNodeSerializer(serializers.Serializer):
    """Generic hierarchy node serializer"""
    id = serializers.IntegerField()
    name = serializers.CharField()
    level = serializers.IntegerField()
    parent_id = serializers.IntegerField(allow_null=True)
    children = serializers.ListField(child=serializers.DictField(), default=list)