from rest_framework import permissions
from django.contrib.auth import get_user_model

User = get_user_model()

class IsTenantUser(permissions.BasePermission):
    """
    Allows access only to users belonging to the current tenant.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request, 'tenant')

class IsTenantAdmin(permissions.BasePermission):
    """
    Allows access only to tenant admin users.
    """
    def has_permission(self, request, view):
        return (request.user.is_authenticated and 
                hasattr(request, 'tenant') and 
                request.user.is_tenant_admin)

class IsObjectOwnerOrTenantAdmin(permissions.BasePermission):
    """
    Allows access to object owners or tenant admins.
    """
    def has_object_permission(self, request, view, obj):
        # Check if the user is tenant admin
        if request.user.is_tenant_admin:
            return True
            
        # For objects that have created_by field
        if hasattr(obj, 'created_by'):
            return obj.created_by == request.user
            
        # For objects that have user field
        if hasattr(obj, 'user'):
            return obj.user == request.user
            
        return False

class IsContactOwnerOrTenantAdmin(permissions.BasePermission):
    """
    Special permission for contact-related objects.
    Allows access if user owns the contact or is tenant admin.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_tenant_admin:
            return True
            
        # Handle different object types
        if hasattr(obj, 'contact'):
            return obj.contact.created_by == request.user
        elif hasattr(obj, 'created_by'):
            return obj.created_by == request.user
            
        return False