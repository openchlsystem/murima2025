# apps/cases/filters.py
import django_filters
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from .models import Case, CaseActivity, CaseService, CaseReferral, CaseNote


class CaseFilter(django_filters.FilterSet):
    """Comprehensive filter for Case model"""
    
    # Text search
    search = django_filters.CharFilter(method='filter_search', label='Search')
    
    # Status filters
    status = django_filters.CharFilter(field_name='status__name', lookup_expr='icontains')
    status_id = django_filters.NumberFilter(field_name='status__id')
    is_open = django_filters.BooleanFilter(method='filter_is_open', label='Is Open')
    is_closed = django_filters.BooleanFilter(method='filter_is_closed', label='Is Closed')
    
    # Priority filters
    priority = django_filters.CharFilter(field_name='priority__name', lookup_expr='icontains')
    priority_id = django_filters.NumberFilter(field_name='priority__id')
    
    # Type filters
    case_type = django_filters.CharFilter(field_name='case_type__name', lookup_expr='icontains')
    case_type_id = django_filters.NumberFilter(field_name='case_type__id')
    
    # Assignment filters
    assigned_to = django_filters.NumberFilter(field_name='assigned_to__id')
    assigned_to_name = django_filters.CharFilter(
        field_name='assigned_to__first_name', 
        lookup_expr='icontains'
    )
    unassigned = django_filters.BooleanFilter(
        field_name='assigned_to', 
        lookup_expr='isnull'
    )
    
    # Escalation filters
    escalated_to = django_filters.NumberFilter(field_name='escalated_to__id')
    is_escalated = django_filters.BooleanFilter(
        field_name='escalated_to', 
        lookup_expr='isnull',
        exclude=True
    )
    
    # Reporter filters
    reporter = django_filters.NumberFilter(field_name='reporter__id')
    reporter_name = django_filters.CharFilter(
        field_name='reporter__full_name', 
        lookup_expr='icontains'
    )
    reporter_phone = django_filters.CharFilter(
        field_name='reporter__primary_phone', 
        lookup_expr='icontains'
    )
    
    # Date filters
    created_after = django_filters.DateTimeFilter(
        field_name='created_at', 
        lookup_expr='gte'
    )
    created_before = django_filters.DateTimeFilter(
        field_name='created_at', 
        lookup_expr='lte'
    )
    created_date = django_filters.DateFilter(
        field_name='created_at__date'
    )
    
    due_date_after = django_filters.DateTimeFilter(
        field_name='due_date', 
        lookup_expr='gte'
    )
    due_date_before = django_filters.DateTimeFilter(
        field_name='due_date', 
        lookup_expr='lte'
    )
    
    closed_after = django_filters.DateTimeFilter(
        field_name='closed_date', 
        lookup_expr='gte'
    )
    closed_before = django_filters.DateTimeFilter(
        field_name='closed_date', 
        lookup_expr='lte'
    )
    
    # Incident date filters
    incident_after = django_filters.DateTimeFilter(
        field_name='incident_date', 
        lookup_expr='gte'
    )
    incident_before = django_filters.DateTimeFilter(
        field_name='incident_date', 
        lookup_expr='lte'
    )
    
    # Special status filters
    is_overdue = django_filters.BooleanFilter(method='filter_is_overdue', label='Is Overdue')
    is_stale = django_filters.BooleanFilter(method='filter_is_stale', label='Is Stale')
    created_today = django_filters.BooleanFilter(method='filter_created_today', label='Created Today')
    created_this_week = django_filters.BooleanFilter(method='filter_created_this_week', label='Created This Week')
    
    # GBV and special case filters
    is_gbv_related = django_filters.BooleanFilter()
    medical_exam_done = django_filters.BooleanFilter()
    incident_reported_to_police = django_filters.BooleanFilter()
    reporter_is_afflicted = django_filters.BooleanFilter()
    
    # Source filters
    source_type = django_filters.CharFilter(lookup_expr='icontains')
    source_channel = django_filters.NumberFilter(field_name='source_channel__id')
    
    # AI analysis filters
    ai_analysis_completed = django_filters.BooleanFilter()
    ai_risk_score_min = django_filters.NumberFilter(
        field_name='ai_risk_score', 
        lookup_expr='gte'
    )
    ai_risk_score_max = django_filters.NumberFilter(
        field_name='ai_risk_score', 
        lookup_expr='lte'
    )
    ai_urgency_score_min = django_filters.NumberFilter(
        field_name='ai_urgency_score', 
        lookup_expr='gte'
    )
    ai_urgency_score_max = django_filters.NumberFilter(
        field_name='ai_urgency_score', 
        lookup_expr='lte'
    )
    
    # Count filters
    client_count = django_filters.NumberFilter()
    client_count_min = django_filters.NumberFilter(
        field_name='client_count', 
        lookup_expr='gte'
    )
    client_count_max = django_filters.NumberFilter(
        field_name='client_count', 
        lookup_expr='lte'
    )
    
    perpetrator_count = django_filters.NumberFilter()
    perpetrator_count_min = django_filters.NumberFilter(
        field_name='perpetrator_count', 
        lookup_expr='gte'
    )
    perpetrator_count_max = django_filters.NumberFilter(
        field_name='perpetrator_count', 
        lookup_expr='lte'
    )
    
    # Category filters
    has_category = django_filters.NumberFilter(
        field_name='categories__category__id'
    )
    category_name = django_filters.CharFilter(
        field_name='categories__category__name', 
        lookup_expr='icontains'
    )
    
    class Meta:
        model = Case
        fields = []  # All fields are defined above
    
    def filter_search(self, queryset, name, value):
        """Full-text search across multiple fields"""
        if not value:
            return queryset
        
        return queryset.filter(
            Q(case_number__icontains=value) |
            Q(title__icontains=value) |
            Q(narrative__icontains=value) |
            Q(action_plan__icontains=value) |
            Q(reporter__full_name__icontains=value) |
            Q(reporter__primary_phone__icontains=value) |
            Q(incident_reference_number__icontains=value) |
            Q(police_ob_number__icontains=value)
        ).distinct()
    
    def filter_is_open(self, queryset, name, value):
        """Filter for open cases"""
        if value:
            return queryset.filter(
                status__name__in=['open', 'in_progress', 'pending']
            )
        else:
            return queryset.exclude(
                status__name__in=['open', 'in_progress', 'pending']
            )
    
    def filter_is_closed(self, queryset, name, value):
        """Filter for closed cases"""
        if value:
            return queryset.filter(
                status__name__in=['closed', 'resolved', 'cancelled']
            )
        else:
            return queryset.exclude(
                status__name__in=['closed', 'resolved', 'cancelled']
            )
    
    def filter_is_overdue(self, queryset, name, value):
        """Filter for overdue cases"""
        if value:
            return queryset.filter(
                due_date__lt=timezone.now(),
                status__name__in=['open', 'in_progress', 'pending']
            )
        else:
            return queryset.filter(
                Q(due_date__gte=timezone.now()) |
                Q(due_date__isnull=True) |
                Q(status__name__in=['closed', 'resolved', 'cancelled'])
            )
    
    def filter_is_stale(self, queryset, name, value):
        """Filter for cases not updated in 7 days"""
        week_ago = timezone.now() - timedelta(days=7)
        if value:
            return queryset.filter(
                updated_at__lt=week_ago,
                status__name__in=['open', 'in_progress', 'pending']
            )
        else:
            return queryset.filter(
                Q(updated_at__gte=week_ago) |
                Q(status__name__in=['closed', 'resolved', 'cancelled'])
            )
    
    def filter_created_today(self, queryset, name, value):
        """Filter for cases created today"""
        today = timezone.now().date()
        if value:
            return queryset.filter(created_at__date=today)
        else:
            return queryset.exclude(created_at__date=today)
    
    def filter_created_this_week(self, queryset, name, value):
        """Filter for cases created this week"""
        week_ago = timezone.now() - timedelta(days=7)
        if value:
            return queryset.filter(created_at__gte=week_ago)
        else:
            return queryset.exclude(created_at__gte=week_ago)


