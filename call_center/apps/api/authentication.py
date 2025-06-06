# apps/api/authentication.py
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.utils import timezone
from datetime import timedelta
from django.conf import settings

class ExpiringTokenAuthentication(TokenAuthentication):
    """
    Token authentication with expiry.
    """
    
    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise AuthenticationFailed('Invalid token')

        if not token.user.is_active:
            raise AuthenticationFailed('User inactive or deleted')

        # Check if token has expired
        token_expiry = getattr(settings, 'TOKEN_EXPIRY_HOURS', 24)
        expiry_time = token.created + timedelta(hours=token_expiry)
        
        if expiry_time < timezone.now():
            token.delete()
            raise AuthenticationFailed('Token has expired')

        return (token.user, token)