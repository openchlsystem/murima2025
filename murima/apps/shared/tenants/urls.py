"""
Tenants App URLs

Provides URL routing for tenant management with clear separation between:
- Platform admin endpoints (cross-tenant management)
- Tenant self-management endpoints
- Public endpoints (invitations, health checks)
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

# Create routers for different API sections
platform_router = DefaultRouter()
tenant_router = DefaultRouter()
simple_router = SimpleRouter()

# Platform Admin Routes (cross-tenant management)
platform_router.register(
    r'tenants', 
    views.PlatformTenantViewSet, 
    basename='platform-tenant'
)
platform_router.register(
    r'domains', 
    views.PlatformDomainViewSet, 
    basename='platform-domain'
)

# Tenant Self-Management Routes
tenant_router.register(
    r'tenant', 
    views.TenantSelfManagementViewSet, 
    basename='tenant-self'
)
tenant_router.register(
    r'invitations', 
    views.TenantInvitationViewSet, 
    basename='tenant-invitation'
)
tenant_router.register(
    r'settings', 
    views.TenantSettingsViewSet, 
    basename='tenant-settings'
)

# App name for namespacing
app_name = 'tenants'

urlpatterns = [
    
    # ==============================================
    # PLATFORM ADMIN ENDPOINTS
    # ==============================================
    # These endpoints are for platform administrators
    # to manage all tenants across the platform
    
    path('api/platform/', include([
        # RESTful tenant and domain management
        path('', include(platform_router.urls)),
        
        # Additional platform admin endpoints
        path('statistics/', 
             views.PlatformTenantViewSet.as_view({'get': 'platform_statistics'}),
             name='platform-statistics'),
        
        path('system-status/', 
             views.system_status, 
             name='system-status'),
        
        # Bulk operations
        path('tenants/bulk-action/', 
             views.PlatformTenantViewSet.as_view({'post': 'bulk_action'}),
             name='platform-tenant-bulk-action'),
        
        path('domains/bulk-verify/', 
             views.PlatformDomainViewSet.as_view({'post': 'bulk_verify'}),
             name='platform-domain-bulk-verify'),
    ])),
    
    
    # ==============================================
    # TENANT SELF-MANAGEMENT ENDPOINTS  
    # ==============================================
    # These endpoints are for tenant owners/admins
    # to manage their own tenant
    
    path('api/v1/', include([
        # RESTful tenant self-management
        path('', include(tenant_router.urls)),
        
        # Specific tenant management actions
        path('tenant/<str:pk>/branding/', 
             views.TenantSelfManagementViewSet.as_view({'post': 'update_branding'}),
             name='tenant-update-branding'),
        
        path('tenant/<str:pk>/feature/', 
             views.TenantSelfManagementViewSet.as_view({'post': 'toggle_feature'}),
             name='tenant-toggle-feature'),
        
        path('tenant/<str:pk>/settings/', 
             views.TenantSelfManagementViewSet.as_view({'get': 'settings'}),
             name='tenant-settings-list'),
        
        # Invitation management
        path('invitations/<uuid:pk>/reminder/', 
             views.TenantInvitationViewSet.as_view({'post': 'send_reminder'}),
             name='invitation-send-reminder'),
        
        path('invitations/<uuid:pk>/revoke/', 
             views.TenantInvitationViewSet.as_view({'post': 'revoke'}),
             name='invitation-revoke'),
        
        path('invitations/bulk-reminders/', 
             views.TenantInvitationViewSet.as_view({'post': 'bulk_send_reminders'}),
             name='invitation-bulk-reminders'),
        
        # Settings management
        path('settings/by-category/', 
             views.TenantSettingsViewSet.as_view({'get': 'by_category'}),
             name='settings-by-category'),
        
        path('settings/bulk-update/', 
             views.TenantSettingsViewSet.as_view({'post': 'bulk_update'}),
             name='settings-bulk-update'),
    ])),
    
    
    # ==============================================
    # PUBLIC ENDPOINTS
    # ==============================================
    # These endpoints don't require authentication
    # and are used for public-facing functionality
    
    path('api/public/', include([
        # Tenant public information (for branding, etc.)
        path('tenant/<str:subdomain>/', 
             views.tenant_public_info, 
             name='tenant-public-info'),
        
        # Invitation handling (public access needed)
        path('invitation/<uuid:token>/', 
             views.invitation_details, 
             name='invitation-details'),
        
        path('invitation/accept/', 
             views.accept_invitation, 
             name='invitation-accept'),
        
        # Subdomain validation (for signup forms)
        path('validate-subdomain/', 
             views.validate_subdomain, 
             name='validate-subdomain'),
        
        # Health check
        path('health/', 
             views.health_check, 
             name='health-check'),
    ])),
    
    
    # ==============================================
    # LEGACY/ALTERNATIVE ENDPOINTS
    # ==============================================
    # Alternative URL patterns for backward compatibility
    # or different client needs
    
    # Direct tenant access by subdomain (alternative pattern)
    path('tenant/<str:subdomain>/', include([
        path('info/', 
             views.tenant_public_info, 
             name='tenant-info-alt'),
        
        # Could add more tenant-specific endpoints here
    ])),
    
    # Direct invitation access (alternative pattern)  
    path('invite/', include([
        path('<uuid:token>/', 
             views.invitation_details, 
             name='invitation-alt'),
        
        path('accept/', 
             views.accept_invitation, 
             name='invitation-accept-alt'),
    ])),
    
    
    # ==============================================
    # ADMIN UTILITIES
    # ==============================================
    # Utility endpoints for admin interfaces
    
    path('admin-api/', include([
        # Quick tenant lookup for admin interfaces
        path('tenant-lookup/', 
             views.PlatformTenantViewSet.as_view({'get': 'list'}),
             name='admin-tenant-lookup'),
        
        # System health for admin dashboard
        path('health-detailed/', 
             views.system_status, 
             name='admin-health-detailed'),
    ])),
    
]

# Add format suffix patterns for content negotiation (.json, .xml, etc.)
urlpatterns = format_suffix_patterns(urlpatterns)

# Additional URL patterns for specific use cases
additional_patterns = [
    
    # ==============================================
    # WEBHOOK ENDPOINTS
    # ==============================================
    # For future webhook integrations
    
    path('webhooks/', include([
        # Domain verification webhooks (future)
        path('domain-verification/', 
             views.health_check,  # Placeholder
             name='webhook-domain-verification'),
        
        # Payment webhooks (future)
        path('payment-status/', 
             views.health_check,  # Placeholder
             name='webhook-payment-status'),
    ])),
    
    
    # ==============================================
    # EXPORT ENDPOINTS
    # ==============================================
    # For data export functionality
    
    path('export/', include([
        # Tenant data export (future implementation)
        path('tenant-data/<str:tenant_id>/', 
             views.health_check,  # Placeholder
             name='export-tenant-data'),
        
        # Platform statistics export (future implementation)
        path('platform-stats/', 
             views.health_check,  # Placeholder
             name='export-platform-stats'),
    ])),
    
]

# Conditionally add additional patterns
# (could be controlled by settings or feature flags)
urlpatterns.extend(additional_patterns)

# URL pattern examples for different client types:

"""
USAGE EXAMPLES:

