# apps/security/admin.py
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import SecurityEvent


@admin.register(SecurityEvent)
class SecurityEventAdmin(admin.ModelAdmin):
    list_display = [
        'event_type', 'user', 'severity', 'ip_address', 'created_at'
    ]
    list_filter = ['event_type', 'severity', 'created_at']
    search_fields = ['user__username', 'ip_address', 'description']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    fieldsets = (
        (_('Event Information'), {
            'fields': ('user', 'event_type', 'severity')
        }),
        (_('Details'), {
            'fields': ('ip_address', 'user_agent', 'description')
        }),
        (_('Additional Data'), {
            'fields': ('additional_data',),
            'classes': ('collapse',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False