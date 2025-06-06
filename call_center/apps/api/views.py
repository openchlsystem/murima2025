# apps/api/views.py
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone

class AuditedModelViewSet(viewsets.ModelViewSet):
    """
    ViewSet for models that need audit tracking.
    Automatically sets created_by and handles audit logging.
    """
    
    def perform_create(self, serializer):
        """Set created_by when creating objects."""
        serializer.save(created_by=self.request.user)
        
        # Log the creation
        from apps.core.services import AuditService # type: ignore
        AuditService.log_activity(
            user=self.request.user,
            action='create',
            entity_type=self.get_serializer().Meta.model.__name__.lower(),
            entity_id=serializer.instance.id,
            new_values=serializer.data,
            ip_address=self.request.META.get('REMOTE_ADDR'),
            user_agent=self.request.META.get('HTTP_USER_AGENT')
        )
    
    def perform_update(self, serializer):
        """Log the update."""
        # Get the old values
        old_values = {}
        for field in serializer.fields:
            if field in serializer.validated_data:
                old_values[field] = getattr(serializer.instance, field)
        
        # Save the changes
        serializer.save()
        
        # Log the update
        from apps.core.services import AuditService # type: ignore
        AuditService.log_activity(
            user=self.request.user,
            action='update',
            entity_type=self.get_serializer().Meta.model.__name__.lower(),
            entity_id=serializer.instance.id,
            old_values=old_values,
            new_values=serializer.validated_data,
            ip_address=self.request.META.get('REMOTE_ADDR'),
            user_agent=self.request.META.get('HTTP_USER_AGENT')
        )

class ReadOnlyAuditViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for providing read-only access with audit logging.
    """
    
    def retrieve(self, request, *args, **kwargs):
        """Log access to the detail view."""
        response = super().retrieve(request, *args, **kwargs)
        
        # Log the view access
        from apps.core.services import AuditService # type: ignore
        AuditService.log_activity(
            user=request.user,
            action='view',
            entity_type=self.get_serializer().Meta.model.__name__.lower(),
            entity_id=kwargs.get('pk'),
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT')
        )
        
        return response