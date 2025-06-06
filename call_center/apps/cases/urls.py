# apps/cases/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'cases'

# API Router for ViewSets
router = DefaultRouter()
router.register(r'cases', views.CaseViewSet)
router.register(r'activities', views.CaseActivityViewSet)
router.register(r'services', views.CaseServiceViewSet)
router.register(r'referrals', views.CaseReferralViewSet)
router.register(r'notes', views.CaseNoteViewSet)
router.register(r'attachments', views.CaseAttachmentViewSet)
router.register(r'updates', views.CaseUpdateViewSet)
router.register(r'categories', views.CaseCategoryViewSet)

urlpatterns = [
    # API URLs
    path('api/v1/', include(router.urls)),
    
    # Custom API endpoints
    path('api/v1/cases/<int:case_id>/assign/', views.AssignCaseView.as_view(), name='assign-case'),
    path('api/v1/cases/<int:case_id>/escalate/', views.EscalateCaseView.as_view(), name='escalate-case'),
    path('api/v1/cases/<int:case_id>/close/', views.CloseCaseView.as_view(), name='close-case'),
    path('api/v1/cases/<int:case_id>/reopen/', views.ReopenCaseView.as_view(), name='reopen-case'),
    path('api/v1/cases/<int:case_id>/add-contact/', views.AddCaseContactView.as_view(), name='add-case-contact'),
    path('api/v1/cases/<int:case_id>/statistics/', views.CaseStatisticsView.as_view(), name='case-statistics'),
    
    # Search and analytics
    path('api/v1/cases/search/', views.CaseSearchView.as_view(), name='case-search'),
    path('api/v1/cases/overdue/', views.OverdueCasesView.as_view(), name='overdue-cases'),
    path('api/v1/cases/follow-up/', views.FollowUpCasesView.as_view(), name='follow-up-cases'),
    path('api/v1/analytics/metrics/', views.CaseMetricsView.as_view(), name='case-metrics'),
    
    # Bulk operations
    path('api/v1/cases/bulk/assign/', views.BulkAssignCasesView.as_view(), name='bulk-assign-cases'),
    path('api/v1/cases/bulk/close/', views.BulkCloseCasesView.as_view(), name='bulk-close-cases'),
    path('api/v1/cases/bulk/export/', views.ExportCasesView.as_view(), name='export-cases'),
    
    # AI endpoints
    path('api/v1/cases/<int:case_id>/ai-analysis/', views.CaseAIAnalysisView.as_view(), name='case-ai-analysis'),
    path('api/v1/cases/<int:case_id>/ai-suggestions/', views.CaseAISuggestionsView.as_view(), name='case-ai-suggestions'),
]