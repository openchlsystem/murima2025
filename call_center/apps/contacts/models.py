# apps/contacts/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils import timezone
from apps.core.models import TimeStampedModel, SoftDeleteModel
import uuid
import re


class ContactManager(models.Manager):
    """Custom manager for Contact model with common queries"""
    
    def by_phone(self, phone_number):
        """Find contacts by phone number (primary or secondary)"""
        cleaned_phone = self._clean_phone(phone_number)
        if not cleaned_phone:
            return self.none()
        
        return self.filter(
            models.Q(primary_phone=cleaned_phone) |
            models.Q(secondary_phone=cleaned_phone)
        )
    
    def search(self, query):
        """Search contacts by name, phone, or email"""
        return self.filter(
            models.Q(full_name__icontains=query) |
            models.Q(first_name__icontains=query) |
            models.Q(last_name__icontains=query) |
            models.Q(primary_phone__icontains=query) |
            models.Q(secondary_phone__icontains=query) |
            models.Q(email__icontains=query)
        )
    
    def by_location(self, location):
        """Get contacts by location (any level)"""
        return self.filter(
            models.Q(region=location) |
            models.Q(district=location) |
            models.Q(subcounty=location) |
            models.Q(parish=location) |
            models.Q(village=location)
        )
    
    def reporters(self):
        """Get contacts who have been reporters"""
        return self.filter(roles__role='reporter').distinct()
    
    def clients(self):
        """Get contacts who have been clients"""
        return self.filter(roles__role='client').distinct()
    
    def perpetrators(self):
        """Get contacts who have been perpetrators"""
        return self.filter(roles__role='perpetrator').distinct()
    
    def _clean_phone(self, phone):
        """Clean phone number for searching"""
        if not phone:
            return None
        # Remove all non-digit characters
        cleaned = re.sub(r'\D', '', str(phone))
        return cleaned if len(cleaned) >= 7 else None


