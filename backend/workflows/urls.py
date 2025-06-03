# workflows/urls.py
from django.urls import path
from .views import (
    WorkflowListCreateView,
    WorkflowRetrieveUpdateDestroyView,
    StepListCreateView,
    StepRetrieveUpdateDestroyView
)

urlpatterns = [
    # Workflows
    path('tenants/<int:tenant_id>/workflows/', 
         WorkflowListCreateView.as_view(), name='workflow-list-create'),
    path('tenants/<int:tenant_id>/workflows/<int:pk>/', 
         WorkflowRetrieveUpdateDestroyView.as_view(), name='workflow-detail'),
    
    # Steps
    path('workflows/<int:workflow_id>/steps/', 
         StepListCreateView.as_view(), name='step-list-create'),
    path('workflows/<int:workflow_id>/steps/<int:pk>/', 
         StepRetrieveUpdateDestroyView.as_view(), name='step-detail'),
]