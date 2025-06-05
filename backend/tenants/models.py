from django.db import models
from django_tenants.models import TenantMixin, DomainMixin  # ✅ Required for multi-tenancy


class TimeStampedUserModel(models.Model):
    """
    Abstract model with timestamps + user tracking.
    Handles cases where request.user may be None (e.g., API calls without auth).
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        'users.User',  # Use string reference to avoid import issues
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_%(class)s'
    )
    updated_by = models.ForeignKey(
        'users.User',  # Use string reference here as well
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='updated_%(class)s'
    )

    class Meta:
        abstract = True


class Tenant(TenantMixin, models.Model):  # 👈 must inherit from both
    name = models.CharField(max_length=100)
    paid_until = models.DateField()
    on_trial = models.BooleanField(default=True)
    created_on = models.DateField(auto_now_add=True)
    enable_ai = models.BooleanField(default=False)
    enable_analytics = models.BooleanField(default=False)

    auto_create_schema = True  # only relevant during schema creation

    def __str__(self):
        return self.name


class Domain(DomainMixin):
    pass
