# analytics/urls.py
from django.urls import path
from .views import (
    DashboardListCreateView,
    DashboardRetrieveUpdateDestroyView,
    WidgetListCreateView,
    WidgetRetrieveUpdateDestroyView
)

urlpatterns = [
    # Dashboards
    path('dashboards/', DashboardListCreateView.as_view(), name='dashboard-list-create'),
    path('dashboards/<int:pk>/', DashboardRetrieveUpdateDestroyView.as_view(), name='dashboard-retrieve-update-destroy'),
    
    # Widgets (nested under dashboards)
    path('dashboards/<int:dashboard_id>/widgets/', WidgetListCreateView.as_view(), name='widget-list-create'),
    path('dashboards/<int:dashboard_id>/widgets/<int:widget_id>/', WidgetRetrieveUpdateDestroyView.as_view(), name='widget-retrieve-update-destroy'),
]