# config/settings/production.py
"""
Production-specific settings for Call Center project.
"""

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    os.environ.get('DJANGO_ALLOWED_HOSTS', 'callcenter.example.com').split(',')
]

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT', '3306'),
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

# CORS settings for production
CORS_ALLOWED_ORIGINS = os.environ.get('CORS_ALLOWED_ORIGINS', '').split(',')

# Password validation - stronger in production
AUTH_PASSWORD_VALIDATORS.append({
    'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    'OPTIONS': {
        'min_length': 12,
    }
})

# Security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Email settings
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')
SERVER_EMAIL = os.environ.get('SERVER_EMAIL', DEFAULT_FROM_EMAIL)

# Logging settings - more comprehensive in production
LOGGING['handlers']['file']['level'] = 'WARNING'
LOGGING['handlers']['mail_admins'] = {
    'level': 'ERROR',
    'class': 'django.utils.log.AdminEmailHandler',
    'formatter': 'verbose',
}
LOGGING['loggers']['django']['handlers'].append('mail_admins')

# AI settings for production
AI_SETTINGS.update({
    'providers': {
        'openai': {
            'api_key': os.environ.get('OPENAI_API_KEY'),
            'model': os.environ.get('OPENAI_MODEL', 'gpt-4'),
        },
        'azure': {
            'api_key': os.environ.get('AZURE_OPENAI_API_KEY'),
            'api_url': os.environ.get('AZURE_OPENAI_ENDPOINT'),
            'model': os.environ.get('AZURE_OPENAI_MODEL', 'gpt-4'),
        }
    }
})