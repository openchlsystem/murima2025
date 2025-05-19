
from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class TimeStampedUserModel(models.Model):
    """
    Abstract model with timestamps + user tracking.
    Handles cases where request.user may be None (e.g., API calls without auth).
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_%(class)s'  # Dynamic related name (e.g., 'created_tenant')
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='updated_%(class)s'
    )

    class Meta:
        abstract = True




class Tenant(TenantMixin):
    name = models.CharField(max_length=100)
    paid_until = models.DateField()
    on_trial = models.BooleanField(default=True)
    created_on = models.DateField(auto_now_add=True)
    enable_ai = models.BooleanField(default=False)
    enable_analytics = models.BooleanField(default=False)
    auto_create_schema = True

class Domain(DomainMixin):
    pass