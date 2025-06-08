from django.urls import path
from .views.reference_data_type import (
    ReferenceDataTypeListCreateView,
    ReferenceDataTypeDetailView,
)
from .views.reference_data import (
    ReferenceDataListCreateView,
    ReferenceDataDetailView,
    ReferenceDataByTypeView,
    ReferenceDataBulkUpdateView,
)
from .views.reference_data_history import (
    ReferenceDataHistoryListView,
    ReferenceDataHistoryDetailView,
)

urlpatterns = [
    path('types/', ReferenceDataTypeListCreateView.as_view(), name='reference-data-type-list'),
    path('types/<str:name>/', ReferenceDataTypeDetailView.as_view(), name='reference-data-type-detail'),
    path('data/', ReferenceDataListCreateView.as_view(), name='reference-data-list'),
    path('data/<int:pk>/', ReferenceDataDetailView.as_view(), name='reference-data-detail'),
    path('data/type/<str:data_type>/', ReferenceDataByTypeView.as_view(), name='reference-data-by-type'),
    path('data/bulk/', ReferenceDataBulkUpdateView.as_view(), name='reference-data-bulk-update'),
    path('history/', ReferenceDataHistoryListView.as_view(), name='reference-data-history-list'),
    path('history/<int:pk>/', ReferenceDataHistoryDetailView.as_view(), name='reference-data-history-detail'),
]