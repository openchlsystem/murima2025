# apps/cases/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from apps.core.models import ReferenceData, TimeStampedModel, SoftDeleteModel, UUIDModel
import uuid
from datetime import datetime, timedelta


class CaseManager(models.Manager):
    """Custom manager for Case model with common queries"""
    
    def active(self):
        """Get active cases"""
        return self.filter(status__in=['open', 'in_progress', 'pending'], is_active=True)
    
    def closed(self):
        """Get closed cases"""
        return self.filter(status__in=['closed', 'resolved', 'cancelled'])
    
    def urgent(self):
        """Get urgent priority cases"""
        return self.filter(priority__name__icontains='urgent', is_active=True)
    
    def by_status(self, status):
        """Get cases by status"""
        if hasattr(status, 'name'):
            return self.filter(status=status)
        return self.filter(status__name__icontains=status)
    
    def by_category(self, category):
        """Get cases by category"""
        return self.filter(categories__category=category).distinct()
    
    def by_agent(self, user):
        """Get cases assigned to specific agent"""
        return self.filter(assigned_to=user, is_active=True)
    
    def escalated(self):
        """Get escalated cases"""
        return self.filter(escalated_to__isnull=False, is_active=True)
    
    def overdue(self):
        """Get overdue cases"""
        return self.filter(
            due_date__lt=timezone.now(),
            status__in=['open', 'in_progress', 'pending'],
            is_active=True
        )
    
    def by_date_range(self, start_date, end_date):
        """Get cases within date range"""
        return self.filter(created_at__date__range=[start_date, end_date])
    
    def with_gbv(self):
        """Get GBV-related cases"""
        return self.filter(is_gbv_related=True, is_active=True)
    
    def today(self):
        """Get today's cases"""
        today = timezone.now().date()
        return self.filter(created_at__date=today)


