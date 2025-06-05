# apps/cases/admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db.models import Count, Q
from django.utils import timezone
from django.contrib.admin import SimpleListFilter
from .models import (
    Case, CaseCategory, CaseActivity, CaseService, CaseReferral,
    CaseNote, CaseAttachment, CaseUpdate
)


class CaseStatusFilter(SimpleListFilter):
    """Custom filter for case status"""
    title = _('Status')
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return [
            ('open', _('Open Cases')),
            ('closed', _('Closed Cases')),
            ('escalated', _('Escalated Cases')),
            ('overdue', _('Overdue Cases')),
            ('today', _('Created Today')),
            ('this_week', _('Created This Week')),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'open':
            return queryset.filter(status__name__in=['open', 'in_progress', 'pending'])
        elif self.value() == 'closed':
            return queryset.filter(status__name__in=['closed', 'resolved'])
        elif self.value() == 'escalated':
            return queryset.filter(escalated_to__isnull=False)
        elif self.value() == 'overdue':
            return queryset.filter(
                due_date__lt=timezone.now(),
                status__name__in=['open', 'in_progress', 'pending']
            )
        elif self.value() == 'today':
            return queryset.filter(created_at__date=timezone.now().date())
        elif self.value() == 'this_week':
            week_ago = timezone.now() - timezone.timedelta(days=7)
            return queryset.filter(created_at__gte=week_ago)
        return queryset


class GBVFilter(SimpleListFilter):
    """Filter for GBV-related cases"""
    title = _('GBV Related')
    parameter_name = 'gbv'

    def lookups(self, request, model_admin):
        return [
            ('yes', _('GBV Cases')),
            ('no', _('Non-GBV Cases')),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(is_gbv_related=True)
        elif self.value() == 'no':
            return queryset.filter(is_gbv_related=False)
        return queryset


class CaseCategoryInline(admin.TabularInline):
    """Inline for case categories"""
    model = CaseCategory
    extra = 1
    fields = ['category', 'is_primary', 'confidence_score', 'added_by']
    readonly_fields = ['added_by']
    
    def save_model(self, request, obj, form, change):
        if not obj.added_by:
            obj.added_by = request.user
        super().save_model(request, obj, form, change)


class CaseServiceInline(admin.TabularInline):
    """Inline for case services"""
    model = CaseService
    extra = 0
    fields = ['service', 'service_date', 'provided_by', 'details', 'cost', 'is_completed']
    readonly_fields = ['provided_by']
    
    def save_model(self, request, obj, form, change):
        if not obj.provided_by:
            obj.provided_by = request.user
        super().save_model(request, obj, form, change)


class CaseReferralInline(admin.TabularInline):
    """Inline for case referrals"""
    model = CaseReferral
    extra = 0
    fields = ['referral_type', 'organization', 'status', 'referral_date', 'follow_up_date']
    readonly_fields = ['referral_date']


class CaseNoteInline(admin.StackedInline):
    """Inline for case notes"""
    model = CaseNote
    extra = 0
    fields = ['note_type', 'title', 'content', 'is_private', 'is_important', 'visible_to_client']
    readonly_fields = ['author', 'created_at']
    
    def save_model(self, request, obj, form, change):
        if not obj.author:
            obj.author = request.user
        super().save_model(request, obj, form, change)


class CaseAttachmentInline(admin.TabularInline):
    """Inline for case attachments"""
    model = CaseAttachment
    extra = 0
    fields = ['attachment_type', 'title', 'file_name', 'file_size_human', 'is_confidential', 'access_level']
    readonly_fields = ['file_size_human', 'uploaded_by', 'created_at']


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    """Admin interface for Case model"""
    
    list_display = [
        'case_number', 'case_status_badge', 'priority_badge', 'case_type', 
        'reporter_link', 'assigned_to', 'age_display', 'is_gbv_badge', 
        'activity_count', 'created_at'
    ]
    list_filter = [
        CaseStatusFilter, GBVFilter, 'case_type', 'priority', 
        'assigned_to', 'escalated_to', 'created_at', 'is_gbv_related'
    ]
    search_fields = [
        'case_number', 'title', 'narrative', 'reporter__full_name',
        'reporter__primary_phone', 'incident_reference_number'
    ]
    readonly_fields = [
        'uuid', 'case_number', 'age_display', 'time_to_resolution_display',
        'created_at', 'updated_at', 'created_by', 'updated_by',
        'ai_analysis_completed', 'ai_analysis_date', 'migration_notes'
    ]
    
    fieldsets = (
        (_('Basic Information'), {
            'fields': (
                'uuid', 'case_number', 'title', 'case_type', 'status', 'priority'
            )
        }),
        (_('Reporter Information'), {
            'fields': (
                'reporter', 'reporter_is_afflicted', 'knows_about_116'
            )
        }),
        (_('Assignment'), {
            'fields': (
                'assigned_to', 'escalated_to', 'escalated_by', 'escalation_date'
            )
        }),
        (_('Case Details'), {
            'fields': (
                'narrative', 'action_plan', 'incident_date', 'incident_location',
                'report_location', 'due_date'
            )
        }),
        (_('Source Information'), {
            'fields': (
                'source_type', 'source_reference', 'source_channel'
            ),
            'classes': ('collapse',)
        }),
        (_('GBV Specific'), {
            'fields': (
                'is_gbv_related', 'medical_exam_done', 'incident_reported_to_police',
                'police_ob_number', 'hiv_tested', 'hiv_test_result', 'pep_given',
                'art_given', 'ecp_given', 'counselling_given', 'counselling_organization'
            ),
            'classes': ('collapse',)
        }),
        (_('Case Management'), {
            'fields': (
                'client_count', 'perpetrator_count', 'incident_reference_number',
                'closed_date', 'resolution_summary'
            ),
            'classes': ('collapse',)
        }),
        (_('AI Analysis'), {
            'fields': (
                'ai_risk_score', 'ai_urgency_score', 'ai_suggested_category',
                'ai_suggested_priority', 'ai_summary', 'ai_sentiment_score',
                'ai_analysis_completed', 'ai_analysis_date'
            ),
            'classes': ('collapse',)
        }),
        (_('Migration Data'), {
            'fields': (
                'legacy_case_id', 'legacy_nsr', 'migration_notes'
            ),
            'classes': ('collapse',)
        }),
        (_('Timestamps'), {
            'fields': (
                'created_at', 'updated_at', 'created_by', 'updated_by'
            ),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [
        CaseCategoryInline, CaseServiceInline, CaseReferralInline, 
        CaseNoteInline, CaseAttachmentInline
    ]
    
    actions = ['escalate_cases', 'close_cases', 'assign_to_me', 'mark_for_ai_analysis']
    
    def get_queryset(self, request):
        """Optimize queryset with select_related"""
        return super().get_queryset(request).select_related(
            'case_type', 'status', 'priority', 'reporter', 'assigned_to',
            'escalated_to', 'source_channel'
        ).prefetch_related('categories', 'activities')
    
    def case_status_badge(self, obj):
        """Display status as colored badge"""
        if not obj.status:
            return '-'
        
        color_map = {
            'open': 'green',
            'in_progress': 'blue',
            'pending': 'orange',
            'escalated': 'red',
            'resolved': 'purple',
            'closed': 'gray',
            'cancelled': 'black',
        }
        
        status_name = obj.status.name.lower()
        color = color_map.get(status_name, 'gray')
        
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 6px; '
            'border-radius: 3px; font-size: 11px;">{}</span>',
            color, obj.status.name
        )
    case_status_badge.short_description = _('Status')
    case_status_badge.admin_order_field = 'status__name'
    
    def priority_badge(self, obj):
        """Display priority as colored badge"""
        if not obj.priority:
            return '-'
        
        color_map = {
            'critical': '#dc3545',
            'high': '#fd7e14',
            'medium': '#ffc107',
            'low': '#28a745',
            'lowest': '#6c757d',
        }
        
        priority_name = obj.priority.name.lower()
        color = color_map.get(priority_name, '#6c757d')
        
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 6px; '
            'border-radius: 3px; font-size: 11px;">{}</span>',
            color, obj.priority.name
        )
    priority_badge.short_description = _('Priority')
    priority_badge.admin_order_field = 'priority__name'
    
    def reporter_link(self, obj):
        """Display reporter as link to contact"""
        if not obj.reporter:
            return '-'
        
        url = reverse('admin:contacts_contact_change', args=[obj.reporter.pk])
        return format_html(
            '<a href="{}">{}</a>',
            url, obj.reporter.full_name or obj.reporter.primary_phone
        )
    reporter_link.short_description = _('Reporter')
    reporter_link.admin_order_field = 'reporter__full_name'
    
    def is_gbv_badge(self, obj):
        """Display GBV status as badge"""
        if obj.is_gbv_related:
            return format_html(
                '<span style="background-color: #dc3545; color: white; padding: 2px 6px; '
                'border-radius: 3px; font-size: 11px;">GBV</span>'
            )
        return '-'
    is_gbv_badge.short_description = _('GBV')
    is_gbv_badge.admin_order_field = 'is_gbv_related'
    
    def age_display(self, obj):
        """Display case age"""
        age = obj.age_in_days
        if age == 0:
            return _('Today')
        elif age == 1:
            return _('1 day')
        elif age < 7:
            return _(f'{age} days')
        elif age < 30:
            weeks = age // 7
            return _(f'{weeks} week(s)')
        else:
            months = age // 30
            return _(f'{months} month(s)')
    age_display.short_description = _('Age')
    
    def activity_count(self, obj):
        """Display number of activities"""
        return obj.activities.count()
    activity_count.short_description = _('Activities')
    
    def time_to_resolution_display(self, obj):
        """Display time to resolution"""
        if obj.time_to_resolution:
            days = obj.time_to_resolution.days
            hours = obj.time_to_resolution.seconds // 3600
            return f"{days}d {hours}h"
        return '-'
    time_to_resolution_display.short_description = _('Resolution Time')
    
    def escalate_cases(self, request, queryset):
        """Bulk escalate cases"""
        # This would open a form to select who to escalate to
        count = queryset.count()
        self.message_user(
            request,
            f'{count} case(s) marked for escalation. '
            'Please escalate them individually to assign to specific supervisors.'
        )
    escalate_cases.short_description = _('Mark selected cases for escalation')
    
    def close_cases(self, request, queryset):
        """Bulk close cases"""
        from apps.core.models import ReferenceData
        
        # Get closed status
        closed_status = ReferenceData.objects.filter(
            category='case_status', name__icontains='closed'
        ).first()
        
        if closed_status:
            count = 0
            for case in queryset:
                if case.status.name.lower() not in ['closed', 'resolved']:
                    case.close_case(closed_by=request.user, resolution_summary='Bulk closure')
                    count += 1
            
            self.message_user(
                request,
                f'{count} case(s) were successfully closed.'
            )
        else:
            self.message_user(
                request,
                'Could not find closed status in reference data.',
                level='error'
            )
    close_cases.short_description = _('Close selected cases')
    
    def assign_to_me(self, request, queryset):
        """Assign selected cases to current user"""
        count = 0
        for case in queryset:
            case.assign_to(request.user, assigned_by=request.user)
            count += 1
        
        self.message_user(
            request,
            f'{count} case(s) were assigned to you.'
        )
    assign_to_me.short_description = _('Assign selected cases to me')
    
    def mark_for_ai_analysis(self, request, queryset):
        """Mark cases for AI analysis"""
        queryset.update(ai_analysis_completed=False)
        count = queryset.count()
        self.message_user(
            request,
            f'{count} case(s) marked for AI analysis.'
        )
    mark_for_ai_analysis.short_description = _('Mark for AI analysis')


@admin.register(CaseActivity)
class CaseActivityAdmin(admin.ModelAdmin):
    """Admin interface for Case Activity"""
    
    list_display = [
        'case_link', 'activity_type', 'user', 'description_short', 
        'is_important', 'created_at'
    ]
    list_filter = [
        'activity_type', 'is_important', 'is_internal', 'created_at', 'user'
    ]
    search_fields = [
        'case__case_number', 'description', 'title', 'user__first_name', 
        'user__last_name'
    ]
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        (_('Activity Information'), {
            'fields': (
                'case', 'activity_type', 'user', 'title', 'description'
            )
        }),
        (_('Additional Data'), {
            'fields': (
                'data', 'field_changes', 'source_reference'
            ),
            'classes': ('collapse',)
        }),
        (_('Settings'), {
            'fields': (
                'is_important', 'is_internal'
            )
        }),
        (_('Migration'), {
            'fields': (
                'legacy_activity_id',
            ),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('case', 'user')
    
    def case_link(self, obj):
        """Display case as link"""
        url = reverse('admin:cases_case_change', args=[obj.case.pk])
        return format_html('<a href="{}">{}</a>', url, obj.case.case_number)
    case_link.short_description = _('Case')
    case_link.admin_order_field = 'case__case_number'
    
    def description_short(self, obj):
        """Display truncated description"""
        return obj.description[:100] + '...' if len(obj.description) > 100 else obj.description
    description_short.short_description = _('Description')


@admin.register(CaseService)
class CaseServiceAdmin(admin.ModelAdmin):
    """Admin interface for Case Services"""
    
    list_display = [
        'case_link', 'service', 'service_date', 'provided_by', 
        'cost', 'is_completed'
    ]
    list_filter = [
        'service', 'is_completed', 'service_date', 'provided_by'
    ]
    search_fields = [
        'case__case_number', 'service__name', 'details'
    ]
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'case', 'service', 'provided_by'
        )
    
    def case_link(self, obj):
        """Display case as link"""
        url = reverse('admin:cases_case_change', args=[obj.case.pk])
        return format_html('<a href="{}">{}</a>', url, obj.case.case_number)
    case_link.short_description = _('Case')
    case_link.admin_order_field = 'case__case_number'


@admin.register(CaseReferral)
class CaseReferralAdmin(admin.ModelAdmin):
    """Admin interface for Case Referrals"""
    
    list_display = [
        'case_link', 'organization', 'referral_type', 'status', 
        'referral_date', 'follow_up_date', 'is_overdue_badge'
    ]
    list_filter = [
        'status', 'referral_type', 'urgency', 'referral_date', 'referred_by'
    ]
    search_fields = [
        'case__case_number', 'organization', 'contact_person', 'reason'
    ]
    
    fieldsets = (
        (_('Referral Information'), {
            'fields': (
                'case', 'referral_type', 'organization', 'contact_person',
                'contact_phone', 'contact_email'
            )
        }),
        (_('Details'), {
            'fields': (
                'reason', 'urgency', 'status', 'referred_by', 'referral_date'
            )
        }),
        (_('Follow-up'), {
            'fields': (
                'follow_up_date', 'outcome', 'notes'
            )
        }),
        (_('Attachments'), {
            'fields': ('attachments',),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'case', 'referral_type', 'urgency', 'referred_by'
        )
    
    def case_link(self, obj):
        """Display case as link"""
        url = reverse('admin:cases_case_change', args=[obj.case.pk])
        return format_html('<a href="{}">{}</a>', url, obj.case.case_number)
    case_link.short_description = _('Case')
    case_link.admin_order_field = 'case__case_number'
    
    def is_overdue_badge(self, obj):
        """Display overdue status"""
        if obj.is_overdue:
            return format_html(
                '<span style="background-color: #dc3545; color: white; padding: 2px 6px; '
                'border-radius: 3px; font-size: 11px;">OVERDUE</span>'
            )
        return '-'
    is_overdue_badge.short_description = _('Status')


@admin.register(CaseNote)
class CaseNoteAdmin(admin.ModelAdmin):
    """Admin interface for Case Notes"""
    
    list_display = [
        'case_link', 'note_type', 'title', 'author', 'is_important', 
        'is_private', 'created_at'
    ]
    list_filter = [
        'note_type', 'is_important', 'is_private', 'visible_to_client', 
        'created_at', 'author'
    ]
    search_fields = [
        'case__case_number', 'title', 'content', 'author__first_name', 
        'author__last_name'
    ]
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        (_('Note Information'), {
            'fields': (
                'case', 'note_type', 'author', 'title', 'content'
            )
        }),
        (_('Visibility'), {
            'fields': (
                'is_private', 'is_important', 'visible_to_client'
            )
        }),
        (_('Attachments'), {
            'fields': ('attachments',),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('case', 'author')
    
    def case_link(self, obj):
        """Display case as link"""
        url = reverse('admin:cases_case_change', args=[obj.case.pk])
        return format_html('<a href="{}">{}</a>', url, obj.case.case_number)
    case_link.short_description = _('Case')
    case_link.admin_order_field = 'case__case_number'


@admin.register(CaseAttachment)
class CaseAttachmentAdmin(admin.ModelAdmin):
    """Admin interface for Case Attachments"""
    
    list_display = [
        'case_link', 'file_name', 'attachment_type', 'file_size_display', 
        'is_confidential', 'access_level', 'uploaded_by', 'created_at'
    ]
    list_filter = [
        'attachment_type', 'is_confidential', 'access_level', 'created_at', 
        'uploaded_by'
    ]
    search_fields = [
        'case__case_number', 'file_name', 'title', 'description'
    ]
    readonly_fields = ['file_size_display', 'checksum', 'created_at']
    
    fieldsets = (
        (_('Attachment Information'), {
            'fields': (
                'case', 'attachment_type', 'title', 'description'
            )
        }),
        (_('File Details'), {
            'fields': (
                'file_name', 'file_path', 'file_size_display', 'mime_type', 'checksum'
            )
        }),
        (_('Access Control'), {
            'fields': (
                'is_confidential', 'access_level', 'uploaded_by'
            )
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('case', 'uploaded_by')
    
    def case_link(self, obj):
        """Display case as link"""
        url = reverse('admin:cases_case_change', args=[obj.case.pk])
        return format_html('<a href="{}">{}</a>', url, obj.case.case_number)
    case_link.short_description = _('Case')
    case_link.admin_order_field = 'case__case_number'
    
    def file_size_display(self, obj):
        """Display human-readable file size"""
        return obj.file_size_human
    file_size_display.short_description = _('File Size')


@admin.register(CaseUpdate)
class CaseUpdateAdmin(admin.ModelAdmin):
    """Admin interface for Case Updates"""
    
    list_display = [
        'case_link', 'summary', 'status_at_update', 'progress_percentage', 
        'updated_by', 'created_at'
    ]
    list_filter = [
        'status_at_update', 'priority_at_update', 'created_at', 'updated_by'
    ]
    search_fields = [
        'case__case_number', 'summary', 'details', 'next_actions'
    ]
    readonly_fields = ['created_at']
    
    fieldsets = (
        (_('Update Information'), {
            'fields': (
                'case', 'updated_by', 'summary', 'details'
            )
        }),
        (_('Status at Update'), {
            'fields': (
                'status_at_update', 'priority_at_update', 'progress_percentage'
            )
        }),
        (_('Next Steps'), {
            'fields': (
                'next_actions', 'next_update_due'
            )
        }),
        (_('Changes'), {
            'fields': ('changes_made',),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'case', 'updated_by', 'status_at_update', 'priority_at_update'
        )
    
    def case_link(self, obj):
        """Display case as link"""
        url = reverse('admin:cases_case_change', args=[obj.case.pk])
        return format_html('<a href="{}">{}</a>', url, obj.case.case_number)
    case_link.short_description = _('Case')
    case_link.admin_order_field = 'case__case_number'


@admin.register(CaseCategory)
class CaseCategoryAdmin(admin.ModelAdmin):
    """Admin interface for Case Categories"""
    
    list_display = [
        'case_link', 'category', 'is_primary', 'confidence_score', 'added_by'
    ]
    list_filter = ['category', 'is_primary', 'added_by']
    search_fields = ['case__case_number', 'category__name']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('case', 'category', 'added_by')
    
    def case_link(self, obj):
        """Display case as link"""
        url = reverse('admin:cases_case_change', args=[obj.case.pk])
        return format_html('<a href="{}">{}</a>', url, obj.case.case_number)
    case_link.short_description = _('Case')
    case_link.admin_order_field = 'case__case_number'


# Custom admin site modifications
admin.site.site_header = _('Call Center Case Management')
admin.site.site_title = _('Case Management')
admin.site.index_title = _('Case Management Administration')