class Contact(SoftDeleteModel):
    """
    Unified contact model that handles all contact types.
    Maps to legacy contact, reporter, client, and perpetrator tables.
    """
    
    CONTACT_TYPES = [
        ('person', _('Person')),
        ('organization', _('Organization')),
        ('anonymous', _('Anonymous')),
    ]
    
    ID_TYPES = [
        ('national_id', _('National ID')),
        ('passport', _('Passport')),
        ('drivers_license', _('Driver\'s License')),
        ('birth_certificate', _('Birth Certificate')),
        ('refugee_id', _('Refugee ID')),
        ('other', _('Other')),
    ]
    
    # Core Identity
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, db_index=True)
    contact_type = models.CharField(
        max_length=20,
        choices=CONTACT_TYPES,
        default='person',
        verbose_name=_("Contact Type")
    )
    
    # Personal Information
    full_name = models.CharField(
        max_length=255,
        db_index=True,
        blank=True,  # Allow blank in forms
        default='',  # Provide default value
        verbose_name=_("Full Name"),
        help_text=_("Complete name of the contact")
    )
    first_name = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("First Name")
    )
    last_name = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Last Name")
    )
    
    # Contact Details
    primary_phone = models.CharField(
        max_length=20,
        db_index=True,
        blank=True,
        verbose_name=_("Primary Phone"),
        help_text=_("Main phone number")
    )
    secondary_phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name=_("Secondary Phone"),
        help_text=_("Alternative phone number")
    )
    email = models.EmailField(
        blank=True,
        verbose_name=_("Email Address")
    )
    
    # Demographics
    date_of_birth = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Date of Birth")
    )
    age = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name=_("Age"),
        help_text=_("Age in years")
    )
    age_group = models.ForeignKey(
        'core.ReferenceData',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'category': 'age_group'},
        related_name='contacts_by_age_group',
        verbose_name=_("Age Group")
    )
    gender = models.ForeignKey(
        'core.ReferenceData',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'category': 'gender'},
        related_name='contacts_by_gender',
        verbose_name=_("Gender")
    )
    
    # Location Hierarchy (Uganda administrative structure)
    country = models.ForeignKey(
        'core.Country',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Country")
    )
    region = models.ForeignKey(
        'core.Location',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'location_type': 'region'},
        related_name='contacts_by_region',
        verbose_name=_("Region")
    )
    district = models.ForeignKey(
        'core.Location',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'location_type': 'district'},
        related_name='contacts_by_district',
        verbose_name=_("District")
    )
    county = models.ForeignKey(
        'core.Location',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'location_type': 'county'},
        related_name='contacts_by_county',
        verbose_name=_("County")
    )
    subcounty = models.ForeignKey(
        'core.Location',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'location_type': 'subcounty'},
        related_name='contacts_by_subcounty',
        verbose_name=_("Subcounty")
    )
    parish = models.ForeignKey(
        'core.Location',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'location_type': 'parish'},
        related_name='contacts_by_parish',
        verbose_name=_("Parish")
    )
    village = models.ForeignKey(
        'core.Location',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'location_type': 'village'},
        related_name='contacts_by_village',
        verbose_name=_("Village")
    )
    
    # Address Information
    physical_address = models.TextField(
        blank=True,
        verbose_name=_("Physical Address"),
        help_text=_("Detailed address information")
    )
    residence = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Residence"),
        help_text=_("Current place of residence")
    )
    landmark = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Landmark"),
        help_text=_("Nearby landmark for location")
    )
    
    # Identity Documents
    national_id = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("National ID Number")
    )
    national_id_type = models.CharField(
        max_length=20,
        choices=ID_TYPES,
        blank=True,
        verbose_name=_("ID Type")
    )
    
    # Cultural Information
    nationality = models.ForeignKey(
        'core.ReferenceData',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'category': 'nationality'},
        related_name='contacts_by_nationality',
        verbose_name=_("Nationality")
    )
    tribe = models.ForeignKey(
        'core.ReferenceData',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'category': 'tribe'},
        related_name='contacts_by_tribe',
        verbose_name=_("Tribe")
    )
    language = models.ForeignKey(
        'core.Language',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Primary Language")
    )
    
    # Additional Information (JSON for flexibility)
    additional_info = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("Additional Information"),
        help_text=_("Additional contact details stored as JSON")
    )
    
    # Migration Helper Fields (to be removed post-migration)
    legacy_contact_id = models.IntegerField(
        null=True,
        blank=True,
        db_index=True,
        verbose_name=_("Legacy Contact ID"),
        help_text=_("Original contact table ID")
    )
    legacy_client_id = models.IntegerField(
        null=True,
        blank=True,
        db_index=True,
        verbose_name=_("Legacy Client ID"),
        help_text=_("Original client table ID")
    )
    legacy_reporter_id = models.IntegerField(
        null=True,
        blank=True,
        db_index=True,
        verbose_name=_("Legacy Reporter ID"),
        help_text=_("Original reporter table ID")
    )
    legacy_perpetrator_id = models.IntegerField(
        null=True,
        blank=True,
        db_index=True,
        verbose_name=_("Legacy Perpetrator ID"),
        help_text=_("Original perpetrator table ID")
    )
    migration_notes = models.TextField(
        blank=True,
        verbose_name=_("Migration Notes"),
        help_text=_("Notes about migration process or deduplication")
    )
    migration_source = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_("Migration Source"),
        help_text=_("Which legacy table this record came from")
    )
    
    # Manager
    objects = ContactManager()
    
    class Meta:
        verbose_name = _("Contact")
        verbose_name_plural = _("Contacts")
        ordering = ['full_name']
        indexes = [
            # Primary lookup indexes
            models.Index(fields=['full_name']),
            models.Index(fields=['primary_phone']),
            models.Index(fields=['secondary_phone']),
            models.Index(fields=['email']),
            models.Index(fields=['national_id']),
            
            # Name-based searches
            models.Index(fields=['first_name', 'last_name']),
            models.Index(fields=['full_name', 'primary_phone']),
            
            # Location-based searches
            models.Index(fields=['district', 'subcounty']),
            models.Index(fields=['region', 'district']),
            
            # Migration indexes (to be removed)
            models.Index(fields=['legacy_contact_id']),
            models.Index(fields=['legacy_client_id']),
            models.Index(fields=['legacy_reporter_id']),
            models.Index(fields=['legacy_perpetrator_id']),
            models.Index(fields=['migration_source']),
            
            # Composite indexes for common queries
            models.Index(fields=['is_active', 'full_name']),
            models.Index(fields=['contact_type', 'is_active']),
        ]
        constraints = [
            # Ensure at least one contact method is provided
            models.CheckConstraint(
                check=(
                    models.Q(primary_phone__isnull=False, primary_phone__gt='') |
                    models.Q(email__isnull=False, email__gt='') |
                    models.Q(physical_address__isnull=False, physical_address__gt='')
                ),
                name='contact_has_contact_method'
            ),
        ]
    
    def __str__(self):
        if self.full_name and self.full_name.strip():
            return self.full_name
        elif self.first_name or self.last_name:
            return f"{self.first_name or ''} {self.last_name or ''}".strip()
        else:
            return f"Contact {str(self.uuid)[:8]}"
    
    def clean(self):
        """Validate the contact data"""
        super().clean()
        
        # Validate age vs date_of_birth consistency
        if self.date_of_birth and self.age:
            calculated_age = timezone.now().date().year - self.date_of_birth.year
            if abs(calculated_age - self.age) > 1:  # Allow 1 year difference
                raise ValidationError(_("Age doesn't match date of birth"))
        
        # Clean phone numbers
        if self.primary_phone:
            self.primary_phone = self._clean_phone_number(self.primary_phone)
        if self.secondary_phone:
            self.secondary_phone = self._clean_phone_number(self.secondary_phone)
    
    def save(self, *args, **kwargs):
        """Override save to handle automatic fields"""
        # Auto-calculate age from date of birth if not provided
        if self.date_of_birth and not self.age:
            self.age = timezone.now().date().year - self.date_of_birth.year
        
        # Auto-generate full name if not provided
        if not self.full_name and (self.first_name or self.last_name):
            self.full_name = f"{self.first_name} {self.last_name}".strip()
        
        # Split full name into parts if first/last names not provided
        if self.full_name and not (self.first_name or self.last_name):
            name_parts = self.full_name.strip().split()
            if len(name_parts) >= 2:
                self.first_name = name_parts[0]
                self.last_name = ' '.join(name_parts[1:])
            elif len(name_parts) == 1:
                self.first_name = name_parts[0]
        
        super().save(*args, **kwargs)
    
    def _clean_phone_number(self, phone):
        """Clean and format phone number"""
        if not phone:
            return phone
        
        # Remove all non-digit characters except +
        cleaned = re.sub(r'[^\d+]', '', str(phone))
        
        # Handle Uganda phone numbers
        if cleaned.startswith('0'):
            cleaned = '+256' + cleaned[1:]
        elif cleaned.startswith('256'):
            cleaned = '+' + cleaned
        elif not cleaned.startswith('+'):
            # Assume Uganda number if no country code
            if len(cleaned) == 9:
                cleaned = '+256' + cleaned
        
        return cleaned
    
    @property
    def age_calculated(self):
        """Calculate age from date of birth"""
        if self.date_of_birth:
            today = timezone.now().date()
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return self.age
    
    @property
    def full_location(self):
        """Get full location path"""
        locations = []
        for location in [self.village, self.parish, self.subcounty, self.county, self.district, self.region]:
            if location:
                locations.append(location.name)
        return ' > '.join(locations) if locations else ''
    
    @property
    def display_phone(self):
        """Get primary phone for display"""
        return self.primary_phone or self.secondary_phone or ''
    
    @property
    def has_complete_profile(self):
        """Check if contact has reasonably complete information"""
        required_fields = [self.full_name, self.primary_phone]
        optional_fields = [self.email, self.physical_address, self.district]
        
        has_required = all(field for field in required_fields)
        has_optional = sum(1 for field in optional_fields if field) >= 2
        
        return has_required and has_optional
    
    def get_roles_in_cases(self):
        """Get all roles this contact has played in cases"""
        # Commented until cases app is ready
        # return self.roles.values_list('role', flat=True).distinct()
    
    def get_recent_cases(self, limit=5):
        """Get recent cases involving this contact"""
        # Commented until cases app is ready
        # return self.roles.select_related('case').order_by('-case__created_at')[:limit]
    
    def get_call_history(self, limit=10):
        """Get recent call history for this contact"""
        return self.calls.order_by('-start_time')[:limit]
    
    def find_potential_duplicates(self):
        """Find potential duplicate contacts based on phone and name"""
        duplicates = Contact.objects.exclude(id=self.id).filter(
            models.Q(primary_phone=self.primary_phone) |
            models.Q(secondary_phone=self.primary_phone) |
            models.Q(primary_phone=self.secondary_phone) |
            (models.Q(full_name__iexact=self.full_name) & models.Q(full_name__isnull=False))
        )
        return duplicates.filter(is_active=True)


