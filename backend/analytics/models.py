# core/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='%(class)s_created'
    )
    updated_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='%(class)s_updated'
    )

    class Meta:
        abstract = True  # Marks this as a reusable base class
        

# analytics/models.py
from django.db import models
from core.models import BaseModel
from tenants.models import Tenant

class Dashboard(BaseModel):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.tenant.name})"

class Widget(BaseModel):
    dashboard = models.ForeignKey(Dashboard, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    widget_type = models.CharField(max_length=50)  # e.g., "line_chart", "pie_chart"
    data_config = models.JSONField()  # Stores chart configuration

    class Meta:
        ordering = ['-created_at']