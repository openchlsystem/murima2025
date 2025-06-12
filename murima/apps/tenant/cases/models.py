from django.db import models
from django.forms import ValidationError
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.contenttypes.fields import GenericRelation
from apps.shared.accounts.models import User
from apps.shared.core.models import BaseModel, AuditLog
from django.contrib.postgres.fields import ArrayField
from django.db.models import JSONField

class CaseType(BaseModel):
    """
    Defines different types of cases with their specific configurations.
    """
    name = models.CharField(
        max_length=100,
        help_text="Name of the case type (e.g., 'Complaint', 'Support Ticket')"
    )
    code = models.SlugField(
        max_length=50,
        unique=True,
        help_text="Short code for the case type"
    )
    description = models.TextField(
        blank=True,
        help_text="Description of this case type"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this case type is active and available for use"
    )
    icon = models.CharField(
        max_length=50,
        blank=True,
        help_text="Icon to represent this case type in the UI"
    )
    color = models.CharField(
        max_length=20,
        blank=True,
        help_text="Color code to represent this case type"
    )
    default_priority = models.PositiveSmallIntegerField(
        default=3,
        help_text="Default priority for cases of this type (1-5, 1 being highest)"
    )
    default_sla_hours = models.PositiveIntegerField(
        default=72,
        help_text="Default SLA in hours for this case type"
    )
    metadata = JSONField(
        default=dict,
        blank=True,
        help_text="Additional configuration for this case type"
    )

    class Meta:
        verbose_name = "Case Type"
        verbose_name_plural = "Case Types"
        ordering = ['name']
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return self.name


class CasePriority(models.IntegerChoices):
    """
    Enumeration for case priority levels.
    """
    CRITICAL = 1, 'Critical'
    HIGH = 2, 'High'
    MEDIUM = 3, 'Medium'
    LOW = 4, 'Low'
    VERY_LOW = 5, 'Very Low'


class CaseStatus(BaseModel):
    """
    Configurable statuses that cases can have during their lifecycle.
    """
    name = models.CharField(
        max_length=50,
        help_text="Name of the status (e.g., 'Open', 'In Progress')"
    )
    code = models.SlugField(
        max_length=30,
        unique=True,
        help_text="Short code for the status"
    )
    description = models.TextField(
        blank=True,
        help_text="Description of this status"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this status is available for use"
    )
    is_closed = models.BooleanField(
        default=False,
        help_text="Whether this status represents a closed case"
    )
    is_default = models.BooleanField(
        default=False,
        help_text="Whether this is the default status for new cases"
    )
    color = models.CharField(
        max_length=20,
        blank=True,
        help_text="Color code to represent this status"
    )
    order = models.PositiveSmallIntegerField(
        default=0,
        help_text="Order in which statuses should be displayed"
    )
    allowed_next_statuses = models.ManyToManyField(
        'self',
        symmetrical=False,
        blank=True,
        help_text="Statuses that can follow this one in workflow"
    )

    class Meta:
        verbose_name = "Case Status"
        verbose_name_plural = "Case Statuses"
        ordering = ['order', 'name']
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['is_active']),
            models.Index(fields=['is_closed']),
        ]

    def __str__(self):
        return self.name

    def clean(self):
        if self.is_default and CaseStatus.objects.filter(is_default=True).exclude(pk=self.pk).exists():
            raise ValidationError("There can only be one default status")

    def save(self, *args, **kwargs):
        if self.is_default:
            # Ensure no other status is marked as default
            CaseStatus.objects.filter(is_default=True).exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)