class ContactRole(TimeStampedModel):
    """
    Track different roles a contact plays in various cases.
    This replaces the separate reporter, client, perpetrator tables.
    """
    
    CONTACT_ROLES = [
        ('reporter', _('Reporter')),
        ('client', _('Client/Victim')),
        ('perpetrator', _('Perpetrator')),
        ('witness', _('Witness')),
        ('guardian', _('Guardian')),
        ('relative', _('Relative')),
        ('other', _('Other')),
    ]
    
    contact = models.ForeignKey(
        Contact,
        on_delete=models.CASCADE,
        related_name='roles',
        verbose_name=_("Contact")
    )
    # case = models.ForeignKey(
    #     'cases.Case',
    #     on_delete=models.CASCADE,
    #     related_name='contact_roles',
    #     verbose_name=_("Case")
    # )
    role = models.CharField(
        max_length=20,
        choices=CONTACT_ROLES,
        verbose_name=_("Role")
    )
    is_primary = models.BooleanField(
        default=False,
        verbose_name=_("Is Primary"),
        help_text=_("Whether this is the primary contact for this role in the case")
    )
    
    # Role-specific information stored as JSON for flexibility
    role_data = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("Role Data"),
        help_text=_("Additional role-specific information")
    )
    
    # Relationship to victim (for perpetrators and others)
    relationship = models.ForeignKey(
        'core.ReferenceData',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'category': 'relationship'},
        verbose_name=_("Relationship"),
        help_text=_("Relationship to the victim/client")
    )
    
    # Migration tracking
    legacy_role_id = models.IntegerField(
        null=True,
        blank=True,
        verbose_name=_("Legacy Role ID"),
        help_text=_("ID from original role-specific table")
    )
    
    class Meta:
        verbose_name = _("Contact Role")
        verbose_name_plural = _("Contact Roles")
        # unique_together = ['contact', 'case', 'role']
        indexes = [
            models.Index(fields=['contact', 'role']),
            # models.Index(fields=['case', 'role']),
            models.Index(fields=['role', 'is_primary']),
            models.Index(fields=['legacy_role_id']),
        ]
    
    def __str__(self):
        # return f"{self.contact.full_name} as {self.get_role_display()} in Case {self.case.case_number}"
        return f"{self.contact.full_name} as {self.get_role_display()}"  # Simplified until cases app ready



