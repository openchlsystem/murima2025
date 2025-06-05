from rest_framework import generics, viewsets, permissions, status
from rest_framework.response import Response
from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (
    UserSerializer, UserManagementSerializer,
    RequestOTPSerializer, VerifyOTPSerializer, RegisterUserSerializer
)
from .models import OTP

User = get_user_model()


class RegisterUserView(generics.CreateAPIView):
    """
    Register a new user. Returns user data with JWT tokens.
    """
    serializer_class = RegisterUserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        
        response_data = {
            'user': UserSerializer(user).data,
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }
        
        return Response(response_data, status=status.HTTP_201_CREATED)


class RequestOTPView(generics.GenericAPIView):
    """
    Request OTP to be sent via SMS, Email or WhatsApp.
    Includes rate limiting and proper error handling.
    """
    serializer_class = RequestOTPSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        contact = serializer.validated_data['contact']
        method = serializer.validated_data['method']

        try:
            # Find user by email or phone
            user = User.objects.filter(email=contact).first() or User.objects.filter(phone=contact).first()
            if not user:
                return Response(
                    {"detail": "User not found"}, 
                    status=status.HTTP_404_NOT_FOUND
                )

            # Generate and send OTP
            otp_instance = OTP.generate_otp(user, method)
            OTP.send_otp(user, otp_instance)

            # Mask contact info in response
            masked_contact = (
                f"***{contact[-4:]}" if method != 'email' 
                else f"{contact[0]}***{contact.split('@')[1]}"
            )

            return Response({
                "detail": f"OTP sent via {method}",
                "masked_contact": masked_contact,
                "method": method,
                "expires_in": "5 minutes"  # Should match your OTP expiry
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"detail": f"Failed to send OTP: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class VerifyOTPView(generics.GenericAPIView):
    """
    Verify OTP and return JWT tokens upon success.
    """
    serializer_class = VerifyOTPSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        access_token = serializer.validated_data['access']
        refresh_token = serializer.validated_data['refresh']

        # Mark user as verified
        user.is_verified = True
        user.save()

        # Set last login
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])

        return Response({
            "user": UserSerializer(user).data,
            "access": access_token,
            "refresh": refresh_token,
            "detail": "OTP verified successfully"
        }, status=status.HTTP_200_OK)


class IsAdminUser(permissions.BasePermission):
    """
    Custom admin check with tenant awareness.
    """
    def has_permission(self, request, view):
        return request.user and (request.user.is_staff or request.user.is_superuser)


class UserManagementViewSet(viewsets.ModelViewSet):
    """
    Admin viewset for managing users within the same tenant.
    Includes JWT authentication and tenant filtering.
    """
    serializer_class = UserManagementSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return User.objects.all()
        elif user.is_staff:
            return User.objects.filter(tenant=user.tenant)
        return User.objects.none()

    def perform_create(self, serializer):
        serializer.save(
            tenant=self.request.user.tenant,
            created_by=self.request.user
        )

    def perform_update(self, serializer):
        serializer.save(
            updated_by=self.request.user
        )