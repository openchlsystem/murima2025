# config/settings/test.py
"""
Test-specific settings for Call Center project.
"""

from .base import *

# Set debug to False in tests
DEBUG = False

# Use a fast password hasher for testing
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Use in-memory SQLite database for testing
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Disable migrations in tests
class DisableMigrations:
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return None

MIGRATION_MODULES = DisableMigrations()

# Disable celery tasks in tests
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

# Use console email backend for tests
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Reduce password strength requirements for tests
AUTH_PASSWORD_VALIDATORS = []

# Mock AI services for testing
AI_SETTINGS.update({
    'log_interactions': False,
    'providers': {
        'mock': {
            'api_key': 'test-key',
            'model': 'test-model',
        }
    }
})