class ContactAddress(TimeStampedModel):
    """
    Multiple addresses for a contact (home, work, etc.)
    """
    
    ADDRESS_TYPES = [
        ('home', _('Home')),
        ('work', _('Work')),
        ('mailing', _('Mailing')),
        ('emergency', _('Emergency')),
        ('other', _('Other')),
    ]
    
    contact = models.ForeignKey(
        Contact,
        on_delete=models.CASCADE,
        related_name='addresses',
        verbose_name=_("Contact")
    )
    address_type = models.CharField(
        max_length=20,
        choices=ADDRESS_TYPES,
        default='home',
        verbose_name=_("Address Type")
    )
    address_line_1 = models.CharField(
        max_length=255,
        verbose_name=_("Address Line 1")
    )
    address_line_2 = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Address Line 2")
    )
    
    # Location fields (can be different from contact's main location)
    district = models.ForeignKey(
        'core.Location',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'location_type': 'district'},
        related_name='addresses_by_district',
        verbose_name=_("District")
    )
    subcounty = models.ForeignKey(
        'core.Location',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'location_type': 'subcounty'},
        related_name='addresses_by_subcounty',
        verbose_name=_("Subcounty")
    )
    
    landmark = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Landmark")
    )
    postal_code = models.CharField(
        max_length=20,
        blank=True,
        verbose_name=_("Postal Code")
    )
    is_primary = models.BooleanField(
        default=False,
        verbose_name=_("Is Primary Address")
    )
    
    class Meta:
        verbose_name = _("Contact Address")
        verbose_name_plural = _("Contact Addresses")
        ordering = ['-is_primary', 'address_type']
        indexes = [
            models.Index(fields=['contact', 'address_type']),
            models.Index(fields=['contact', 'is_primary']),
        ]
    
    def __str__(self):
        return f"{self.contact.full_name} - {self.get_address_type_display()}"