class Case(SoftDeleteModel):
    """
    Main case model for tracking all types of cases.
    Maps to legacy 'kase' table with modern enhancements.
    """
    
    CASE_STATUSES = [
        ('open', _('Open')),
        ('in_progress', _('In Progress')),
        ('pending', _('Pending')),
        ('escalated', _('Escalated')),
        ('resolved', _('Resolved')),
        ('closed', _('Closed')),
        ('cancelled', _('Cancelled')),
        ('on_hold', _('On Hold')),
    ]
    
    PRIORITY_LEVELS = [
        (1, _('Critical')),
        (2, _('High')),
        (3, _('Medium')),
        (4, _('Low')),
        (5, _('Lowest')),
    ]
    
    # Core Case Identification
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, db_index=True)
    case_number = models.CharField(
        max_length=50,
        unique=True,
        db_index=True,
        verbose_name=_("Case Number"),
        help_text=_("Unique case identifier")
    )
    
    # Case Classification
    case_type = models.ForeignKey(
        'core.ReferenceData',
        on_delete=models.PROTECT,
        limit_choices_to={'category': 'case_type'},
        related_name='cases_by_type',
        verbose_name=_("Case Type"),
        help_text=_("Primary case type/category")
    )
    
    # Case Status and Priority
    status = models.ForeignKey(
        'core.ReferenceData',
        on_delete=models.PROTECT,
        limit_choices_to={'category': 'case_status'},
        related_name='cases_by_status',
        verbose_name=_("Status")
    )
    priority = models.ForeignKey(
        'core.ReferenceData',
        on_delete=models.PROTECT,
        limit_choices_to={'category': 'case_priority'},
        related_name='cases_by_priority',
        verbose_name=_("Priority")
    )
    
    # Reporter Information (who reported the case)
    reporter = models.ForeignKey(
        'contacts.Contact',
        on_delete=models.PROTECT,
        related_name='reported_cases',
        verbose_name=_("Reporter"),
        help_text=_("Person who reported this case")
    )
    reporter_is_afflicted = models.BooleanField(
        default=False,
        verbose_name=_("Reporter is Affected"),
        help_text=_("Whether the reporter is also the victim/client")
    )
    knows_about_116 = models.ForeignKey(
        'core.ReferenceData',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'category': 'knowledge_source'},
        related_name='cases_by_knowledge_source',
        verbose_name=_("How did you know about 116?"),
        help_text=_("How the reporter learned about the 116 service")
    )
    
    # Case Assignment
    assigned_to = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_cases',
        verbose_name=_("Assigned To"),
        help_text=_("Current case handler")
    )
    escalated_to = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='escalated_cases',
        verbose_name=_("Escalated To"),
        help_text=_("Supervisor or specialist the case is escalated to")
    )
    escalated_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='cases_escalated_by_me',
        verbose_name=_("Escalated By"),
        help_text=_("Who escalated this case")
    )
    escalation_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Escalation Date")
    )
    
    # Case Content
    title = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Case Title"),
        help_text=_("Brief title/summary of the case")
    )
    narrative = models.TextField(
        verbose_name=_("Narrative"),
        help_text=_("Detailed description of the case")
    )
    action_plan = models.TextField(
        blank=True,
        verbose_name=_("Action Plan"),
        help_text=_("Planned actions to resolve the case")
    )
    
    # Location and Incident Details
    incident_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Incident Date"),
        help_text=_("When the incident occurred")
    )
    incident_location = models.TextField(
        blank=True,
        verbose_name=_("Incident Location"),
        help_text=_("Where the incident occurred")
    )
    report_location = models.TextField(
        blank=True,
        verbose_name=_("Report Location"),
        help_text=_("Where the case was reported")
    )
    
    # Source Information (call, email, walk-in, etc.)
    source_type = models.CharField(
        max_length=50,
        default='call',
        verbose_name=_("Source Type"),
        help_text=_("How the case was reported (call, email, etc.)")
    )
    source_reference = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Source Reference"),
        help_text=_("Reference to source (call ID, email, etc.)")
    )
    source_channel = models.ForeignKey(
        'campaigns.Campaign',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='cases',
        verbose_name=_("Source Channel"),
        help_text=_("Campaign/queue where case originated")
    )
    
    # GBV Specific Fields
    is_gbv_related = models.BooleanField(
        default=False,
        verbose_name=_("GBV Related"),
        help_text=_("Whether this case involves gender-based violence")
    )
    medical_exam_done = models.BooleanField(
        default=False,
        verbose_name=_("Medical Exam Done"),
        help_text=_("Whether medical examination was conducted")
    )
    incident_reported_to_police = models.BooleanField(
        default=False,
        verbose_name=_("Reported to Police"),
        help_text=_("Whether incident was reported to police")
    )
    police_ob_number = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Police OB Number"),
        help_text=_("Police occurrence book number")
    )
    hiv_tested = models.BooleanField(
        default=False,
        verbose_name=_("HIV Tested")
    )
    hiv_test_result = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_("HIV Test Result")
    )
    pep_given = models.BooleanField(
        default=False,
        verbose_name=_("PEP Given"),
        help_text=_("Post-exposure prophylaxis provided")
    )
    art_given = models.BooleanField(
        default=False,
        verbose_name=_("ART Given"),
        help_text=_("Antiretroviral therapy provided")
    )
    ecp_given = models.BooleanField(
        default=False,
        verbose_name=_("ECP Given"),
        help_text=_("Emergency contraceptive pill provided")
    )
    counselling_given = models.BooleanField(
        default=False,
        verbose_name=_("Counselling Given")
    )
    counselling_organization = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Counselling Organization")
    )
    
    # Case Management
    due_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Due Date"),
        help_text=_("When case should be resolved by")
    )
    closed_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Closed Date")
    )
    resolution_summary = models.TextField(
        blank=True,
        verbose_name=_("Resolution Summary"),
        help_text=_("Summary of how the case was resolved")
    )
    
    # Client/Victim Count
    client_count = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Client Count"),
        help_text=_("Number of clients/victims in this case")
    )
    perpetrator_count = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Perpetrator Count"),
        help_text=_("Number of perpetrators involved")
    )
    
    # Reference Numbers
    incident_reference_number = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Incident Reference Number"),
        help_text=_("External reference number for the incident")
    )
    
    # AI Enhancement Fields
    ai_risk_score = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_("AI Risk Score"),
        help_text=_("AI-calculated risk score (0.0 to 1.0)")
    )
    ai_urgency_score = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_("AI Urgency Score"),
        help_text=_("AI-calculated urgency score (0.0 to 1.0)")
    )
    ai_suggested_category = models.ForeignKey(
        'core.ReferenceData',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'category': 'case_category'},
        related_name='ai_suggested_cases',
        verbose_name=_("AI Suggested Category")
    )
    ai_suggested_priority = models.ForeignKey(
        'core.ReferenceData',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'category': 'case_priority'},
        related_name='ai_suggested_priority_cases',
        verbose_name=_("AI Suggested Priority")
    )
    ai_summary = models.TextField(
        blank=True,
        verbose_name=_("AI Summary"),
        help_text=_("AI-generated case summary")
    )
    ai_keywords = models.JSONField(
        default=list,
        blank=True,
        verbose_name=_("AI Keywords"),
        help_text=_("AI-extracted keywords from case content")
    )
    ai_sentiment_score = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_("AI Sentiment Score"),
        help_text=_("AI-analyzed sentiment score (-1.0 to 1.0)")
    )
    ai_analysis_completed = models.BooleanField(
        default=False,
        verbose_name=_("AI Analysis Completed")
    )
    ai_analysis_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("AI Analysis Date")
    )
    
    # Migration Helper Fields
    legacy_case_id = models.IntegerField(
        null=True,
        blank=True,
        db_index=True,
        verbose_name=_("Legacy Case ID"),
        help_text=_("Original kase table ID")
    )
    legacy_nsr = models.IntegerField(
        null=True,
        blank=True,
        verbose_name=_("Legacy NSR"),
        help_text=_("Original NSR (case serial number)")
    )
    legacy_data = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("Legacy Data"),
        help_text=_("Original case data for migration tracking")
    )
    migration_notes = models.TextField(
        blank=True,
        verbose_name=_("Migration Notes")
    )
    
    # Manager
    objects = CaseManager()
    
    class Meta:
        verbose_name = _("Case")
        verbose_name_plural = _("Cases")
        ordering = ['-created_at']
        indexes = [
            # Primary lookup indexes
            models.Index(fields=['case_number']),
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['priority', '-created_at']),
            models.Index(fields=['assigned_to', 'status']),
            models.Index(fields=['reporter', '-created_at']),
            models.Index(fields=['case_type', '-created_at']),
            
            # Assignment and escalation indexes
            models.Index(fields=['escalated_to', 'escalation_date']),
            models.Index(fields=['assigned_to', 'due_date']),
            
            # Date-based indexes
            models.Index(fields=['due_date', 'status']),
            models.Index(fields=['incident_date', 'is_gbv_related']),
            models.Index(fields=['closed_date', 'status']),
            
            # GBV specific indexes
            models.Index(fields=['is_gbv_related', 'status']),
            models.Index(fields=['is_gbv_related', '-created_at']),
            
            # AI indexes
            models.Index(fields=['ai_analysis_completed', '-created_at']),
            models.Index(fields=['ai_risk_score', '-created_at']),
            models.Index(fields=['ai_urgency_score', '-created_at']),
            
            # Migration indexes
            models.Index(fields=['legacy_case_id']),
            models.Index(fields=['legacy_nsr']),
            
            # Composite indexes for common queries
            models.Index(fields=['is_active', 'status', '-created_at']),
            models.Index(fields=['assigned_to', 'is_active', 'status']),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(ai_risk_score__gte=0.0) & models.Q(ai_risk_score__lte=1.0),
                name='valid_ai_risk_score'
            ),
            models.CheckConstraint(
                check=models.Q(ai_urgency_score__gte=0.0) & models.Q(ai_urgency_score__lte=1.0),
                name='valid_ai_urgency_score'
            ),
            models.CheckConstraint(
                check=models.Q(ai_sentiment_score__gte=-1.0) & models.Q(ai_sentiment_score__lte=1.0),
                name='valid_ai_sentiment_score'
            ),
        ]
    
    def __str__(self):
        return f"{self.case_number}: {self.title or 'Case'}"
    
    def save(self, *args, **kwargs):
        """Override save to handle auto-generation of case number"""
        if not self.case_number:
            self.case_number = self.generate_case_number()
        
        # Auto-generate title if not provided
        if not self.title and self.narrative:
            # Take first 50 characters of narrative as title
            self.title = self.narrative[:50].strip()
            if len(self.narrative) > 50:
                self.title += "..."
        
        # Set closed date when status changes to closed
        if self.status and 'closed' in self.status.name.lower():
            if not self.closed_date:
                self.closed_date = timezone.now()
        
        # Set escalation date when escalated
        if self.escalated_to and not self.escalation_date:
            self.escalation_date = timezone.now()
        
        super().save(*args, **kwargs)
    
    def generate_case_number(self):
        """Generate unique case number"""
        from django.conf import settings
        
        # Format: CASE-YYYY-NNNNNN
        year = timezone.now().year
        
        # Get the latest case number for this year
        latest_case = Case.objects.filter(
            case_number__startswith=f"CASE-{year}-"
        ).order_by('-case_number').first()
        
        if latest_case:
            # Extract number and increment
            try:
                last_num = int(latest_case.case_number.split('-')[-1])
                next_num = last_num + 1
            except (ValueError, IndexError):
                next_num = 1
        else:
            next_num = 1
        
        return f"CASE-{year}-{next_num:06d}"
    
    @property
    def is_overdue(self):
        """Check if case is overdue"""
        return (
            self.due_date and
            self.due_date < timezone.now() and
            self.status.name.lower() not in ['closed', 'resolved', 'cancelled']
        )
    
    @property
    def age_in_days(self):
        """Get case age in days"""
        if self.closed_date:
            return (self.closed_date - self.created_at).days
        return (timezone.now() - self.created_at).days
    
    @property
    def is_escalated(self):
        """Check if case is escalated"""
        return bool(self.escalated_to)
    
    @property
    def time_to_resolution(self):
        """Get time taken to resolve case"""
        if self.closed_date:
            return self.closed_date - self.created_at
        return None
    
    def get_primary_client(self):
        """Get primary client/victim for this case"""
        return self.contact_roles.filter(role='client', is_primary=True).first()
    
    def get_primary_perpetrator(self):
        """Get primary perpetrator for this case"""
        return self.contact_roles.filter(role='perpetrator', is_primary=True).first()
    
    def get_all_clients(self):
        """Get all clients/victims for this case"""
        return self.contact_roles.filter(role='client')
    
    def get_all_perpetrators(self):
        """Get all perpetrators for this case"""
        return self.contact_roles.filter(role='perpetrator')
    
    def escalate_to(self, user, escalated_by=None, reason=''):
        """Escalate case to another user"""
        self.escalated_to = user
        self.escalated_by = escalated_by
        self.escalation_date = timezone.now()
        
        # Create activity log
        CaseActivity.objects.create(
            case=self,
            activity_type='escalated',
            user=escalated_by,
            description=f"Case escalated to {user.get_full_name()}. Reason: {reason}",
            data={'escalated_to': user.id, 'reason': reason}
        )
        
        self.save(update_fields=['escalated_to', 'escalated_by', 'escalation_date'])
    
    def assign_to(self, user, assigned_by=None):
        """Assign case to a user"""
        old_assignee = self.assigned_to
        self.assigned_to = user
        
        # Create activity log
        CaseActivity.objects.create(
            case=self,
            activity_type='assigned',
            user=assigned_by,
            description=f"Case assigned to {user.get_full_name()}",
            data={
                'assigned_to': user.id,
                'previous_assignee': old_assignee.id if old_assignee else None
            }
        )
        
        self.save(update_fields=['assigned_to'])
    
    def close_case(self, closed_by=None, resolution_summary=''):
        """Close the case"""
        # Update to closed status
        closed_status = ReferenceData.objects.filter(
            category='case_status', name__icontains='closed'
        ).first()
        
        if closed_status:
            self.status = closed_status
        
        self.closed_date = timezone.now()
        if resolution_summary:
            self.resolution_summary = resolution_summary
        
        # Create activity log
        CaseActivity.objects.create(
            case=self,
            activity_type='closed',
            user=closed_by,
            description="Case closed",
            data={'resolution_summary': resolution_summary}
        )
        
        self.save(update_fields=['status', 'closed_date', 'resolution_summary'])
    
    def update_counts(self):
        """Update client and perpetrator counts"""
        self.client_count = self.contact_roles.filter(role='client').count()
        self.perpetrator_count = self.contact_roles.filter(role='perpetrator').count()
        self.save(update_fields=['client_count', 'perpetrator_count'])


