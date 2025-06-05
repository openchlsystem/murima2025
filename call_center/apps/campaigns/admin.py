# apps/campaigns/admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .models import Campaign, CampaignMember, CampaignContact


class CampaignMemberInline(admin.TabularInline):
    """Inline for campaign members"""
    model = CampaignMember
    extra = 0
    readonly_fields = ('assigned_date', 'calls_handled')
    fields = ('agent', 'role', 'is_active', 'assigned_date', 'calls_handled')


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    """Admin interface for Campaign model"""
    
    list_display = [
        'name', 'campaign_type', 'status_badge', 'queue_name', 
        'agent_count', 'is_current_display', 'created_at'
    ]
    
    list_filter = [
        'campaign_type', 'status', 'created_at',
        'start_date', 'end_date'
    ]
    
    search_fields = ['name', 'queue_name', 'description', 'caller_id']
    
    readonly_fields = [
        'uuid', 'is_current', 'progress_percentage', 'success_rate',
        'answer_rate', 'abandon_rate'
    ]
    
    fieldsets = (
        (_('Campaign Information'), {
            'fields': (
                'uuid', 'name', 'description',
                ('campaign_type', 'status'),
            )
        }),
        (_('Queue Configuration'), {
            'fields': (
                'queue_name', 'caller_id',
                ('ring_strategy', 'max_agents'),
                ('ring_timeout', 'wrapup_time')
            )
        }),
        (_('Schedule'), {
            'fields': (
                ('start_date', 'end_date'),
                'working_hours',
                'is_current'
            )
        }),
        (_('Targets & Performance'), {
            'fields': (
                ('target_contacts', 'contacts_attempted', 'contacts_reached'),
                ('progress_percentage', 'success_rate'),
            )
        }),
        (_('SLA Configuration'), {
            'fields': (
                ('sla_target_answer', 'sla_target_abandon'),
                'sla_compliance_rate'
            ),
            'classes': ('collapse',)
        }),
        (_('Outbound Settings'), {
            'fields': (
                ('retry_attempts', 'retry_interval'),
            ),
            'classes': ('collapse',)
        }),
        (_('Statistics'), {
            'fields': (
                ('total_calls', 'answered_calls', 'abandoned_calls'),
                ('avg_talk_time', 'avg_wait_time', 'avg_hold_time'),
                ('answer_rate', 'abandon_rate')
            ),
            'classes': ('collapse',)
        }),
        (_('Migration Data'), {
            'fields': ('legacy_campaign_id', 'legacy_data'),
            'classes': ('collapse',)
        })
    )
    
    inlines = [CampaignMemberInline]
    
    actions = ['activate_campaigns', 'pause_campaigns', 'update_statistics']
    
    def get_queryset(self, request):
        """Optimize queryset with select_related"""
        return super().get_queryset(request).select_related(
            'category', 'voice_prompt'
        ).prefetch_related('members')
    
    def status_badge(self, obj):
        """Display status with colored badge"""
        colors = {
            'active': 'green',
            'paused': 'orange',
            'completed': 'blue',
            'cancelled': 'red',
            'draft': 'gray',
            'scheduled': 'purple'
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 6px; '
            'border-radius: 3px; font-size: 11px;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = _('Status')
    
    def agent_count(self, obj):
        """Display agent count vs maximum"""
        current = obj.get_agent_count()
        maximum = obj.max_agents
        color = 'green' if current <= maximum else 'red'
        return format_html(
            '<span style="color: {};">{}/{}</span>',
            color, current, maximum
        )
    agent_count.short_description = _('Agents')
    
    def is_current_display(self, obj):
        """Display if campaign is currently running"""
        if obj.is_current:
            return format_html('<span style="color: green;">✓ Running</span>')
        elif obj.status == 'scheduled':
            return format_html('<span style="color: blue;">⏰ Scheduled</span>')
        else:
            return format_html('<span style="color: gray;">⏸ Not Running</span>')
    is_current_display.short_description = _('Current')
    
    # Admin Actions
    def activate_campaigns(self, request, queryset):
        """Activate selected campaigns"""
        now = timezone.now()
        activated = 0
        
        for campaign in queryset:
            if campaign.status in ['draft', 'paused', 'scheduled']:
                # Ensure dates are valid
                if campaign.start_date <= now <= campaign.end_date:
                    campaign.status = 'active'
                    campaign.save()
                    activated += 1
        
        self.message_user(request, f"{activated} campaigns activated.")
    activate_campaigns.short_description = _("Activate selected campaigns")
    
    def pause_campaigns(self, request, queryset):
        """Pause selected campaigns"""
        updated = queryset.filter(status='active').update(status='paused')
        self.message_user(request, f"{updated} campaigns paused.")
    pause_campaigns.short_description = _("Pause selected campaigns")
    
    def update_statistics(self, request, queryset):
        """Update statistics for selected campaigns"""
        for campaign in queryset:
            campaign.update_statistics()
        
        self.message_user(request, f"Statistics updated for {queryset.count()} campaigns.")
    update_statistics.short_description = _("Update statistics for selected campaigns")


@admin.register(CampaignMember)
class CampaignMemberAdmin(admin.ModelAdmin):
    """Admin interface for CampaignMember model"""
    
    list_display = [
        'agent', 'campaign', 'role', 'is_active', 
        'calls_handled', 'success_rate_display', 'assigned_date'
    ]
    
    list_filter = [
        'role', 'is_active', 'assigned_date', 'campaign__campaign_type'
    ]
    
    search_fields = [
        'agent__username', 'agent__first_name', 'agent__last_name',
        'campaign__name'
    ]
    
    readonly_fields = [
        'assigned_date', 'calls_handled', 'calls_answered', 'calls_successful',
        'success_rate_display', 'answer_rate_display', 'total_talk_time',
        'avg_talk_time', 'quality_score'
    ]
    
    fieldsets = (
        (_('Assignment'), {
            'fields': (
                ('campaign', 'agent'),
                ('role', 'is_active'),
                'assigned_date'
            )
        }),
        (_('Performance'), {
            'fields': (
                ('calls_handled', 'calls_answered', 'calls_successful'),
                ('success_rate_display', 'answer_rate_display'),
                ('total_talk_time', 'avg_talk_time'),
                'quality_score'
            )
        })
    )
    
    actions = ['deactivate_members', 'update_member_statistics']
    
    def success_rate_display(self, obj):
        """Display success rate percentage"""
        return f"{obj.success_rate:.1f}%"
    success_rate_display.short_description = _('Success Rate')
    
    def answer_rate_display(self, obj):
        """Display answer rate percentage"""
        return f"{obj.answer_rate:.1f}%"
    answer_rate_display.short_description = _('Answer Rate')
    
    # Admin Actions
    def deactivate_members(self, request, queryset):
        """Deactivate selected campaign members"""
        updated = queryset.update(is_active=False, unassigned_date=timezone.now())
        self.message_user(request, f"{updated} members deactivated.")
    deactivate_members.short_description = _("Deactivate selected members")
    
    def update_member_statistics(self, request, queryset):
        """Update statistics for selected members"""
        for member in queryset:
            member.update_statistics()
        
        self.message_user(request, f"Statistics updated for {queryset.count()} members.")
    update_member_statistics.short_description = _("Update member statistics")


@admin.register(CampaignContact)
class CampaignContactAdmin(admin.ModelAdmin):
    """Admin interface for CampaignContact model"""
    
    list_display = [
        'contact', 'campaign', 'status', 'priority', 
        'attempts_display', 'last_attempt', 'next_attempt',
        'assigned_agent', 'is_overdue_display'
    ]
    
    list_filter = [
        'status', 'priority', 'campaign', 'assigned_agent',
        'last_attempt', 'next_attempt'
    ]
    
    search_fields = [
        'contact__full_name', 'contact__primary_phone',
        'campaign__name', 'notes'
    ]
    
    readonly_fields = ['created_at', 'can_attempt_display', 'is_overdue_display']
    
    fieldsets = (
        (_('Assignment'), {
            'fields': (
                ('campaign', 'contact'),
                ('status', 'priority'),
                'assigned_agent'
            )
        }),
        (_('Attempt Tracking'), {
            'fields': (
                ('attempts_made', 'max_attempts'),
                ('last_attempt', 'next_attempt'),
                ('can_attempt_display', 'is_overdue_display')
            )
        }),
        (_('Results'), {
            'fields': ('result', 'notes')
        })
    )
    
    actions = ['reset_attempts', 'schedule_next_attempts', 'mark_do_not_call']
    
    def attempts_display(self, obj):
        """Display attempts made vs maximum"""
        color = 'red' if obj.attempts_made >= obj.max_attempts else 'green'
        return format_html(
            '<span style="color: {};">{}/{}</span>',
            color, obj.attempts_made, obj.max_attempts
        )
    attempts_display.short_description = _('Attempts')
    
    def can_attempt_display(self, obj):
        """Display if contact can be attempted"""
        if obj.can_attempt:
            return format_html('<span style="color: green;">✓ Can Attempt</span>')
        return format_html('<span style="color: red;">✗ Max Reached</span>')
    can_attempt_display.short_description = _('Can Attempt')
    
    def is_overdue_display(self, obj):
        """Display if attempt is overdue"""
        if obj.is_overdue:
            return format_html('<span style="color: red;">⚠ Overdue</span>')
        return format_html('<span style="color: green;">✓ On Time</span>')
    is_overdue_display.short_description = _('Status')
    
    # Admin Actions
    def reset_attempts(self, request, queryset):
        """Reset attempt counts for selected contacts"""
        updated = queryset.update(
            attempts_made=0,
            status='pending',
            last_attempt=None,
            next_attempt=timezone.now()
        )
        self.message_user(request, f"Reset attempts for {updated} contacts.")
    reset_attempts.short_description = _("Reset attempts for selected contacts")
    
    def schedule_next_attempts(self, request, queryset):
        """Schedule next attempts for selected contacts"""
        count = 0
        for contact in queryset:
            if contact.can_attempt:
                contact.schedule_next_attempt()
                count += 1
        
        self.message_user(request, f"Scheduled next attempts for {count} contacts.")
    schedule_next_attempts.short_description = _("Schedule next attempts")
    
    def mark_do_not_call(self, request, queryset):
        """Mark selected contacts as do not call"""
        updated = queryset.update(status='do_not_call')
        self.message_user(request, f"Marked {updated} contacts as do not call.")
    mark_do_not_call.short_description = _("Mark as do not call")