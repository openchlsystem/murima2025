"""
Tenants App Views

Provides comprehensive views for tenant management including:
- Platform admin views (cross-tenant management)
- Tenant self-management views
- Public views (invitation acceptance, etc.)
- Bulk operations and utilities
"""

import uuid
from datetime import timedelta
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.models import Q, Count, Sum
from django.db import transaction
from django.http import Http404
from django.core.exceptions import ValidationError as DjangoValidationError
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework import status, permissions
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import ValidationError, PermissionDenied, NotFound
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import Tenant, Domain, TenantInvitation, TenantSettings
from .serializers import (
    TenantListSerializer, TenantDetailSerializer, TenantCreateSerializer,
    TenantPublicSerializer, DomainSerializer, TenantInvitationSerializer,
    TenantInvitationAcceptSerializer, TenantSettingsSerializer,
    BulkTenantActionSerializer
)

User = get_user_model()


# Custom Permissions (will be moved to accounts app later)
class IsPlatformAdmin(permissions.BasePermission):
    """Permission for platform administrators only."""
    
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            getattr(request.user, 'is_platform_admin', request.user.is_superuser)
        )


class IsTenantOwnerOrAdmin(permissions.BasePermission):
    """Permission for tenant owners and admins."""
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # For now, allow tenant owners and superusers
        # This will be enhanced when accounts app is available
        if hasattr(obj, 'owner'):
            return obj.owner == request.user or request.user.is_superuser
        elif hasattr(obj, 'tenant'):
            return obj.tenant.owner == request.user or request.user.is_superuser
        return request.user.is_superuser


class TenantPagination(PageNumberPagination):
    """Custom pagination for tenant lists."""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


# Platform Admin Views (Cross-tenant management)

