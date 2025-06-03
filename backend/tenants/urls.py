from django.urls import path
from .views import (
    TenantListCreateAPIView, TenantRetrieveUpdateDestroyAPIView,
    DomainListCreateAPIView, DomainRetrieveUpdateDestroyAPIView
)

urlpatterns = [
    # Tenant URLs
    path('tenants/', TenantListCreateAPIView.as_view(), name='tenant-list-create'),
    path('tenants/<int:id>/', TenantRetrieveUpdateDestroyAPIView.as_view(), name='tenant-retrieve-update-destroy'),
    
    # Domain URLs
    path('domains/', DomainListCreateAPIView.as_view(), name='domain-list-create'),
    path('domains/<int:id>/', DomainRetrieveUpdateDestroyAPIView.as_view(), name='domain-retrieve-update-destroy'),
]