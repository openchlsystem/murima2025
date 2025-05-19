from rest_framework import generics, permissions
from .models import AIService, AIModel
from .serializers import AIServiceSerializer, AIModelSerializer
from tenants.models import Tenant
from django.shortcuts import get_object_or_404

class AIServiceListCreateView(generics.ListCreateAPIView):
    serializer_class = AIServiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filter by tenant (assuming tenant_id is passed in query params)
        tenant_id = self.request.query_params.get('tenant_id')
        if tenant_id:
            return AIService.objects.filter(tenant_id=tenant_id)
        return AIService.objects.none()

    def perform_create(self, serializer):
        tenant = get_object_or_404(Tenant, id=self.request.data.get('tenant_id'))
        serializer.save(
            created_by=self.request.user,
            updated_by=self.request.user,
            tenant=tenant
        )

class AIServiceRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AIService.objects.all()
    serializer_class = AIServiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

class AIModelListCreateView(generics.ListCreateAPIView):
    serializer_class = AIModelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        service_id = self.kwargs.get('service_id')
        return AIModel.objects.filter(service_id=service_id)

    def perform_create(self, serializer):
        service = get_object_or_404(AIService, id=self.kwargs.get('service_id'))
        serializer.save(
            created_by=self.request.user,
            updated_by=self.request.user,
            service=service
        )