1. Platform Admin (managing all tenants):
   GET  /api/platform/tenants/                    # List all tenants
   POST /api/platform/tenants/                    # Create new tenant
   GET  /api/platform/tenants/{id}/               # Get tenant details
   PUT  /api/platform/tenants/{id}/               # Update tenant
   POST /api/platform/tenants/bulk-action/       # Bulk actions
   GET  /api/platform/statistics/                # Platform stats

2. Tenant Owner/Admin (managing own tenant):
   GET  /api/v1/tenant/                           # List own tenants
   GET  /api/v1/tenant/{id}/                      # Get own tenant details
   PUT  /api/v1/tenant/{id}/                      # Update own tenant
   POST /api/v1/tenant/{id}/branding/             # Update branding
   POST /api/v1/tenant/{id}/feature/              # Toggle features
   
   GET  /api/v1/invitations/                      # List invitations
   POST /api/v1/invitations/                      # Create invitation
   POST /api/v1/invitations/{id}/reminder/       # Send reminder
   
   GET  /api/v1/settings/                         # List settings
   POST /api/v1/settings/                         # Create setting
   GET  /api/v1/settings/by-category/             # Group by category

3. Public Access (no authentication):
   GET  /api/public/tenant/{subdomain}/           # Public tenant info
   GET  /api/public/invitation/{token}/           # Invitation details
   POST /api/public/invitation/accept/            # Accept invitation
   POST /api/public/validate-subdomain/           # Check availability
   GET  /api/public/health/                       # Health check

4. Alternative Patterns:
   GET  /tenant/{subdomain}/info/                 # Alternative tenant info
   GET  /invite/{token}/                          # Alternative invitation
   POST /invite/accept/                           # Alternative accept

5. Admin Utilities:
   GET  /admin-api/tenant-lookup/                 # Quick tenant search
   GET  /admin-api/health-detailed/               # Detailed system status

Frontend Integration Examples:

// Platform admin dashboard
const tenants = await fetch('/api/platform/tenants/');
const stats = await fetch('/api/platform/statistics/');

// Tenant admin panel  
const myTenant = await fetch('/api/v1/tenant/');
const invitations = await fetch('/api/v1/invitations/');

// Public signup form
const isValid = await fetch('/api/public/validate-subdomain/', {
  method: 'POST',
  body: JSON.stringify({subdomain: 'acme'})
});

// Invitation acceptance page
const invitation = await fetch(`/api/public/invitation/${token}/`);
await fetch('/api/public/invitation/accept/', {
  method: 'POST', 
  body: JSON.stringify({token})
});
"""