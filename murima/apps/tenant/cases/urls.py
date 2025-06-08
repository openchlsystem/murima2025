from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'cases', views.CaseViewSet, basename='case')

urlpatterns = [
    path('', include(router.urls)),
    
    # Case Types
    path('case-types/', views.CaseTypeListCreateView.as_view(), name='case-type-list'),
    path('case-types/<int:pk>/', views.CaseTypeRetrieveUpdateDestroyView.as_view(), name='case-type-detail'),
    
    # Case Statuses
    path('case-statuses/', views.CaseStatusListCreateView.as_view(), name='case-status-list'),
    path('case-statuses/<int:pk>/', views.CaseStatusRetrieveUpdateDestroyView.as_view(), name='case-status-detail'),
    
    # Case Bulk Actions
    path('cases/bulk-update/', views.CaseBulkUpdateView.as_view(), name='case-bulk-update'),
    
    # Nested Resources
    path('cases/<int:case_id>/notes/', views.CaseNoteListCreateView.as_view(), name='case-note-list'),
    path('cases/<int:case_id>/attachments/', views.CaseAttachmentListCreateView.as_view(), name='case-attachment-list'),
    path('cases/<int:case_id>/event-logs/', views.CaseEventLogListView.as_view(), name='case-event-log-list'),
    
    # Workflows and SLAs
    path('workflows/', views.CaseWorkflowListCreateView.as_view(), name='case-workflow-list'),
    path('slas/', views.CaseSLAListCreateView.as_view(), name='case-sla-list'),
]