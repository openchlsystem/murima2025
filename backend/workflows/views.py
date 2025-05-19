# workflows/views.py
from rest_framework import generics, permissions
from .models import Workflow, Step
from .serializers import WorkflowSerializer, StepSerializer
from tenants.models import Tenant
from django.shortcuts import get_object_or_404

class WorkflowListCreateView(generics.ListCreateAPIView):
    serializer_class = WorkflowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filter by tenant (from URL or JWT)
        tenant_id = self.kwargs.get('tenant_id')
        return Workflow.objects.filter(tenant_id=tenant_id)

    def perform_create(self, serializer):
        tenant = get_object_or_404(Tenant, id=self.kwargs['tenant_id'])
        serializer.save(tenant=tenant, created_by=self.request.user)

class WorkflowRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WorkflowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        tenant_id = self.kwargs.get('tenant_id')
        return Workflow.objects.filter(tenant_id=tenant_id)

class StepListCreateView(generics.ListCreateAPIView):
    serializer_class = StepSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        workflow_id = self.kwargs.get('workflow_id')
        return Step.objects.filter(workflow_id=workflow_id)

    def perform_create(self, serializer):
        workflow = get_object_or_404(Workflow, id=self.kwargs['workflow_id'])
        serializer.save(workflow=workflow, created_by=self.request.user)

class StepRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StepSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        workflow_id = self.kwargs.get('workflow_id')
        return Step.objects.filter(workflow_id=workflow_id)