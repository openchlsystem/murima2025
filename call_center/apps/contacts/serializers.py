# apps/contacts/serializers.py
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from .models import (
    Contact, ContactRole, ContactAddress, ContactPhone, 
    ContactRelationship, ContactMergeLog
)
from apps.core.serializers import ReferenceDataSerializer, CountrySerializer, LocationSerializer


class ContactPhoneSerializer(serializers.ModelSerializer):
    """Serializer for Contact Phone numbers"""
    
    class Meta:
        model = ContactPhone
        fields = [
            'id', 'phone_type', 'phone_number', 'is_primary',
            'is_verified', 'notes', 'created_at'
        ]
        read_only_fields = ['created_at']
    
    def validate_phone_number(self, value):
        """Validate phone number format"""
        if not value:
            raise serializers.ValidationError(_("Phone number is required"))
        
        # Remove all non-digit characters except +
        import re
        cleaned = re.sub(r'[^\d+]', '', str(value))
        
        if len(cleaned) < 7:
            raise serializers.ValidationError(_("Phone number too short"))
        
        return cleaned


class ContactAddressSerializer(serializers.ModelSerializer):
    """Serializer for Contact Addresses"""
    
    district = LocationSerializer(read_only=True)
    district_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    subcounty = LocationSerializer(read_only=True)
    subcounty_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    
    class Meta:
        model = ContactAddress
        fields = [
            'id', 'address_type', 'address_line_1', 'address_line_2',
            'district', 'district_id', 'subcounty', 'subcounty_id',
            'landmark', 'postal_code', 'is_primary', 'created_at'
        ]
        read_only_fields = ['created_at']


class ContactRelationshipSerializer(serializers.ModelSerializer):
    """Serializer for Contact Relationships"""
    
    contact_from = serializers.StringRelatedField(read_only=True)
    contact_to = serializers.StringRelatedField(read_only=True)
    contact_to_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = ContactRelationship
        fields = [
            'id', 'contact_from', 'contact_to', 'contact_to_id',
            'relationship_type', 'description', 'is_verified', 'created_at'
        ]
        read_only_fields = ['contact_from', 'created_at']
    
    def validate_contact_to_id(self, value):
        """Validate contact_to exists"""
        if not Contact.objects.filter(id=value, is_active=True).exists():
            raise serializers.ValidationError(_("Contact not found"))
        return value


class ContactRoleSerializer(serializers.ModelSerializer):
    """Serializer for Contact Roles in cases"""
    
    contact = serializers.StringRelatedField(read_only=True)
    contact_name = serializers.CharField(source='contact.full_name', read_only=True)
    contact_phone = serializers.CharField(source='contact.display_phone', read_only=True)
    relationship = ReferenceDataSerializer(read_only=True)
    relationship_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    
    class Meta:
        model = ContactRole
        fields = [
            'id', 'contact', 'contact_name', 'contact_phone', 'role',
            'is_primary', 'relationship', 'relationship_id', 'role_data',
            'created_at'
        ]
        read_only_fields = ['contact', 'created_at']


