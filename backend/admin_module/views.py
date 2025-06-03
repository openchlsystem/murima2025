from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from .models import SystemConfiguration, AuditLog
from .serializers import SystemConfigurationSerializer, AuditLogSerializer

class SystemConfigurationViewList(LoginRequiredMixin, generics.ListCreateAPIView):
    queryset = SystemConfiguration.objects.all()
    serializer_class = SystemConfigurationSerializer
    permission_classes = [IsAdminUser]

class SystemConfigurationViewDetail(LoginRequiredMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = SystemConfiguration.objects.all()
    serializer_class = SystemConfigurationSerializer
    permission_classes = [IsAdminUser]
    
    def get_object(self):
        return SystemConfiguration.objects.first() or SystemConfiguration.objects.create()

class AuditLogListCreateView(LoginRequiredMixin, generics.ListCreateAPIView):
    serializer_class = AuditLogSerializer
    permission_classes = [IsAdminUser]
    queryset = AuditLog.objects.all().order_by('-timestamp')
    
    def get_queryset(self):
        queryset = super().get_queryset()
        user_id = self.request.query_params.get('user_id')
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        return queryset

class AuditLogDetailView(LoginRequiredMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AuditLogSerializer
    permission_classes = [IsAdminUser]
    queryset = AuditLog.objects.all()