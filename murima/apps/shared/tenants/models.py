from django_tenants.models import TenantMixin, DomainMixin
from django.db import models
import uuid

class Tenant(TenantMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    subdomain = models.CharField(max_length=100, unique=True)
    owner = models.ForeignKey('accounts.User', on_delete=models.PROTECT)
    sector = models.CharField(max_length=50, default='general')
    is_active = models.BooleanField(default=True)
    subscription_plan = models.CharField(max_length=50, default='basic')
    created_at = models.DateTimeField(auto_now_add=True)
    settings = models.JSONField(default=dict)

    # Default database schema is 'public'
    auto_create_schema = True

    def __str__(self):
        return self.name

class Domain(DomainMixin):
    pass