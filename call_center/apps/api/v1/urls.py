# apps/api/v1/urls.py
from django.urls import path, include
from .health_views import health_check, SystemInfoView

app_name = 'api_v1'

urlpatterns = [
    # Health check endpoints
    path('health/', health_check, name='health_check'),
    path('system/', SystemInfoView.as_view(), name='system_info'),
    
    # Tenant management (available in all schemas)
    path('tenant/', include('apps.tenant.urls')),
]