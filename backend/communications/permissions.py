# communications/permissions.py
from rest_framework.permissions import BasePermission

class IsTenantMember(BasePermission):
    """
    Allows access only to users who belong to a tenant.
    """
    def has_permission(self, request, view):
        return hasattr(request.user, 'tenant')

    def has_object_permission(self, request, view, obj):
        # For models that have a tenant field
        if hasattr(obj, 'tenant'):
            return obj.tenant == request.user.tenant
        # For models that are related to tenant through a foreign key
        elif hasattr(obj, 'channel') and hasattr(obj.channel, 'tenant'):
            return obj.channel.tenant == request.user.tenant
        return False

class IsTenantAdmin(BasePermission):
    """
    Allows access only to tenant admin users.
    """
    def has_permission(self, request, view):
        return hasattr(request.user, 'tenant') and request.user.is_tenant_admin

    def has_object_permission(self, request, view, obj):
        if hasattr(request.user, 'is_tenant_admin'):
            return request.user.is_tenant_admin
        return False