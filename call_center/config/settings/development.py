# config/settings/development.py
from .base import *
from decouple import config

DEBUG = True

# Additional development-specific settings
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '*.localhost', 'demo.localhost', 'public.localhost']

# Development-specific middleware
MIDDLEWARE += [
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',  # Commented out for now
]

# Development-specific apps
INSTALLED_APPS += [
    # 'debug_toolbar',  # Commented out for now
    # 'django_extensions',  # Can be added if needed
]

INTERNAL_IPS = [
    '127.0.0.1',
    'localhost',
]

# CORS settings for development
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# Cache settings for development (disable caching)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# Email backend for development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Additional debugging
LOGGING['loggers']['django']['level'] = 'DEBUG'
LOGGING['loggers']['apps']['level'] = 'DEBUG'