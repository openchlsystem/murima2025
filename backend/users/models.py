from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from tenants.models import Tenant  # Adjust import path if needed
from django.core.mail import send_mail



class BaseModel(models.Model):
    """
    Abstract base model to add audit fields.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        'User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(class)s_created_by'
    )
    updated_by = models.ForeignKey(
        'User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(class)s_updated_by'
    )

    class Meta:
        abstract = True


class User(AbstractUser):
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='users'
    )
    phone = models.CharField(max_length=20, blank=True)
    is_verified = models.BooleanField(default=False)

    # Fix reverse accessor clashes with groups and permissions
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_('The groups this user belongs to.'),
        related_name="custom_user_set",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="custom_user_set",
        related_query_name="user",
    )

    def __str__(self):
        return self.username or self.phone or self.email or "User"


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    permissions = models.ManyToManyField(Permission, blank=True)
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='roles'
    )

    def __str__(self):
        return self.name


from django.db import models
from django.utils import timezone
from datetime import timedelta

class OTP(models.Model):
    class DeliveryMethods(models.TextChoices):
        SMS = 'sms', 'SMS'
        EMAIL = 'email', 'Email'
        WHATSAPP = 'whatsapp', 'WhatsApp'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='otps')
    code = models.CharField(max_length=6)
    delivery_method = models.CharField(max_length=10, choices=DeliveryMethods.choices)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_valid(self):
        return not self.is_used and timezone.now() < self.expires_at

    def __str__(self):
        return f"OTP for {self.user} via {self.delivery_method}"

    @classmethod
    def generate_otp(cls, user, method, length=6, expiry_minutes=5):
        import random

        code = ''.join(str(random.randint(0, 9)) for _ in range(length))
        expires_at = timezone.now() + timedelta(minutes=expiry_minutes)

        otp_instance = cls.objects.create(
            user=user,
            code=code,
            delivery_method=method,
            expires_at=expires_at
        )
        return otp_instance

    @classmethod
    def verify_otp(cls, user, code, method):
        now = timezone.now()
        try:
            otp = cls.objects.get(
                user=user,
                code=code,
                delivery_method=method,
                is_used=False,
                expires_at__gt=now
            )
        except cls.DoesNotExist:
            return False

        otp.is_used = True
        otp.save()
        return True


    @classmethod
    def send_otp(cls, user, otp_instance):
        contact = user.email if otp_instance.delivery_method == cls.DeliveryMethods.EMAIL else user.phone

        if otp_instance.delivery_method == cls.DeliveryMethods.EMAIL:
            subject = 'Your OTP Code'
            message = (
                f"Hello {user.username},\n\n"
                f"Your OTP code is: {otp_instance.code}\n"
                f"It will expire in 5 minutes.\n\n"
                f"Thanks,\nBITZ Support Team"
            )
            try:
                send_mail(
                    subject,
                    message,
                    'support@bitz-itc.com',  # Must match your DEFAULT_FROM_EMAIL
                    [contact],
                    fail_silently=False,
                )
                print("✅ OTP email sent.")
            except Exception as e:
                print("❌ EMAIL ERROR:", e)
        else:
            print(f"Sending OTP {otp_instance.code} to {contact} via {otp_instance.delivery_method}")