from django.urls import path
from .views import CaseListCreateView, CaseRetrieveUpdateDestroyView

urlpatterns = [
    path('cases/', CaseListCreateView.as_view(), name='case-list-create'),
    path('cases/<int:pk>/', CaseRetrieveUpdateDestroyView.as_view(), name='case-detail'),
]