class CaseActivityFilter(django_filters.FilterSet):
    """Filter for Case Activities"""
    
    # Case filters
    case = django_filters.NumberFilter(field_name='case__id')
    case_number = django_filters.CharFilter(
        field_name='case__case_number', 
        lookup_expr='icontains'
    )
    
    # Activity type filters
    activity_type = django_filters.CharFilter(lookup_expr='icontains')
    activity_type_exact = django_filters.CharFilter(field_name='activity_type')
    
    # User filters
    user = django_filters.NumberFilter(field_name='user__id')
    user_name = django_filters.CharFilter(
        field_name='user__first_name', 
        lookup_expr='icontains'
    )
    
    # Date filters
    created_after = django_filters.DateTimeFilter(
        field_name='created_at', 
        lookup_expr='gte'
    )
    created_before = django_filters.DateTimeFilter(
        field_name='created_at', 
        lookup_expr='lte'
    )
    created_date = django_filters.DateFilter(
        field_name='created_at__date'
    )
    
    # Content filters
    search = django_filters.CharFilter(method='filter_search', label='Search')
    is_important = django_filters.BooleanFilter()
    is_internal = django_filters.BooleanFilter()
    
    # Source filters
    source_reference = django_filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model = CaseActivity
        fields = []
    
    def filter_search(self, queryset, name, value):
        """Search in activity content"""
        if not value:
            return queryset
        
        return queryset.filter(
            Q(title__icontains=value) |
            Q(description__icontains=value)
        ).distinct()


