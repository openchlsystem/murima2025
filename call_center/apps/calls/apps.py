# apps/calls/apps.py
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CallsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.calls'
    verbose_name = _('Calls')
    
    def ready(self):
        """Import signal handlers when app is ready"""
        try:
            import apps.calls.signals  # noqa F401
        except ImportError:
            pass