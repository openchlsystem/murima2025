from rest_framework import generics, permissions
from .models import Case
from .serializers import CaseSerializer
from django_tenants.utils import tenant_context

class CaseListCreateView(generics.ListCreateAPIView):
    serializer_class = CaseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filter cases by current tenant
        return Case.objects.filter(tenant=self.request.user.tenant)

    def perform_create(self, serializer):
        # Tenant and created_by are auto-set in serializer
        serializer.save()

class CaseRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CaseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Ensure users can only access their tenant's cases
        return Case.objects.filter(tenant=self.request.user.tenant)