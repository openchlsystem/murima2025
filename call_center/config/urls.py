# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse

def home_view(request):
    """Simple home view"""
    from django.db import connection
    
    tenant_info = {
        'schema_name': getattr(connection, 'schema_name', 'unknown'),
        'message': 'Call Center System - Tenant Schema'
    }
    
    if hasattr(connection, 'tenant') and connection.tenant:
        tenant_info.update({
            'tenant_name': connection.tenant.name,
            'is_active': connection.tenant.is_active,
        })
    
    return JsonResponse({
        'status': 'success',
        'tenant': tenant_info,
        'available_endpoints': {
            'admin': '/admin/',
            'api_health': '/api/v1/health/',
            'api_system': '/api/v1/system/',
        }
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('apps.api.v1.urls')),
    path('', home_view, name='home'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
    
    # Serve media files in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)