from django_tenants.models import TenantMixin
from tenants.models import Tenant

class Case(BaseModel):
    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('IN_PROGRESS', 'In Progress'),
        ('CLOSED', 'Closed'),
    ]

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)  # Tenant isolation
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPEN')
    assigned_to = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='assigned_cases'
    )

    def __str__(self):
        return f"{self.title} ({self.status})"