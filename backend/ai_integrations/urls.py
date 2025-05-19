from django.urls import path
from .views import (
    AIServiceListCreateView,
    AIServiceRetrieveUpdateDestroyView,
    AIModelListCreateView
)

urlpatterns = [
    # AI Services
    path('services/', AIServiceListCreateView.as_view(), name='ai-service-list'),
    path('services/<int:pk>/', AIServiceRetrieveUpdateDestroyView.as_view(), name='ai-service-detail'),
    
    # AI Models (nested under services)
    path('services/<int:service_id>/models/', AIModelListCreateView.as_view(), name='ai-model-list'),
]