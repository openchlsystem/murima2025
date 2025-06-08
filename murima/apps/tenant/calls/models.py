from django.db import models

# Create your models here.
# asterisk_app/models.py
from django.db import models
from django.conf import settings
import secrets
import string


class AsteriskExtension(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='asterisk_extension'
    )
    extension_number = models.CharField(max_length=20, unique=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)
    tenant = models.ForeignKey(
        'users.Tenant',  # Adjust this to your actual Tenant model path
        on_delete=models.CASCADE,
        related_name='asterisk_extensions'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Asterisk specific fields
    asterisk_created = models.BooleanField(default=False)
    asterisk_error = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = 'asterisk_extensions'
        verbose_name = 'Asterisk Extension'
        verbose_name_plural = 'Asterisk Extensions'
    
    def __str__(self):
        return f"{self.user.email} - {self.extension_number}"
    
    @classmethod
    def generate_extension_number(cls, tenant_id):
        """Generate unique extension number for tenant"""
        # Start with tenant-specific prefix (e.g., tenant_id + base)
        base_number = 1000 + (tenant_id * 1000)
        
        # Find the next available number
        existing_extensions = cls.objects.filter(
            tenant_id=tenant_id
        ).values_list('extension_number', flat=True)
        
        for i in range(100):  # Support up to 100 extensions per tenant
            candidate = str(base_number + i)
            if candidate not in existing_extensions:
                return candidate
        
        raise ValueError(f"No available extension numbers for tenant {tenant_id}")
    
    @classmethod
    def generate_credentials(cls):
        """Generate random username and password"""
        # Username: 8 characters alphanumeric
        username = ''.join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(8))
        
        # Password: 12 characters with special chars
        password_chars = string.ascii_letters + string.digits + "!@#$%^&*"
        password = ''.join(secrets.choice(password_chars) for _ in range(12))
        
        return username, password