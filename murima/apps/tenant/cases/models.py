from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from apps.shared.core.models import (
    BaseModel,
    TenantModel,
)
from apps.tenant.contacts.models import Contact
from apps.tenant.documents.models import Document
from enum import Enum
import uuid

User = get_user_model()

class CasePriority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

class CaseType(BaseModel, TenantModel):
    """Configurable case types with custom forms and workflows"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    requires_approval = models.BooleanField(default=False)
    default_priority = models.PositiveSmallIntegerField(
        choices=CasePriority.choices(),
        default=CasePriority.MEDIUM.value
    )
    form_schema = models.JSONField(default=dict)  # For dynamic form configuration
    workflow_definition = models.JSONField(default=dict)  # For workflow automation
    
    class Meta:
        unique_together = ('tenant', 'name')
        verbose_name = _("Case Type")
        verbose_name_plural = _("Case Types")

    def __str__(self):
        return self.name

class CaseStatus(BaseModel, TenantModel):
    """Configurable statuses with workflow transitions"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    is_closed = models.BooleanField(default=False)
    is_initial = models.BooleanField(default=False)
    allowed_transitions = models.ManyToManyField(
        'self',
        symmetrical=False,
        blank=True,
        through='CaseStatusTransition'
    )
    
    class Meta:
        unique_together = ('tenant', 'name')
        verbose_name = _("Case Status")
        verbose_name_plural = _("Case Statuses")

class CaseStatusTransition(BaseModel, TenantModel):
    """Allowed status transitions with optional conditions"""
    from_status = models.ForeignKey(
        CaseStatus,
        on_delete=models.CASCADE,
        related_name='from_transitions'
    )
    to_status = models.ForeignKey(
        CaseStatus,
        on_delete=models.CASCADE,
        related_name='to_transitions'
    )
    condition = models.JSONField(blank=True, null=True)  # For conditional transitions
    requires_comment = models.BooleanField(default=False)
    requires_approval = models.BooleanField(default=False)

    class Meta:
        unique_together = ('tenant', 'from_status', 'to_status')

class Case(BaseModel, TenantModel):
    """Core case model with comprehensive tracking"""
    CASE_SOURCE_CHOICES = [
        ('web', 'Web Portal'),
        ('email', 'Email'),
        ('phone', 'Phone'),
        ('api', 'API'),
        ('walkin', 'Walk-in'),
        ('referral', 'Referral'),
    ]
    
    # Core Identification
    case_number = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
        default=lambda: f"CASE-{uuid.uuid4().hex[:8].upper()}"
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    # Relationships
    case_type = models.ForeignKey(
        CaseType,
        on_delete=models.PROTECT,
        related_name='cases'
    )
    status = models.ForeignKey(
        CaseStatus,
        on_delete=models.PROTECT,
        related_name='cases'
    )
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='assigned_cases',
        null=True,
        blank=True
    )
    assigned_team = models.ForeignKey(
        'accounts.Team',
        on_delete=models.PROTECT,
        related_name='assigned_cases',
        null=True,
        blank=True
    )
    contact = models.ForeignKey(
        Contact,
        on_delete=models.PROTECT,
        related_name='cases',
        null=True,
        blank=True
    )
    related_cases = models.ManyToManyField(
        'self',
        symmetrical=False,
        through='RelatedCase',
        through_fields=('primary_case', 'related_case'),
        blank=True
    )
    
    # Metadata
    priority = models.PositiveSmallIntegerField(
        choices=CasePriority.choices(),
        default=CasePriority.MEDIUM.value
    )
    source = models.CharField(
        max_length=20,
        choices=CASE_SOURCE_CHOICES,
        default='web'
    )
    custom_fields = models.JSONField(default=dict)  # For dynamic field storage
    
    # Dates
    opened_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True, blank=True)
    resolved_date = models.DateTimeField(null=True, blank=True)
    closed_date = models.DateTimeField(null=True, blank=True)
    
    # SLA Tracking
    sla_due_date = models.DateTimeField(null=True, blank=True)
    sla_breached = models.BooleanField(default=False)
    response_time = models.DurationField(null=True, blank=True)
    resolution_time = models.DurationField(null=True, blank=True)
    
    # Workflow
    current_stage = models.CharField(max_length=50, blank=True)
    requires_approval = models.BooleanField(default=False)
    is_escalated = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-opened_date']
        indexes = [
            models.Index(fields=['case_number']),
            models.Index(fields=['status']),
            models.Index(fields=['assigned_to']),
            models.Index(fields=['priority']),
            models.Index(fields=['opened_date']),
        ]
        verbose_name = _("Case")
        verbose_name_plural = _("Cases")

    def __str__(self):
        return f"{self.case_number}: {self.title}"

    def save(self, *args, **kwargs):
        if not self.case_number:
            self.case_number = self.generate_case_number()
        super().save(*args, **kwargs)

    def generate_case_number(self):
        return f"CASE-{uuid.uuid4().hex[:8].upper()}"

