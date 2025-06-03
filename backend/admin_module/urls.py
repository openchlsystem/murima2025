
from django.urls import path
from . import views

urlpatterns = [
    path('system-configuration/', views.SystemConfigurationViewList.as_view(), name='system-configuration-list'),
    path('system-configuration/<int:pk>/', views.SystemConfigurationViewDetail.as_view(), name='system-configuration-detail'),
    path('audit-logs/', views.AuditLogListCreateView.as_view(), name='audit-log-list'),
    path('audit-logs/<int:pk>/', views.AuditLogDetailView.as_view(), name='audit-log-detail'),
]
