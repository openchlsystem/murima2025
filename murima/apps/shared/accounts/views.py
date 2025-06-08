"""
Accounts App Views

Provides API endpoints for user management, authentication,
tenant membership, and OTP-based verification workflows.

Includes comprehensive authentication flow with email/password + OTP
support for email, SMS, and WhatsApp delivery channels.
"""

from datetime import timedelta
from django.contrib.auth import login, logout
from django.contrib.auth.tokens import default_token_generator
from django.db import transaction
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, permissions, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import (
    User, TenantMembership, TenantRole, PlatformRole,
    OTPToken, UserSession, UserInvitation
)
from .serializers import (
    UserRegistrationSerializer, UserProfileSerializer, ChangePasswordSerializer,
    LoginSerializer, OTPRequestSerializer, OTPVerificationSerializer,
    PasswordResetRequestSerializer, PasswordResetConfirmSerializer,
    TenantMembershipSerializer, TenantRoleSerializer, UserInvitationSerializer,
    InvitationAcceptSerializer, UserSessionSerializer, PlatformRoleSerializer
)


def get_client_ip(request):
    """Get client IP address from request."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


# Authentication Views
class AuthViewSet(GenericViewSet):
    """
    ViewSet for authentication operations.
    
    Provides endpoints for registration, login, logout, OTP operations,
    and password reset functionality.
    """
    
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['post'])
    def register(self, request):
        """
        Register a new user account.
        
        Creates a new user and optionally sends email verification OTP.
        """
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                user = serializer.save()
                
                # Generate email verification OTP if email is provided
                if user.email:
                    otp_token = OTPToken.objects.create_otp(
                        user=user,
                        token_type='email_verification',
                        delivery_method='email',
                        recipient=user.email,
                        expires_in_minutes=30,
                        ip_address=get_client_ip(request),
                        user_agent=request.META.get('HTTP_USER_AGENT', '')
                    )
                    
                    # TODO: Send email with OTP token
                    # send_verification_email(user, otp_token.token)
                
                return Response({
                    'user': UserProfileSerializer(user).data,
                    'message': 'Registration successful. Please check your email for verification code.',
                    'requires_verification': True
                }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        """
        Authenticate user with email and password.
        
        Returns user data and session info. May require 2FA if enabled.
        """
        serializer = LoginSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            remember_me = serializer.validated_data.get('remember_me', False)
            
            # Check if 2FA is required
            requires_2fa = user.two_factor_enabled and user.is_verified
            
            if requires_2fa:
                # Generate 2FA OTP
                otp_token = OTPToken.objects.create_otp(
                    user=user,
                    token_type='login_2fa',
                    delivery_method=user.preferred_2fa_method,
                    recipient=user.email if user.preferred_2fa_method == 'email' else user.phone,
                    expires_in_minutes=10,
                    ip_address=get_client_ip(request),
                    user_agent=request.META.get('HTTP_USER_AGENT', '')
                )
                
                # TODO: Send OTP via selected method
                # send_otp_token(user, otp_token, user.preferred_2fa_method)
                
                return Response({
                    'requires_2fa': True,
                    'delivery_method': user.preferred_2fa_method,
                    'message': f'2FA code sent via {user.preferred_2fa_method}',
                    'user_id': user.id  # Temporary for 2FA completion
                }, status=status.HTTP_200_OK)
            
            # Complete login without 2FA
            login(request, user)
            
            # Set session expiry based on remember_me
            if remember_me:
                request.session.set_expiry(30 * 24 * 60 * 60)  # 30 days
            else:
                request.session.set_expiry(0)  # Browser session
            
            # Create session record
            UserSession.objects.create_session(
                user=user,
                session_key=request.session.session_key,
                ip_address=get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )
            
            return Response({
                'user': UserProfileSerializer(user).data,
                'session_key': request.session.session_key,
                'message': 'Login successful'
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def verify_2fa(self, request):
        """
        Complete login with 2FA verification.
        """
        # Get user from request data (temporary during 2FA flow)
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({
                'error': 'User ID required for 2FA verification'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({
                'error': 'Invalid user ID'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Verify OTP
        serializer = OTPVerificationSerializer(
            data=request.data, 
            context={'request': type('obj', (object,), {'user': user})()}
        )
        
        if serializer.is_valid():
            # Complete login
            login(request, user)
            
            # Set session expiry
            remember_me = request.data.get('remember_me', False)
            if remember_me:
                request.session.set_expiry(30 * 24 * 60 * 60)  # 30 days
            else:
                request.session.set_expiry(0)  # Browser session
            
            # Create session record
            UserSession.objects.create_session(
                user=user,
                session_key=request.session.session_key,
                ip_address=get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )
            
            return Response({
                'user': UserProfileSerializer(user).data,
                'session_key': request.session.session_key,
                'message': '2FA verification successful'
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        """
        Log out the current user and end session.
        """
        # End user session record
        if hasattr(request, 'session') and request.session.session_key:
            UserSession.objects.filter(
                session_key=request.session.session_key,
                is_active=True
            ).update(
                is_active=False,
                ended_at=timezone.now()
            )
        
        logout(request)
        return Response({
            'message': 'Logout successful'
        }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'])
    def request_otp(self, request):
        """
        Request an OTP token for various purposes.
        
        Can be used for email verification, phone verification, 2FA, etc.
        """
        # For non-authenticated requests (like password reset)
        if not request.user.is_authenticated:
            email = request.data.get('email')
            if not email:
                return Response({
                    'error': 'Email required for OTP request'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                user = User.objects.get(email=email, is_active=True)
            except User.DoesNotExist:
                # Don't reveal if email exists for security
                return Response({
                    'message': 'If the email exists, an OTP has been sent.'
                }, status=status.HTTP_200_OK)
        else:
            user = request.user
        
        serializer = OTPRequestSerializer(
            data=request.data,
            context={'request': type('obj', (object,), {'user': user})()}
        )
        
        if serializer.is_valid():
            otp_token = OTPToken.objects.create_otp(
                user=user,
                token_type=serializer.validated_data['token_type'],
                delivery_method=serializer.validated_data['delivery_method'],
                recipient=serializer.validated_data['recipient'],
                expires_in_minutes=15,
                ip_address=get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )
            
            # TODO: Send OTP via selected method
            # send_otp_token(user, otp_token, delivery_method)
            
            return Response({
                'message': f'OTP sent via {serializer.validated_data["delivery_method"]}',
                'delivery_method': serializer.validated_data['delivery_method'],
                'recipient': serializer.validated_data['recipient']
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def verify_otp(self, request):
        """
        Verify an OTP token.
        
        Used for email verification, phone verification, etc.
        """
        # Handle both authenticated and non-authenticated requests
        if request.user.is_authenticated:
            user = request.user
        else:
            # For password reset and other non-authenticated flows
            email = request.data.get('email')
            if not email:
                return Response({
                    'error': 'Email required for OTP verification'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                user = User.objects.get(email=email, is_active=True)
            except User.DoesNotExist:
                return Response({
                    'error': 'Invalid email address'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = OTPVerificationSerializer(
            data=request.data,
            context={'request': type('obj', (object,), {'user': user})()}
        )
        
        if serializer.is_valid():
            otp_token = serializer.validated_data['otp_token']
            token_type = serializer.validated_data['token_type']
            
            # Handle different verification types
            if token_type == 'email_verification':
                user.is_verified = True
                user.email_verified_at = timezone.now()
                user.save(update_fields=['is_verified', 'email_verified_at'])
                
                return Response({
                    'message': 'Email verified successfully',
                    'user': UserProfileSerializer(user).data
                }, status=status.HTTP_200_OK)
            
            elif token_type == 'phone_verification':
                user.phone_verified_at = timezone.now()
                user.save(update_fields=['phone_verified_at'])
                
                return Response({
                    'message': 'Phone verified successfully',
                    'user': UserProfileSerializer(user).data
                }, status=status.HTTP_200_OK)
            
            else:
                return Response({
                    'message': 'OTP verified successfully',
                    'verified': True
                }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def reset_password_request(self, request):
        """
        Request password reset via email.
        """
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            
            # Check if user exists (don't reveal in response)
            try:
                user = User.objects.get(email=email, is_active=True)
                
                # Generate password reset OTP
                otp_token = OTPToken.objects.create_otp(
                    user=user,
                    token_type='password_reset',
                    delivery_method='email',
                    recipient=user.email,
                    expires_in_minutes=30,
                    ip_address=get_client_ip(request),
                    user_agent=request.META.get('HTTP_USER_AGENT', '')
                )
                
                # TODO: Send password reset email
                # send_password_reset_email(user, otp_token.token)
                
            except User.DoesNotExist:
                # Don't reveal if email exists
                pass
            
            return Response({
                'message': 'If the email exists, a password reset code has been sent.'
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def reset_password_confirm(self, request):
        """
        Confirm password reset with OTP.
        """
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            new_password = serializer.validated_data['new_password']
            
            # Update password
            user.set_password(new_password)
            user.last_password_change = timezone.now()
            user.failed_login_attempts = 0  # Reset failed attempts
            user.account_locked_until = None  # Unlock account
            user.save(update_fields=[
                'password', 'last_password_change', 
                'failed_login_attempts', 'account_locked_until'
            ])
            
            # End all existing sessions for security
            UserSession.objects.filter(user=user, is_active=True).update(
                is_active=False,
                ended_at=timezone.now()
            )
            
            return Response({
                'message': 'Password reset successful. Please log in with your new password.'
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# User Profile Management
class UserProfileViewSet(GenericViewSet):
    """
    ViewSet for user profile management.
    
    Provides endpoints for viewing and updating user profiles,
    changing passwords, and managing account settings.
    """
    
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer
    
    def get_object(self):
        """Return the current user."""
        return self.request.user
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """
        Get current user's profile information.
        """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['put', 'patch'])
    def update_profile(self, request):
        """
        Update current user's profile information.
        """
        serializer = self.get_serializer(
            request.user, 
            data=request.data, 
            partial=request.method == 'PATCH'
        )
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def change_password(self, request):
        """
        Change user's password.
        """
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            serializer.save()
            
            # End all other sessions for security
            UserSession.objects.filter(
                user=request.user, 
                is_active=True
            ).exclude(
                session_key=request.session.session_key
            ).update(
                is_active=False,
                ended_at=timezone.now()
            )
            
            return Response({
                'message': 'Password changed successfully'
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def enable_2fa(self, request):
        """
        Enable two-factor authentication for user.
        """
        user = request.user
        
        # Verify user's email or phone based on preferred method
        preferred_method = request.data.get('preferred_2fa_method', 'email')
        
        if preferred_method in ['sms', 'whatsapp'] and not user.phone:
            return Response({
                'error': 'Phone number required for SMS/WhatsApp 2FA'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if preferred_method == 'email' and not user.is_verified:
            return Response({
                'error': 'Email must be verified before enabling 2FA'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Generate verification OTP
        recipient = user.email if preferred_method == 'email' else user.phone
        otp_token = OTPToken.objects.create_otp(
            user=user,
            token_type='email_verification' if preferred_method == 'email' else 'phone_verification',
            delivery_method=preferred_method,
            recipient=recipient,
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        return Response({
            'message': f'Verification code sent via {preferred_method}',
            'step': 'verify_method',
            'delivery_method': preferred_method
        })
    
    @action(detail=False, methods=['post'])
    def confirm_2fa_setup(self, request):
        """
        Confirm 2FA setup with OTP verification.
        """
        serializer = OTPVerificationSerializer(
            data=request.data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            user = request.user
            preferred_method = request.data.get('preferred_2fa_method', 'email')
            
            user.two_factor_enabled = True
            user.preferred_2fa_method = preferred_method
            user.save(update_fields=['two_factor_enabled', 'preferred_2fa_method'])
            
            return Response({
                'message': '2FA enabled successfully',
                'user': UserProfileSerializer(user).data
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def disable_2fa(self, request):
        """
        Disable two-factor authentication.
        """
        user = request.user
        user.two_factor_enabled = False
        user.save(update_fields=['two_factor_enabled'])
        
        return Response({
            'message': '2FA disabled successfully',
            'user': UserProfileSerializer(user).data
        })


# Session Management
class UserSessionViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        GenericViewSet):
    """
    ViewSet for managing user sessions.
    
    Allows users to view and manage their active sessions.
    """
    
    permission_classes = [IsAuthenticated]
    serializer_class = UserSessionSerializer
    
    def get_queryset(self):
        """Return sessions for the current user."""
        return UserSession.objects.filter(
            user=self.request.user
        ).order_by('-last_activity')
    
    @action(detail=True, methods=['post'])
    def end_session(self, request, pk=None):
        """
        End a specific session.
        """
        session = self.get_object()
        
        if session.user != request.user:
            return Response({
                'error': 'You can only end your own sessions'
            }, status=status.HTTP_403_FORBIDDEN)
        
        session.end_session()
        
        return Response({
            'message': 'Session ended successfully'
        })
    
    @action(detail=False, methods=['post'])
    def end_all_other_sessions(self, request):
        """
        End all sessions except the current one.
        """
        current_session_key = request.session.session_key
        
        ended_count = UserSession.objects.filter(
            user=request.user,
            is_active=True
        ).exclude(
            session_key=current_session_key
        ).update(
            is_active=False,
            ended_at=timezone.now()
        )
        
        return Response({
            'message': f'Ended {ended_count} other session(s)'
        })


# Tenant Management Views
class TenantMembershipViewSet(ModelViewSet):
    """
    ViewSet for tenant membership management.
    
    Requires proper tenant context and permissions.
    """
    
    permission_classes = [IsAuthenticated]
    serializer_class = TenantMembershipSerializer
    
    def get_queryset(self):
        """Return memberships for current tenant."""
        # TODO: Add tenant filtering when tenants app is implemented
        # tenant = get_current_tenant(self.request)
        # return TenantMembership.objects.filter(tenant=tenant)
        return TenantMembership.objects.none()  # Placeholder


class TenantRoleViewSet(ModelViewSet):
    """
    ViewSet for tenant role management.
    """
    
    permission_classes = [IsAuthenticated]
    serializer_class = TenantRoleSerializer
    
    def get_queryset(self):
        """Return roles for current tenant."""
        # TODO: Add tenant filtering when tenants app is implemented
        return TenantRole.objects.none()  # Placeholder


class UserInvitationViewSet(ModelViewSet):
    """
    ViewSet for user invitation management.
    """
    
    permission_classes = [IsAuthenticated]
    serializer_class = UserInvitationSerializer
    
    def get_queryset(self):
        """Return invitations for current tenant."""
        # TODO: Add tenant filtering when tenants app is implemented
        return UserInvitation.objects.none()  # Placeholder
    
    @action(detail=True, methods=['post'])
    def resend(self, request, pk=None):
        """
        Resend an invitation email.
        """
        invitation = self.get_object()
        
        if not invitation.is_valid():
            return Response({
                'error': 'Invitation is no longer valid'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # TODO: Send invitation email
        # send_invitation_email(invitation)
        
        return Response({
            'message': 'Invitation resent successfully'
        })
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """
        Cancel an invitation.
        """
        invitation = self.get_object()
        invitation.soft_delete(user=request.user)
        
        return Response({
            'message': 'Invitation cancelled successfully'
        })


# Public Invitation Views
class PublicInvitationView(APIView):
    """
    Public view for accepting invitations without authentication.
    """
    
    permission_classes = [AllowAny]
    
    def get(self, request, token):
        """
        Get invitation details by token.
        """
        try:
            invitation = UserInvitation.objects.get(token=token)
            if not invitation.is_valid():
                return Response({
                    'error': 'Invitation has expired or been used'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Check if user already exists
            user_exists = User.objects.filter(email=invitation.email).exists()
            
            return Response({
                'invitation': {
                    'tenant_name': invitation.tenant.name,
                    'role_name': invitation.role.display_name,
                    'invited_by': invitation.invited_by.get_full_name(),
                    'email': invitation.email,
                    'message': invitation.message,
                    'expires_at': invitation.expires_at
                },
                'user_exists': user_exists
            })
            
        except UserInvitation.DoesNotExist:
            return Response({
                'error': 'Invalid invitation token'
            }, status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request, token):
        """
        Accept an invitation.
        """
        data = request.data.copy()
        data['token'] = token
        
        serializer = InvitationAcceptSerializer(data=data)
        if serializer.is_valid():
            invitation = serializer.validated_data['invitation']
            user_exists = serializer.validated_data['user_exists']
            
            with transaction.atomic():
                if user_exists:
                    user = serializer.validated_data['user']
                else:
                    # Create new user
                    user_serializer = UserRegistrationSerializer(
                        data=serializer.validated_data['user_data']
                    )
                    if user_serializer.is_valid():
                        user = user_serializer.save()
                    else:
                        return Response(
                            user_serializer.errors, 
                            status=status.HTTP_400_BAD_REQUEST
                        )
                
                # Accept invitation and create membership
                membership = invitation.accept(user)
                
                return Response({
                    'message': 'Invitation accepted successfully',
                    'user': UserProfileSerializer(user).data,
                    'membership': TenantMembershipSerializer(membership).data
                }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Platform Administration Views
class PlatformRoleViewSet(ModelViewSet):
    """
    ViewSet for platform role management.
    
    Restricted to platform administrators.
    """
    
    permission_classes = [IsAuthenticated]  # TODO: Add PlatformAdminPermission
    serializer_class = PlatformRoleSerializer
    queryset = PlatformRole.objects.all()
    
    def perform_create(self, serializer):
        """Set granted_by to current user."""
        serializer.save(
            granted_by=self.request.user,
            created_by=self.request.user,
            updated_by=self.request.user
        )
    
    def perform_update(self, serializer):
        """Set updated_by to current user."""
        serializer.save(updated_by=self.request.user)


# Health Check View
class HealthCheckView(APIView):
    """
    Simple health check endpoint for the accounts app.
    """
    
    permission_classes = [AllowAny]
    
    def get(self, request):
        """Return health status."""
        return Response({
            'status': 'healthy',
            'service': 'accounts',
            'timestamp': timezone.now()
        })