from rest_framework import serializers
from apps.reference_data.models import (
    ReferenceDataType,
    ReferenceData,
    ReferenceDataHistory
)
from apps.tenants.models import Tenant
from django.core.exceptions import ValidationError
from django.core.cache import cache

class BaseModelSerializer(serializers.ModelSerializer):
    """
    Base serializer with common fields and functionality
    """
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    created_by = serializers.StringRelatedField(read_only=True)
    updated_by = serializers.StringRelatedField(read_only=True)

class ReferenceDataTypeSerializer(BaseModelSerializer):
    """
    Serializer for Reference Data Type model
    """
    class Meta:
        model = ReferenceDataType
        fields = [
            'name',
            'description',
            'is_tenant_specific',
            'is_system_managed',
            'created_at',
            'updated_at',
            'created_by',
            'updated_by'
        ]
        read_only_fields = [
            'is_system_managed',
            'created_at',
            'updated_at',
            'created_by',
            'updated_by'
        ]

    def validate_name(self, value):
        """Ensure name is lowercase and uses underscores"""
        if not value.islower() or ' ' in value:
            raise ValidationError("Name must be lowercase and use underscores instead of spaces")
        return value


class ReferenceDataSerializer(BaseModelSerializer):
    """
    Serializer for Reference Data model
    """
    data_type = serializers.SlugRelatedField(
        slug_field='name',
        queryset=ReferenceDataType.objects.all()
    )
    parent = serializers.SlugRelatedField(
        slug_field='code',
        queryset=ReferenceData.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = ReferenceData
        fields = [
            'id',
            'data_type',
            'code',
            'display_value',
            'description',
            'parent',
            'sort_order',
            'is_active',
            'metadata',
            'version',
            'created_at',
            'updated_at',
            'created_by',
            'updated_by'
        ]
        read_only_fields = [
            'id',
            'version',
            'created_at',
            'updated_at',
            'created_by',
            'updated_by'
        ]
        extra_kwargs = {
            'code': {
                'validators': []  # We'll handle validation in validate method
            }
        }

    def validate(self, data):
        """Validate the reference data entry"""
        tenant = self.context.get('tenant')
        data_type = data.get('data_type') or (self.instance.data_type if self.instance else None)
        code = data.get('code') or (self.instance.code if self.instance else None)

        # Check for duplicate code within the same tenant and data type
        if code and data_type and tenant:
            queryset = ReferenceData.objects.filter(
                tenant=tenant,
                data_type=data_type,
                code=code
            )
            if self.instance:
                queryset = queryset.exclude(pk=self.instance.pk)
            
            if queryset.exists():
                raise ValidationError({
                    'code': f'A reference data entry with this code already exists for type {data_type.name}'
                })

        return data


class ReferenceDataHistorySerializer(BaseModelSerializer):
    """
    Serializer for Reference Data History model
    """
    reference_data = serializers.PrimaryKeyRelatedField(
        queryset=ReferenceData.objects.all()
    )
    changed_by = serializers.StringRelatedField()
    previous_state = serializers.JSONField()

    class Meta:
        model = ReferenceDataHistory
        fields = [
            'id',
            'reference_data',
            'version',
            'change_reason',
            'changed_fields',
            'previous_state',
            'changed_at',
            'changed_by'
        ]
        read_only_fields = fields


class ReferenceDataBulkUpdateSerializer(serializers.Serializer):
    """
    Serializer for bulk operations on Reference Data
    """
    data_type = serializers.SlugRelatedField(
        slug_field='name',
        queryset=ReferenceDataType.objects.all()
    )
    entries = serializers.ListField(
        child=serializers.DictField(),
        allow_empty=False
    )
    delete_missing = serializers.BooleanField(default=False)

    def validate_entries(self, value):
        """Validate each entry in the bulk update"""
        for entry in value:
            if 'code' not in entry or not entry['code']:
                raise ValidationError("Each entry must have a 'code' field")
            if 'display_value' not in entry or not entry['display_value']:
                raise ValidationError("Each entry must have a 'display_value' field")
        return value

    def validate(self, data):
        """Validate the bulk update request"""
        tenant = self.context.get('tenant')
        data_type = data['data_type']

        # Check if data type belongs to tenant
        if data_type.is_tenant_specific and not tenant:
            raise ValidationError("This data type requires a tenant context")

        # Check for duplicate codes in the request
        codes = [entry['code'] for entry in data['entries']]
        if len(codes) != len(set(codes)):
            raise ValidationError("Duplicate codes found in the request")

        return data

    def create(self, validated_data):
        """Handle the bulk create/update operation"""
        tenant = self.context['tenant']
        request = self.context['request']
        data_type = validated_data['data_type']
        entries = validated_data['entries']
        delete_missing = validated_data['delete_missing']

        # Get existing entries for this type
        existing_entries = ReferenceData.objects.filter(
            tenant=tenant,
            data_type=data_type
        )
        existing_codes = set(existing_entries.values_list('code', flat=True))
        new_codes = {entry['code'] for entry in entries}

        results = {
            'created': 0,
            'updated': 0,
            'deleted': 0,
            'details': []
        }

        # Delete missing entries if requested
        if delete_missing:
            to_delete = existing_entries.exclude(code__in=new_codes)
            delete_count = to_delete.count()
            to_delete.delete()
            results['deleted'] = delete_count

        # Process each entry
        for entry_data in entries:
            code = entry_data.pop('code')
            entry_data['data_type'] = data_type
            entry_data['tenant'] = tenant

            # Try to get existing entry
            try:
                instance = ReferenceData.objects.get(
                    tenant=tenant,
                    data_type=data_type,
                    code=code
                )
                serializer = ReferenceDataSerializer(
                    instance,
                    data=entry_data,
                    partial=True,
                    context={'tenant': tenant}
                )
                action = 'updated'
            except ReferenceData.DoesNotExist:
                serializer = ReferenceDataSerializer(
                    data={**entry_data, 'code': code},
                    context={'tenant': tenant}
                )
                action = 'created'

            if serializer.is_valid():
                serializer.save(
                    created_by=request.user if action == 'created' else None,
                    updated_by=request.user
                )
                results[action] += 1
                results['details'].append({
                    'code': code,
                    'status': f'{action}_successfully',
                    'action': action
                })
            else:
                results['details'].append({
                    'code': code,
                    'status': 'failed',
                    'errors': serializer.errors,
                    'action': action
                })

        # Clear cache for this data type
        cache_key = f"ref_data_{tenant.id}_{data_type.name}"
        cache.delete(cache_key)

        return results