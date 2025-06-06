# apps/tenant/management/commands/fix_domains.py
from django.core.management.base import BaseCommand
from apps.tenant.models import Tenant, Domain


class Command(BaseCommand):
    help = 'Fix domain configurations for tenants'

    def add_arguments(self, parser):
        parser.add_argument(
            '--port',
            type=str,
            default='8000',
            help='Port number to use in domain names'
        )

    def handle(self, *args, **options):
        port = options['port']
        
        self.stdout.write(self.style.SUCCESS(f'Fixing domains with port {port}...'))
        
        # Fix public tenant domain
        try:
            public_tenant = Tenant.objects.get(schema_name='public')
            public_domain, created = Domain.objects.get_or_create(
                tenant=public_tenant,
                is_primary=True,
                defaults={'domain': f'public.localhost:{port}'}
            )
            
            if not created:
                # Update existing domain
                public_domain.domain = f'public.localhost:{port}'
                public_domain.save()
                self.stdout.write(f'Updated public domain: {public_domain.domain}')
            else:
                self.stdout.write(f'Created public domain: {public_domain.domain}')
                
        except Tenant.DoesNotExist:
            self.stdout.write(self.style.ERROR('Public tenant not found!'))
            return
        
        # Fix demo tenant domain
        try:
            demo_tenant = Tenant.objects.get(schema_name='demo')
            demo_domain, created = Domain.objects.get_or_create(
                tenant=demo_tenant,
                is_primary=True,
                defaults={'domain': f'demo.localhost:{port}'}
            )
            
            if not created:
                # Update existing domain
                demo_domain.domain = f'demo.localhost:{port}'
                demo_domain.save()
                self.stdout.write(f'Updated demo domain: {demo_domain.domain}')
            else:
                self.stdout.write(f'Created demo domain: {demo_domain.domain}')
                
        except Tenant.DoesNotExist:
            self.stdout.write(self.style.ERROR('Demo tenant not found!'))
            return
        
        # Also create domains without port for production use
        if port == '8000':
            # Create additional domains without port
            public_domain_no_port, created = Domain.objects.get_or_create(
                tenant=public_tenant,
                domain='public.localhost',
                defaults={'is_primary': False}
            )
            if created:
                self.stdout.write(f'Created additional public domain: {public_domain_no_port.domain}')
            
            demo_domain_no_port, created = Domain.objects.get_or_create(
                tenant=demo_tenant,
                domain='demo.localhost',
                defaults={'is_primary': False}
            )
            if created:
                self.stdout.write(f'Created additional demo domain: {demo_domain_no_port.domain}')
        
        self.stdout.write(self.style.SUCCESS('\nDomain fix complete!'))
        self.stdout.write('You can now access:')
        self.stdout.write(f'  Public: http://public.localhost:{port}/')
        self.stdout.write(f'  Demo:   http://demo.localhost:{port}/')
        
        if port == '8000':
            self.stdout.write('\nAlso available without port:')
            self.stdout.write('  Public: http://public.localhost/')
            self.stdout.write('  Demo:   http://demo.localhost/')