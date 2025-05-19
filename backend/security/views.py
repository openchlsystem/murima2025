from rest_framework import generics, permissions
from .models import AuditLog, EncryptionKey
from .serializers import AuditLogSerializer, EncryptionKeySerializer
from tenants.utils import get_current_tenant
from core.models import BaseModel

class AuditLogListCreateView(generics.ListCreateAPIView):
    serializer_class = AuditLogSerializer
    permission_classes = [permissions.IsAdminUser]  # Only admins can view logs
    
    def get_queryset(self):
        tenant = get_current_tenant(self.request)
        return AuditLog.objects.filter(tenant=tenant).order_by('-created_at')
    
    def perform_create(self, serializer):
        serializer.save(
            created_by=self.request.user,
            tenant=get_current_tenant(self.request)
        )

class AuditLogDetailView(generics.RetrieveDestroyAPIView):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = [permissions.IsAdminUser]

class EncryptionKeyViewSet(generics.ListCreateAPIView):
    serializer_class = EncryptionKeySerializer
    permission_classes = [permissions.IsAdminUser]
    
    def get_queryset(self):
        tenant = get_current_tenant(self.request)
        return EncryptionKey.objects.filter(tenant=tenant)
    
    def perform_create(self, serializer):
        serializer.save(
            created_by=self.request.user,
            tenant=get_current_tenant(self.request)
        )

class EncryptionKeyDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EncryptionKeySerializer
    permission_classes = [permissions.IsAdminUser]
    
    def get_queryset(self):
        tenant = get_current_tenant(self.request)
        return EncryptionKey.objects.filter(tenant=tenant)