class Case(BaseModel):
    """
    Core case model representing a single case record in the system.
    """
    case_type = models.ForeignKey(
        CaseType,
        on_delete=models.PROTECT,
        related_name='cases',
        help_text="Type of this case"
    )
    case_number = models.CharField(
        max_length=50,
        unique=True,
        editable=False,
        help_text="Auto-generated case number for reference"
    )
    title = models.CharField(
        max_length=200,
        help_text="Short title describing the case"
    )
    description = models.TextField(
        blank=True,
        help_text="Detailed description of the case"
    )
    status = models.ForeignKey(
        CaseStatus,
        on_delete=models.PROTECT,
        related_name='cases',
        help_text="Current status of the case"
    )
    priority = models.PositiveSmallIntegerField(
        choices=CasePriority.choices,
        default=CasePriority.MEDIUM,
        help_text="Priority level of the case"
    )
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='assigned_cases',
        null=True,
        blank=True,
        help_text="User currently assigned to this case"
    )
    # assigned_team = models.ForeignKey(
    #     'accounts.Team',
    #     on_delete=models.PROTECT,
    #     related_name='assigned_cases',
    #     null=True,
    #     blank=True,
    #     help_text="Team currently assigned to this case"
    # )
    due_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Date by which the case should be resolved"
    )
    resolved_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When the case was marked as resolved"
    )
    resolved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='resolved_cases',
        null=True,
        blank=True,
        help_text="User who resolved the case"
    )
    sla_expires_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When the SLA for this case expires"
    )
    is_high_priority = models.BooleanField(
        default=False,
        help_text="Flag for cases that require special attention"
    )
    is_confidential = models.BooleanField(
        default=False,
        help_text="Whether this case contains sensitive information"
    )
    source_channel = models.CharField(
        max_length=50,
        blank=True,
        help_text="Channel through which the case was created (email, web, phone, etc.)"
    )
    reference_id = models.CharField(
        max_length=100,
        blank=True,
        help_text="External reference ID for this case"
    )
    custom_fields = JSONField(
        default=dict,
        blank=True,
        help_text="Custom field values for this case"
    )
    tags = ArrayField(
        models.CharField(max_length=50),
        default=list,
        blank=True,
        help_text="Tags for categorizing and filtering cases"
    )
    audit_logs = GenericRelation(AuditLog, related_query_name='case')

    class Meta:
        verbose_name = "Case"
        verbose_name_plural = "Cases"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['case_number']),
            models.Index(fields=['case_type']),
            models.Index(fields=['status']),
            models.Index(fields=['priority']),
            models.Index(fields=['assigned_to']),
            # models.Index(fields=['assigned_team']),
            models.Index(fields=['due_date']),
            models.Index(fields=['is_high_priority']),
            models.Index(fields=['is_confidential']),
            models.Index(fields=['tags']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.case_number} - {self.title}"

    def save(self, *args, **kwargs):
        if not self.case_number:
            # Generate case number when first saving
            prefix = self.case_type.code.upper() if self.case_type else 'CASE'
            timestamp = timezone.now().strftime('%y%m%d')
            last_id = Case.objects.filter(case_number__startswith=f"{prefix}-{timestamp}").count()
            self.case_number = f"{prefix}-{timestamp}-{last_id + 1:04d}"
        
        if not self.sla_expires_at and self.case_type:
            # Set SLA expiration if not set
            self.sla_expires_at = timezone.now() + timezone.timedelta(hours=self.case_type.default_sla_hours)
        
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return f"/cases/{self.id}/"

    @property
    def is_overdue(self):
        """Check if the case is past its due date or SLA."""
        now = timezone.now()
        return (
            (self.due_date and self.due_date < now) or
            (self.sla_expires_at and self.sla_expires_at < now)
        )

    @property
    def time_to_resolution(self):
        """Calculate the time taken to resolve the case."""
        if self.resolved_at and self.created_at:
            return self.resolved_at - self.created_at
        return None

    def add_note(self, content, user, is_internal=False):
        """Helper method to add a note to this case."""
        return CaseNote.objects.create(
            case=self,
            content=content,
            created_by=user,
            is_internal=is_internal
        )

    def attach_document(self, file, uploaded_by, description=''):
        """Helper method to attach a document to this case."""
        return CaseDocument.objects.create(
            case=self,
            file=file,
            description=description,
            uploaded_by=uploaded_by
        )

    def update_status(self, new_status, changed_by, comment=''):
        """Transition the case to a new status with audit logging."""
        old_status = self.status
        self.status = new_status
        
        if new_status.is_closed and not self.resolved_at:
            self.resolved_at = timezone.now()
            self.resolved_by = changed_by
        
        self.save()
        
        # Log the status change
        CaseHistory.objects.create(
            case=self,
            action='STATUS_CHANGE',
            changed_by=changed_by,
            from_status=old_status,
            to_status=new_status,
            comment=comment
        )