class CaseCategory(TimeStampedModel):
    """
    Case categories - many-to-many relationship with cases.
    Maps to legacy categories and case_categories.
    """
    
    case = models.ForeignKey(
        Case,
        on_delete=models.CASCADE,
        related_name='categories',
        verbose_name=_("Case")
    )
    category = models.ForeignKey(
        'core.ReferenceData',
        on_delete=models.CASCADE,
        limit_choices_to={'category': 'case_category'},
        verbose_name=_("Category")
    )
    is_primary = models.BooleanField(
        default=False,
        verbose_name=_("Is Primary Category"),
        help_text=_("Whether this is the main category for the case")
    )
    confidence_score = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_("Confidence Score"),
        help_text=_("AI confidence in this categorization (0.0 to 1.0)")
    )
    added_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Added By")
    )
    
    class Meta:
        verbose_name = _("Case Category")
        verbose_name_plural = _("Case Categories")
        unique_together = ['case', 'category']
        indexes = [
            models.Index(fields=['case', 'is_primary']),
            models.Index(fields=['category', 'is_primary']),
        ]
    
    def __str__(self):
        return f"{self.case.case_number}: {self.category.name}"


class CaseActivity(TimeStampedModel):
    """
    Track all activities/changes on a case.
    Maps to legacy kase_activity table.
    """
    
    ACTIVITY_TYPES = [
        ('created', _('Case Created')),
        ('updated', _('Case Updated')),
        ('assigned', _('Case Assigned')),
        ('escalated', _('Case Escalated')),
        ('status_changed', _('Status Changed')),
        ('priority_changed', _('Priority Changed')),
        ('note_added', _('Note Added')),
        ('contact_added', _('Contact Added')),
        ('contact_removed', _('Contact Removed')),
        ('category_added', _('Category Added')),
        ('category_removed', _('Category Removed')),
        ('service_added', _('Service Added')),
        ('referral_added', _('Referral Added')),
        ('call_logged', _('Call Logged')),
        ('document_uploaded', _('Document Uploaded')),
        ('closed', _('Case Closed')),
        ('reopened', _('Case Reopened')),
        ('ai_analysis', _('AI Analysis Completed')),
        ('other', _('Other')),
    ]
    
    case = models.ForeignKey(
        Case,
        on_delete=models.CASCADE,
        related_name='activities',
        verbose_name=_("Case")
    )
    activity_type = models.CharField(
        max_length=30,
        choices=ACTIVITY_TYPES,
        db_index=True,
        verbose_name=_("Activity Type")
    )
    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='case_activities',
        verbose_name=_("User"),
        help_text=_("User who performed this activity")
    )
    
    # Activity details
    title = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Title"),
        help_text=_("Brief title of the activity")
    )
    description = models.TextField(
        verbose_name=_("Description"),
        help_text=_("Detailed description of what happened")
    )
    
    # Structured data for the activity
    data = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("Activity Data"),
        help_text=_("Structured data related to this activity")
    )
    
    # Change tracking
    field_changes = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("Field Changes"),
        help_text=_("Details of what fields changed (before/after values)")
    )
    
    # Priority and visibility
    is_important = models.BooleanField(
        default=False,
        verbose_name=_("Is Important"),
        help_text=_("Mark this activity as important")
    )
    is_internal = models.BooleanField(
        default=False,
        verbose_name=_("Is Internal"),
        help_text=_("Whether this activity is internal only (not visible to clients)")
    )
    
    # External references
    source_reference = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Source Reference"),
        help_text=_("Reference to source (call ID, email, etc.)")
    )
    
    # Migration fields
    legacy_activity_id = models.IntegerField(
        null=True,
        blank=True,
        db_index=True,
        verbose_name=_("Legacy Activity ID")
    )
    
    class Meta:
        verbose_name = _("Case Activity")
        verbose_name_plural = _("Case Activities")
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['case', '-created_at']),
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['activity_type', '-created_at']),
            models.Index(fields=['is_important', '-created_at']),
            models.Index(fields=['case', 'activity_type']),
            models.Index(fields=['legacy_activity_id']),
        ]
    
    def __str__(self):
        return f"{self.case.case_number}: {self.get_activity_type_display()}"


