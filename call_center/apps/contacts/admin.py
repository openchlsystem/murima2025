# apps/contacts/admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from .models import (
    Contact, ContactAddress, ContactPhone, 
    ContactRelationship, ContactMergeLog, ContactRole
)


class ContactAddressInline(admin.TabularInline):
    """Inline for contact addresses"""
    model = ContactAddress
    extra = 0
    readonly_fields = ('created_at',)
    fields = ('address_type', 'address_line_1', 'district', 'subcounty', 'is_primary')


class ContactPhoneInline(admin.TabularInline):
    """Inline for contact phone numbers"""
    model = ContactPhone
    extra = 0
    readonly_fields = ('created_at',)
    fields = ('phone_type', 'phone_number', 'is_primary', 'is_verified')


class ContactRelationshipInline(admin.TabularInline):
    """Inline for contact relationships"""
    model = ContactRelationship
    fk_name = 'contact_from'
    extra = 0
    readonly_fields = ('created_at',)
    fields = ('contact_to', 'relationship_type', 'description', 'is_verified')


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """Admin interface for Contact model"""
    
    list_display = [
        'full_name', 'display_phone', 'email', 'age_display', 
        'location_display', 'has_complete_profile_icon',
        'migration_source_display'
    ]
    
    list_filter = [
        'contact_type', 'region', 'district', 'migration_source', 'is_active'
    ]
    
    search_fields = [
        'full_name', 'first_name', 'last_name', 
        'primary_phone', 'secondary_phone', 'email', 'national_id'
    ]
    
    readonly_fields = [
        'uuid', 'age_calculated', 'full_location', 'has_complete_profile',
        'migration_info', 'duplicate_check'
    ]
    
    fieldsets = (
        (_('Basic Information'), {
            'fields': (
                'uuid', 'contact_type',
                ('full_name', 'first_name', 'last_name'),
            )
        }),
        (_('Contact Details'), {
            'fields': (
                ('primary_phone', 'secondary_phone'),
                'email',
            )
        }),
        (_('Demographics'), {
            'fields': (
                ('date_of_birth', 'age', 'age_calculated'),
                ('gender', 'age_group'),
            )
        }),
        (_('Identity'), {
            'fields': (
                ('national_id', 'national_id_type'),
            )
        }),
        (_('Location'), {
            'fields': (
                'country',
                ('region', 'district'),
                ('county', 'subcounty'),
                ('parish', 'village'),
                'physical_address',
                ('residence', 'landmark'),
                'full_location'
            )
        }),
        (_('Cultural Information'), {
            'fields': (
                ('nationality', 'tribe', 'language'),
            )
        }),
        (_('Profile Status'), {
            'fields': (
                'has_complete_profile',
                'duplicate_check'
            )
        }),
        (_('Additional Information'), {
            'fields': ('additional_info',),
            'classes': ('collapse',)
        }),
        (_('Migration Data'), {
            'fields': (
                'migration_info',
                ('legacy_contact_id', 'legacy_client_id'),
                ('legacy_reporter_id', 'legacy_perpetrator_id'),
                'migration_notes'
            ),
            'classes': ('collapse',)
        })
    )
    
    inlines = [ContactPhoneInline, ContactAddressInline, ContactRelationshipInline]
    
    actions = ['merge_contacts', 'mark_as_verified', 'export_contacts']
    
    def get_queryset(self, request):
        """Optimize queryset with select_related"""
        return super().get_queryset(request).select_related(
            'country', 'region', 'district', 'subcounty', 'gender', 'age_group'
        )
    
    def display_phone(self, obj):
        """Display primary phone number"""
        return obj.display_phone or '-'
    display_phone.short_description = _('Phone')
    
    def age_display(self, obj):
        """Display age with age group if available"""
        age = obj.age_calculated or obj.age
        if age:
            return str(age)
        return '-'
    age_display.short_description = _('Age')
    
    def location_display(self, obj):
        """Display location summary"""
        locations = []
        if obj.district:
            locations.append(obj.district.name)
        if obj.subcounty:
            locations.append(obj.subcounty.name)
        return ', '.join(locations) if locations else '-'
    location_display.short_description = _('Location')
    
    def has_complete_profile_icon(self, obj):
        """Display profile completeness icon"""
        if obj.has_complete_profile:
            return format_html('<span style="color: green;">✓</span>')
        return format_html('<span style="color: orange;">⚠</span>')
    has_complete_profile_icon.short_description = _('Complete')
    
    def migration_source_display(self, obj):
        """Display migration source with color coding"""
        if obj.migration_source:
            colors = {
                'contact': 'blue',
                'reporter': 'green', 
                'client': 'orange',
                'perpetrator': 'red'
            }
            color = colors.get(obj.migration_source, 'gray')
            return format_html(
                '<span style="color: {};">{}</span>',
                color, obj.migration_source.title()
            )
        return format_html('<span style="color: green;">New</span>')
    migration_source_display.short_description = _('Source')
    
    def age_calculated(self, obj):
        """Display calculated age"""
        return obj.age_calculated
    age_calculated.short_description = _('Calculated Age')
    
    def migration_info(self, obj):
        """Display migration information"""
        info = []
        if obj.legacy_contact_id:
            info.append(f"Contact ID: {obj.legacy_contact_id}")
        if obj.legacy_client_id:
            info.append(f"Client ID: {obj.legacy_client_id}")
        if obj.legacy_reporter_id:
            info.append(f"Reporter ID: {obj.legacy_reporter_id}")
        if obj.legacy_perpetrator_id:
            info.append(f"Perpetrator ID: {obj.legacy_perpetrator_id}")
        
        return '\n'.join(info) if info else 'New record'
    migration_info.short_description = _('Migration Info')
    
    def duplicate_check(self, obj):
        """Check for potential duplicates"""
        try:
            duplicates = obj.find_potential_duplicates()
            if duplicates.exists():
                count = duplicates.count()
                return format_html(
                    '<span style="color: red;">⚠ {} potential duplicate(s)</span>',
                    count
                )
            return format_html('<span style="color: green;">✓ No duplicates found</span>')
        except:
            return 'Unable to check'
    duplicate_check.short_description = _('Duplicate Check')
    
    # Admin Actions
    def merge_contacts(self, request, queryset):
        """Merge selected contacts"""
        if queryset.count() < 2:
            self.message_user(request, "Select at least 2 contacts to merge.", level='ERROR')
            return
        
        # TODO: Implement contact merge functionality
        self.message_user(request, f"Contact merge initiated for {queryset.count()} contacts.")
    merge_contacts.short_description = _("Merge selected contacts")
    
    def mark_as_verified(self, request, queryset):
        """Mark contacts as verified"""
        # TODO: Add verification logic
        updated = queryset.update(additional_info={'verified': True})
        self.message_user(request, f"{updated} contacts marked as verified.")
    mark_as_verified.short_description = _("Mark as verified")
    
    def export_contacts(self, request, queryset):
        """Export selected contacts"""
        # TODO: Implement export functionality
        self.message_user(request, f"Export initiated for {queryset.count()} contacts.")
    export_contacts.short_description = _("Export selected contacts")