class CaseServiceFilter(django_filters.FilterSet):
    """Filter for Case Services"""
    
    case = django_filters.NumberFilter(field_name='case__id')
    case_number = django_filters.CharFilter(
        field_name='case__case_number', 
        lookup_expr='icontains'
    )
    
    service = django_filters.NumberFilter(field_name='service__id')
    service_name = django_filters.CharFilter(
        field_name='service__name', 
        lookup_expr='icontains'
    )
    
    provided_by = django_filters.NumberFilter(field_name='provided_by__id')
    provided_by_name = django_filters.CharFilter(
        field_name='provided_by__first_name', 
        lookup_expr='icontains'
    )
    
    service_date_after = django_filters.DateTimeFilter(
        field_name='service_date', 
        lookup_expr='gte'
    )
    service_date_before = django_filters.DateTimeFilter(
        field_name='service_date', 
        lookup_expr='lte'
    )
    service_date = django_filters.DateFilter(
        field_name='service_date__date'
    )
    
    is_completed = django_filters.BooleanFilter()
    
    cost_min = django_filters.NumberFilter(
        field_name='cost', 
        lookup_expr='gte'
    )
    cost_max = django_filters.NumberFilter(
        field_name='cost', 
        lookup_expr='lte'
    )
    
    search = django_filters.CharFilter(method='filter_search', label='Search')
    
    class Meta:
        model = CaseService
        fields = []
    
    def filter_search(self, queryset, name, value):
        """Search in service details"""
        if not value:
            return queryset
        
        return queryset.filter(
            Q(service__name__icontains=value) |
            Q(details__icontains=value)
        ).distinct()


class CaseReferralFilter(django_filters.FilterSet):
    """Filter for Case Referrals"""
    
    case = django_filters.NumberFilter(field_name='case__id')
    case_number = django_filters.CharFilter(
        field_name='case__case_number', 
        lookup_expr='icontains'
    )
    
    referral_type = django_filters.NumberFilter(field_name='referral_type__id')
    referral_type_name = django_filters.CharFilter(
        field_name='referral_type__name', 
        lookup_expr='icontains'
    )
    
    organization = django_filters.CharFilter(lookup_expr='icontains')
    status = django_filters.CharFilter(lookup_expr='icontains')
    
    referred_by = django_filters.NumberFilter(field_name='referred_by__id')
    referred_by_name = django_filters.CharFilter(
        field_name='referred_by__first_name', 
        lookup_expr='icontains'
    )
    
    referral_date_after = django_filters.DateTimeFilter(
        field_name='referral_date', 
        lookup_expr='gte'
    )
    referral_date_before = django_filters.DateTimeFilter(
        field_name='referral_date', 
        lookup_expr='lte'
    )
    referral_date = django_filters.DateFilter(
        field_name='referral_date__date'
    )
    
    follow_up_date_after = django_filters.DateTimeFilter(
        field_name='follow_up_date', 
        lookup_expr='gte'
    )
    follow_up_date_before = django_filters.DateTimeFilter(
        field_name='follow_up_date', 
        lookup_expr='lte'
    )
    
    is_overdue = django_filters.BooleanFilter(method='filter_is_overdue', label='Is Overdue')
    
    urgency = django_filters.NumberFilter(field_name='urgency__id')
    urgency_name = django_filters.CharFilter(
        field_name='urgency__name', 
        lookup_expr='icontains'
    )
    
    search = django_filters.CharFilter(method='filter_search', label='Search')
    
    class Meta:
        model = CaseReferral
        fields = []
    
    def filter_search(self, queryset, name, value):
        """Search in referral content"""
        if not value:
            return queryset
        
        return queryset.filter(
            Q(organization__icontains=value) |
            Q(contact_person__icontains=value) |
            Q(reason__icontains=value) |
            Q(outcome__icontains=value) |
            Q(notes__icontains=value)
        ).distinct()
    
    def filter_is_overdue(self, queryset, name, value):
        """Filter for overdue referrals"""
        if value:
            return queryset.filter(
                follow_up_date__lt=timezone.now(),
                status__in=['pending', 'sent', 'acknowledged']
            )
        else:
            return queryset.filter(
                Q(follow_up_date__gte=timezone.now()) |
                Q(follow_up_date__isnull=True) |
                Q(status__in=['completed', 'rejected', 'cancelled'])
            )