class CaseService(TimeStampedModel):
    """
    Services provided for a case.
    Maps to legacy service table.
    """
    
    case = models.ForeignKey(
        Case,
        on_delete=models.CASCADE,
        related_name='services',
        verbose_name=_("Case")
    )
    service = models.ForeignKey(
        'core.ReferenceData',
        on_delete=models.CASCADE,
        limit_choices_to={'category': 'service'},
        verbose_name=_("Service")
    )
    provided_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Provided By")
    )
    service_date = models.DateTimeField(
        default=timezone.now,
        verbose_name=_("Service Date")
    )
    details = models.TextField(
        blank=True,
        verbose_name=_("Service Details"),
        help_text=_("Additional details about the service provided")
    )
    cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("Cost"),
        help_text=_("Cost of the service if applicable")
    )
    is_completed = models.BooleanField(
        default=True,
        verbose_name=_("Is Completed"),
        help_text=_("Whether the service was successfully completed")
    )
    
    # Migration fields
    legacy_service_id = models.IntegerField(
        null=True,
        blank=True,
        db_index=True,
        verbose_name=_("Legacy Service ID")
    )
    
    class Meta:
        verbose_name = _("Case Service")
        verbose_name_plural = _("Case Services")
        ordering = ['-service_date']
        indexes = [
            models.Index(fields=['case', '-service_date']),
            models.Index(fields=['service', '-service_date']),
            models.Index(fields=['provided_by', '-service_date']),
            models.Index(fields=['legacy_service_id']),
        ]
    
    def __str__(self):
        return f"{self.case.case_number}: {self.service.name}"


