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
        related_name="%(class)s_created"
    )
    updated_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name="%(class)s_updated"
    )

    class Meta:
        abstract = True  # Makes this a reusable base class
        

from django.db import models
from tenants.models import Tenant
from core.models import BaseModel

class AIService(BaseModel):
    SERVICE_CHOICES = [
        ('OPENAI', 'OpenAI'),
        ('HUGGINGFACE', 'Hugging Face'),
        ('DIALOGFLOW', 'Dialogflow'),
    ]
    
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    service_type = models.CharField(max_length=50, choices=SERVICE_CHOICES)
    api_key = models.CharField(max_length=255, blank=True)  # Encrypt in production!
    is_active = models.BooleanField(default=False)
    config = models.JSONField(default=dict)  # For flexible service-specific settings

    def __str__(self):
        return f"{self.name} ({self.service_type})"

class AIModel(BaseModel):
    service = models.ForeignKey(AIService, on_delete=models.CASCADE)
    model_name = models.CharField(max_length=100)  # e.g., "gpt-4", "bert-base"
    is_default = models.BooleanField(default=False)

    class Meta:
        unique_together = ['service', 'model_name']