class PlatformTenantViewSet(ModelViewSet):
    """
    Platform admin viewset for managing all tenants.
    Provides full CRUD operations and bulk actions.
    """
    
    queryset = Tenant.objects.all().select_related('owner').annotate(
        user_count=Count('tenantmembership', distinct=True),
        domain_count=Count('domains', distinct=True)
    )
    permission_classes = [IsPlatformAdmin]
    pagination_class = TenantPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['sector', 'subscription_plan', 'is_active', 'require_2fa']
    search_fields = ['name', 'subdomain', 'primary_contact_email', 'owner__email']
    ordering_fields = ['name', 'created_at', 'subscription_expires_at', 'user_count']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'list':
            return TenantListSerializer
        elif self.action == 'create':
            return TenantCreateSerializer
        else:
            return TenantDetailSerializer
    
    def perform_create(self, serializer):
        """Create tenant with automatic domain setup."""
        tenant = serializer.save()
        
        # Create audit log entry
        # Note: This will be enhanced when core.utils is available
        
        return tenant
    
    @action(detail=False, methods=['post'])
    def bulk_action(self, request):
        """Perform bulk actions on multiple tenants."""
        serializer = BulkTenantActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        tenant_ids = serializer.validated_data['tenant_ids']
        action_type = serializer.validated_data['action']
        reason = serializer.validated_data.get('reason', '')
        
        tenants = Tenant.objects.filter(schema_name__in=tenant_ids)
        results = {'success': [], 'errors': []}
        
        with transaction.atomic():
            for tenant in tenants:
                try:
                    if action_type == 'activate':
                        tenant.is_active = True
                        tenant.save()
                        results['success'].append(f"Activated {tenant.name}")
                    
                    elif action_type == 'deactivate':
                        tenant.is_active = False
                        tenant.save()
                        results['success'].append(f"Deactivated {tenant.name}")
                    
                    elif action_type == 'extend_trial':
                        days = serializer.validated_data.get('trial_extension_days', 7)
                        if tenant.trial_ends_at:
                            tenant.trial_ends_at += timedelta(days=days)
                            tenant.save()
                            results['success'].append(f"Extended trial for {tenant.name} by {days} days")
                        else:
                            results['errors'].append(f"{tenant.name} is not on trial")
                    
                    elif action_type == 'change_plan':
                        new_plan = serializer.validated_data['subscription_plan']
                        old_plan = tenant.subscription_plan
                        tenant.subscription_plan = new_plan
                        tenant.save()
                        results['success'].append(f"Changed {tenant.name} from {old_plan} to {new_plan}")
                
                except Exception as e:
                    results['errors'].append(f"Error with {tenant.name}: {str(e)}")
        
        return Response({
            'message': f"Bulk action '{action_type}' completed",
            'results': results,
            'reason': reason
        })
    
    @action(detail=True, methods=['post'])
    def verify_domains(self, request, pk=None):
        """Verify all domains for a tenant."""
        tenant = self.get_object()
        domains = tenant.domains.filter(verified_at__isnull=True)
        
        verified_count = 0
        for domain in domains:
            domain.mark_as_verified()
            verified_count += 1
        
        return Response({
            'message': f"Verified {verified_count} domain(s) for {tenant.name}",
            'verified_domains': [d.domain for d in domains]
        })
    
    @action(detail=True, methods=['get'])
    def usage_report(self, request, pk=None):
        """Get detailed usage report for a tenant."""
        tenant = self.get_object()
        
        # This would be expanded with actual usage data when other apps are built
        usage_data = {
            'tenant': TenantListSerializer(tenant).data,
            'usage_stats': tenant.get_usage_stats(),
            'subscription_info': {
                'plan': tenant.subscription_plan,
                'is_trial': tenant.is_trial,
                'trial_days_remaining': tenant.trial_days_remaining,
                'subscription_expires_at': tenant.subscription_expires_at,
                'is_expired': tenant.is_subscription_expired
            },
            'limits': {
                'max_users': tenant.max_users,
                'max_storage_mb': tenant.max_storage_mb,
                'max_monthly_calls': tenant.max_monthly_calls,
                'max_monthly_sms': tenant.max_monthly_sms
            },
            'domains': [
                {
                    'domain': d.domain,
                    'is_primary': d.is_primary,
                    'is_verified': d.is_verified,
                    'is_custom': d.is_custom
                }
                for d in tenant.domains.all()
            ]
        }
        
        return Response(usage_data)
    
    @action(detail=False, methods=['get'])
    def platform_statistics(self, request):
        """Get platform-wide statistics."""
        stats = {
            'total_tenants': Tenant.objects.count(),
            'active_tenants': Tenant.objects.filter(is_active=True).count(),
            'trial_tenants': Tenant.objects.filter(subscription_plan='trial').count(),
            'expired_trials': Tenant.objects.filter(
                subscription_plan='trial',
                trial_ends_at__lt=timezone.now()
            ).count(),
            'tenants_by_sector': dict(
                Tenant.objects.values_list('sector').annotate(
                    count=Count('id')
                )
            ),
            'tenants_by_plan': dict(
                Tenant.objects.values_list('subscription_plan').annotate(
                    count=Count('id')
                )
            ),
            'recent_signups': Tenant.objects.filter(
                created_at__gte=timezone.now() - timedelta(days=30)
            ).count(),
        }
        
        return Response(stats)