class CaseReferral(TimeStampedModel):
    """
    External referrals made for a case.
    Maps to legacy referal table.
    """
    
    REFERRAL_STATUSES = [
        ('pending', _('Pending')),
        ('sent', _('Sent')),
        ('acknowledged', _('Acknowledged')),
        ('completed', _('Completed')),
        ('rejected', _('Rejected')),
        ('cancelled', _('Cancelled')),
    ]
    
    case = models.ForeignKey(
        Case,
        on_delete=models.CASCADE,
        related_name='referrals',
        verbose_name=_("Case")
    )
    referral_type = models.ForeignKey(
        'core.ReferenceData',
        on_delete=models.CASCADE,
        related_name='referrals_by_type',
        limit_choices_to={'category': 'referral_type'},
        verbose_name=_("Referral Type")
    )
    organization = models.CharField(
        max_length=255,
        verbose_name=_("Organization"),
        help_text=_("Organization or service provider being referred to")
    )
    contact_person = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Contact Person")
    )
    contact_phone = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_("Contact Phone")
    )
    contact_email = models.EmailField(
        blank=True,
        verbose_name=_("Contact Email")
    )
    
    # Referral details
    reason = models.TextField(
        verbose_name=_("Reason for Referral"),
        help_text=_("Why this referral is being made")
    )
    urgency = models.ForeignKey(
        'core.ReferenceData',
        on_delete=models.SET_NULL,
        related_name='referrals_by_urgency',
        null=True,
        blank=True,
        limit_choices_to={'category': 'urgency'},
        verbose_name=_("Urgency Level")
    )
    
    # Status tracking
    status = models.CharField(
        max_length=20,
        choices=REFERRAL_STATUSES,
        default='pending',
        verbose_name=_("Status")
    )
    referred_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Referred By")
    )
    referral_date = models.DateTimeField(
        default=timezone.now,
        verbose_name=_("Referral Date")
    )
    
    # Follow-up
    follow_up_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Follow-up Date")
    )
    outcome = models.TextField(
        blank=True,
        verbose_name=_("Outcome"),
        help_text=_("Result of the referral")
    )
    
    # Additional details
    notes = models.TextField(
        blank=True,
        verbose_name=_("Notes")
    )
    attachments = models.JSONField(
        default=list,
        blank=True,
        verbose_name=_("Attachments"),
        help_text=_("List of attached documents/files")
    )
    
    # Migration fields
    legacy_referral_id = models.IntegerField(
        null=True,
        blank=True,
        db_index=True,
        verbose_name=_("Legacy Referral ID")
    )
    
    class Meta:
        verbose_name = _("Case Referral")
        verbose_name_plural = _("Case Referrals")
        ordering = ['-referral_date']
        indexes = [
            models.Index(fields=['case', '-referral_date']),
            models.Index(fields=['status', '-referral_date']),
            models.Index(fields=['referred_by', '-referral_date']),
            models.Index(fields=['follow_up_date', 'status']),
            models.Index(fields=['legacy_referral_id']),
        ]
    
    def __str__(self):
        return f"{self.case.case_number}: Referral to {self.organization}"
    
    @property
    def is_overdue(self):
        """Check if referral follow-up is overdue"""
        return (
            self.follow_up_date and
            self.follow_up_date < timezone.now() and
            self.status not in ['completed', 'rejected', 'cancelled']
        )


