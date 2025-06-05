# config/settings/base.py
"""
Base settings for Call Center project.
These settings are common to all environments.
"""

import os
from pathlib import Path
from django.db import connections
from decouple import config

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('DJANGO_SECRET_KEY', default='your-default-development-only-secret-key')

# Database configuration for django-tenants
DATABASES = {
    'default': {
        'ENGINE': 'django_tenants.postgresql_backend',
        'NAME': config('DB_NAME', default='callcenter_db'),
        'USER': config('DB_USER', default='callcenter_user'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}

DATABASE_ROUTERS = (
    'django_tenants.routers.TenantSyncRouter',
)

# Django Tenants Configuration
TENANT_MODEL = "tenant.Tenant"
TENANT_DOMAIN_MODEL = "tenant.Domain"

# Shared apps (available to all tenants and public schema)
SHARED_APPS = [
    'django_tenants',  # Must be first
    
    # Django core apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party apps that should be shared
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'django_filters',
    'import_export',
    'phonenumber_field',
    'drf_yasg',
    
    # Your shared apps (tenant management, core utilities)
    'apps.tenant.apps.TenantConfig',  # Tenant management
    'apps.core',    # Core utilities and base models
    'apps.accounts', # User management (shared across tenants)
    'apps.security.apps.SecurityConfig', # Security middleware and models
    'apps.admin_config.apps.AdminConfigConfig', # Admin configuration
]

# Tenant-specific apps (isolated per tenant)
TENANT_APPS = [
    # Django core apps (needed in tenant schemas)
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    
    # Third-party apps for tenant data
    'simple_history',
    
    # Your tenant-specific apps
    'apps.contacts',      # Contact management
    'apps.calls',         # Call tracking and management
    'apps.campaigns',     # Campaign management
    'apps.cases',         # Case management
    'apps.communications', # Communications/messaging
    'apps.ivr',           # IVR and voice management
    'apps.quality',       # Quality assurance
    'apps.analytics',     # Analytics and reporting
    'apps.notifications', # Notifications
    'apps.ai',            # AI services
    'apps.workflows',     # Workflow management
    'apps.api',           # API endpoints
]

# Combined INSTALLED_APPS (django-tenants will handle routing)
INSTALLED_APPS = list(SHARED_APPS) + [app for app in TENANT_APPS if app not in SHARED_APPS]

# Middleware configuration for django-tenants
MIDDLEWARE = [
    'django_tenants.middleware.main.TenantMainMiddleware',  # Must be first
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'simple_history.middleware.HistoryRequestMiddleware',  # Commented out for now
    # 'apps.core.middleware.AuditMiddleware',  # Will be created later
    # 'apps.security.middleware.SecurityMiddleware',  # Will be created later
]

ROOT_URLCONF = 'config.urls'

# Template configuration
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 10,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Custom user model
AUTH_USER_MODEL = 'accounts.User'

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Nairobi'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'apps.api.pagination.StandardResultsSetPagination',
    'PAGE_SIZE': 25,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
    'EXCEPTION_HANDLER': 'apps.api.exceptions.custom_exception_handler',
}

# CORS settings
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # Vue.js frontend
    "http://127.0.0.1:3000",
    "http://localhost:8080",  # Alternative Vue.js port
    "http://127.0.0.1:8080",
]

# SWAGGER settings
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },
    'USE_SESSION_AUTH': True,
    'LOGIN_URL': 'rest_framework:login',
    'LOGOUT_URL': 'rest_framework:logout',
}

# Django Tenants specific settings
TENANT_APPS_DIR = 'apps'
PUBLIC_SCHEMA_URLCONF = 'config.urls_public'

# Main URLconf for tenant schemas
ROOT_URLCONF = 'config.urls'

# Show tenant context in logs
SHOW_TENANT_IN_LOGS = True

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {name} {funcName} {lineno} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs' / 'callcenter.log',
            'maxBytes': 10 * 1024 * 1024,  # 10 MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True,
        },
        'django_tenants': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'callcenter': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'apps': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

# Celery configuration
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE

# Email configuration (configured in environment-specific settings)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# AI settings
AI_SETTINGS = {
    'default_provider': 'openai',
    'log_interactions': True,
    'max_suggestions': 5,
    'cache_responses': True,
    'cache_timeout': 3600,  # 1 hour
}

# Asterisk Integration Settings
ASTERISK_SETTINGS = {
    'ami': {
        'host': os.environ.get('ASTERISK_HOST', 'localhost'),
        'port': int(os.environ.get('ASTERISK_PORT', 5038)),
        'username': os.environ.get('ASTERISK_AMI_USER', 'admin'),
        'password': os.environ.get('ASTERISK_AMI_PASSWORD', 'admin'),
    },
    'agi': {
        'host': os.environ.get('FASTAGI_HOST', '0.0.0.0'),
        'port': int(os.environ.get('FASTAGI_PORT', 4573)),
    },
    'recording_path': os.environ.get('RECORDING_PATH', '/var/spool/asterisk/monitor/'),
}

# Cache configuration (Redis recommended for multi-tenant)
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': config('REDIS_URL', default='redis://127.0.0.1:6379/1'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        'KEY_PREFIX': 'callcenter',
        'TIMEOUT': 300,  # 5 minutes default
    }
}

# Session configuration (will be overridden in development)
SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # Use database by default
SESSION_COOKIE_AGE = 86400  # 24 hours
SESSION_COOKIE_SECURE = False  # Will be True in production
SESSION_COOKIE_HTTPONLY = True

# Security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# File upload settings
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB

# Tenant-specific storage (if needed)
DEFAULT_FILE_STORAGE = 'django_tenants.files.storage.TenantFileSystemStorage'

# Create required directories
logs_dir = BASE_DIR / 'logs'
logs_dir.mkdir(exist_ok=True)

media_dir = BASE_DIR / 'media'
media_dir.mkdir(exist_ok=True)

static_dir = BASE_DIR / 'static'
static_dir.mkdir(exist_ok=True)