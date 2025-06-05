# apps/accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin configuration for custom User model"""
    
    list_display = [
        'username', 'email', 'first_name', 'last_name', 
        'role', 'agent_status', 'is_online', 'is_active'
    ]
    list_filter = [
        'role', 'agent_status', 'is_online', 'is_active', 
        'is_staff', 'date_joined'
    ]
    search_fields = ['username', 'first_name', 'last_name', 'email']
    ordering = ['username']
    
    # Fieldsets for viewing/editing users
    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        (_('Personal info'), {
            'fields': ('first_name', 'last_name', 'email')
        }),
        (_('Work info'), {
            'fields': ('role', 'extension', 'agent_number', 'agent_status')
        }),
        (_('Permissions'), {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
            ),
        }),
        (_('Important dates'), {
            'fields': ('last_login', 'date_joined')
        }),
        (_('Status'), {
            'fields': ('is_online',)
        }),
    )
    
    # Fieldsets for adding new users
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
        (_('Personal info'), {
            'fields': ('first_name', 'last_name')
        }),
        (_('Work info'), {
            'fields': ('role', 'extension', 'agent_number')
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff')
        }),
    )
    
    readonly_fields = ['date_joined', 'last_login']
    
    def get_readonly_fields(self, request, obj=None):
        """Make certain fields readonly for non-superusers"""
        readonly_fields = list(self.readonly_fields)
        
        if not request.user.is_superuser:
            readonly_fields.extend(['is_staff', 'is_superuser', 'groups', 'user_permissions'])
            
        return readonly_fields