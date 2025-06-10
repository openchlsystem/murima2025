from django.urls import path
from .views import (
    ReferenceDataTypeListCreateView,
    ReferenceDataTypeDetailView,
    ReferenceDataListCreateView,
    ReferenceDataDetailView,
    ReferenceDataHistoryListView,
    ReferenceDataHistoryDetailView,
)

urlpatterns = [
    # Reference Data Types
    path('types/', ReferenceDataTypeListCreateView.as_view(), name='reference-data-type-list'),
    path('types/<uuid:pk>/', ReferenceDataTypeDetailView.as_view(), name='reference-data-type-detail'),

    # Reference Data Entries
    path('entries/', ReferenceDataListCreateView.as_view(), name='reference-data-entry-list'),
    path('entries/<uuid:pk>/', ReferenceDataDetailView.as_view(), name='reference-data-entry-detail'),

    # Reference Data History
    path('history/', ReferenceDataHistoryListView.as_view(), name='reference-data-history-list'),
    path('history/<uuid:pk>/', ReferenceDataHistoryDetailView.as_view(), name='reference-data-history-detail'),
]
