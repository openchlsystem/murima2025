# apps/api/schemas/schema.py
from rest_framework import permissions
from drf_yasg.views import get_schema_view # type: ignore
from drf_yasg import openapi # type: ignore
from django.urls import path

schema_view = get_schema_view(
    openapi.Info(
        title="Call Center API",
        default_version='v1',
        description="API documentation for the Call Center system",
        terms_of_service="https://www.example.com/policies/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.IsAuthenticated],
)

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]