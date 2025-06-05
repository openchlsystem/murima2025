from django.urls import path
from .views import *

urlpatterns = [
    # System Configuration
    path('system-config/', SystemConfigurationListCreateView.as_view()),
    path('system-config/<int:pk>/', SystemConfigurationRetrieveUpdateDestroyView.as_view()),

    # Tenant Configuration
    path('tenant-config/', TenantConfigurationListCreateView.as_view()),
    path('tenant-config/<int:pk>/', TenantConfigurationRetrieveUpdateDestroyView.as_view()),

    # Audit Log
    path('audit-logs/', AuditLogListView.as_view()),
    path('audit-logs/<int:pk>/', AuditLogDetailView.as_view()),

    # Category Types
    path('category-types/', CategoryTypeListCreateView.as_view()),
    path('category-types/<int:pk>/', CategoryTypeRetrieveUpdateDestroyView.as_view()),

    # Categories
    path('categories/', CategoryListCreateView.as_view()),
    path('categories/<int:pk>/', CategoryRetrieveUpdateDestroyView.as_view()),

    # System Notifications
    path('system-notifications/', SystemNotificationListCreateView.as_view()),
    path('system-notifications/<int:pk>/', SystemNotificationRetrieveUpdateDestroyView.as_view()),
]
