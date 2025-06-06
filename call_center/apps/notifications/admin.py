# apps/notifications/admin.py
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Notification, NotificationTemplate, NotificationPreference


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'recipient', 'notification_type', 'priority', 
        'is_read', 'email_sent', 'created_at'
    ]
    list_filter = [
        'notification_type', 'priority', 'is_read', 'email_sent', 'created_at'
    ]
    search_fields = ['title', 'message', 'recipient__username', 'sender__username']
    readonly_fields = ['created_at', 'updated_at', 'read_at', 'email_sent_at']
    ordering = ['-created_at']
    
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('recipient', 'sender', 'notification_type', 'priority')
        }),
        (_('Content'), {
            'fields': ('title', 'message')
        }),
        (_('Related Object'), {
            'fields': ('content_type', 'object_id'),
            'classes': ('collapse',)
        }),
        (_('Status'), {
            'fields': ('is_read', 'read_at', 'email_sent', 'email_sent_at')
        }),
        (_('Additional Data'), {
            'fields': ('data', 'expires_at'),
            'classes': ('collapse',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('recipient', 'sender', 'content_type')
    
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        """Mark selected notifications as read"""
        from django.utils import timezone
        updated = queryset.filter(is_read=False).update(
            is_read=True,
            read_at=timezone.now()
        )
        self.message_user(request, f'{updated} notifications marked as read.')
    mark_as_read.short_description = _('Mark selected notifications as read')
    
    def mark_as_unread(self, request, queryset):
        """Mark selected notifications as unread"""
        updated = queryset.filter(is_read=True).update(
            is_read=False,
            read_at=None
        )
        self.message_user(request, f'{updated} notifications marked as unread.')
    mark_as_unread.short_description = _('Mark selected notifications as unread')


@admin.register(NotificationTemplate)
class NotificationTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'notification_type', 'default_priority', 'is_active']
    list_filter = ['notification_type', 'default_priority', 'is_active']
    search_fields = ['name', 'title_template', 'message_template']
    
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('name', 'notification_type', 'default_priority', 'is_active')
        }),
        (_('Templates'), {
            'fields': ('title_template', 'message_template', 'email_template')
        }),
    )


@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'email_enabled', 'browser_enabled', 'sms_enabled'
    ]
    list_filter = ['email_enabled', 'browser_enabled', 'sms_enabled']
    search_fields = ['user__username', 'user__email']
    
    fieldsets = (
        (_('User'), {
            'fields': ('user',)
        }),
        (_('Email Preferences'), {
            'fields': ('email_enabled', 'email_digest')
        }),
        (_('Browser Preferences'), {
            'fields': ('browser_enabled', 'sound_enabled')
        }),
        (_('SMS Preferences'), {
            'fields': ('sms_enabled', 'sms_urgent_only')
        }),
        (_('Advanced'), {
            'fields': ('notification_types',),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')