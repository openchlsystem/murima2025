from django.urls import path
from . import views

app_name = 'calls'

urlpatterns = [
    # Extension management endpoints
    path('v1/extensions/', views.create_extension, name='create_extension'),
    path('v1/extensions/user/<int:user_id>/', views.get_user_extension, name='get_user_extension'),
    path('v1/extensions/<int:extension_id>/status/', views.extension_status, name='extension_status'),
    path('v1/extensions/<int:extension_id>/', views.delete_extension, name='delete_extension'),
    
    # Call logs endpoints
    path('call-logs/user/<int:user_id>/', views.get_user_call_logs, name='get_user_call_logs'),
]