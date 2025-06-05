# apps/admin_config/apps.py
from django.apps import AppConfig


class AdminConfigConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.admin_config'
    verbose_name = 'Admin Configuration'