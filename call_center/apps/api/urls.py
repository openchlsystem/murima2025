# apps/api/urls.py (updated)
from django.urls import path, include
from .schemas.schema import urlpatterns as schema_urls

urlpatterns = [
    # API v1 urls
    path('v1/', include('apps.api.v1.urls')),
    
    # Auth endpoints
    path('auth/', include('apps.accounts.urls')),
    
    # API documentation
    *schema_urls,
]