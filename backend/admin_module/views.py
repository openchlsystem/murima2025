from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import (
    SystemConfiguration,
    TenantConfiguration,
    AuditLog,
    CategoryType,
    Category,
    SystemNotification
)

from .serializers import (
    SystemConfigurationSerializer,
    TenantConfigurationSerializer,
    AuditLogSerializer,
    CategoryTypeSerializer,
    CategorySerializer,
    SystemNotificationSerializer
)

# 🔒 Optional: Read-only for non-admins
class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and (
            request.user.is_staff or request.method in permissions.SAFE_METHODS
        )


# 🔧 System Configuration Views
class SystemConfigurationListCreateView(generics.ListCreateAPIView):
    queryset = SystemConfiguration.objects.all()
    serializer_class = SystemConfigurationSerializer
    permission_classes = [permissions.IsAdminUser]


class SystemConfigurationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SystemConfiguration.objects.all()
    serializer_class = SystemConfigurationSerializer
    permission_classes = [permissions.IsAdminUser]


# 🏢 Tenant Configuration Views
class TenantConfigurationListCreateView(generics.ListCreateAPIView):
    queryset = TenantConfiguration.objects.select_related('tenant', 'default_assignee')
    serializer_class = TenantConfigurationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['tenant__id']


class TenantConfigurationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TenantConfiguration.objects.select_related('tenant', 'default_assignee')
    serializer_class = TenantConfigurationSerializer
    permission_classes = [permissions.IsAuthenticated]


# 🕵️ Audit Log (Read Only)
class AuditLogListView(generics.ListAPIView):
    queryset = AuditLog.objects.select_related('user').all()
    serializer_class = AuditLogSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['action', 'model_name']
    search_fields = ['user__email', 'model_name', 'object_id']
    ordering_fields = ['timestamp']
    ordering = ['-timestamp']


class AuditLogDetailView(generics.RetrieveAPIView):
    queryset = AuditLog.objects.select_related('user').all()
    serializer_class = AuditLogSerializer
    permission_classes = [permissions.IsAdminUser]


# 📁 Category Type Views
class CategoryTypeListCreateView(generics.ListCreateAPIView):
    queryset = CategoryType.objects.all()
    serializer_class = CategoryTypeSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class CategoryTypeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CategoryType.objects.all()
    serializer_class = CategoryTypeSerializer
    permission_classes = [IsAdminOrReadOnly]


# 📂 Category Views
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.select_related('category_type', 'parent').all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category_type', 'is_active']
    search_fields = ['name']
    ordering_fields = ['sort_order']
    ordering = ['category_type', 'sort_order']


class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.select_related('category_type', 'parent').all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


# 🔔 System Notification Views
class SystemNotificationListCreateView(generics.ListCreateAPIView):
    queryset = SystemNotification.objects.prefetch_related('affected_tenants').select_related('created_by')
    serializer_class = SystemNotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['severity', 'is_active']
    search_fields = ['title', 'message']


class SystemNotificationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SystemNotification.objects.prefetch_related('affected_tenants').select_related('created_by')
    serializer_class = SystemNotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