class ContactSerializer(serializers.ModelSerializer):
    """Main Contact serializer"""
    
    # Location fields
    country = CountrySerializer(read_only=True)
    country_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    region = LocationSerializer(read_only=True)
    region_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    district = LocationSerializer(read_only=True)
    district_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    county = LocationSerializer(read_only=True)
    county_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    subcounty = LocationSerializer(read_only=True)
    subcounty_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    parish = LocationSerializer(read_only=True)
    parish_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    village = LocationSerializer(read_only=True)
    village_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    
    # Reference data fields
    age_group = ReferenceDataSerializer(read_only=True)
    age_group_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    gender = ReferenceDataSerializer(read_only=True)
    gender_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    nationality = ReferenceDataSerializer(read_only=True)
    nationality_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    tribe = ReferenceDataSerializer(read_only=True)
    tribe_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    language = serializers.StringRelatedField(read_only=True)
    language_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    
    # Computed fields
    age_calculated = serializers.IntegerField(read_only=True)
    full_location = serializers.CharField(read_only=True)
    display_phone = serializers.CharField(read_only=True)
    has_complete_profile = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Contact
        fields = [
            'id', 'uuid', 'contact_type', 'full_name', 'first_name', 'last_name',
            'primary_phone', 'secondary_phone', 'email', 'date_of_birth', 'age',
            'age_calculated', 'age_group', 'age_group_id', 'gender', 'gender_id',
            'country', 'country_id', 'region', 'region_id', 'district', 'district_id',
            'county', 'county_id', 'subcounty', 'subcounty_id', 'parish', 'parish_id',
            'village', 'village_id', 'physical_address', 'residence', 'landmark',
            'national_id', 'national_id_type', 'nationality', 'nationality_id',
            'tribe', 'tribe_id', 'language', 'language_id', 'additional_info',
            'full_location', 'display_phone', 'has_complete_profile',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'uuid', 'age_calculated', 'full_location', 'display_phone',
            'has_complete_profile', 'created_at', 'updated_at'
        ]
    
    def validate_email(self, value):
        """Validate email uniqueness if provided"""
        if value:
            # Check for duplicates, excluding current instance
            queryset = Contact.objects.filter(email__iexact=value, is_active=True)
            if self.instance:
                queryset = queryset.exclude(id=self.instance.id)
            
            if queryset.exists():
                raise serializers.ValidationError(_("Contact with this email already exists"))
        
        return value
    
    def validate_primary_phone(self, value):
        """Validate primary phone"""
        if value:
            # Clean phone number
            import re
            cleaned = re.sub(r'[^\d+]', '', str(value))
            
            if len(cleaned) < 7:
                raise serializers.ValidationError(_("Phone number too short"))
            
            return cleaned
        return value
    
    def validate(self, data):
        """Cross-field validation"""
        # Ensure at least one contact method is provided
        primary_phone = data.get('primary_phone') or (self.instance.primary_phone if self.instance else None)
        email = data.get('email') or (self.instance.email if self.instance else None)
        physical_address = data.get('physical_address') or (self.instance.physical_address if self.instance else None)
        
        if not any([primary_phone, email, physical_address]):
            raise serializers.ValidationError(
                _("At least one contact method (phone, email, or address) is required")
            )
        
        # Validate age vs date_of_birth consistency
        age = data.get('age')
        dob = data.get('date_of_birth')
        if age and dob:
            from django.utils import timezone
            calculated_age = timezone.now().date().year - dob.year
            if abs(calculated_age - age) > 1:
                raise serializers.ValidationError(
                    _("Age doesn't match date of birth")
                )
        
        return data


class ContactDetailSerializer(ContactSerializer):
    """Detailed Contact serializer with related data"""
    
    phone_numbers = ContactPhoneSerializer(many=True, read_only=True)
    addresses = ContactAddressSerializer(many=True, read_only=True)
    relationships_from = ContactRelationshipSerializer(many=True, read_only=True)
    relationships_to = ContactRelationshipSerializer(many=True, read_only=True)
    
    class Meta(ContactSerializer.Meta):
        fields = ContactSerializer.Meta.fields + [
            'phone_numbers', 'addresses', 'relationships_from', 'relationships_to'
        ]


class ContactCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating contacts with additional validation"""
    
    # Optional related data
    phone_numbers = ContactPhoneSerializer(many=True, required=False)
    addresses = ContactAddressSerializer(many=True, required=False)
    
    class Meta:
        model = Contact
        fields = [
            'contact_type', 'full_name', 'first_name', 'last_name',
            'primary_phone', 'secondary_phone', 'email', 'date_of_birth', 'age',
            'age_group_id', 'gender_id', 'country_id', 'region_id', 'district_id',
            'county_id', 'subcounty_id', 'parish_id', 'village_id',
            'physical_address', 'residence', 'landmark', 'national_id',
            'national_id_type', 'nationality_id', 'tribe_id', 'language_id',
            'additional_info', 'phone_numbers', 'addresses'
        ]
    
    def create(self, validated_data):
        """Create contact with related data"""
        phone_numbers_data = validated_data.pop('phone_numbers', [])
        addresses_data = validated_data.pop('addresses', [])
        
        # Create the contact
        contact = Contact.objects.create(**validated_data)
        
        # Create phone numbers
        for phone_data in phone_numbers_data:
            ContactPhone.objects.create(contact=contact, **phone_data)
        
        # Create addresses
        for address_data in addresses_data:
            ContactAddress.objects.create(contact=contact, **address_data)
        
        return contact
    
    def validate_full_name(self, value):
        """Validate full name"""
        if not value or not value.strip():
            raise serializers.ValidationError(_("Full name is required"))
        return value.strip()


class ContactSimpleSerializer(serializers.ModelSerializer):
    """Simple contact serializer for dropdowns and references"""
    
    display_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Contact
        fields = ['id', 'full_name', 'display_name', 'primary_phone', 'email']
    
    def get_display_name(self, obj):
        """Get display name with phone"""
        name = obj.full_name or f"{obj.first_name} {obj.last_name}".strip()
        phone = obj.display_phone
        if phone:
            return f"{name} ({phone})"
        return name


class ContactSearchSerializer(serializers.Serializer):
    """Serializer for contact search parameters"""
    
    query = serializers.CharField(required=False, allow_blank=True)
    contact_type = serializers.CharField(required=False, allow_blank=True)
    gender = serializers.CharField(required=False, allow_blank=True)
    age_group = serializers.CharField(required=False, allow_blank=True)
    district = serializers.IntegerField(required=False, allow_null=True)
    subcounty = serializers.IntegerField(required=False, allow_null=True)
    has_phone = serializers.BooleanField(required=False)
    has_email = serializers.BooleanField(required=False)
    created_after = serializers.DateTimeField(required=False)
    created_before = serializers.DateTimeField(required=False)
    page = serializers.IntegerField(default=1, min_value=1)
    page_size = serializers.IntegerField(default=20, min_value=1, max_value=100)


class ContactMergeSerializer(serializers.Serializer):
    """Serializer for merging contacts"""
    
    primary_contact_id = serializers.IntegerField()
    secondary_contact_id = serializers.IntegerField()
    merge_reason = serializers.CharField(max_length=500)
    keep_secondary_data = serializers.BooleanField(default=False)
    
    def validate_primary_contact_id(self, value):
        """Validate primary contact exists"""
        if not Contact.objects.filter(id=value, is_active=True).exists():
            raise serializers.ValidationError(_("Primary contact not found"))
        return value
    
    def validate_secondary_contact_id(self, value):
        """Validate secondary contact exists"""
        if not Contact.objects.filter(id=value, is_active=True).exists():
            raise serializers.ValidationError(_("Secondary contact not found"))
        return value
    
    def validate(self, data):
        """Validate merge data"""
        if data['primary_contact_id'] == data['secondary_contact_id']:
            raise serializers.ValidationError(_("Cannot merge contact with itself"))
        return data


class ContactMergeLogSerializer(serializers.ModelSerializer):
    """Serializer for Contact Merge Log"""
    
    primary_contact = ContactSimpleSerializer(read_only=True)
    merged_by = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = ContactMergeLog
        fields = [
            'id', 'primary_contact', 'merged_contact_id', 'merged_contact_name',
            'merged_by', 'merge_reason', 'merged_data', 'created_at'
        ]
        read_only_fields = ['created_at']


class ContactDuplicatesSerializer(serializers.Serializer):
    """Serializer for finding duplicate contacts"""
    
    contact_id = serializers.IntegerField()
    similarity_threshold = serializers.FloatField(default=0.8, min_value=0.0, max_value=1.0)
    max_results = serializers.IntegerField(default=10, min_value=1, max_value=50)


class ContactStatsSerializer(serializers.Serializer):
    """Serializer for contact statistics"""
    
    date_from = serializers.DateField(required=False)
    date_to = serializers.DateField(required=False)
    group_by = serializers.ChoiceField(
        choices=['gender', 'age_group', 'district', 'contact_type'],
        required=False
    )


class BulkContactOperationSerializer(serializers.Serializer):
    """Serializer for bulk contact operations"""
    
    contact_ids = serializers.ListField(
        child=serializers.IntegerField(),
        min_length=1,
        max_length=100
    )
    operation = serializers.ChoiceField(choices=[
        ('activate', 'Activate'),
        ('deactivate', 'Deactivate'),
        ('delete', 'Delete'),
        ('export', 'Export'),
        ('tag', 'Add Tag')
    ])
    tag = serializers.CharField(required=False, allow_blank=True)
    
    def validate(self, data):
        """Validate bulk operation"""
        if data['operation'] == 'tag' and not data.get('tag'):
            raise serializers.ValidationError(_("Tag is required for tag operation"))
        return data


class ContactImportSerializer(serializers.Serializer):
    """Serializer for importing contacts from file"""
    
    file = serializers.FileField()
    file_type = serializers.ChoiceField(choices=[
        ('csv', 'CSV'),
        ('excel', 'Excel'),
        ('json', 'JSON')
    ])
    skip_duplicates = serializers.BooleanField(default=True)
    update_existing = serializers.BooleanField(default=False)
    
    def validate_file(self, value):
        """Validate uploaded file"""
        # Check file size (max 10MB)
        if value.size > 10 * 1024 * 1024:
            raise serializers.ValidationError(_("File size too large. Maximum 10MB allowed."))
        
        # Check file type
        file_type = self.initial_data.get('file_type')
        allowed_extensions = {
            'csv': ['.csv'],
            'excel': ['.xlsx', '.xls'],
            'json': ['.json']
        }
        
        if file_type and file_type in allowed_extensions:
            import os
            file_ext = os.path.splitext(value.name)[1].lower()
            if file_ext not in allowed_extensions[file_type]:
                raise serializers.ValidationError(
                    _("File extension doesn't match selected file type")
                )
        
        return value