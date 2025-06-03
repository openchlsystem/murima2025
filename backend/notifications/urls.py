from django.urls import path
from .views import (
    NotificationListCreateView,
    NotificationRetrieveUpdateDestroyView
)

urlpatterns = [
    path('', NotificationListCreateView.as_view(), name='notification-list-create'),
    path('<int:pk>/', NotificationRetrieveUpdateDestroyView.as_view(), name='notification-detail'),
]