class CaseDocument(BaseModel):
    """
    Documents attached to a case.
    """
    case = models.ForeignKey(
        Case,
        on_delete=models.CASCADE,
        related_name='case_documents',
        help_text="Case this document belongs to"
    )
    file = models.FileField(
        upload_to='case_documents/%Y/%m/%d/',
        help_text="The document file"
    )
    description = models.TextField(
        blank=True,
        help_text="Description of the document"
    )
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='uploaded_case_documents',
        help_text="User who uploaded this document"
    )
    file_type = models.CharField(
        max_length=50,
        blank=True,
        help_text="File type (extension)"
    )
    file_size = models.PositiveIntegerField(
        help_text="File size in bytes"
    )
    version = models.PositiveIntegerField(
        default=1,
        help_text="Version number of this document"
    )
    is_current = models.BooleanField(
        default=True,
        help_text="Whether this is the current version"
    )
    metadata = JSONField(
        default=dict,
        blank=True,
        help_text="Additional metadata about the document"
    )

    class Meta:
        verbose_name = "Case Document"
        verbose_name_plural = "Case Documents"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['case']),
            models.Index(fields=['uploaded_by']),
            models.Index(fields=['file_type']),
        ]

    def __str__(self):
        return f"Document for {self.case.case_number}"

    def save(self, *args, **kwargs):
        if self.file:
            if not self.file_type:
                self.file_type = self.file.name.split('.')[-1].lower()
            if not self.file_size:
                self.file_size = self.file.size
        super().save(*args, **kwargs)


class CaseNote(BaseModel):
    """
    Notes and comments added to a case.
    """
    case = models.ForeignKey(
        Case,
        on_delete=models.CASCADE,
        related_name='notes',
        help_text="Case this note belongs to"
    )
    content = models.TextField(
        help_text="The note content"
    )
    is_internal = models.BooleanField(
        default=False,
        help_text="Whether this note is internal only (not visible to customers)"
    )
    pinned = models.BooleanField(
        default=False,
        help_text="Whether this note is pinned to the top"
    )
    reply_to = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='replies',
        help_text="If this is a reply, the note being replied to"
    )
    metadata = JSONField(
        default=dict,
        blank=True,
        help_text="Additional metadata about the note"
    )

    class Meta:
        verbose_name = "Case Note"
        verbose_name_plural = "Case Notes"
        ordering = ['-pinned', '-created_at']
        indexes = [
            models.Index(fields=['case']),
            models.Index(fields=['is_internal']),
            models.Index(fields=['pinned']),
        ]

    def __str__(self):
        return f"Note on {self.case.case_number} by {self.created_by}"


class CaseHistory(BaseModel):
    """
    Audit trail of all significant changes to a case.
    """
    case = models.ForeignKey(
        Case,
        on_delete=models.CASCADE,
        related_name='history',
        help_text="Case this history item belongs to"
    )
    ACTION_CHOICES = [
        ('CREATE', 'Case Created'),
        ('STATUS_CHANGE', 'Status Changed'),
        ('ASSIGNMENT', 'Assignment Changed'),
        ('PRIORITY_CHANGE', 'Priority Changed'),
        ('NOTE_ADDED', 'Note Added'),
        ('DOCUMENT_ADDED', 'Document Added'),
        ('FIELD_UPDATE', 'Field Updated'),
        ('MERGE', 'Case Merged'),
        ('LINK', 'Case Linked'),
        ('ESCALATE', 'Case Escalated'),
        ('SLA_UPDATE', 'SLA Updated'),
        ('DUE_DATE_UPDATE', 'Due Date Updated'),
    ]
    action = models.CharField(
        max_length=50,
        choices=ACTION_CHOICES,
        help_text="Type of action performed"
    )
    changed_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='case_changes',
        help_text="User who performed this action"
    )
    from_status = models.ForeignKey(
        CaseStatus,
        on_delete=models.PROTECT,
        related_name='history_from',
        null=True,
        blank=True,
        help_text="Previous status (for status changes)"
    )
    to_status = models.ForeignKey(
        CaseStatus,
        on_delete=models.PROTECT,
        related_name='history_to',
        null=True,
        blank=True,
        help_text="New status (for status changes)"
    )
    from_priority = models.PositiveSmallIntegerField(
        choices=CasePriority.choices,
        null=True,
        blank=True,
        help_text="Previous priority (for priority changes)"
    )
    to_priority = models.PositiveSmallIntegerField(
        choices=CasePriority.choices,
        null=True,
        blank=True,
        help_text="New priority (for priority changes)"
    )
    from_assignment = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='history_from_assignment',
        null=True,
        blank=True,
        help_text="Previous assignee (for assignment changes)"
    )
    to_assignment = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='history_to_assignment',
        null=True,
        blank=True,
        help_text="New assignee (for assignment changes)"
    )
    related_note = models.ForeignKey(
        CaseNote,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Related note (for note-related actions)"
    )
    related_document = models.ForeignKey(
        CaseDocument,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Related document (for document-related actions)"
    )
    comment = models.TextField(
        blank=True,
        help_text="Additional comments about this change"
    )
    changes = JSONField(
        default=dict,
        blank=True,
        help_text="Detailed changes in JSON format"
    )

    class Meta:
        verbose_name = "Case History"
        verbose_name_plural = "Case Histories"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['case']),
            models.Index(fields=['action']),
            models.Index(fields=['changed_by']),
        ]

    def __str__(self):
        return f"{self.get_action_display()} on {self.case.case_number}"