class CaseNoteFilter(django_filters.FilterSet):
    """Filter for Case Notes"""
    
    case = django_filters.NumberFilter(field_name='case__id')
    case_number = django_filters.CharFilter(
        field_name='case__case_number', 
        lookup_expr='icontains'
    )
    
    note_type = django_filters.CharFilter(lookup_expr='icontains')
    note_type_exact = django_filters.CharFilter(field_name='note_type')
    
    author = django_filters.NumberFilter(field_name='author__id')
    author_name = django_filters.CharFilter(
        field_name='author__first_name', 
        lookup_expr='icontains'
    )
    
    is_private = django_filters.BooleanFilter()
    is_important = django_filters.BooleanFilter()
    visible_to_client = django_filters.BooleanFilter()
    
    created_after = django_filters.DateTimeFilter(
        field_name='created_at', 
        lookup_expr='gte'
    )
    created_before = django_filters.DateTimeFilter(
        field_name='created_at', 
        lookup_expr='lte'
    )
    created_date = django_filters.DateFilter(
        field_name='created_at__date'
    )
    
    search = django_filters.CharFilter(method='filter_search', label='Search')
    
    class Meta:
        model = CaseNote
        fields = []
    
    def filter_search(self, queryset, name, value):
        """Search in note content"""
        if not value:
            return queryset
        
        return queryset.filter(
            Q(title__icontains=value) |
            Q(content__icontains=value)
        ).distinct()


