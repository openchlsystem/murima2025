# analytics/views.py
from rest_framework import generics, permissions
from .models import Dashboard, Widget
from .serializers import DashboardSerializer, WidgetSerializer
from core.models import BaseModel
from django.shortcuts import get_object_or_404

class DashboardListCreateView(generics.ListCreateAPIView):
    queryset = Dashboard.objects.all()
    serializer_class = DashboardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Auto-set created_by/updated_by to current user
        serializer.save(
            created_by=self.request.user,
            updated_by=self.request.user
        )

class DashboardRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Dashboard.objects.all()
    serializer_class = DashboardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

class WidgetListCreateView(generics.ListCreateAPIView):
    serializer_class = WidgetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        dashboard_id = self.kwargs['dashboard_id']
        return Widget.objects.filter(dashboard_id=dashboard_id)

    def perform_create(self, serializer):
        dashboard = get_object_or_404(Dashboard, id=self.kwargs['dashboard_id'])
        serializer.save(
            dashboard=dashboard,
            created_by=self.request.user,
            updated_by=self.request.user
        )

class WidgetRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WidgetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return get_object_or_404(
            Widget,
            id=self.kwargs['widget_id'],
            dashboard_id=self.kwargs['dashboard_id']
        )

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)