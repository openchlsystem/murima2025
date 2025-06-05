# apps/api/permissions.py
from rest_framework import permissions

class IsOwnerOrStaff(permissions.BasePermission):
    """
    Object-level permission to only allow owners or staff to access an object.
    """
    
    def has_object_permission(self, request, view, obj):
        # Staff can access everything
        if request.user.is_staff:
            return True
            
        # Check if the object has a user field
        if hasattr(obj, 'user'):
            return obj.user == request.user
            
        # Check if the object has a created_by field
        if hasattr(obj, 'created_by'):
            return obj.created_by == request.user
            
        return False

class HasCasePermission(permissions.BasePermission):
    """
    Custom permission to handle case access.
    """
    
    def has_permission(self, request, view):
        # Standard permissions for list/create
        if view.action == 'list':
            return request.user.has_perm('cases.view_case')
        elif view.action == 'create':
            return request.user.has_perm('cases.add_case')
        return True
    
    def has_object_permission(self, request, view, obj):
        # Read permissions
        if request.method in permissions.SAFE_METHODS:
            return request.user.has_perm('cases.view_case')
            
        # Write permissions
        if view.action == 'update' or view.action == 'partial_update':
            return request.user.has_perm('cases.change_case')
        elif view.action == 'destroy':
            return request.user.has_perm('cases.delete_case')
            
        # Custom actions
        if view.action == 'close_case':
            return request.user.has_perm('cases.close_case')
        elif view.action == 'escalate':
            return request.user.has_perm('cases.escalate_case')
            
        return False