# apps/core/permissions.py
from rest_framework import permissions
from rest_framework.permissions import BasePermission
from django.contrib.auth.models import AnonymousUser
from django.utils.translation import gettext_lazy as _
from typing import Any
import logging

logger = logging.getLogger(__name__)


class IsAuthenticated(BasePermission):
    """
    Custom authentication permission that works with our multi-tenant setup.
    Allows access only to authenticated users with active accounts.
    """
    message = _('Authentication credentials were not provided or are invalid.')
    
    def has_permission(self, request, view):
        """
        Check if user is authenticated and active.
        """
        return bool(
            request.user and
            not isinstance(request.user, AnonymousUser) and
            request.user.is_authenticated and
            request.user.is_active
        )


class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    Read permissions are allowed to any request.
    """
    message = _('You can only modify your own records.')
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the record.
        return obj.created_by == request.user


class IsAgentOrAbove(BasePermission):
    """
    Permission class for users with agent role or higher.
    Hierarchy: agent < supervisor < manager < admin
    """
    message = _('You need agent level access or higher to perform this action.')
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        allowed_roles = ['agent', 'supervisor', 'manager', 'admin']
        return request.user.role in allowed_roles


class IsSupervisorOrAbove(BasePermission):
    """
    Permission class for users with supervisor role or higher.
    """
    message = _('You need supervisor level access or higher to perform this action.')
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        allowed_roles = ['supervisor', 'manager', 'admin']
        return request.user.role in allowed_roles


class IsManagerOrAbove(BasePermission):
    """
    Permission class for users with manager role or higher.
    """
    message = _('You need manager level access or higher to perform this action.')
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        allowed_roles = ['manager', 'admin']
        return request.user.role in allowed_roles


class IsAdminUser(BasePermission):
    """
    Permission class for admin users only.
    """
    message = _('You need admin access to perform this action.')
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        return request.user.role == 'admin' or request.user.is_superuser


class IsReadOnlyOrAgent(BasePermission):
    """
    Permission that allows read access to everyone but write access only to agents and above.
    """
    message = _('You need agent level access or higher to modify this resource.')
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Read permissions for all authenticated users
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions for agents and above
        allowed_roles = ['agent', 'supervisor', 'manager', 'admin']
        return request.user.role in allowed_roles


class CanHandleCases(BasePermission):
    """
    Permission for users who can handle cases (agents, supervisors, managers, admins).
    """
    message = _('You are not authorized to handle cases.')
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        allowed_roles = ['agent', 'supervisor', 'manager', 'admin']
        return request.user.role in allowed_roles and request.user.is_active


class CanEscalateCases(BasePermission):
    """
    Permission for users who can escalate cases (supervisors, managers, admins).
    """
    message = _('You are not authorized to escalate cases.')
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        allowed_roles = ['supervisor', 'manager', 'admin']
        return request.user.role in allowed_roles and request.user.is_active


class CanManageUsers(BasePermission):
    """
    Permission for users who can manage other users (managers, admins).
    """
    message = _('You are not authorized to manage users.')
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        allowed_roles = ['manager', 'admin']
        return request.user.role in allowed_roles and request.user.is_active


class CanAccessReports(BasePermission):
    """
    Permission for users who can access reports and analytics.
    """
    message = _('You are not authorized to access reports.')
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # All authenticated users can access basic reports
        # Detailed reports might require higher permissions
        return request.user.is_active


class CanAccessConfidentialData(BasePermission):
    """
    Permission for accessing confidential case data.
    """
    message = _('You are not authorized to access confidential data.')
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Only supervisors and above can access confidential data
        allowed_roles = ['supervisor', 'manager', 'admin']
        return request.user.role in allowed_roles and request.user.is_active


class IsAssignedToCase(BasePermission):
    """
    Permission that checks if user is assigned to a specific case.
    """
    message = _('You are not assigned to this case.')
    
    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Check if user is assigned to the case or escalated to
        if hasattr(obj, 'assigned_to') and obj.assigned_to == request.user:
            return True
        if hasattr(obj, 'escalated_to') and obj.escalated_to == request.user:
            return True
        if hasattr(obj, 'created_by') and obj.created_by == request.user:
            return True
        
        # Supervisors and above can access all cases
        allowed_roles = ['supervisor', 'manager', 'admin']
        return request.user.role in allowed_roles


class CanViewCaseDetails(BasePermission):
    """
    Permission for viewing detailed case information.
    Combines multiple checks for case access.
    """
    message = _('You are not authorized to view this case details.')
    
    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Case object
        case = obj
        if hasattr(obj, 'case'):
            case = obj.case
        
        # Check assignment
        if case.assigned_to == request.user:
            return True
        if case.escalated_to == request.user:
            return True
        if case.created_by == request.user:
            return True
        
        # Check if user has role permissions
        if request.user.role in ['supervisor', 'manager', 'admin']:
            return True
        
        # Check if user is in the same team/department (if implemented)
        # This could be extended based on organizational structure
        
        return False


class CanModifyCase(BasePermission):
    """
    Permission for modifying cases.
    More restrictive than viewing.
    """
    message = _('You are not authorized to modify this case.')
    
    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Case object
        case = obj
        if hasattr(obj, 'case'):
            case = obj.case
        
        # Read permissions
        if request.method in permissions.SAFE_METHODS:
            return CanViewCaseDetails().has_object_permission(request, view, obj)
        
        # Write permissions - must be assigned or have supervisor+ role
        if case.assigned_to == request.user:
            return True
        if case.escalated_to == request.user:
            return True
        
        # Supervisors and above can modify any case
        allowed_roles = ['supervisor', 'manager', 'admin']
        return request.user.role in allowed_roles


class TenantPermission(BasePermission):
    """
    Permission that ensures users can only access data within their tenant.
    This works with django-tenants to provide tenant isolation.
    """
    message = _('You do not have access to this tenant data.')
    
    def has_permission(self, request, view):
        # Basic authentication check
        if not request.user or not request.user.is_authenticated:
            return False
        
        # In a multi-tenant setup, this would check tenant membership
        # For now, we'll allow all authenticated users
        return True
    
    def has_object_permission(self, request, view, obj):
        # This could check if the object belongs to the user's tenant
        # Implementation would depend on your tenant model structure
        return True


class IsCreatorOrSupervisor(BasePermission):
    """
    Permission that allows access to the creator of an object or supervisors.
    """
    message = _('You can only access records you created or you need supervisor access.')
    
    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Allow access to creators
        if hasattr(obj, 'created_by') and obj.created_by == request.user:
            return True
        if hasattr(obj, 'author') and obj.author == request.user:
            return True
        if hasattr(obj, 'user') and obj.user == request.user:
            return True
        
        # Allow access to supervisors and above
        allowed_roles = ['supervisor', 'manager', 'admin']
        return request.user.role in allowed_roles


class DynamicRolePermission(BasePermission):
    """
    Dynamic permission class that accepts required roles during initialization.
    Usage: DynamicRolePermission(['supervisor', 'manager'])
    """
    
    def __init__(self, required_roles=None):
        self.required_roles = required_roles or []
        super().__init__()
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        if not self.required_roles:
            return True
        
        return request.user.role in self.required_roles and request.user.is_active


class TimeBasedPermission(BasePermission):
    """
    Permission that checks if current time is within allowed working hours.
    Useful for restricting certain operations to business hours.
    """
    message = _('This operation is only allowed during business hours.')
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Basic implementation - this could be enhanced with
        # per-tenant working hours, timezone handling, etc.
        from django.utils import timezone
        
        now = timezone.now()
        current_hour = now.hour
        
        # Allow operations between 6 AM and 10 PM
        business_hours = range(6, 22)
        
        # Admins can always perform operations
        if request.user.role == 'admin':
            return True
        
        # Emergency operations (POST to certain endpoints) are always allowed
        emergency_views = ['emergency', 'urgent', 'critical']
        if any(keyword in str(view.__class__.__name__).lower() for keyword in emergency_views):
            return True
        
        return current_hour in business_hours


class CombinedPermission(BasePermission):
    """
    Utility class to combine multiple permissions with AND logic.
    Usage: CombinedPermission([IsAuthenticated, CanHandleCases])
    """
    
    def __init__(self, permission_classes):
        self.permission_classes = permission_classes
    
    def has_permission(self, request, view):
        for permission_class in self.permission_classes:
            permission = permission_class()
            if not permission.has_permission(request, view):
                return False
        return True
    
    def has_object_permission(self, request, view, obj):
        for permission_class in self.permission_classes:
            permission = permission_class()
            if hasattr(permission, 'has_object_permission'):
                if not permission.has_object_permission(request, view, obj):
                    return False
        return True


# Utility functions for permission checking
def user_can_handle_cases(user) -> bool:
    """Check if user can handle cases"""
    if not user or not user.is_authenticated:
        return False
    return user.role in ['agent', 'supervisor', 'manager', 'admin'] and user.is_active


def user_can_escalate_cases(user) -> bool:
    """Check if user can escalate cases"""
    if not user or not user.is_authenticated:
        return False
    return user.role in ['supervisor', 'manager', 'admin'] and user.is_active


def user_can_access_confidential(user) -> bool:
    """Check if user can access confidential data"""
    if not user or not user.is_authenticated:
        return False
    return user.role in ['supervisor', 'manager', 'admin'] and user.is_active


def user_can_manage_users(user) -> bool:
    """Check if user can manage other users"""
    if not user or not user.is_authenticated:
        return False
    return user.role in ['manager', 'admin'] and user.is_active


def get_user_permission_level(user) -> int:
    """Get numeric permission level for user"""
    if not user or not user.is_authenticated:
        return 0
    
    role_levels = {
        'agent': 1,
        'supervisor': 2,
        'manager': 3,
        'admin': 4
    }
    
    return role_levels.get(user.role, 0)


def user_has_minimum_role(user, required_role: str) -> bool:
    """Check if user has minimum required role level"""
    user_level = get_user_permission_level(user)
    required_level = get_user_permission_level(type('obj', (), {'role': required_role, 'is_authenticated': True}))
    
    return user_level >= required_level


# Permission mixins for views
class AgentRequiredMixin:
    """Mixin to require agent level access"""
    permission_classes = [IsAuthenticated, IsAgentOrAbove]


class SupervisorRequiredMixin:
    """Mixin to require supervisor level access"""
    permission_classes = [IsAuthenticated, IsSupervisorOrAbove]


class ManagerRequiredMixin:
    """Mixin to require manager level access"""
    permission_classes = [IsAuthenticated, IsManagerOrAbove]


class AdminRequiredMixin:
    """Mixin to require admin access"""
    permission_classes = [IsAuthenticated, IsAdminUser]


class CaseHandlerMixin:
    """Mixin for case-related views"""
    permission_classes = [IsAuthenticated, CanHandleCases]


class ConfidentialDataMixin:
    """Mixin for confidential data access"""
    permission_classes = [IsAuthenticated, CanAccessConfidentialData]