from django.contrib import admin

# Register your models here.
# apps/core/admin.py
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import ReferenceData, AuditLog, Setting, Country, Language, Location


@admin.register(ReferenceData)
class ReferenceDataAdmin(admin.ModelAdmin):
    list_display = ['category', 'name', 'code', 'parent', 'level', 'sort_order', 'is_active']
    list_filter = ['category', 'level', 'is_active']
    search_fields = ['name', 'code', 'category']
    ordering = ['category', 'level', 'sort_order', 'name']
    
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('category', 'code', 'name', 'parent')
        }),
        (_('Hierarchy'), {
            'fields': ('level', 'sort_order')
        }),
        (_('Details'), {
            'fields': ('description', 'metadata')
        }),
        (_('Status'), {
            'fields': ('is_active',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('parent')


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'object_repr', 'created_at', 'ip_address']
    list_filter = ['action', 'created_at', 'content_type']
    search_fields = ['user__username', 'object_repr', 'ip_address']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'content_type')
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    list_display = ['key', 'category', 'setting_type', 'is_sensitive', 'is_active']
    list_filter = ['category', 'setting_type', 'is_sensitive', 'is_active']
    search_fields = ['key', 'description']
    ordering = ['category', 'key']
    
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('key', 'category', 'setting_type')
        }),
        (_('Value'), {
            'fields': ('value',)
        }),
        (_('Details'), {
            'fields': ('description', 'is_sensitive')
        }),
        (_('Status'), {
            'fields': ('is_active',)
        }),
    )


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'code3', 'phone_code', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'code', 'code3']
    ordering = ['name']


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'native_name', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'code', 'native_name']
    ordering = ['name']


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'location_type', 'parent', 'level', 'is_active']
    list_filter = ['location_type', 'level', 'is_active']
    search_fields = ['name', 'code']
    ordering = ['level', 'name']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('parent')