class RelatedCase(BaseModel):
    """Model for linking related cases"""
    primary_case = models.ForeignKey(
        Case,
        on_delete=models.CASCADE,
        related_name='primary_relations'
    )
    related_case = models.ForeignKey(
        Case,
        on_delete=models.CASCADE,
        related_name='related_relations'
    )
    relationship_type = models.CharField(max_length=50)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ('primary_case', 'related_case', 'relationship_type')

class CaseNote(BaseModel, TenantModel):
    """Structured and unstructured case notes"""
    case = models.ForeignKey(
        Case,
        on_delete=models.CASCADE,
        related_name='notes'
    )
    content = models.TextField()
    is_internal = models.BooleanField(default=False)
    document = models.ForeignKey(
        Document,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Case Note")
        verbose_name_plural = _("Case Notes")

    def __str__(self):
        return f"Note for {self.case.case_number}"

class CaseAttachment(BaseModel, TenantModel):
    """Document attachments for cases"""
    case = models.ForeignKey(
        Case,
        on_delete=models.CASCADE,
        related_name='attachments'
    )
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name='case_attachments'
    )
    description = models.CharField(max_length=255, blank=True)
    is_private = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Case Attachment")
        verbose_name_plural = _("Case Attachments")

class CaseWorkflow(BaseModel, TenantModel):
    """Workflow automation rules"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    trigger_event = models.CharField(max_length=100)
    condition = models.JSONField(default=dict)  # For rule conditions
    actions = models.JSONField(default=list)  # List of actions to execute
    is_active = models.BooleanField(default=True)
    priority = models.PositiveSmallIntegerField(default=0)

    class Meta:
        unique_together = ('tenant', 'name')
        verbose_name = _("Case Workflow")
        verbose_name_plural = _("Case Workflows")

class CaseSLA(BaseModel, TenantModel):
    """Service Level Agreement definitions"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    case_type = models.ForeignKey(
        CaseType,
        on_delete=models.CASCADE,
        related_name='slas'
    )
    initial_response_time = models.DurationField()
    resolution_time = models.DurationField()
    business_hours = models.JSONField(default=dict)  # For custom business hours
    escalation_path = models.JSONField(default=list)  # For escalation rules
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('tenant', 'name')
        verbose_name = _("Case SLA")
        verbose_name_plural = _("Case SLAs")

class CaseEventLog(BaseModel, TenantModel):
    """Comprehensive audit trail for case events"""
    EVENT_TYPES = [
        ('status_change', 'Status Change'),
        ('assignment', 'Assignment'),
        ('note_added', 'Note Added'),
        ('document_added', 'Document Added'),
        ('sla_breach', 'SLA Breach'),
        ('workflow_trigger', 'Workflow Trigger'),
    ]
    
    case = models.ForeignKey(
        Case,
        on_delete=models.CASCADE,
        related_name='event_logs'
    )
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES)
    previous_value = models.JSONField(null=True, blank=True)
    new_value = models.JSONField(null=True, blank=True)
    metadata = models.JSONField(default=dict)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Case Event Log")
        verbose_name_plural = _("Case Event Logs")