class PlatformDomainViewSet(ModelViewSet):
    """Platform admin viewset for managing all domains."""
    
    queryset = Domain.objects.all().select_related('tenant')
    serializer_class = DomainSerializer
    permission_classes = [IsPlatformAdmin]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_primary', 'is_custom', 'tenant']
    search_fields = ['domain', 'tenant__name']
    ordering = ['-created_at']
    
    @action(detail=False, methods=['post'])
    def bulk_verify(self, request):
        """Bulk verify domains."""
        domain_ids = request.data.get('domain_ids', [])
        if not domain_ids:
            return Response(
                {'error': 'No domain IDs provided'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        domains = Domain.objects.filter(id__in=domain_ids, verified_at__isnull=True)
        verified_count = 0
        
        for domain in domains:
            domain.mark_as_verified()
            verified_count += 1
        
        return Response({
            'message': f"Verified {verified_count} domain(s)",
            'verified_domains': [d.domain for d in domains]
        })


# Tenant Self-Management Views

class TenantSelfManagementViewSet(ModelViewSet):
    """
    Viewset for tenant owners/admins to manage their own tenant.
    """
    
    serializer_class = TenantDetailSerializer
    permission_classes = [IsTenantOwnerOrAdmin]
    
    def get_queryset(self):
        """Return only the user's own tenants."""
        if self.request.user.is_superuser:
            return Tenant.objects.all()
        return Tenant.objects.filter(owner=self.request.user)
    
    def get_object(self):
        """Get tenant object with permission check."""
        obj = super().get_object()
        self.check_object_permissions(self.request, obj)
        return obj
    
    @action(detail=True, methods=['get'])
    def settings(self, request, pk=None):
        """Get all settings for this tenant."""
        tenant = self.get_object()
        settings = TenantSettings.objects.filter(tenant=tenant)
        serializer = TenantSettingsSerializer(settings, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def update_branding(self, request, pk=None):
        """Update tenant branding settings."""
        tenant = self.get_object()
        branding_data = request.data.get('branding_settings', {})
        
        # Validate branding data structure
        allowed_keys = ['logo_url', 'primary_color', 'secondary_color', 'font_family', 'custom_css']
        filtered_branding = {k: v for k, v in branding_data.items() if k in allowed_keys}
        
        tenant.branding_settings.update(filtered_branding)
        tenant.save(update_fields=['branding_settings'])
        
        return Response({
            'message': 'Branding updated successfully',
            'branding_settings': tenant.branding_settings
        })
    
    @action(detail=True, methods=['post'])
    def toggle_feature(self, request, pk=None):
        """Enable or disable a feature for this tenant."""
        tenant = self.get_object()
        feature_name = request.data.get('feature_name')
        enabled = request.data.get('enabled', True)
        
        if not feature_name:
            return Response(
                {'error': 'feature_name is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if enabled:
            tenant.enable_feature(feature_name)
        else:
            tenant.disable_feature(feature_name)
        
        return Response({
            'message': f"Feature '{feature_name}' {'enabled' if enabled else 'disabled'}",
            'feature_flags': tenant.feature_flags
        })


class TenantInvitationViewSet(ModelViewSet):
    """
    Viewset for managing tenant invitations.
    """
    
    serializer_class = TenantInvitationSerializer
    permission_classes = [IsTenantOwnerOrAdmin]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'role_name']
    search_fields = ['email']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Return invitations for user's tenants only."""
        if self.request.user.is_superuser:
            return TenantInvitation.objects.all().select_related(
                'tenant', 'invited_by', 'accepted_by', 'revoked_by'
            )
        
        user_tenants = Tenant.objects.filter(owner=self.request.user)
        return TenantInvitation.objects.filter(
            tenant__in=user_tenants
        ).select_related('tenant', 'invited_by', 'accepted_by', 'revoked_by')
    
    def perform_create(self, serializer):
        """Create invitation with proper user context."""
        serializer.save(invited_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def send_reminder(self, request, pk=None):
        """Send reminder email for this invitation."""
        invitation = self.get_object()
        
        if not invitation.is_pending:
            return Response(
                {'error': 'Can only send reminders for pending invitations'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        success = invitation.send_reminder()
        
        if success:
            return Response({'message': 'Reminder sent successfully'})
        else:
            return Response(
                {'error': 'Failed to send reminder'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'])
    def revoke(self, request, pk=None):
        """Revoke this invitation."""
        invitation = self.get_object()
        reason = request.data.get('reason', '')
        
        try:
            invitation.revoke(user=request.user, reason=reason)
            return Response({'message': 'Invitation revoked successfully'})
        except DjangoValidationError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['post'])
    def bulk_send_reminders(self, request):
        """Send reminders for multiple invitations."""
        invitation_ids = request.data.get('invitation_ids', [])
        invitations = self.get_queryset().filter(
            id__in=invitation_ids,
            status='pending'
        )
        
        sent_count = 0
        for invitation in invitations:
            if invitation.send_reminder():
                sent_count += 1
        
        return Response({
            'message': f"Sent {sent_count} reminder(s)",
            'total_requested': len(invitation_ids)
        })


class TenantSettingsViewSet(ModelViewSet):
    """
    Viewset for managing tenant settings.
    """
    
    serializer_class = TenantSettingsSerializer
    permission_classes = [IsTenantOwnerOrAdmin]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['category', 'setting_type', 'is_sensitive', 'is_system']
    search_fields = ['key', 'name', 'description']
    
    def get_queryset(self):
        """Return settings for user's tenants only."""
        if self.request.user.is_superuser:
            return TenantSettings.objects.all().select_related('tenant')
        
        user_tenants = Tenant.objects.filter(owner=self.request.user)
        return TenantSettings.objects.filter(
            tenant__in=user_tenants
        ).select_related('tenant')
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Get settings grouped by category."""
        queryset = self.get_queryset()
        tenant_id = request.query_params.get('tenant')
        
        if tenant_id:
            queryset = queryset.filter(tenant__schema_name=tenant_id)
        
        # Group by category
        categories = {}
        for setting in queryset:
            if setting.category not in categories:
                categories[setting.category] = []
            categories[setting.category].append(
                TenantSettingsSerializer(setting).data
            )
        
        return Response(categories)
    
    @action(detail=False, methods=['post'])
    def bulk_update(self, request):
        """Update multiple settings at once."""
        settings_data = request.data.get('settings', [])
        updated_count = 0
        errors = []
        
        with transaction.atomic():
            for setting_data in settings_data:
                try:
                    setting_id = setting_data.get('id')
                    if not setting_id:
                        continue
                    
                    setting = self.get_queryset().get(id=setting_id)
                    serializer = TenantSettingsSerializer(
                        setting, 
                        data=setting_data, 
                        partial=True
                    )
                    
                    if serializer.is_valid():
                        serializer.save(updated_by=request.user)
                        updated_count += 1
                    else:
                        errors.append({
                            'setting_id': setting_id,
                            'errors': serializer.errors
                        })
                
                except TenantSettings.DoesNotExist:
                    errors.append({
                        'setting_id': setting_data.get('id'),
                        'errors': 'Setting not found'
                    })
        
        return Response({
            'message': f"Updated {updated_count} setting(s)",
            'errors': errors
        })


# Public Views (No authentication required)

@api_view(['GET'])
@permission_classes([AllowAny])
def tenant_public_info(request, subdomain):
    """
    Get public information about a tenant by subdomain.
    Used for branding and public-facing information.
    """
    try:
        tenant = Tenant.objects.get(subdomain=subdomain, is_active=True)
        serializer = TenantPublicSerializer(tenant)
        return Response(serializer.data)
    except Tenant.DoesNotExist:
        return Response(
            {'error': 'Tenant not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def invitation_details(request, token):
    """
    Get invitation details by token (for invitation acceptance page).
    """
    try:
        invitation = TenantInvitation.objects.select_related('tenant').get(token=token)
        
        if not invitation.is_pending:
            return Response(
                {'error': 'Invitation is no longer valid'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if invitation.is_expired:
            return Response(
                {'error': 'Invitation has expired'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response({
            'tenant_name': invitation.tenant.name,
            'email': invitation.email,
            'role_name': invitation.role_name,
            'invited_by': invitation.invited_by.get_full_name() or invitation.invited_by.email,
            'message': invitation.message,
            'expires_at': invitation.expires_at,
            'days_until_expiry': invitation.days_until_expiry
        })
    
    except TenantInvitation.DoesNotExist:
        return Response(
            {'error': 'Invalid invitation token'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_invitation(request):
    """
    Accept a tenant invitation.
    """
    serializer = TenantInvitationAcceptSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    token = serializer.validated_data['token']
    
    try:
        invitation = TenantInvitation.objects.select_related('tenant').get(token=token)
        
        # Accept the invitation
        invitation.accept(user=request.user)
        
        # Note: Creating TenantMembership would happen here
        # when accounts app is available
        
        return Response({
            'message': 'Invitation accepted successfully',
            'tenant': {
                'name': invitation.tenant.name,
                'subdomain': invitation.tenant.subdomain,
                'url': invitation.tenant.get_absolute_url()
            },
            'role': invitation.role_name
        })
    
    except TenantInvitation.DoesNotExist:
        return Response(
            {'error': 'Invalid invitation token'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    except DjangoValidationError as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )


# Health Check and Utility Views

@api_view(['GET'])
@permission_classes([AllowAny])
@method_decorator(cache_page(60 * 5))  # Cache for 5 minutes
def health_check(request):
    """
    Basic health check endpoint.
    """
    try:
        # Simple database connectivity check
        tenant_count = Tenant.objects.count()
        
        return Response({
            'status': 'healthy',
            'timestamp': timezone.now().isoformat(),
            'tenant_count': tenant_count,
            'database': 'connected'
        })
    
    except Exception as e:
        return Response({
            'status': 'unhealthy',
            'timestamp': timezone.now().isoformat(),
            'error': str(e),
            'database': 'error'
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)


@api_view(['GET'])
@permission_classes([IsPlatformAdmin])
def system_status(request):
    """
    Detailed system status for platform administrators.
    """
    try:
        now = timezone.now()
        
        # Basic statistics
        total_tenants = Tenant.objects.count()
        active_tenants = Tenant.objects.filter(is_active=True).count()
        trial_tenants = Tenant.objects.filter(subscription_plan='trial').count()
        
        # Expiring trials (next 7 days)
        expiring_trials = Tenant.objects.filter(
            subscription_plan='trial',
            trial_ends_at__lte=now + timedelta(days=7),
            trial_ends_at__gt=now
        ).count()
        
        # Expired trials
        expired_trials = Tenant.objects.filter(
            subscription_plan='trial',
            trial_ends_at__lte=now
        ).count()
        
        # Pending invitations
        pending_invitations = TenantInvitation.objects.filter(
            status='pending',
            expires_at__gt=now
        ).count()
        
        # Recent signups (last 24 hours)
        recent_signups = Tenant.objects.filter(
            created_at__gte=now - timedelta(hours=24)
        ).count()
        
        return Response({
            'status': 'healthy',
            'timestamp': now.isoformat(),
            'statistics': {
                'total_tenants': total_tenants,
                'active_tenants': active_tenants,
                'trial_tenants': trial_tenants,
                'expiring_trials': expiring_trials,
                'expired_trials': expired_trials,
                'pending_invitations': pending_invitations,
                'recent_signups_24h': recent_signups
            },
            'alerts': {
                'expired_trials': expired_trials > 0,
                'expiring_trials_soon': expiring_trials > 0
            }
        })
    
    except Exception as e:
        return Response({
            'status': 'error',
            'timestamp': now.isoformat(),
            'error': str(e)
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)


# Subdomain validation utility

@api_view(['POST'])
@permission_classes([AllowAny])
def validate_subdomain(request):
    """
    Validate subdomain availability and format.
    Public endpoint for tenant creation forms.
    """
    subdomain = request.data.get('subdomain', '').lower().strip()
    
    if not subdomain:
        return Response({
            'valid': False,
            'error': 'Subdomain is required'
        })
    
    # Use the same validation as in serializers
    try:
        from .serializers import TenantDetailSerializer
        serializer = TenantDetailSerializer()
        validated_subdomain = serializer.validate_subdomain(subdomain)
        
        # Check if already exists
        if Tenant.objects.filter(subdomain=validated_subdomain).exists():
            return Response({
                'valid': False,
                'error': 'Subdomain is already taken'
            })
        
        return Response({
            'valid': True,
            'subdomain': validated_subdomain,
            'url': f"https://{validated_subdomain}.murima.com"
        })
    
    except ValidationError as e:
        return Response({
            'valid': False,
            'error': str(e.detail[0]) if e.detail else 'Invalid subdomain'
        })