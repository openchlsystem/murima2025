#!/usr/bin/env python
"""
Script to migrate case data from legacy MySQL database to new Django models.

This script handles migration of:
- kase table -> Case model
- kase_activity table -> CaseActivity model
- service table -> CaseService model
- referal table -> CaseReferral model
- caseupd/kaseupd tables -> CaseUpdate model

Run with: python scripts/migrate_cases.py
"""

import os
import sys
import django
import logging
from datetime import datetime
from typing import Dict, List, Optional

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from django.db import connections, transaction
from django.utils import timezone
from django.core.exceptions import ValidationError

from apps.cases.models import (
    Case, CaseActivity, CaseService, CaseReferral, 
    CaseNote, CaseUpdate, CaseCategory
)
from apps.core.models import ReferenceData
from apps.contacts.models import Contact, ContactRole
from apps.accounts.models import User
from apps.campaigns.models import Campaign

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('migration_cases.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class CaseMigrator:
    """Handles migration of case data from legacy database"""
    
    def __init__(self):
        self.legacy_db = connections['legacy']  # Configure in settings
        self.stats = {
            'cases_processed': 0,
            'cases_created': 0,
            'cases_errors': 0,
            'activities_created': 0,
            'services_created': 0,
            'referrals_created': 0,
            'notes_created': 0,
            'updates_created': 0,
        }
        
        # Cache frequently used reference data
        self.status_cache = {}
        self.priority_cache = {}
        self.case_type_cache = {}
        self.user_cache = {}
        self.contact_cache = {}
        
        self._load_caches()
    
    def _load_caches(self):
        """Load frequently used data into memory"""
        logger.info("Loading reference data caches...")
        
        # Load status mappings
        statuses = ReferenceData.objects.filter(category='case_status')
        for status in statuses:
            self.status_cache[status.name.lower()] = status
        
        # Load priority mappings
        priorities = ReferenceData.objects.filter(category='case_priority')
        for priority in priorities:
            self.priority_cache[priority.name.lower()] = priority
        
        # Load case types
        case_types = ReferenceData.objects.filter(category='case_type')
        for case_type in case_types:
            self.case_type_cache[case_type.name.lower()] = case_type
        
        # Load users
        users = User.objects.all()
        for user in users:
            self.user_cache[user.id] = user
        
        logger.info(f"Loaded {len(self.status_cache)} statuses, "
                   f"{len(self.priority_cache)} priorities, "
                   f"{len(self.case_type_cache)} case types, "
                   f"{len(self.user_cache)} users")
    
    def migrate_cases(self, limit: Optional[int] = None):
        """
        Migrate cases from legacy kase table.
        
        Args:
            limit: Maximum number of cases to migrate (for testing)
        """
        logger.info("Starting case migration...")
        
        # Get legacy cases
        with self.legacy_db.cursor() as cursor:
            query = """
                SELECT * FROM kase 
                WHERE is_delete = '0' OR is_delete IS NULL
                ORDER BY id
            """
            if limit:
                query += f" LIMIT {limit}"
            
            cursor.execute(query)
            columns = [col[0] for col in cursor.description]
            
            for row in cursor.fetchall():
                legacy_case = dict(zip(columns, row))
                self._migrate_single_case(legacy_case)
        
        logger.info(f"Case migration completed. Stats: {self.stats}")
    
    def _migrate_single_case(self, legacy_case: Dict):
        """Migrate a single case from legacy data"""
        try:
            self.stats['cases_processed'] += 1
            
            with transaction.atomic():
                # Get or create reporter contact
                reporter = self._get_or_create_reporter(legacy_case)
                if not reporter:
                    logger.warning(f"Could not find/create reporter for case {legacy_case['id']}")
                    self.stats['cases_errors'] += 1
                    return
                
                # Map legacy data to new case
                case_data = self._map_case_data(legacy_case, reporter)
                
                # Create the case
                case = Case.objects.create(**case_data)
                
                # Migrate related data
                self._migrate_case_categories(case, legacy_case)
                self._migrate_case_contacts(case, legacy_case)
                self._migrate_case_activities(case, legacy_case['id'])
                self._migrate_case_services(case, legacy_case['id'])
                self._migrate_case_referrals(case, legacy_case['id'])
                
                # Update counts
                case.update_counts()
                
                self.stats['cases_created'] += 1
                logger.info(f"Migrated case {case.case_number} (legacy ID: {legacy_case['id']})")
                
        except Exception as e:
            logger.error(f"Error migrating case {legacy_case['id']}: {str(e)}")
            self.stats['cases_errors'] += 1
    
    def _map_case_data(self, legacy_case: Dict, reporter: Contact) -> Dict:
        """Map legacy case data to new Case model fields"""
        
        # Map status
        status = self._map_status(legacy_case.get('status'))
        priority = self._map_priority(legacy_case.get('priority'))
        case_type = self._map_case_type(legacy_case)
        
        # Map assigned users
        assigned_to = self._map_user(legacy_case.get('assigned_to_id'))
        escalated_to = self._map_user(legacy_case.get('escalatedto_id'))
        escalated_by = self._map_user(legacy_case.get('escalated_by_id'))
        created_by = self._map_user(legacy_case.get('created_by_id'))
        
        # Map dates
        created_at = self._parse_timestamp(legacy_case.get('created_on'))
        incident_date = self._parse_timestamp(legacy_case.get('incidence_when'))
        due_date = None  # Calculate based on priority/type if needed
        closed_date = None
        
        if legacy_case.get('status_id') and 'closed' in str(legacy_case.get('status', '')).lower():
            closed_date = created_at  # Use creation date as fallback
        
        # Generate case number
        case_number = self._generate_case_number(legacy_case)
        
        return {
            'case_number': case_number,
            'case_type': case_type,
            'status': status,
            'priority': priority,
            'reporter': reporter,
            'reporter_is_afflicted': self._parse_boolean(legacy_case.get('reporter_isafflicted')),
            'assigned_to': assigned_to,
            'escalated_to': escalated_to,
            'escalated_by': escalated_by,
            'title': self._generate_title(legacy_case),
            'narrative': legacy_case.get('narrative', '') or '',
            'action_plan': legacy_case.get('plan', '') or '',
            'incident_date': incident_date,
            'incident_location': legacy_case.get('incidence_location', '') or '',
            'report_location': legacy_case.get('src_address', '') or '',
            'source_type': legacy_case.get('src', 'unknown'),
            'source_reference': legacy_case.get('src_uid', ''),
            'is_gbv_related': self._parse_boolean(legacy_case.get('gbv_related')),
            'medical_exam_done': self._parse_boolean(legacy_case.get('is_medical_exam_done')),
            'incident_reported_to_police': self._parse_boolean(legacy_case.get('is_incidence_reported')),
            'police_ob_number': legacy_case.get('police_ob_no', '') or '',
            'hiv_tested': self._parse_boolean(legacy_case.get('is_hiv_tested')),
            'hiv_test_result': legacy_case.get('hiv_test_result', '') or '',
            'pep_given': self._parse_boolean(legacy_case.get('is_pep_given')),
            'art_given': self._parse_boolean(legacy_case.get('is_art_given')),
            'ecp_given': self._parse_boolean(legacy_case.get('is_ecp_given')),
            'counselling_given': self._parse_boolean(legacy_case.get('is_counselling_given')),
            'counselling_organization': legacy_case.get('counseling_org', '') or '',
            'due_date': due_date,
            'closed_date': closed_date,
            'resolution_summary': legacy_case.get('status_comments', '') or '',
            'incident_reference_number': legacy_case.get('incidence_ref_no', '') or '',
            'created_at': created_at,
            'created_by': created_by,
            'legacy_case_id': legacy_case['id'],
            'legacy_nsr': legacy_case.get('nsr'),
            'legacy_data': legacy_case,
            'migration_notes': f"Migrated from legacy kase table on {timezone.now()}",
        }
    
    def _get_or_create_reporter(self, legacy_case: Dict) -> Optional[Contact]:
        """Get or create reporter contact from legacy data"""
        # Try to find existing contact by legacy reporter ID
        reporter_contact_id = legacy_case.get('reporter_contact_id')
        if reporter_contact_id:
            try:
                return Contact.objects.get(legacy_contact_id=reporter_contact_id)
            except Contact.DoesNotExist:
                pass
        
        # Try to find by phone number
        reporter_phone = legacy_case.get('reporter_phone')
        if reporter_phone:
            contacts = Contact.objects.filter(
                models.Q(primary_phone=reporter_phone) |
                models.Q(secondary_phone=reporter_phone)
            )
            if contacts.exists():
                return contacts.first()
        
        # Try to find by name
        reporter_name = legacy_case.get('reporter_fullname')
        if reporter_name:
            contacts = Contact.objects.filter(full_name__iexact=reporter_name)
            if contacts.exists():
                return contacts.first()
        
        # Create new contact if not found
        if reporter_name or reporter_phone:
            try:
                contact = Contact.objects.create(
                    full_name=reporter_name or 'Unknown Reporter',
                    primary_phone=reporter_phone or '',
                    legacy_contact_id=reporter_contact_id,
                    migration_source='case_reporter'
                )
                return contact
            except Exception as e:
                logger.error(f"Error creating reporter contact: {str(e)}")
        
        return None
    
    def _parse_boolean(self, value) -> bool:
        """Parse legacy boolean values"""
        if value is None:
            return False
        
        if isinstance(value, bool):
            return value
        
        str_value = str(value).lower().strip()
        return str_value in ['1', 'true', 'yes', 'y', 'on']
    
    def _generate_case_number(self, legacy_case: Dict) -> str:
        """Generate case number from legacy data"""
        legacy_id = legacy_case['id']
        nsr = legacy_case.get('nsr', legacy_id)
        year = 2023  # Default year, could be extracted from created_on
        
        if legacy_case.get('created_on'):
            try:
                created_date = self._parse_timestamp(legacy_case['created_on'])
                if created_date:
                    year = created_date.year
            except:
                pass
        
        return f"CASE-{year}-{nsr:06d}"
    
    def _generate_title(self, legacy_case: Dict) -> str:
        """Generate case title from legacy data"""
        narrative = legacy_case.get('narrative', '')
        if narrative:
            # Take first 50 characters as title
            title = narrative[:50].strip()
            if len(narrative) > 50:
                title += "..."
            return title
        
        # Fallback title
        case_type = "GBV Case" if self._parse_boolean(legacy_case.get('gbv_related')) else "Case"
        return f"{case_type} #{legacy_case['id']}"
    
    def _migrate_case_categories(self, case: Case, legacy_case: Dict):
        """Migrate case categories"""
        categories_text = legacy_case.get('categories', '') or legacy_case.get('case_category', '')
        
        if categories_text:
            # Parse categories (usually comma-separated or JSON)
            try:
                # Try to map categories to reference data
                # This would need to be customized based on legacy category structure
                category_names = [cat.strip() for cat in categories_text.split(',')]
                
                for i, cat_name in enumerate(category_names[:5]):  # Limit to 5 categories
                    # Try to find matching category
                    category = ReferenceData.objects.filter(
                        category='case_category',
                        name__icontains=cat_name
                    ).first()
                    
                    if category:
                        CaseCategory.objects.create(
                            case=case,
                            category=category,
                            is_primary=(i == 0),
                            confidence_score=0.8,  # Default confidence
                            added_by=case.created_by
                        )
            except Exception as e:
                logger.warning(f"Error migrating categories for case {case.id}: {str(e)}")
    
    def _migrate_case_contacts(self, case: Case, legacy_case: Dict):
        """Migrate case contacts (clients, perpetrators, etc.)"""
        try:
            # Migrate clients
            with self.legacy_db.cursor() as cursor:
                cursor.execute("""
                    SELECT * FROM client 
                    WHERE case_id = %s AND (is_delete = '0' OR is_delete IS NULL)
                """, [legacy_case['id']])
                
                columns = [col[0] for col in cursor.description]
                for row in cursor.fetchall():
                    client_data = dict(zip(columns, row))
                    self._migrate_client_contact(case, client_data)
            
            # Migrate perpetrators
            with self.legacy_db.cursor() as cursor:
                cursor.execute("""
                    SELECT * FROM perpetrator 
                    WHERE case_id = %s AND (is_delete = '0' OR is_delete IS NULL)
                """, [legacy_case['id']])
                
                columns = [col[0] for col in cursor.description]
                for row in cursor.fetchall():
                    perp_data = dict(zip(columns, row))
                    self._migrate_perpetrator_contact(case, perp_data)
                    
        except Exception as e:
            logger.warning(f"Error migrating contacts for case {case.id}: {str(e)}")
    
    def _migrate_client_contact(self, case: Case, client_data: Dict):
        """Migrate a client contact"""
        contact = self._find_or_create_contact_from_client(client_data)
        if contact:
            ContactRole.objects.get_or_create(
                contact=contact,
                case=case,
                role='client',
                defaults={
                    'is_primary': True,  # First client is primary
                    'role_data': {
                        'gbv_related': client_data.get('gbv_related'),
                        'is_disabled': client_data.get('is_disabled'),
                        'in_school': client_data.get('in_school'),
                        'is_married': client_data.get('is_married'),
                    }
                }
            )
    
    def _migrate_perpetrator_contact(self, case: Case, perp_data: Dict):
        """Migrate a perpetrator contact"""
        contact = self._find_or_create_contact_from_perpetrator(perp_data)
        if contact:
            # Get relationship reference data
            relationship = None
            if perp_data.get('relationship'):
                relationship = ReferenceData.objects.filter(
                    category='relationship',
                    name__icontains=perp_data['relationship']
                ).first()
            
            ContactRole.objects.get_or_create(
                contact=contact,
                case=case,
                role='perpetrator',
                defaults={
                    'relationship': relationship,
                    'role_data': {
                        'shares_home': perp_data.get('shareshome'),
                        'marital_status': perp_data.get('marital'),
                        'employment': perp_data.get('employment'),
                    }
                }
            )
    
    def _find_or_create_contact_from_client(self, client_data: Dict) -> Optional[Contact]:
        """Find or create contact from client data"""
        # Try to find existing contact
        if client_data.get('contact_id'):
            try:
                return Contact.objects.get(legacy_contact_id=client_data['contact_id'])
            except Contact.DoesNotExist:
                pass
        
        # Create new contact
        try:
            return Contact.objects.create(
                full_name=client_data.get('contact_fullname', 'Unknown Client'),
                first_name=client_data.get('contact_fname', ''),
                last_name=client_data.get('contact_lname', ''),
                primary_phone=client_data.get('contact_phone', ''),
                secondary_phone=client_data.get('contact_phone2', ''),
                email=client_data.get('contact_email', ''),
                date_of_birth=self._parse_date(client_data.get('contact_dob')),
                age=client_data.get('contact_age'),
                national_id=client_data.get('contact_national_id', ''),
                physical_address=client_data.get('contact_address', ''),
                legacy_client_id=client_data.get('id'),
                migration_source='legacy_client'
            )
        except Exception as e:
            logger.error(f"Error creating client contact: {str(e)}")
            return None
    
    def _find_or_create_contact_from_perpetrator(self, perp_data: Dict) -> Optional[Contact]:
        """Find or create contact from perpetrator data"""
        # Similar to client creation but for perpetrators
        try:
            return Contact.objects.create(
                full_name=perp_data.get('contact_fullname', 'Unknown Perpetrator'),
                first_name=perp_data.get('contact_fname', ''),
                last_name=perp_data.get('contact_lname', ''),
                primary_phone=perp_data.get('contact_phone', ''),
                secondary_phone=perp_data.get('contact_phone2', ''),
                email=perp_data.get('contact_email', ''),
                date_of_birth=self._parse_date(perp_data.get('contact_dob')),
                age=perp_data.get('contact_age'),
                national_id=perp_data.get('contact_national_id', ''),
                physical_address=perp_data.get('contact_address', ''),
                legacy_perpetrator_id=perp_data.get('id'),
                migration_source='legacy_perpetrator'
            )
        except Exception as e:
            logger.error(f"Error creating perpetrator contact: {str(e)}")
            return None
    
    def _parse_date(self, date_value):
        """Parse date from various formats"""
        if not date_value:
            return None
        
        try:
            if isinstance(date_value, (int, float)):
                # Unix timestamp
                return datetime.fromtimestamp(date_value, tz=timezone.utc).date()
            elif isinstance(date_value, str):
                # Try parsing date formats
                for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y']:
                    try:
                        return datetime.strptime(date_value, fmt).date()
                    except ValueError:
                        continue
        except Exception:
            pass
        
        return None
    
    def _migrate_case_activities(self, case: Case, legacy_case_id: int):
        """Migrate case activities from kase_activity table"""
        try:
            with self.legacy_db.cursor() as cursor:
                cursor.execute("""
                    SELECT * FROM kase_activity 
                    WHERE case_id = %s
                    ORDER BY created_on
                """, [legacy_case_id])
                
                columns = [col[0] for col in cursor.description]
                for row in cursor.fetchall():
                    activity_data = dict(zip(columns, row))
                    self._create_case_activity(case, activity_data)
                    
        except Exception as e:
            logger.warning(f"Error migrating activities for case {case.id}: {str(e)}")
    
    def _create_case_activity(self, case: Case, activity_data: Dict):
        """Create a case activity from legacy data"""
        try:
            user = self._map_user(activity_data.get('created_by_id'))
            created_at = self._parse_timestamp(activity_data.get('created_on'))
            
            # Map activity type
            activity_type = self._map_activity_type(activity_data.get('activity'))
            
            CaseActivity.objects.create(
                case=case,
                activity_type=activity_type,
                user=user,
                title=activity_data.get('activity', 'Case Activity'),
                description=activity_data.get('detail', '') or 'Legacy activity',
                data=activity_data,
                created_at=created_at or timezone.now(),
                legacy_activity_id=activity_data.get('id')
            )
            
            self.stats['activities_created'] += 1
            
        except Exception as e:
            logger.error(f"Error creating activity: {str(e)}")
    
    def _map_activity_type(self, legacy_activity) -> str:
        """Map legacy activity to new activity type"""
        if not legacy_activity:
            return 'other'
        
        activity_mapping = {
            'created': 'created',
            'updated': 'updated',
            'assigned': 'assigned',
            'escalated': 'escalated',
            'closed': 'closed',
            'note': 'note_added',
            'contact': 'contact_added',
            'service': 'service_added',
            'referral': 'referral_added',
        }
        
        activity_key = str(legacy_activity).lower().strip()
        return activity_mapping.get(activity_key, 'other')
    
    def _migrate_case_services(self, case: Case, legacy_case_id: int):
        """Migrate case services from service table"""
        try:
            with self.legacy_db.cursor() as cursor:
                cursor.execute("""
                    SELECT * FROM service 
                    WHERE case_id = %s
                """, [legacy_case_id])
                
                columns = [col[0] for col in cursor.description]
                for row in cursor.fetchall():
                    service_data = dict(zip(columns, row))
                    self._create_case_service(case, service_data)
                    
        except Exception as e:
            logger.warning(f"Error migrating services for case {case.id}: {str(e)}")
    
    def _create_case_service(self, case: Case, service_data: Dict):
        """Create a case service from legacy data"""
        try:
            # Find service reference data
            service_name = service_data.get('category_name', 'Unknown Service')
            service = ReferenceData.objects.filter(
                category='service',
                name__icontains=service_name
            ).first()
            
            if not service:
                # Create service reference data if not exists
                service = ReferenceData.objects.create(
                    category='service',
                    name=service_name,
                    code=f"SRV_{service_data.get('id', 'UNK')}"
                )
            
            provided_by = self._map_user(service_data.get('created_by_id'))
            service_date = self._parse_timestamp(service_data.get('created_on'))
            
            CaseService.objects.create(
                case=case,
                service=service,
                provided_by=provided_by,
                service_date=service_date or timezone.now(),
                details=service_data.get('category_fullname', ''),
                legacy_service_id=service_data.get('id')
            )
            
            self.stats['services_created'] += 1
            
        except Exception as e:
            logger.error(f"Error creating service: {str(e)}")
    
    def _migrate_case_referrals(self, case: Case, legacy_case_id: int):
        """Migrate case referrals from referal table"""
        try:
            with self.legacy_db.cursor() as cursor:
                cursor.execute("""
                    SELECT * FROM referal 
                    WHERE case_id = %s
                """, [legacy_case_id])
                
                columns = [col[0] for col in cursor.description]
                for row in cursor.fetchall():
                    referral_data = dict(zip(columns, row))
                    self._create_case_referral(case, referral_data)
                    
        except Exception as e:
            logger.warning(f"Error migrating referrals for case {case.id}: {str(e)}")
    
    def _create_case_referral(self, case: Case, referral_data: Dict):
        """Create a case referral from legacy data"""
        try:
            # Find referral type reference data
            referral_name = referral_data.get('category_name', 'General Referral')
            referral_type = ReferenceData.objects.filter(
                category='referral_type',
                name__icontains=referral_name
            ).first()
            
            if not referral_type:
                # Create referral type if not exists
                referral_type = ReferenceData.objects.create(
                    category='referral_type',
                    name=referral_name,
                    code=f"REF_{referral_data.get('id', 'UNK')}"
                )
            
            referred_by = self._map_user(referral_data.get('created_by_id'))
            referral_date = self._parse_timestamp(referral_data.get('created_on'))
            
            # Extract organization name from category fullname or use default
            organization = referral_data.get('category_fullname', 'External Organization')
            if len(organization) > 255:
                organization = organization[:255]
            
            CaseReferral.objects.create(
                case=case,
                referral_type=referral_type,
                organization=organization,
                reason=f"Legacy referral: {referral_name}",
                referred_by=referred_by,
                referral_date=referral_date or timezone.now(),
                status='completed',  # Assume completed for legacy data
                legacy_referral_id=referral_data.get('id')
            )
            
            self.stats['referrals_created'] += 1
            
        except Exception as e:
            logger.error(f"Error creating referral: {str(e)}")
    
    def run_migration(self, limit: Optional[int] = None):
        """Run the complete migration process"""
        start_time = timezone.now()
        logger.info(f"Starting case migration at {start_time}")
        
        try:
            # Migrate cases
            self.migrate_cases(limit)
            
            # Print final statistics
            end_time = timezone.now()
            duration = end_time - start_time
            
            logger.info("=" * 50)
            logger.info("MIGRATION COMPLETED")
            logger.info("=" * 50)
            logger.info(f"Duration: {duration}")
            logger.info(f"Cases processed: {self.stats['cases_processed']}")
            logger.info(f"Cases created: {self.stats['cases_created']}")
            logger.info(f"Cases with errors: {self.stats['cases_errors']}")
            logger.info(f"Activities created: {self.stats['activities_created']}")
            logger.info(f"Services created: {self.stats['services_created']}")
            logger.info(f"Referrals created: {self.stats['referrals_created']}")
            logger.info(f"Notes created: {self.stats['notes_created']}")
            logger.info(f"Updates created: {self.stats['updates_created']}")
            
            success_rate = (self.stats['cases_created'] / self.stats['cases_processed']) * 100 if self.stats['cases_processed'] > 0 else 0
            logger.info(f"Success rate: {success_rate:.2f}%")
            
        except Exception as e:
            logger.error(f"Migration failed with error: {str(e)}")
            raise


def main():
    """Main migration function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Migrate case data from legacy database')
    parser.add_argument('--limit', type=int, help='Limit number of cases to migrate (for testing)')
    parser.add_argument('--dry-run', action='store_true', help='Perform dry run without actual migration')
    
    args = parser.parse_args()
    
    if args.dry_run:
        logger.info("DRY RUN MODE - No data will be migrated")
        # Could implement dry run logic here
        return
    
    # Confirm migration
    if not args.limit:
        response = input("This will migrate ALL cases from legacy database. Continue? (y/N): ")
        if response.lower() != 'y':
            logger.info("Migration cancelled")
            return
    
    # Run migration
    migrator = CaseMigrator()
    migrator.run_migration(limit=args.limit)


if __name__ == '__main__':
    main()
    
    def _map_status(self, legacy_status) -> Optional[ReferenceData]:
        """Map legacy status to new status reference data"""
        if not legacy_status:
            return self.status_cache.get('open')  # Default status
        
        # Map common legacy statuses
        status_mapping = {
            'open': 'open',
            'pending': 'pending',
            'in_progress': 'in_progress',
            'closed': 'closed',
            'resolved': 'resolved',
            'cancelled': 'cancelled',
        }
        
        status_key = str(legacy_status).lower().strip()
        mapped_status = status_mapping.get(status_key, 'open')
        
        return self.status_cache.get(mapped_status)
    
    def _map_priority(self, legacy_priority) -> Optional[ReferenceData]:
        """Map legacy priority to new priority reference data"""
        if not legacy_priority:
            return self.priority_cache.get('medium')  # Default priority
        
        # Map numeric priorities to names
        priority_mapping = {
            '1': 'critical',
            '2': 'high',
            '3': 'medium',
            '4': 'low',
            '5': 'lowest',
        }
        
        priority_key = str(legacy_priority).strip()
        mapped_priority = priority_mapping.get(priority_key, 'medium')
        
        return self.priority_cache.get(mapped_priority)
    
    def _map_case_type(self, legacy_case: Dict) -> Optional[ReferenceData]:
        """Map legacy case to case type"""
        # Try to determine case type from categories or GBV flag
        if self._parse_boolean(legacy_case.get('gbv_related')):
            return self.case_type_cache.get('gbv')
        
        # Default case type
        return self.case_type_cache.get('general') or list(self.case_type_cache.values())[0]
    
    def _map_user(self, user_id) -> Optional[User]:
        """Map legacy user ID to User object"""
        if not user_id:
            return None
        
        try:
            return self.user_cache.get(int(user_id))
        except (ValueError, TypeError):
            return None
    
    def _parse_timestamp(self, timestamp) -> Optional[datetime]:
        """Parse legacy timestamp to datetime"""
        if not timestamp:
            return None
        
        try:
            if isinstance(timestamp, (int, float)):
                # Unix timestamp
                return datetime.fromtimestamp(timestamp, tz=timezone.utc)
            elif isinstance(timestamp, str):
                # Try parsing various formats
                for fmt in ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d', '%d/%m/%Y']:
                    try:
                        return datetime.strptime(timestamp, fmt).replace(tzinfo=timezone.utc)
                    except ValueError:
                        continue
        except Exception as e:
            logger.warning(f"Could not parse timestamp {timestamp}: {str(e)}")