class CaseLink(BaseModel):
    """
    Relationships between cases (parent-child, related, etc.).
    """
    source_case = models.ForeignKey(
        Case,
        on_delete=models.CASCADE,
        related_name='outgoing_links',
        help_text="The source case in this relationship"
    )
    target_case = models.ForeignKey(
        Case,
        on_delete=models.CASCADE,
        related_name='incoming_links',
        help_text="The target case in this relationship"
    )
    RELATIONSHIP_TYPES = [
        ('RELATED', 'Related To'),
        ('DUPLICATE', 'Duplicate Of'),
        ('BLOCKS', 'Blocks'),
        ('BLOCKED_BY', 'Blocked By'),
        ('PARENT', 'Parent Of'),
        ('CHILD', 'Child Of'),
        ('MERGED', 'Merged From'),
        ('SPLIT', 'Split From'),
        ('FOLLOWUP', 'Follow-up To'),
    ]
    relationship_type = models.CharField(
        max_length=20,
        choices=RELATIONSHIP_TYPES,
        help_text="Type of relationship between the cases"
    )
    description = models.TextField(
        blank=True,
        help_text="Description of the relationship"
    )

    class Meta:
        verbose_name = "Case Link"
        verbose_name_plural = "Case Links"
        unique_together = [('source_case', 'target_case', 'relationship_type')]
        indexes = [
            models.Index(fields=['source_case']),
            models.Index(fields=['target_case']),
            models.Index(fields=['relationship_type']),
        ]

    def __str__(self):
        return f"{self.source_case} {self.get_relationship_type_display()} {self.target_case}"


