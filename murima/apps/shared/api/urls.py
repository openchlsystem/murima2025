from django.urls import path, include

urlpatterns = [
    path('auth/', include('apps.shared.accounts.urls')),
    path('tenants/', include('apps.shared.tenants.urls')),
    path('cases/', include('apps.tenant.cases.urls')),
    path('communications/', include('apps.tenant.communications.urls')),
    path('calls/', include('apps.tenant.calls.urls')),
    path('contacts/', include('apps.tenant.contacts.urls')),
]