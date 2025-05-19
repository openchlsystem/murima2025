from rest_framework import generics, permissions
from .models import Notification
from .serializers import NotificationSerializer
from tenants.utils import get_current_tenant

class NotificationListCreateView(generics.ListCreateAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        tenant = get_current_tenant(self.request)
        return Notification.objects.filter(tenant=tenant)

    def perform_create(self, serializer):
        tenant = get_current_tenant(self.request)
        serializer.save(
            tenant=tenant,
            created_by=self.request.user,
            updated_by=self.request.user
        )

class NotificationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        tenant = get_current_tenant(self.request)
        return Notification.objects.filter(tenant=tenant)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)