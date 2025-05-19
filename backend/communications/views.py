from rest_framework import generics, permissions
from .models import Channel, Message
from .serializers import ChannelSerializer, MessageSerializer
from django_tenants.utils import tenant_context

class ChannelListCreateView(generics.ListCreateAPIView):
    serializer_class = ChannelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filter by current tenant (assuming tenant is set via middleware/JWT)
        return Channel.objects.filter(tenant=self.request.user.tenant)

    def perform_create(self, serializer):
        # Auto-set tenant and created_by
        serializer.save(
            tenant=self.request.user.tenant,
            created_by=self.request.user
        )

class ChannelRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ChannelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Channel.objects.filter(tenant=self.request.user.tenant)

class MessageListCreateView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filter by tenant + optional channel_id query param
        queryset = Message.objects.filter(channel__tenant=self.request.user.tenant)
        channel_id = self.request.query_params.get('channel_id')
        if channel_id:
            queryset = queryset.filter(channel_id=channel_id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(
            created_by=self.request.user,
            updated_by=self.request.user
        )