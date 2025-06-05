# config/urls_public.py
"""
URL configuration for the public schema.
This is used for tenant management and shared resources.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse

def public_schema_view(request):
    """Simple view for public schema"""
    return JsonResponse({
        'message': 'Call Center System - Public Schema',
        'schema': 'public',
        'version': '1.0.0',
        'available_endpoints': {
            'admin': '/admin/',
            'health_check': '/api/v1/health/',
            'system_info': '/api/v1/system/',
            'tenant_management': '/api/public/',
        }
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', public_schema_view, name='public_home'),
    
    # Include the same API endpoints as tenant schemas
    path('api/v1/', include('apps.api.v1.urls')),
    
    # Public-specific tenant management APIs
    path('api/public/', include('apps.tenant.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)