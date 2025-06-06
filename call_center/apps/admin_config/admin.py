# apps/admin_config/admin.py
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import AdminConfiguration


@admin.register(AdminConfiguration)
class AdminConfigurationAdmin(admin.ModelAdmin):
    list_display = ['key', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['key', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        (_('Configuration'), {
            'fields': ('key', 'value', 'is_active')
        }),
        (_('Details'), {
            'fields': ('description',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )