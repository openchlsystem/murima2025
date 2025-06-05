from rest_framework import generics, viewsets, permissions, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import (
    UserSerializer, UserManagementSerializer,
    RequestOTPSerializer, VerifyOTPSerializer, RegisterUserSerializer
)
from .models import OTP

User = get_user_model()


class RegisterUserView(generics.CreateAPIView):
    """
    Register a new user. Accepts username, email, phone, tenant, and password.
    """
    serializer_class = RegisterUserSerializer
    permission_classes = [permissions.AllowAny]


class RequestOTPView(generics.GenericAPIView):
    """
    Request OTP to be sent via SMS, Email or WhatsApp.
    """
    serializer_class = RequestOTPSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        contact = serializer.validated_data['contact']
        method = serializer.validated_data['method']

        # Find user by email or phone
        user = User.objects.filter(email=contact).first() or User.objects.filter(phone=contact).first()
        if not user:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Generate and send OTP using User instance
        otp_code = OTP.generate_otp(user, method)
        OTP.send_otp(user, otp_code)


        return Response({"detail": f"OTP sent via {method} to {contact}"}, status=status.HTTP_200_OK)




class VerifyOTPView(generics.GenericAPIView):
    """
    Verify the OTP code for a given contact and method.
    """
    serializer_class = VerifyOTPSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        contact = serializer.validated_data['contact']
        code = serializer.validated_data['code']
        method = serializer.validated_data['method']

        # Find the user first
        user = User.objects.filter(email=contact).first() or User.objects.filter(phone=contact).first()
        if not user:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Verify OTP with user instance, not contact string
        if OTP.verify_otp(user, code, method):
            user.is_verified = True
            user.save()
            return Response({"detail": "OTP verified", "user_id": user.id}, status=status.HTTP_200_OK)

        return Response({"detail": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)


class IsAdminUser(permissions.BasePermission):
    """
    Custom admin check.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_staff


class UserManagementViewSet(viewsets.ModelViewSet):
    """
    Admin viewset for managing users within the same tenant.
    """
    serializer_class = UserManagementSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return User.objects.all()
        return User.objects.filter(tenant=user.tenant)
