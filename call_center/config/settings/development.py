# config/settings/development.py
from .base import *
from decouple import config

DEBUG = True

# Additional development-specific settings
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '.localhost',
]

ASTERISK_ARI_URL = 'http://YOUR_ASTERISK_SERVER_IP:8088/ari'
ASTERISK_ARI_WS_URL = 'ws://YOUR_ASTERISK_SERVER_IP:8088/ari/events'
ASTERISK_ARI_USERNAME = 'djangoari'
ASTERISK_ARI_PASSWORD = '2001'
ASTERISK_ARI_APP = 'django_calls'


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