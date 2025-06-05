# apps/tenant/admin.py
from django.contrib import admin
from django_tenants.admin import TenantAdminMixin
from django.utils.translation import gettext_lazy as _
from .models import Tenant, Domain, TenantSetting


class TenantSettingInline(admin.TabularInline):
    model = TenantSetting
    extra = 0
    fields = ['key', 'value', 'value_type', 'description']


@admin.register(Tenant)
class TenantAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = [
        'name', 'schema_name', 'is_active', 'is_trial', 
        'subscription_plan', 'created_at'
    ]
    list_filter = [
        'is_active', 'is_trial', 'subscription_plan', 'created_at'
    ]
    search_fields = ['name', 'schema_name', 'contact_email', 'contact_person']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [TenantSettingInline]
    
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('schema_name', 'name', 'description')
        }),
        (_('Contact Information'), {
            'fields': (
                'contact_person', 'contact_email', 'contact_phone'
            )
        }),
        (_('Address'), {
            'fields': (
                'address_line1', 'address_line2', 'city', 
                'state', 'postal_code', 'country'
            ),
            'classes': ('collapse',)
        }),
        (_('Configuration'), {
            'fields': ('timezone', 'language', 'currency')
        }),
        (_('Subscription'), {
            'fields': (
                'subscription_plan', 'max_users', 'max_contacts', 
                'max_campaigns', 'storage_limit_gb'
            )
        }),
        (_('Billing'), {
            'fields': ('billing_contact', 'billing_email'),
            'classes': ('collapse',)
        }),
        (_('Status'), {
            'fields': (
                'is_active', 'is_trial', 'trial_end_date'
            )
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ['domain', 'tenant', 'is_primary']
    list_filter = ['is_primary']
    search_fields = ['domain', 'tenant__name']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('tenant')


@admin.register(TenantSetting)
class TenantSettingAdmin(admin.ModelAdmin):
    list_display = ['tenant', 'key', 'value_type', 'updated_at']
    list_filter = ['value_type', 'tenant']
    search_fields = ['tenant__name', 'key', 'description']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('tenant')