class CaseNote(TimeStampedModel):
    """
    Notes and comments on cases.
    Provides detailed tracking of case progress.
    """
    
    NOTE_TYPES = [
        ('general', _('General Note')),
        ('update', _('Case Update')),
        ('follow_up', _('Follow-up')),
        ('supervisor', _('Supervisor Note')),
        ('client_contact', _('Client Contact')),
        ('internal', _('Internal Note')),
        ('resolution', _('Resolution Note')),
    ]
    
    case = models.ForeignKey(
        Case,
        on_delete=models.CASCADE,
        related_name='notes',
        verbose_name=_("Case")
    )
    note_type = models.CharField(
        max_length=20,
        choices=NOTE_TYPES,
        default='general',
        verbose_name=_("Note Type")
    )
    author = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_("Author")
    )
    title = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Title")
    )
    content = models.TextField(
        verbose_name=_("Content")
    )
    is_private = models.BooleanField(
        default=False,
        verbose_name=_("Is Private"),
        help_text=_("Whether this note is private to staff only")
    )
    is_important = models.BooleanField(
        default=False,
        verbose_name=_("Is Important")
    )
    
    # Visibility and sharing
    visible_to_client = models.BooleanField(
        default=False,
        verbose_name=_("Visible to Client"),
        help_text=_("Whether client can see this note")
    )
    
    # Attachments and references
    attachments = models.JSONField(
        default=list,
        blank=True,
        verbose_name=_("Attachments")
    )
    
    class Meta:
        verbose_name = _("Case Note")
        verbose_name_plural = _("Case Notes")
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['case', '-created_at']),
            models.Index(fields=['author', '-created_at']),
            models.Index(fields=['note_type', '-created_at']),
            models.Index(fields=['is_important', '-created_at']),
            models.Index(fields=['case', 'note_type']),
        ]
    
    def __str__(self):
        return f"{self.case.case_number}: {self.title or self.content[:50]}"


