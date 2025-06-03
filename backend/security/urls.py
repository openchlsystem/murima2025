from django.urls import path
from .views import (
    AuditLogListCreateView,
    AuditLogDetailView,
    EncryptionKeyViewSet,
    EncryptionKeyDetailView
)

urlpatterns = [
    # Audit Logs
    path('audit-logs/', AuditLogListCreateView.as_view(), name='audit-log-list'),
    path('audit-logs/<int:pk>/', AuditLogDetailView.as_view(), name='audit-log-detail'),
    
    # Encryption Keys
    path('encryption-keys/', EncryptionKeyViewSet.as_view(), name='encryption-key-list'),
    path('encryption-keys/<int:pk>/', EncryptionKeyDetailView.as_view(), name='encryption-key-detail'),
]