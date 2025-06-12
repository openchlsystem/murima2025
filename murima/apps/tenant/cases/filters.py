import django_filters
from .models import Case, AuditLog
from django.db import models

class CaseFilter(django_filters.FilterSet):
    case_type = django_filters.CharFilter(field_name='case_type__code')
    status = django_filters.CharFilter(field_name='status__code')
    priority = django_filters.NumberFilter()
    assigned_to = django_filters.CharFilter(field_name='assigned_to__username')
    assigned_team = django_filters.CharFilter(field_name='assigned_team__code')
    is_overdue = django_filters.BooleanFilter(method='filter_is_overdue')
    
class AuditLogFilter(django_filters.FilterSet):
    action = django_filters.CharFilter(field_name='action__code')
    object_type = django_filters.CharFilter(field_name='object_type__code')
    user = django_filters.CharFilter(field_name='user__username')
    case = django_filters.CharFilter(field_name='case__id')

    class Meta:
        model = AuditLog
        fields = '__all__'
        filter_overrides = {
            models.JSONField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'exact',
                }
            },
        }

    def filter_is_overdue(self, queryset, name, value):
        if value:
            return queryset.filter(case__due_date__lt=models.functions.Now())
        return queryset