class CaseAttachment(TimeStampedModel):
    """
    File attachments for cases.
    Maps to legacy attachment table.
    """
    
    ATTACHMENT_TYPES = [
        ('document', _('Document')),
        ('image', _('Image')),
        ('audio', _('Audio Recording')),
        ('video', _('Video')),
        ('medical_report', _('Medical Report')),
        ('police_report', _('Police Report')),
        ('statement', _('Statement')),
        ('evidence', _('Evidence')),
        ('other', _('Other')),
    ]
    
    case = models.ForeignKey(
        Case,
        on_delete=models.CASCADE,
        related_name='attachments',
        verbose_name=_("Case")
    )
    attachment_type = models.CharField(
        max_length=20,
        choices=ATTACHMENT_TYPES,
        default='document',
        verbose_name=_("Attachment Type")
    )
    
    # File information
    file_name = models.CharField(
        max_length=255,
        verbose_name=_("File Name")
    )
    file_path = models.CharField(
        max_length=500,
        verbose_name=_("File Path"),
        help_text=_("Path to the actual file")
    )
    file_size = models.PositiveIntegerField(
        verbose_name=_("File Size (bytes)")
    )
    mime_type = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("MIME Type")
    )
    
    # Metadata
    title = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Title"),
        help_text=_("Descriptive title for the attachment")
    )
    description = models.TextField(
        blank=True,
        verbose_name=_("Description")
    )
    uploaded_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_("Uploaded By")
    )
    
    # Access control
    is_confidential = models.BooleanField(
        default=False,
        verbose_name=_("Is Confidential"),
        help_text=_("Whether this attachment contains sensitive information")
    )
    access_level = models.CharField(
        max_length=20,
        choices=[
            ('public', _('Public')),
            ('staff_only', _('Staff Only')),
            ('supervisor_only', _('Supervisor Only')),
            ('confidential', _('Confidential')),
        ],
        default='staff_only',
        verbose_name=_("Access Level")
    )
    
    # File integrity
    checksum = models.CharField(
        max_length=64,
        blank=True,
        verbose_name=_("Checksum"),
        help_text=_("SHA256 checksum for file integrity")
    )
    
    # Migration fields
    legacy_attachment_id = models.IntegerField(
        null=True,
        blank=True,
        db_index=True,
        verbose_name=_("Legacy Attachment ID")
    )
    
    class Meta:
        verbose_name = _("Case Attachment")
        verbose_name_plural = _("Case Attachments")
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['case', '-created_at']),
            models.Index(fields=['attachment_type', '-created_at']),
            models.Index(fields=['uploaded_by', '-created_at']),
            models.Index(fields=['is_confidential', 'access_level']),
            models.Index(fields=['legacy_attachment_id']),
        ]
    
    def __str__(self):
        return f"{self.case.case_number}: {self.file_name}"
    
    @property
    def file_size_human(self):
        """Get human-readable file size"""
        size = self.file_size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"


