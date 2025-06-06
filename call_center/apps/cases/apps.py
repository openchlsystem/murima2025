# apps/cases/apps.py
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CasesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.cases'
    verbose_name = _('Case Management')
    
    # def ready(self):
    #     """Import signal handlers when app is ready"""
    #     try:
    #         import apps.cases.signals  # noqa F401
    #     except ImportError:
    #         pass