class ContactPhone(TimeStampedModel):
    """
    Multiple phone numbers for a contact
    """
    
    PHONE_TYPES = [
        ('mobile', _('Mobile')),
        ('home', _('Home')),
        ('work', _('Work')),
        ('emergency', _('Emergency')),
        ('other', _('Other')),
    ]
    
    contact = models.ForeignKey(
        Contact,
        on_delete=models.CASCADE,
        related_name='phone_numbers',
        verbose_name=_("Contact")
    )
    phone_type = models.CharField(
        max_length=20,
        choices=PHONE_TYPES,
        default='mobile',
        verbose_name=_("Phone Type")
    )
    phone_number = models.CharField(
        max_length=20,
        verbose_name=_("Phone Number")
    )
    is_primary = models.BooleanField(
        default=False,
        verbose_name=_("Is Primary Phone")
    )
    is_verified = models.BooleanField(
        default=False,
        verbose_name=_("Is Verified"),
        help_text=_("Whether this phone number has been verified")
    )
    notes = models.TextField(
        blank=True,
        verbose_name=_("Notes"),
        help_text=_("Additional notes about this phone number")
    )
    
    class Meta:
        verbose_name = _("Contact Phone")
        verbose_name_plural = _("Contact Phones")
        unique_together = ['contact', 'phone_number']
        ordering = ['-is_primary', 'phone_type']
        indexes = [
            models.Index(fields=['phone_number']),
            models.Index(fields=['contact', 'is_primary']),
            models.Index(fields=['contact', 'phone_type']),
        ]
    
    def __str__(self):
        return f"{self.contact.full_name} - {self.phone_number}"
    
    def clean(self):
        """Clean and validate phone number"""
        if self.phone_number:
            # Use the same cleaning logic as Contact model
            contact_instance = Contact()
            self.phone_number = contact_instance._clean_phone_number(self.phone_number)


