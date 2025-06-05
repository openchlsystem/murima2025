# apps/calls/admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import (
    Call, CallEvent, CallDisposition, CallQualityAssessment, 
    CallNote, CallTransfer, CallCallback
)


class CallEventInline(admin.TabularInline):
    """Inline for call events"""
    model = CallEvent
    extra = 0
    readonly_fields = ('created_at',)
    fields = ('event_type', 'event_time', 'description', 'agent')


class CallNoteInline(admin.TabularInline):
    """Inline for call notes"""
    model = CallNote
    extra = 0
    readonly_fields = ('created_at', 'author')
    fields = ('note_type', 'title', 'content', 'is_important', 'author')


@admin.register(Call)
class CallAdmin(admin.ModelAdmin):
    """Admin interface for Call model"""
    
    list_display = [
        'unique_id_short', 'call_direction', 'caller_number', 'called_number',
        'agent', 'call_status', 'start_time', 'duration_display'
    ]
    
    list_filter = [
        'call_direction', 'call_status', 'call_date', 'agent'
    ]
    
    search_fields = [
        'unique_id', 'caller_number', 'called_number', 
        'agent__username', 'agent__first_name', 'agent__last_name'
    ]
    
    readonly_fields = [
        'uuid', 'call_date', 'call_hour', 'call_day_of_week', 'duration_display'
    ]
    
    fieldsets = (
        (_('Call Information'), {
            'fields': (
                'uuid', 'unique_id',
                ('caller_number', 'caller_name'),
                ('called_number', 'call_direction'),
            )
        }),
        (_('Associations'), {
            'fields': (
                'contact', 'agent', 'campaign', 'case'
            )
        }),
        (_('Timing'), {
            'fields': (
                ('start_time', 'answer_time', 'end_time'),
                'duration_display',
                ('call_date', 'call_hour')
            )
        }),
        (_('Status'), {
            'fields': (
                ('call_status', 'hangup_reason'),
            )
        }),
        (_('Technical'), {
            'fields': (
                ('trunk', 'channel'),
                ('context', 'extension'),
                'recording_file'
            ),
            'classes': ('collapse',)
        }),
        (_('Migration Data'), {
            'fields': (
                'legacy_chan_id',
                'migration_notes',
                'migration_verified'
            ),
            'classes': ('collapse',)
        })
    )
    
    inlines = [CallEventInline, CallNoteInline]
    
    def get_queryset(self, request):
        """Optimize queryset with select_related"""
        return super().get_queryset(request).select_related(
            'contact', 'agent', 'campaign', 'case'
        )
    
    def unique_id_short(self, obj):
        """Display shortened unique ID"""
        if len(obj.unique_id) > 20:
            return obj.unique_id[:20] + '...'
        return obj.unique_id
    unique_id_short.short_description = _('Unique ID')
    
    def duration_display(self, obj):
        """Display formatted call duration"""
        if obj.total_duration:
            total_seconds = int(obj.total_duration.total_seconds())
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            
            if hours > 0:
                return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            else:
                return f"{minutes:02d}:{seconds:02d}"
        return '-'
    duration_display.short_description = _('Duration')


@admin.register(CallEvent)
class CallEventAdmin(admin.ModelAdmin):
    """Admin interface for CallEvent model"""
    
    list_display = ['call_short', 'event_type', 'event_time', 'agent']
    list_filter = ['event_type', 'event_time']
    search_fields = ['call__unique_id', 'description']
    readonly_fields = ['created_at']
    
    def call_short(self, obj):
        if len(obj.call.unique_id) > 15:
            return obj.call.unique_id[:15] + '...'
        return obj.call.unique_id
    call_short.short_description = _('Call')


@admin.register(CallDisposition)
class CallDispositionAdmin(admin.ModelAdmin):
    """Admin interface for CallDisposition model"""
    
    list_display = [
        'call_short', 'disposition', 'case_created', 'follow_up_required', 'created_at'
    ]
    list_filter = [
        'disposition', 'case_created', 'follow_up_required', 'created_at'
    ]
    search_fields = ['call__unique_id', 'notes']
    readonly_fields = ['created_at']
    
    def call_short(self, obj):
        if len(obj.call.unique_id) > 15:
            return obj.call.unique_id[:15] + '...'
        return obj.call.unique_id
    call_short.short_description = _('Call')


@admin.register(CallQualityAssessment)
class CallQualityAssessmentAdmin(admin.ModelAdmin):
    """Admin interface for CallQualityAssessment model"""
    
    list_display = [
        'call_short', 'assessor', 'overall_score', 'created_at'
    ]
    list_filter = ['assessor', 'created_at']
    search_fields = ['call__unique_id', 'comments']
    readonly_fields = ['created_at']
    
    def call_short(self, obj):
        if len(obj.call.unique_id) > 15:
            return obj.call.unique_id[:15] + '...'
        return obj.call.unique_id
    call_short.short_description = _('Call')


@admin.register(CallNote)
class CallNoteAdmin(admin.ModelAdmin):
    """Admin interface for CallNote model"""
    
    list_display = [
        'call_short', 'note_type', 'title_short', 'author', 'is_important', 'created_at'
    ]
    list_filter = ['note_type', 'is_important', 'created_at']
    search_fields = ['call__unique_id', 'title', 'content']
    readonly_fields = ['created_at']
    
    def call_short(self, obj):
        if len(obj.call.unique_id) > 15:
            return obj.call.unique_id[:15] + '...'
        return obj.call.unique_id
    call_short.short_description = _('Call')
    
    def title_short(self, obj):
        display_text = obj.title if obj.title else obj.content
        if len(display_text) > 30:
            return display_text[:30] + '...'
        return display_text
    title_short.short_description = _('Title/Content')


@admin.register(CallTransfer)
class CallTransferAdmin(admin.ModelAdmin):
    """Admin interface for CallTransfer model"""
    
    list_display = [
        'call_short', 'transfer_type', 'from_agent', 'to_destination', 'success', 'transfer_time'
    ]
    list_filter = ['transfer_type', 'transfer_reason', 'success']
    search_fields = ['call__unique_id', 'from_agent__username', 'to_agent__username']
    readonly_fields = ['created_at']
    
    def call_short(self, obj):
        if len(obj.call.unique_id) > 15:
            return obj.call.unique_id[:15] + '...'
        return obj.call.unique_id
    call_short.short_description = _('Call')
    
    def to_destination(self, obj):
        if obj.to_agent:
            return str(obj.to_agent)
        elif obj.to_queue:
            return f"Queue: {obj.to_queue}"
        return 'Unknown'
    to_destination.short_description = _('To')


@admin.register(CallCallback)
class CallCallbackAdmin(admin.ModelAdmin):
    """Admin interface for CallCallback model"""
    
    list_display = [
        'original_call_short', 'contact', 'callback_number', 
        'scheduled_time', 'status', 'assigned_to'
    ]
    list_filter = ['status', 'scheduled_time', 'assigned_to']
    search_fields = ['original_call__unique_id', 'contact__full_name', 'callback_number']
    readonly_fields = ['created_at']
    
    def original_call_short(self, obj):
        if len(obj.original_call.unique_id) > 15:
            return obj.original_call.unique_id[:15] + '...'
        return obj.original_call.unique_id
    original_call_short.short_description = _('Original Call')