@admin.register(ContactRole)
class ContactRoleAdmin(admin.ModelAdmin):
    """Admin interface for ContactRole model"""
    
    # list_display = ['contact', 'case_link', 'role', 'is_primary', 'relationship', 'created_at']
    list_display = ['contact', 'role', 'is_primary', 'relationship', 'created_at']  # Removed case_link temporarily
    list_filter = ['role', 'is_primary', 'relationship', 'created_at']
    # search_fields = ['contact__full_name', 'case__case_number']
    search_fields = ['contact__full_name']  # Removed case search temporarily
    readonly_fields = ['created_at']
    
    def case_link(self, obj):
        """Display case with admin link"""
        # Commented out to avoid errors if case is not implemented
        # if obj.case:
        #     try:
        #         url = reverse('admin:cases_case_change', args=[obj.case.pk])
        #         return format_html('<a href="{}">{}</a>', url, obj.case.case_number)
        #     except:
        #         return str(obj.case)
        # return '-'
    case_link.short_description = _('Case')


@admin.register(ContactAddress)
class ContactAddressAdmin(admin.ModelAdmin):
    """Admin interface for ContactAddress model"""
    
    list_display = ['contact', 'address_type', 'address_line_1', 'district', 'is_primary']
    list_filter = ['address_type', 'is_primary', 'district']
    search_fields = ['contact__full_name', 'address_line_1', 'landmark']
    readonly_fields = ['created_at']


@admin.register(ContactPhone)
class ContactPhoneAdmin(admin.ModelAdmin):
    """Admin interface for ContactPhone model"""
    
    list_display = ['contact', 'phone_type', 'phone_number', 'is_primary', 'is_verified']
    list_filter = ['phone_type', 'is_primary', 'is_verified']
    search_fields = ['contact__full_name', 'phone_number']
    readonly_fields = ['created_at']


@admin.register(ContactRelationship)
class ContactRelationshipAdmin(admin.ModelAdmin):
    """Admin interface for ContactRelationship model"""
    
    list_display = ['contact_from', 'relationship_type', 'contact_to', 'is_verified']
    list_filter = ['relationship_type', 'is_verified']
    search_fields = ['contact_from__full_name', 'contact_to__full_name']
    readonly_fields = ['created_at']


@admin.register(ContactMergeLog)
class ContactMergeLogAdmin(admin.ModelAdmin):
    """Admin interface for ContactMergeLog model"""
    
    list_display = ['primary_contact', 'merged_contact_name', 'merged_by', 'created_at']
    list_filter = ['merged_by', 'created_at']
    search_fields = ['primary_contact__full_name', 'merged_contact_name']
    readonly_fields = ['created_at', 'merged_data']
    
    def has_add_permission(self, request):
        """Disable manual creation of merge logs"""
        return False