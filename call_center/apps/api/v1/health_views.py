# apps/api/v1/health_views.py
from django.http import JsonResponse
from django.db import connection
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json


@require_http_methods(["GET"])
def health_check(request):
    """Simple health check endpoint"""
    try:
        # Test database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        # Get tenant information
        tenant_info = {
            'schema_name': getattr(connection, 'schema_name', 'unknown'),
            'tenant_name': 'unknown'
        }
        
        # Try to get tenant details if we're in a tenant schema
        if hasattr(connection, 'tenant') and connection.tenant:
            tenant_info.update({
                'tenant_name': connection.tenant.name,
                'is_active': connection.tenant.is_active,
                'subscription_plan': getattr(connection.tenant, 'subscription_plan', 'unknown')
            })
        
        return JsonResponse({
            'status': 'healthy',
            'database': 'connected',
            'tenant': tenant_info,
            'message': 'Call Center System API is running'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'unhealthy',
            'error': str(e),
            'tenant': {
                'schema_name': getattr(connection, 'schema_name', 'unknown')
            }
        }, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class SystemInfoView(View):
    """System information endpoint"""
    
    def get(self, request):
        """Get system information"""
        try:
            # Database info
            with connection.cursor() as cursor:
                cursor.execute("SELECT version()")
                db_version = cursor.fetchone()[0] if cursor.rowcount > 0 else "Unknown"
            
            # Tenant info
            tenant_info = {
                'schema_name': getattr(connection, 'schema_name', 'public'),
                'is_public_schema': getattr(connection, 'schema_name', 'public') == 'public'
            }
            
            if hasattr(connection, 'tenant') and connection.tenant:
                tenant_info.update({
                    'tenant_id': connection.tenant.id,
                    'tenant_name': connection.tenant.name,
                    'is_active': connection.tenant.is_active,
                    'subscription_plan': getattr(connection.tenant, 'subscription_plan', 'unknown'),
                    'max_users': getattr(connection.tenant, 'max_users', 0),
                    'created_at': getattr(connection.tenant, 'created_at', None).isoformat() if getattr(connection.tenant, 'created_at', None) else None
                })
            
            # Count some basic stats if we're in a tenant schema
            stats = {}
            if getattr(connection, 'schema_name', 'public') != 'public':
                try:
                    from apps.accounts.models import User
                    stats['users_count'] = User.objects.count()
                    stats['active_users_count'] = User.objects.filter(is_active=True).count()
                    stats['online_users_count'] = User.objects.filter(is_online=True).count()
                except Exception as e:
                    stats['error'] = f"Could not get stats: {str(e)}"
            
            return JsonResponse({
                'status': 'success',
                'system': {
                    'database_version': db_version,
                    'django_version': '5.2+',
                },
                'tenant': tenant_info,
                'stats': stats
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'error': str(e),
                'tenant': {
                    'schema_name': getattr(connection, 'schema_name', 'unknown')
                }
            }, status=500)