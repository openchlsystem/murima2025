from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView
)
from .views import (
    RegisterUserView,
    RequestOTPView,
    VerifyOTPView,
    UserManagementViewSet
)

router = DefaultRouter()
router.register(r'users', UserManagementViewSet, basename='user-management')

auth_urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('otp/request/', RequestOTPView.as_view(), name='request-otp'),
    path('otp/verify/', VerifyOTPView.as_view(), name='verify-otp'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token-verify'),
]

urlpatterns = [
    path('', include(auth_urlpatterns)),
    path('', include(router.urls)),
]