class ContactRelationship(TimeStampedModel):
    """
    Track relationships between contacts (family, professional, etc.)
    """
    
    RELATIONSHIP_TYPES = [
        ('family', _('Family')),
        ('spouse', _('Spouse/Partner')),
        ('parent', _('Parent')),
        ('child', _('Child')),
        ('sibling', _('Sibling')),
        ('guardian', _('Guardian')),
        ('friend', _('Friend')),
        ('colleague', _('Colleague')),
        ('neighbor', _('Neighbor')),
        ('professional', _('Professional')),
        ('other', _('Other')),
    ]
    
    contact_from = models.ForeignKey(
        Contact,
        on_delete=models.CASCADE,
        related_name='relationships_from',
        verbose_name=_("Contact From")
    )
    contact_to = models.ForeignKey(
        Contact,
        on_delete=models.CASCADE,
        related_name='relationships_to',
        verbose_name=_("Contact To")
    )
    relationship_type = models.CharField(
        max_length=20,
        choices=RELATIONSHIP_TYPES,
        verbose_name=_("Relationship Type")
    )
    description = models.TextField(
        blank=True,
        verbose_name=_("Description"),
        help_text=_("Additional description of the relationship")
    )
    is_verified = models.BooleanField(
        default=False,
        verbose_name=_("Is Verified"),
        help_text=_("Whether this relationship has been verified")
    )
    
    class Meta:
        verbose_name = _("Contact Relationship")
        verbose_name_plural = _("Contact Relationships")
        unique_together = ['contact_from', 'contact_to', 'relationship_type']
        indexes = [
            models.Index(fields=['contact_from', 'relationship_type']),
            models.Index(fields=['contact_to', 'relationship_type']),
        ]
    
    def __str__(self):
        return f"{self.contact_from.full_name} -> {self.contact_to.full_name} ({self.get_relationship_type_display()})"
    
    def clean(self):
        """Validate relationship"""
        if self.contact_from == self.contact_to:
            raise ValidationError(_("Contact cannot have relationship with itself"))


class ContactMergeLog(TimeStampedModel):
    """
    Track contact merges for audit purposes
    """
    
    primary_contact = models.ForeignKey(
        Contact,
        on_delete=models.CASCADE,
        related_name='merge_logs_as_primary',
        verbose_name=_("Primary Contact"),
        help_text=_("Contact that was kept after merge")
    )
    merged_contact_id = models.UUIDField(
        verbose_name=_("Merged Contact ID"),
        help_text=_("UUID of contact that was merged and deleted")
    )
    merged_contact_name = models.CharField(
        max_length=255,
        verbose_name=_("Merged Contact Name"),
        help_text=_("Name of contact that was merged")
    )
    merged_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_("Merged By")
    )
    merge_reason = models.TextField(
        verbose_name=_("Merge Reason"),
        help_text=_("Reason for merging the contacts")
    )
    merged_data = models.JSONField(
        verbose_name=_("Merged Data"),
        help_text=_("Data from the merged contact for audit purposes")
    )
    
    class Meta:
        verbose_name = _("Contact Merge Log")
        verbose_name_plural = _("Contact Merge Logs")
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['primary_contact', '-created_at']),
            models.Index(fields=['merged_contact_id']),
            models.Index(fields=['merged_by', '-created_at']),
        ]
    
    def __str__(self):
        return f"Merged {self.merged_contact_name} into {self.primary_contact.full_name}"


# Signal handlers for Contact model
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

@receiver(pre_save, sender=Contact)
def contact_pre_save(sender, instance, **kwargs):
    """Handle pre-save logic for contacts"""
    # Ensure full_name is set
    if not instance.full_name and (instance.first_name or instance.last_name):
        instance.full_name = f"{instance.first_name or ''} {instance.last_name or ''}".strip()


@receiver(post_save, sender=ContactPhone)
def contact_phone_post_save(sender, instance, created, **kwargs):
    """Update contact's primary phone when a primary phone is added"""
    if instance.is_primary:
        # Update contact's primary phone
        contact = instance.contact
        if not contact.primary_phone or contact.primary_phone != instance.phone_number:
            contact.primary_phone = instance.phone_number
            contact.save(update_fields=['primary_phone'])
        
        # Ensure no other phone is marked as primary
        ContactPhone.objects.filter(
            contact=contact
        ).exclude(id=instance.id).update(is_primary=False)