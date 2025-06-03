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
        abstract = True  # Makes this a reusable base class
        
        

# workflows/models.py
from django.db import models
from core.models import BaseModel
from tenants.models import Tenant

class Workflow(BaseModel):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)  # Tenant isolation
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.tenant.name})"

class Step(BaseModel):
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE, related_name='steps')
    name = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0)
    action = models.CharField(max_length=200)  # e.g., "send_email", "escalate"

    class Meta:
        ordering = ['order']