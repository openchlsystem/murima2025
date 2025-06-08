"""
Accounts App URL Configuration

Defines URL patterns for authentication, user management,
tenant membership, and related functionality.

Includes both API endpoints and public invitation URLs.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    AuthViewSet, UserProfileViewSet, UserSessionViewSet,
    TenantMembershipViewSet, TenantRoleViewSet, UserInvitationViewSet,
    PlatformRoleViewSet, PublicInvitationView, HealthCheckView
)

# Create router for ViewSets
router = DefaultRouter()

# Authentication and user management
router.register(r'auth', AuthViewSet, basename='auth')
router.register(r'profile', UserProfileViewSet, basename='profile')
router.register(r'sessions', UserSessionViewSet, basename='sessions')

# Tenant management (these will be properly filtered by tenant when tenants app is ready)
router.register(r'memberships', TenantMembershipViewSet, basename='memberships')
router.register(r'roles', TenantRoleViewSet, basename='roles')
router.register(r'invitations', UserInvitationViewSet, basename='invitations')

# Platform administration
router.register(r'platform-roles', PlatformRoleViewSet, basename='platform-roles')

app_name = 'accounts'

urlpatterns = [
    # Health check endpoint
    path('health/', HealthCheckView.as_view(), name='health-check'),
    
    # Public invitation endpoints (no authentication required)
    path('invitation/<uuid:token>/', PublicInvitationView.as_view(), name='invitation-detail'),
    path('invitation/<uuid:token>/accept/', PublicInvitationView.as_view(), name='invitation-accept'),
    
    # API endpoints
    path('api/v1/', include(router.urls)),
    
    # Additional authentication endpoints (alternative URL structure)
    path('auth/register/', AuthViewSet.as_view({'post': 'register'}), name='register'),
    path('auth/login/', AuthViewSet.as_view({'post': 'login'}), name='login'),
    path('auth/logout/', AuthViewSet.as_view({'post': 'logout'}), name='logout'),
    path('auth/verify-2fa/', AuthViewSet.as_view({'post': 'verify_2fa'}), name='verify-2fa'),
    path('auth/request-otp/', AuthViewSet.as_view({'post': 'request_otp'}), name='request-otp'),
    path('auth/verify-otp/', AuthViewSet.as_view({'post': 'verify_otp'}), name='verify-otp'),
    path('auth/reset-password/', AuthViewSet.as_view({'post': 'reset_password_request'}), name='reset-password'),
    path('auth/reset-password-confirm/', AuthViewSet.as_view({'post': 'reset_password_confirm'}), name='reset-password-confirm'),
    
    # User profile endpoints
    path('profile/me/', UserProfileViewSet.as_view({'get': 'me'}), name='profile-me'),
    path('profile/update/', UserProfileViewSet.as_view({'put': 'update_profile', 'patch': 'update_profile'}), name='profile-update'),
    path('profile/change-password/', UserProfileViewSet.as_view({'post': 'change_password'}), name='change-password'),
    path('profile/enable-2fa/', UserProfileViewSet.as_view({'post': 'enable_2fa'}), name='enable-2fa'),
    path('profile/confirm-2fa/', UserProfileViewSet.as_view({'post': 'confirm_2fa_setup'}), name='confirm-2fa'),
    path('profile/disable-2fa/', UserProfileViewSet.as_view({'post': 'disable_2fa'}), name='disable-2fa'),
]

# URL patterns for different API versions (future extensibility)
v1_patterns = [
    # Authentication endpoints
    path('auth/register/', AuthViewSet.as_view({'post': 'register'}), name='v1-register'),
    path('auth/login/', AuthViewSet.as_view({'post': 'login'}), name='v1-login'),
    path('auth/logout/', AuthViewSet.as_view({'post': 'logout'}), name='v1-logout'),
    path('auth/verify-2fa/', AuthViewSet.as_view({'post': 'verify_2fa'}), name='v1-verify-2fa'),
    path('auth/otp/request/', AuthViewSet.as_view({'post': 'request_otp'}), name='v1-request-otp'),
    path('auth/otp/verify/', AuthViewSet.as_view({'post': 'verify_otp'}), name='v1-verify-otp'),
    path('auth/password/reset/', AuthViewSet.as_view({'post': 'reset_password_request'}), name='v1-reset-password'),
    path('auth/password/confirm/', AuthViewSet.as_view({'post': 'reset_password_confirm'}), name='v1-reset-password-confirm'),
    
    # User profile endpoints
    path('users/me/', UserProfileViewSet.as_view({'get': 'me'}), name='v1-user-me'),
    path('users/me/update/', UserProfileViewSet.as_view({'put': 'update_profile', 'patch': 'update_profile'}), name='v1-user-update'),
    path('users/me/password/', UserProfileViewSet.as_view({'post': 'change_password'}), name='v1-user-change-password'),
    path('users/me/2fa/enable/', UserProfileViewSet.as_view({'post': 'enable_2fa'}), name='v1-user-enable-2fa'),
    path('users/me/2fa/confirm/', UserProfileViewSet.as_view({'post': 'confirm_2fa_setup'}), name='v1-user-confirm-2fa'),
    path('users/me/2fa/disable/', UserProfileViewSet.as_view({'post': 'disable_2fa'}), name='v1-user-disable-2fa'),
    
    # Session management endpoints
    path('users/me/sessions/', UserSessionViewSet.as_view({'get': 'list'}), name='v1-user-sessions'),
    path('users/me/sessions/<uuid:pk>/', UserSessionViewSet.as_view({'get': 'retrieve'}), name='v1-user-session-detail'),
    path('users/me/sessions/<uuid:pk>/end/', UserSessionViewSet.as_view({'post': 'end_session'}), name='v1-user-session-end'),
    path('users/me/sessions/end-others/', UserSessionViewSet.as_view({'post': 'end_all_other_sessions'}), name='v1-user-sessions-end-others'),
    
    # Tenant membership endpoints
    path('memberships/', TenantMembershipViewSet.as_view({'get': 'list', 'post': 'create'}), name='v1-memberships'),
    path('memberships/<uuid:pk>/', TenantMembershipViewSet.as_view({
        'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'
    }), name='v1-membership-detail'),
    
    # Tenant role endpoints
    path('roles/', TenantRoleViewSet.as_view({'get': 'list', 'post': 'create'}), name='v1-roles'),
    path('roles/<uuid:pk>/', TenantRoleViewSet.as_view({
        'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'
    }), name='v1-role-detail'),
    
    # User invitation endpoints
    path('invitations/', UserInvitationViewSet.as_view({'get': 'list', 'post': 'create'}), name='v1-invitations'),
    path('invitations/<uuid:pk>/', UserInvitationViewSet.as_view({
        'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'
    }), name='v1-invitation-detail'),
    path('invitations/<uuid:pk>/resend/', UserInvitationViewSet.as_view({'post': 'resend'}), name='v1-invitation-resend'),
    path('invitations/<uuid:pk>/cancel/', UserInvitationViewSet.as_view({'post': 'cancel'}), name='v1-invitation-cancel'),
    
    # Platform administration endpoints
    path('platform/roles/', PlatformRoleViewSet.as_view({'get': 'list', 'post': 'create'}), name='v1-platform-roles'),
    path('platform/roles/<uuid:pk>/', PlatformRoleViewSet.as_view({
        'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'
    }), name='v1-platform-role-detail'),
]

# Add versioned URL patterns
urlpatterns += [
    path('api/v1/', include(v1_patterns)),
]

# Alternative URL structure for frontend developers who prefer RESTful paths
rest_patterns = [
    # Authentication
    path('register/', AuthViewSet.as_view({'post': 'register'}), name='rest-register'),
    path('login/', AuthViewSet.as_view({'post': 'login'}), name='rest-login'),
    path('logout/', AuthViewSet.as_view({'post': 'logout'}), name='rest-logout'),
    path('verify-2fa/', AuthViewSet.as_view({'post': 'verify_2fa'}), name='rest-verify-2fa'),
    path('request-otp/', AuthViewSet.as_view({'post': 'request_otp'}), name='rest-request-otp'),
    path('verify-otp/', AuthViewSet.as_view({'post': 'verify_otp'}), name='rest-verify-otp'),
    path('forgot-password/', AuthViewSet.as_view({'post': 'reset_password_request'}), name='rest-forgot-password'),
    path('reset-password/', AuthViewSet.as_view({'post': 'reset_password_confirm'}), name='rest-reset-password'),
    
    # User management
    path('me/', UserProfileViewSet.as_view({'get': 'me'}), name='rest-me'),
    path('me/update/', UserProfileViewSet.as_view({'put': 'update_profile', 'patch': 'update_profile'}), name='rest-me-update'),
    path('me/change-password/', UserProfileViewSet.as_view({'post': 'change_password'}), name='rest-change-password'),
    path('me/enable-2fa/', UserProfileViewSet.as_view({'post': 'enable_2fa'}), name='rest-enable-2fa'),
    path('me/disable-2fa/', UserProfileViewSet.as_view({'post': 'disable_2fa'}), name='rest-disable-2fa'),
    path('me/sessions/', UserSessionViewSet.as_view({'get': 'list'}), name='rest-my-sessions'),
    path('me/sessions/end-others/', UserSessionViewSet.as_view({'post': 'end_all_other_sessions'}), name='rest-end-other-sessions'),
]

urlpatterns += [
    path('', include(rest_patterns)),
]

# Admin-friendly URL patterns for management interfaces
admin_patterns = [
    path('admin/users/', include([
        path('', UserProfileViewSet.as_view({'get': 'list'}), name='admin-users-list'),
        path('<uuid:pk>/', UserProfileViewSet.as_view({'get': 'retrieve'}), name='admin-user-detail'),
    ])),
    path('admin/memberships/', include([
        path('', TenantMembershipViewSet.as_view({'get': 'list', 'post': 'create'}), name='admin-memberships-list'),
        path('<uuid:pk>/', TenantMembershipViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='admin-membership-detail'),
    ])),
    path('admin/roles/', include([
        path('', TenantRoleViewSet.as_view({'get': 'list', 'post': 'create'}), name='admin-roles-list'),
        path('<uuid:pk>/', TenantRoleViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='admin-role-detail'),
    ])),
    path('admin/invitations/', include([
        path('', UserInvitationViewSet.as_view({'get': 'list', 'post': 'create'}), name='admin-invitations-list'),
        path('<uuid:pk>/', UserInvitationViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='admin-invitation-detail'),
        path('<uuid:pk>/resend/', UserInvitationViewSet.as_view({'post': 'resend'}), name='admin-invitation-resend'),
    ])),
    path('admin/platform-roles/', include([
        path('', PlatformRoleViewSet.as_view({'get': 'list', 'post': 'create'}), name='admin-platform-roles-list'),
        path('<uuid:pk>/', PlatformRoleViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='admin-platform-role-detail'),
    ])),
]

urlpatterns += [
    path('admin-api/', include(admin_patterns)),
]

# Webhook endpoints for external integrations (future use)
webhook_patterns = [
    # SMS/WhatsApp delivery status webhooks
    path('webhooks/sms/delivery/', AuthViewSet.as_view({'post': 'sms_delivery_webhook'}), name='webhook-sms-delivery'),
    path('webhooks/whatsapp/delivery/', AuthViewSet.as_view({'post': 'whatsapp_delivery_webhook'}), name='webhook-whatsapp-delivery'),
    
    # Email delivery status webhooks
    path('webhooks/email/delivery/', AuthViewSet.as_view({'post': 'email_delivery_webhook'}), name='webhook-email-delivery'),
]

urlpatterns += [
    path('webhooks/', include(webhook_patterns)),
]

"""
URL Pattern Examples:

