# apps/tenant/urls.py
from django.urls import path
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([AllowAny])
def tenant_info(request):
    """Get basic tenant information"""
    try:
        from django_tenants.utils import tenant_context
        from django.db import connection
        
        tenant = getattr(connection, 'tenant', None)
        if tenant:
            return Response({
                'tenant_name': tenant.name,
                'schema_name': tenant.schema_name,
                'is_active': tenant.is_active,
                'created_at': tenant.created_at,
            })
        else:
            return Response({
                'message': 'Public schema',
                'schema_name': 'public'
            })
    except Exception as e:
        return Response({
            'error': str(e),
            'message': 'Unable to get tenant info'
        }, status=500)

urlpatterns = [
    path('info/', tenant_info, name='tenant_info'),
]