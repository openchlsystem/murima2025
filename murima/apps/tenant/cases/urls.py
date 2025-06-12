from django.urls import path
from .views import (
    CaseTypeListCreateView,
    CaseTypeRetrieveUpdateDestroyView,
    CaseStatusListCreateView,
    CaseStatusRetrieveUpdateDestroyView,
    CaseListCreateView,
    CaseRetrieveUpdateDestroyView,
    MyAssignedCasesView,
    MyTeamCasesView,
    CaseDocumentListCreateView,
    CaseDocumentRetrieveUpdateDestroyView,
    CaseNoteListCreateView,
    CaseNoteRetrieveUpdateDestroyView,
    CaseHistoryListView,
    CaseLinkListCreateView,
    CaseLinkRetrieveUpdateDestroyView,
    CaseTemplateListCreateView,
    CaseTemplateRetrieveUpdateDestroyView,
    SLAListCreateView,
    SLARetrieveUpdateDestroyView,
    WorkflowRuleListCreateView,
    WorkflowRuleRetrieveUpdateDestroyView,
    AuditLogListView,
)

urlpatterns = [
    # Case Types
    path('case-types/', CaseTypeListCreateView.as_view(), name='case-type-list'),
    path('case-types/<int:pk>/', CaseTypeRetrieveUpdateDestroyView.as_view(), name='case-type-detail'),
    
    # Case Statuses
    path('case-statuses/', CaseStatusListCreateView.as_view(), name='case-status-list'),
    path('case-statuses/<int:pk>/', CaseStatusRetrieveUpdateDestroyView.as_view(), name='case-status-detail'),
    
    # Cases
    path('cases/', CaseListCreateView.as_view(), name='case-list'),
    path('cases/<int:pk>/', CaseRetrieveUpdateDestroyView.as_view(), name='case-detail'),
    path('my-assigned-cases/', MyAssignedCasesView.as_view(), name='my-assigned-cases'),
    path('my-team-cases/', MyTeamCasesView.as_view(), name='my-team-cases'),
    
    # Case Documents
    path('cases/<int:case_pk>/documents/', CaseDocumentListCreateView.as_view(), name='case-document-list'),
    path('cases/<int:case_pk>/documents/<int:pk>/', CaseDocumentRetrieveUpdateDestroyView.as_view(), name='case-document-detail'),
    
    # Case Notes
    path('cases/<int:case_pk>/notes/', CaseNoteListCreateView.as_view(), name='case-note-list'),
    path('cases/<int:case_pk>/notes/<int:pk>/', CaseNoteRetrieveUpdateDestroyView.as_view(), name='case-note-detail'),
    
    # Case History
    path('cases/<int:case_pk>/history/', CaseHistoryListView.as_view(), name='case-history-list'),
    
    # Case Links
    path('cases/<int:case_pk>/links/', CaseLinkListCreateView.as_view(), name='case-link-list'),
    path('cases/<int:case_pk>/links/<int:pk>/', CaseLinkRetrieveUpdateDestroyView.as_view(), name='case-link-detail'),
    
    # Case Templates
    path('case-templates/', CaseTemplateListCreateView.as_view(), name='case-template-list'),
    path('case-templates/<int:pk>/', CaseTemplateRetrieveUpdateDestroyView.as_view(), name='case-template-detail'),
    
    # SLAs
    path('slas/', SLAListCreateView.as_view(), name='sla-list'),
    path('slas/<int:pk>/', SLARetrieveUpdateDestroyView.as_view(), name='sla-detail'),
    
    # Workflow Rules
    path('workflow-rules/', WorkflowRuleListCreateView.as_view(), name='workflow-rule-list'),
    path('workflow-rules/<int:pk>/', WorkflowRuleRetrieveUpdateDestroyView.as_view(), name='workflow-rule-detail'),
    
    # Audit Logs
    path('audit-logs/', AuditLogListView.as_view(), name='audit-log-list'),
]