class CaseUpdate(TimeStampedModel):
    """
    Structured updates to cases - periodic status updates.
    Maps to legacy caseupd and kaseupd tables.
    """
    
    case = models.ForeignKey(
        Case,
        on_delete=models.CASCADE,
        related_name='updates',
        verbose_name=_("Case")
    )
    updated_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_("Updated By")
    )
    
    # Update content
    summary = models.CharField(
        max_length=255,
        verbose_name=_("Update Summary"),
        help_text=_("Brief summary of this update")
    )
    details = models.TextField(
        verbose_name=_("Update Details"),
        help_text=_("Detailed description of the update")
    )
    
    # Status at time of update
    status_at_update = models.ForeignKey(
        'core.ReferenceData',
        on_delete=models.PROTECT,
        limit_choices_to={'category': 'case_status'},
        related_name='case_updates_at_status',
        verbose_name=_("Status at Update")
    )
    priority_at_update = models.ForeignKey(
        'core.ReferenceData',
        on_delete=models.PROTECT,
        limit_choices_to={'category': 'case_priority'},
        related_name='case_updates_at_priority',
        verbose_name=_("Priority at Update")
    )
    
    # Progress indicators
    progress_percentage = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name=_("Progress Percentage"),
        help_text=_("Estimated completion percentage (0-100)")
    )
    
    # Next steps
    next_actions = models.TextField(
        blank=True,
        verbose_name=_("Next Actions"),
        help_text=_("Planned next actions")
    )
    next_update_due = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Next Update Due")
    )
    
    # Change summary
    changes_made = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("Changes Made"),
        help_text=_("Summary of changes made in this update")
    )
    
    # Migration fields
    legacy_update_id = models.IntegerField(
        null=True,
        blank=True,
        db_index=True,
        verbose_name=_("Legacy Update ID")
    )
    
    class Meta:
        verbose_name = _("Case Update")
        verbose_name_plural = _("Case Updates")
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['case', '-created_at']),
            models.Index(fields=['updated_by', '-created_at']),
            models.Index(fields=['next_update_due', 'case']),
            models.Index(fields=['legacy_update_id']),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(progress_percentage__gte=0) & models.Q(progress_percentage__lte=100),
                name='valid_progress_percentage'
            ),
        ]
    
    def __str__(self):
        return f"{self.case.case_number}: {self.summary}"


