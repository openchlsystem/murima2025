from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

# Document Types
router.register(r'types', views.DocumentTypeViewSet, basename='documenttype')

# Document Templates
router.register(r'templates', views.DocumentTemplateViewSet, basename='documenttemplate')

urlpatterns = [
    path('', include(router.urls)),
    
    # Documents
    path('documents/', views.DocumentListCreateView.as_view(), name='document-list'),
    path('documents/search/', views.DocumentSearchView.as_view(), name='document-search'),
    path('documents/<int:pk>/', views.DocumentRetrieveUpdateDestroyView.as_view(), name='document-detail'),
    path('documents/<int:pk>/download/', views.DocumentDownloadView.as_view(), name='document-download'),
    path('documents/<int:pk>/preview/', views.DocumentPreviewRetrieveView.as_view(), name='document-preview'),
    
    # Document Versions
    path('documents/<int:document_pk>/versions/', views.DocumentVersionListView.as_view(), name='document-version-list'),
    path('documents/<int:document_pk>/versions/<int:version>/download/', 
         views.DocumentVersionDownloadView.as_view(), name='document-version-download'),
    
    # Document Access Logs
    path('documents/<int:document_pk>/access-logs/', 
         views.DocumentAccessLogListView.as_view(), name='document-access-log-list'),
    
    # Document Sharing
    path('documents/<int:document_pk>/share/', 
         views.DocumentShareLinkCreateView.as_view(), name='document-share-create'),
    path('share/<uuid:token>/', views.DocumentShareLinkRetrieveView.as_view(), name='document-share-retrieve'),
    path('share/<uuid:token>/download/', 
         views.DocumentShareLinkDownloadView.as_view(), name='document-share-download'),
    
    # Bulk Operations
    path('documents/bulk-update/', views.DocumentBulkUpdateView.as_view(), name='document-bulk-update'),
    
    # Additional endpoints can be added here
]

# If you want to add versioning to your API
v1_urlpatterns = [
    path('v1/', include(urlpatterns)),
]

urlpatterns += v1_urlpatterns