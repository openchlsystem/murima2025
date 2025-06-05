# apps/tenant/management/commands/setup_tenants.py
from django.core.management.base import BaseCommand
from django.utils.translation import gettext as _
from apps.tenant.models import Tenant, Domain


class Command(BaseCommand):
    help = 'Set up initial tenants (public and demo)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--demo-domain',
            type=str,
            default='demo.localhost:8000',
            help='Domain for the demo tenant'
        )
        parser.add_argument(
            '--public-domain',
            type=str,
            default='public.localhost:8000',
            help='Domain for the public tenant'
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Setting up initial tenants...'))

        # Create public tenant (required by django-tenants)
        public_tenant, created = Tenant.objects.get_or_create(
            schema_name='public',
            defaults={
                'name': 'Public',
                'description': 'Public tenant for shared resources and tenant management'
            }
        )
        
        if created:
            self.stdout.write(
                self.style.SUCCESS(f'Created public tenant: {public_tenant.name}')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'Public tenant already exists: {public_tenant.name}')
            )

        # Create domain for public tenant
        public_domain, created = Domain.objects.get_or_create(
            domain=options['public_domain'],
            defaults={
                'tenant': public_tenant,
                'is_primary': True
            }
        )
        
        if created:
            self.stdout.write(
                self.style.SUCCESS(f'Created public domain: {public_domain.domain}')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'Public domain already exists: {public_domain.domain}')
            )

        # Create demo tenant
        demo_tenant, created = Tenant.objects.get_or_create(
            schema_name='demo',
            defaults={
                'name': 'Demo Organization',
                'description': 'Demo tenant for testing call center functionality',
                'contact_email': 'admin@demo.localhost',
                'contact_person': 'Demo Admin',
                'subscription_plan': 'professional',
                'max_users': 50,
                'max_contacts': 5000,
                'max_campaigns': 10,
            }
        )
        
        if created:
            self.stdout.write(
                self.style.SUCCESS(f'Created demo tenant: {demo_tenant.name}')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'Demo tenant already exists: {demo_tenant.name}')
            )

        # Create domain for demo tenant
        demo_domain, created = Domain.objects.get_or_create(
            domain=options['demo_domain'],
            defaults={
                'tenant': demo_tenant,
                'is_primary': True
            }
        )
        
        if created:
            self.stdout.write(
                self.style.SUCCESS(f'Created demo domain: {demo_domain.domain}')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'Demo domain already exists: {demo_domain.domain}')
            )

        # Summary
        self.stdout.write(
            self.style.SUCCESS('\n=== Tenant Setup Complete ===')
        )
        self.stdout.write(f'Public Schema: {options["public_domain"]}')
        self.stdout.write(f'Demo Tenant: {options["demo_domain"]}')
        self.stdout.write(
            self.style.WARNING('\nNext steps:')
        )
        self.stdout.write('1. Run: python manage.py migrate_schemas')
        self.stdout.write('2. Add domains to /etc/hosts:')
        self.stdout.write(f'   127.0.0.1 {options["demo_domain"].split(":")[0]}')
        self.stdout.write(f'   127.0.0.1 {options["public_domain"].split(":")[0]}')
        self.stdout.write('3. Create superuser: python manage.py createsuperuser')
        self.stdout.write('4. Run server: python manage.py runserver')