class CaseTemplate(BaseModel):
    """
    Templates for common case types to streamline case creation.
    """
    name = models.CharField(
        max_length=100,
        help_text="Name of this template"
    )
    case_type = models.ForeignKey(
        CaseType,
        on_delete=models.PROTECT,
        related_name='templates',
        help_text="Case type this template is for"
    )
    description = models.TextField(
        blank=True,
        help_text="Description of when to use this template"
    )
    default_priority = models.PositiveSmallIntegerField(
        choices=CasePriority.choices,
        default=CasePriority.MEDIUM,
        help_text="Default priority for cases created from this template"
    )
    default_status = models.ForeignKey(
        CaseStatus,
        on_delete=models.PROTECT,
        help_text="Default status for cases created from this template"
    )
    default_assignee = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Default assignee for cases created from this template"
    )
    # default_team = models.ForeignKey(
    #     'accounts.Team',
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     blank=True,
    #     help_text="Default team for cases created from this template"
    # )
    default_sla_hours = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Default SLA in hours for cases from this template"
    )
    content = models.TextField(
        blank=True,
        help_text="Template content for the case description"
    )
    custom_fields = JSONField(
        default=dict,
        blank=True,
        help_text="Default values for custom fields"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this template is available for use"
    )

    class Meta:
        verbose_name = "Case Template"
        verbose_name_plural = "Case Templates"
        ordering = ['case_type', 'name']
        indexes = [
            models.Index(fields=['case_type']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"{self.name} ({self.case_type})"


class SLA(BaseModel):
    """
    Service Level Agreement definitions for case types and priorities.
    """
    name = models.CharField(
        max_length=100,
        help_text="Name of this SLA policy"
    )
    case_type = models.ForeignKey(
        CaseType,
        on_delete=models.CASCADE,
        related_name='slas',
        null=True,
        blank=True,
        help_text="Case type this SLA applies to (null for all types)"
    )
    priority = models.PositiveSmallIntegerField(
        choices=CasePriority.choices,
        null=True,
        blank=True,
        help_text="Priority level this SLA applies to (null for all priorities)"
    )
    response_time_hours = models.PositiveIntegerField(
        help_text="Expected response time in hours"
    )
    resolution_time_hours = models.PositiveIntegerField(
        help_text="Expected resolution time in hours"
    )
    business_hours_only = models.BooleanField(
        default=False,
        help_text="Whether SLA only counts during business hours"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this SLA policy is active"
    )
    description = models.TextField(
        blank=True,
        help_text="Description of this SLA policy"
    )
    escalation_path = models.JSONField(
        default=list,
        blank=True,
        help_text="Escalation path when SLA is breached"
    )

    class Meta:
        verbose_name = "SLA"
        verbose_name_plural = "SLAs"
        ordering = ['case_type', 'priority']
        unique_together = [('case_type', 'priority')]
        indexes = [
            models.Index(fields=['case_type']),
            models.Index(fields=['priority']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"{self.name} ({self.get_priority_display() if self.priority else 'All'} {self.case_type or 'All'})"


class WorkflowRule(BaseModel):
    """
    Rules for automating case workflows and routing.
    """
    name = models.CharField(
        max_length=100,
        help_text="Name of this workflow rule"
    )
    description = models.TextField(
        blank=True,
        help_text="Description of what this rule does"
    )
    case_type = models.ForeignKey(
        CaseType,
        on_delete=models.CASCADE,
        related_name='workflow_rules',
        null=True,
        blank=True,
        help_text="Case type this rule applies to (null for all types)"
    )
    priority = models.PositiveSmallIntegerField(
        choices=CasePriority.choices,
        null=True,
        blank=True,
        help_text="Priority level this rule applies to (null for all priorities)"
    )
    trigger_condition = models.CharField(
        max_length=50,
        choices=[
            ('STATUS_CHANGE', 'Status Change'),
            ('PRIORITY_CHANGE', 'Priority Change'),
            ('ASSIGNMENT_CHANGE', 'Assignment Change'),
            ('CREATION', 'Case Creation'),
            ('DUE_DATE_APPROACHING', 'Due Date Approaching'),
            ('SLA_BREACHED', 'SLA Breached'),
            ('FIELD_UPDATE', 'Field Updated'),
            ('NOTE_ADDED', 'Note Added'),
            ('DOCUMENT_ADDED', 'Document Added'),
        ],
        help_text="When this rule should be triggered"
    )
    condition_expression = JSONField(
        default=dict,
        blank=True,
        help_text="Additional conditions for rule execution"
    )
    action_type = models.CharField(
        max_length=50,
        choices=[
            ('CHANGE_STATUS', 'Change Status'),
            ('CHANGE_PRIORITY', 'Change Priority'),
            ('ASSIGN_TO_USER', 'Assign to User'),
            ('ASSIGN_TO_TEAM', 'Assign to Team'),
            ('SEND_NOTIFICATION', 'Send Notification'),
            ('CREATE_TASK', 'Create Task'),
            ('ESCALATE', 'Escalate Case'),
            ('RUN_SCRIPT', 'Run Custom Script'),
        ],
        help_text="Action to perform when rule is triggered"
    )
    action_parameters = JSONField(
        default=dict,
        blank=True,
        help_text="Parameters for the action"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this rule is active"
    )
    order = models.PositiveSmallIntegerField(
        default=0,
        help_text="Execution order when multiple rules apply"
    )

    class Meta:
        verbose_name = "Workflow Rule"
        verbose_name_plural = "Workflow Rules"
        ordering = ['order', 'name']
        indexes = [
            models.Index(fields=['case_type']),
            models.Index(fields=['priority']),
            models.Index(fields=['trigger_condition']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"{self.name} ({self.get_trigger_condition_display()})"