Authentication:
- POST /accounts/auth/register/
- POST /accounts/auth/login/
- POST /accounts/auth/logout/
- POST /accounts/auth/verify-2fa/
- POST /accounts/auth/request-otp/
- POST /accounts/auth/verify-otp/
- POST /accounts/auth/reset-password/
- POST /accounts/auth/reset-password-confirm/

User Profile:
- GET /accounts/profile/me/
- PUT/PATCH /accounts/profile/update/
- POST /accounts/profile/change-password/
- POST /accounts/profile/enable-2fa/
- POST /accounts/profile/disable-2fa/

Session Management:
- GET /accounts/sessions/
- GET /accounts/sessions/{id}/
- POST /accounts/sessions/{id}/end/
- POST /accounts/sessions/end-others/

Public Invitations:
- GET /accounts/invitation/{token}/
- POST /accounts/invitation/{token}/accept/

Tenant Management:
- GET/POST /accounts/memberships/
- GET/PUT/DELETE /accounts/memberships/{id}/
- GET/POST /accounts/roles/
- GET/PUT/DELETE /accounts/roles/{id}/
- GET/POST /accounts/invitations/
- POST /accounts/invitations/{id}/resend/

Platform Administration:
- GET/POST /accounts/platform-roles/
- GET/PUT/DELETE /accounts/platform-roles/{id}/

Alternative REST Paths:
- POST /accounts/register/
- POST /accounts/login/
- GET /accounts/me/
- PUT /accounts/me/update/

Admin Paths:
- GET /accounts/admin-api/users/
- GET /accounts/admin-api/memberships/
- GET /accounts/admin-api/roles/

Health Check:
- GET /accounts/health/
"""