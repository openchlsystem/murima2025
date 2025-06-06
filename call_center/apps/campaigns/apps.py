# apps/campaigns/apps.py
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CampaignsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.campaigns'
    verbose_name = _('Campaigns')
    
    # def ready(self):
    #     """Import signal handlers when app is ready"""
    #     try:
    #         import apps.campaigns.signals  # noqa F401
    #     except ImportError:
    #         pass