class DateRangeFilter(django_filters.FilterSet):
    """Reusable date range filter mixin"""
    
    # Common date range presets
    date_range = django_filters.ChoiceFilter(
        method='filter_date_range',
        choices=[
            ('today', 'Today'),
            ('yesterday', 'Yesterday'),
            ('this_week', 'This Week'),
            ('last_week', 'Last Week'),
            ('this_month', 'This Month'),
            ('last_month', 'Last Month'),
            ('this_quarter', 'This Quarter'),
            ('last_quarter', 'Last Quarter'),
            ('this_year', 'This Year'),
            ('last_year', 'Last Year'),
        ],
        label='Date Range'
    )
    
    def filter_date_range(self, queryset, name, value):
        """Filter by predefined date ranges"""
        now = timezone.now()
        today = now.date()
        
        if value == 'today':
            return queryset.filter(created_at__date=today)
        elif value == 'yesterday':
            yesterday = today - timedelta(days=1)
            return queryset.filter(created_at__date=yesterday)
        elif value == 'this_week':
            week_start = today - timedelta(days=today.weekday())
            return queryset.filter(created_at__date__gte=week_start)
        elif value == 'last_week':
            week_start = today - timedelta(days=today.weekday() + 7)
            week_end = today - timedelta(days=today.weekday() + 1)
            return queryset.filter(
                created_at__date__gte=week_start,
                created_at__date__lte=week_end
            )
        elif value == 'this_month':
            month_start = today.replace(day=1)
            return queryset.filter(created_at__date__gte=month_start)
        elif value == 'last_month':
            if today.month == 1:
                last_month_start = today.replace(year=today.year - 1, month=12, day=1)
                last_month_end = today.replace(day=1) - timedelta(days=1)
            else:
                last_month_start = today.replace(month=today.month - 1, day=1)
                last_month_end = today.replace(day=1) - timedelta(days=1)
            return queryset.filter(
                created_at__date__gte=last_month_start,
                created_at__date__lte=last_month_end
            )
        elif value == 'this_quarter':
            quarter_start_month = ((today.month - 1) // 3) * 3 + 1
            quarter_start = today.replace(month=quarter_start_month, day=1)
            return queryset.filter(created_at__date__gte=quarter_start)
        elif value == 'last_quarter':
            current_quarter_start_month = ((today.month - 1) // 3) * 3 + 1
            if current_quarter_start_month == 1:
                last_quarter_start = today.replace(year=today.year - 1, month=10, day=1)
                last_quarter_end = today.replace(month=1, day=1) - timedelta(days=1)
            else:
                last_quarter_start_month = current_quarter_start_month - 3
                last_quarter_start = today.replace(month=last_quarter_start_month, day=1)
                last_quarter_end = today.replace(month=current_quarter_start_month, day=1) - timedelta(days=1)
            return queryset.filter(
                created_at__date__gte=last_quarter_start,
                created_at__date__lte=last_quarter_end
            )
        elif value == 'this_year':
            year_start = today.replace(month=1, day=1)
            return queryset.filter(created_at__date__gte=year_start)
        elif value == 'last_year':
            last_year_start = today.replace(year=today.year - 1, month=1, day=1)
            last_year_end = today.replace(month=1, day=1) - timedelta(days=1)
            return queryset.filter(
                created_at__date__gte=last_year_start,
                created_at__date__lte=last_year_end
            )
        
        return queryset


class AdvancedCaseFilter(CaseFilter, DateRangeFilter):
    """Extended case filter with date range presets"""
    
    class Meta:
        model = Case
        fields = []


class CaseReportFilter(django_filters.FilterSet):
    """Special filter for case reporting and analytics"""
    
    # Location-based filters
    reporter_region = django_filters.NumberFilter(field_name='reporter__region__id')
    reporter_district = django_filters.NumberFilter(field_name='reporter__district__id')
    reporter_subcounty = django_filters.NumberFilter(field_name='reporter__subcounty__id')
    
    # Demographics
    reporter_age_group = django_filters.NumberFilter(field_name='reporter__age_group__id')
    reporter_gender = django_filters.NumberFilter(field_name='reporter__gender__id')
    
    # Case outcome metrics
    has_services = django_filters.BooleanFilter(method='filter_has_services')
    has_referrals = django_filters.BooleanFilter(method='filter_has_referrals')
    has_follow_up = django_filters.BooleanFilter(method='filter_has_follow_up')
    
    # Resolution metrics
    resolved_within_days = django_filters.NumberFilter(method='filter_resolved_within_days')
    
    # AI metrics
    has_ai_analysis = django_filters.BooleanFilter(field_name='ai_analysis_completed')
    high_risk = django_filters.BooleanFilter(method='filter_high_risk')
    high_urgency = django_filters.BooleanFilter(method='filter_high_urgency')
    
    class Meta:
        model = Case
        fields = []
    
    def filter_has_services(self, queryset, name, value):
        """Filter cases that have services"""
        if value:
            return queryset.filter(services__isnull=False).distinct()
        else:
            return queryset.filter(services__isnull=True)
    
    def filter_has_referrals(self, queryset, name, value):
        """Filter cases that have referrals"""
        if value:
            return queryset.filter(referrals__isnull=False).distinct()
        else:
            return queryset.filter(referrals__isnull=True)
    
    def filter_has_follow_up(self, queryset, name, value):
        """Filter cases that have follow-up activities"""
        if value:
            return queryset.filter(
                Q(referrals__follow_up_date__isnull=False) |
                Q(due_date__isnull=False)
            ).distinct()
        else:
            return queryset.filter(
                referrals__follow_up_date__isnull=True,
                due_date__isnull=True
            )
    
    def filter_resolved_within_days(self, queryset, name, value):
        """Filter cases resolved within specified days"""
        return queryset.extra(
            where=["DATEDIFF(closed_date, created_at) <= %s"],
            params=[value]
        ).filter(closed_date__isnull=False)
    
    def filter_high_risk(self, queryset, name, value):
        """Filter high-risk cases (AI risk score > 0.7)"""
        if value:
            return queryset.filter(ai_risk_score__gt=0.7)
        else:
            return queryset.filter(
                Q(ai_risk_score__lte=0.7) | 
                Q(ai_risk_score__isnull=True)
            )
    
    def filter_high_urgency(self, queryset, name, value):
        """Filter high-urgency cases (AI urgency score > 0.7)"""
        if value:
            return queryset.filter(ai_urgency_score__gt=0.7)
        else:
            return queryset.filter(
                Q(ai_urgency_score__lte=0.7) | 
                Q(ai_urgency_score__isnull=True)
            )