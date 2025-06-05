# apps/core/services.py
from django.db import transaction
from django.utils import timezone

class AuditService:
    """Service for handling audit logging."""
    
    @staticmethod
    def log_activity(user, action, entity_type, entity_id, old_values=None, new_values=None, ip_address=None, user_agent=None):
        """
        Log an audit entry for user activity.
        
        Args:
            user: The user performing the action
            action: The action performed (e.g., 'create', 'update', 'delete')
            entity_type: The type of entity affected (e.g., 'case', 'contact')
            entity_id: The ID of the entity affected
            old_values: Optional JSON of old values before change
            new_values: Optional JSON of new values after change
            ip_address: Optional IP address of the user
            user_agent: Optional user agent string
        """
        from apps.core.models import AuditLog
        
        AuditLog.objects.create(
            user=user,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            old_values=old_values,
            new_values=new_values,
            ip_address=ip_address,
            user_agent=user_agent
        )


class ReferenceDataService:
    """Service for managing reference data."""
    
    @staticmethod
    def get_by_category(category, active_only=True):
        """
        Get reference data items by category.
        
        Args:
            category: The category to filter by
            active_only: Only return active items if True
        
        Returns:
            QuerySet of ReferenceData objects
        """
        from apps.core.models import ReferenceData
        
        queryset = ReferenceData.objects.filter(category=category)
        
        if active_only:
            queryset = queryset.filter(is_active=True)
            
        return queryset.order_by('level', 'name')
    
    @staticmethod
    def get_choices(category, include_blank=True, active_only=True):
        """
        Get reference data items as choices for forms.
        
        Args:
            category: The category to filter by
            include_blank: Include a blank choice if True
            active_only: Only return active items if True
        
        Returns:
            List of (id, name) tuples for use in forms
        """
        queryset = ReferenceDataService.get_by_category(category, active_only)
        choices = [(item.id, item.name) for item in queryset]
        
        if include_blank:
            choices.insert(0, ('', '----------'))
            
        return choices