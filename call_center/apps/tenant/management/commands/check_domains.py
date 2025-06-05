# apps/tenant/management/commands/check_domains.py
from django.core.management.base import BaseCommand
from apps.tenant.models import Tenant, Domain


class Command(BaseCommand):
    help = 'Check existing tenants and domains'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=== Current Tenants and Domains ==='))
        
        tenants = Tenant.objects.all()
        
        for tenant in tenants:
            self.stdout.write(f'\nTenant: {tenant.name}')
            self.stdout.write(f'  Schema: {tenant.schema_name}')
            self.stdout.write(f'  Active: {tenant.is_active}')
            
            domains = Domain.objects.filter(tenant=tenant)
            self.stdout.write(f'  Domains:')
            for domain in domains:
                primary = " (PRIMARY)" if domain.is_primary else ""
                self.stdout.write(f'    - {domain.domain}{primary}')
            
            if not domains.exists():
                self.stdout.write(f'    - No domains configured!')
        
        if not tenants.exists():
            self.stdout.write(self.style.ERROR('No tenants found in database!'))