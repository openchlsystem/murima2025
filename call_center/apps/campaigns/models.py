# apps/campaigns/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils import timezone
from apps.core.models import TimeStampedModel, SoftDeleteModel
import uuid
from datetime import datetime, timedelta


class CampaignManager(models.Manager):
    """Custom manager for Campaign model"""
    
    def active(self):
        """Get active campaigns"""
        return self.filter(status='active', is_active=True)
    
    def by_type(self, campaign_type):
        """Get campaigns by type"""
        return self.filter(campaign_type=campaign_type)
    
    def current(self):
        """Get campaigns that are currently running"""
        now = timezone.now()
        return self.filter(
            start_date__lte=now,
            end_date__gte=now,
            status='active'
        )
    
    def scheduled(self):
        """Get campaigns scheduled for future"""
        return self.filter(start_date__gt=timezone.now(), status='scheduled')
    
    def completed(self):
        """Get completed campaigns"""
        return self.filter(status='completed')


class Campaign(SoftDeleteModel):
    """
    Campaign model for managing outbound calling campaigns and inbound queues.
    Maps to legacy campaign table.
    """
    
    CAMPAIGN_TYPES = [
        ('outbound', _('Outbound Campaign')),
        ('inbound', _('Inbound Queue')),
        ('blended', _('Blended Campaign')),
        ('preview', _('Preview Dialing')),
        ('predictive', _('Predictive Dialing')),
        ('progressive', _('Progressive Dialing')),
    ]
    
    CAMPAIGN_STATUSES = [
        ('draft', _('Draft')),
        ('scheduled', _('Scheduled')),
        ('active', _('Active')),
        ('paused', _('Paused')),
        ('completed', _('Completed')),
        ('cancelled', _('Cancelled')),
    ]
    
    RING_STRATEGIES = [
        ('rrmemory', _('Round Robin with Memory')),
        ('roundrobin', _('Round Robin')),
        ('leastrecent', _('Least Recent')),
        ('fewestcalls', _('Fewest Calls')),
        ('random', _('Random')),
        ('linear', _('Linear')),
    ]
    
    # Core Campaign Information
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, db_index=True)
    name = models.CharField(
        max_length=255,
        db_index=True,
        verbose_name=_("Campaign Name"),
        help_text=_("Unique name for the campaign")
    )
    description = models.TextField(
        blank=True,
        verbose_name=_("Description"),
        help_text=_("Campaign description and objectives")
    )
    
    # Campaign Type and Configuration
    campaign_type = models.CharField(
        max_length=20,
        choices=CAMPAIGN_TYPES,
        default='inbound',
        verbose_name=_("Campaign Type")
    )
    status = models.CharField(
        max_length=20,
        choices=CAMPAIGN_STATUSES,
        default='draft',
        db_index=True,
        verbose_name=_("Status")
    )
    
    # Queue Configuration (for Asterisk)
    queue_name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_("Queue Name"),
        help_text=_("Asterisk queue name (must be unique)")
    )
    caller_id = models.CharField(
        max_length=50,
        verbose_name=_("Caller ID"),
        help_text=_("Caller ID to display for outbound calls")
    )
    
    # Agent Management
    ring_strategy = models.CharField(
        max_length=20,
        choices=RING_STRATEGIES,
        default='rrmemory',
        verbose_name=_("Ring Strategy"),
        help_text=_("How to distribute calls to agents")
    )
    max_agents = models.PositiveIntegerField(
        default=10,
        verbose_name=_("Maximum Agents"),
        help_text=_("Maximum number of agents in this campaign")
    )
    ring_timeout = models.PositiveIntegerField(
        default=30,
        verbose_name=_("Ring Timeout (seconds)"),
        help_text=_("How long to ring each agent")
    )
    wrapup_time = models.PositiveIntegerField(
        default=60,
        verbose_name=_("Wrapup Time (seconds)"),
        help_text=_("Time for agent to complete call tasks")
    )
    
    # Campaign Schedule
    start_date = models.DateTimeField(
        verbose_name=_("Start Date"),
        help_text=_("When the campaign should start")
    )
    end_date = models.DateTimeField(
        verbose_name=_("End Date"),
        help_text=_("When the campaign should end")
    )
    working_hours = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("Working Hours"),
        help_text=_("Schedule configuration for the campaign")
    )
    
    # IVR and Voice Configuration
    voice_prompt = models.ForeignKey(
        'core.ReferenceData',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'category': 'voice_prompt'},
        related_name='campaigns_using_prompt',
        verbose_name=_("Voice Prompt"),
        help_text=_("IVR voice prompt for this campaign")
    )
    
    # Category and Classification
    category = models.ForeignKey(
        'core.ReferenceData',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'category': 'campaign_category'},
        related_name='campaigns_by_category',
        verbose_name=_("Campaign Category")
    )
    
    # Performance Targets and Metrics
    target_contacts = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Target Contacts"),
        help_text=_("Number of contacts to reach in this campaign")
    )
    contacts_attempted = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Contacts Attempted"),
        help_text=_("Number of contacts attempted so far")
    )
    contacts_reached = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Contacts Reached"),
        help_text=_("Number of contacts successfully reached")
    )
    
    # SLA Targets
    sla_target_answer = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name=_("SLA Answer Target (seconds)"),
        help_text=_("Target time to answer calls")
    )
    sla_target_abandon = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name=_("SLA Abandon Target (seconds)"),
        help_text=_("Target time before call abandonment")
    )
    
    # Outbound Campaign Settings
    retry_attempts = models.PositiveIntegerField(
        default=3,
        verbose_name=_("Retry Attempts"),
        help_text=_("Maximum retry attempts for outbound calls")
    )
    retry_interval = models.PositiveIntegerField(
        default=3600,  # 1 hour
        verbose_name=_("Retry Interval (seconds)"),
        help_text=_("Time between retry attempts")
    )
    
    # Performance Metrics (calculated fields)
    total_calls = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Total Calls"),
        help_text=_("Total number of calls in this campaign")
    )
    answered_calls = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Answered Calls")
    )
    abandoned_calls = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Abandoned Calls")
    )
    
    # Timing Statistics
    avg_talk_time = models.DurationField(
        null=True,
        blank=True,
        verbose_name=_("Average Talk Time")
    )
    avg_wait_time = models.DurationField(
        null=True,
        blank=True,
        verbose_name=_("Average Wait Time")
    )
    avg_hold_time = models.DurationField(
        null=True,
        blank=True,
        verbose_name=_("Average Hold Time")
    )
    
    # SLA Performance
    sla_compliance_rate = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_("SLA Compliance Rate"),
        help_text=_("Percentage of calls meeting SLA targets")
    )
    
    # Migration Helper Fields
    legacy_campaign_id = models.IntegerField(
        null=True,
        blank=True,
        db_index=True,
        verbose_name=_("Legacy Campaign ID"),
        help_text=_("Original campaign table ID")
    )
    legacy_data = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("Legacy Data"),
        help_text=_("Original campaign data for migration tracking")
    )
    
    # Manager
    objects = CampaignManager()
    
    class Meta:
        verbose_name = _("Campaign")
        verbose_name_plural = _("Campaigns")
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['queue_name']),
            models.Index(fields=['status', 'campaign_type']),
            models.Index(fields=['start_date', 'end_date']),
            models.Index(fields=['legacy_campaign_id']),
            models.Index(fields=['is_active', 'status']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.get_campaign_type_display()})"
    
    def clean(self):
        """Validate campaign data"""
        super().clean()
        
        # Validate date range
        if self.start_date and self.end_date:
            if self.start_date >= self.end_date:
                raise ValidationError(_("End date must be after start date"))
        
        # Validate queue name format (Asterisk compatible)
        if self.queue_name:
            import re
            if not re.match(r'^[a-zA-Z0-9_-]+, self.queue_name'):
                raise ValidationError(_("Queue name can only contain letters, numbers, underscores, and hyphens"))
    
    def save(self, *args, **kwargs):
        """Override save to handle auto-calculations"""
        # Auto-generate queue name if not provided
        if not self.queue_name and self.name:
            import re
            queue_name = re.sub(r'[^a-zA-Z0-9_-]', '_', self.name.lower())
            queue_name = re.sub(r'_+', '_', queue_name).strip('_')
            self.queue_name = queue_name[:50]  # Limit length
        
        super().save(*args, **kwargs)
    
    @property
    def is_current(self):
        """Check if campaign is currently running"""
        now = timezone.now()
        return (
            self.status == 'active' and
            self.start_date <= now <= self.end_date
        )
    
    @property
    def progress_percentage(self):
        """Calculate campaign progress percentage"""
        if self.target_contacts > 0:
            return (self.contacts_attempted / self.target_contacts) * 100
        return 0
    
    @property
    def success_rate(self):
        """Calculate success rate (reached/attempted)"""
        if self.contacts_attempted > 0:
            return (self.contacts_reached / self.contacts_attempted) * 100
        return 0
    
    @property
    def answer_rate(self):
        """Calculate answer rate"""
        if self.total_calls > 0:
            return (self.answered_calls / self.total_calls) * 100
        return 0
    
    @property
    def abandon_rate(self):
        """Calculate abandon rate"""
        if self.total_calls > 0:
            return (self.abandoned_calls / self.total_calls) * 100
        return 0
    
    def get_current_agents(self):
        """Get currently assigned agents"""
        return self.members.filter(is_active=True).select_related('agent')
    
    def get_agent_count(self):
        """Get number of active agents"""
        return self.members.filter(is_active=True).count()
    
    def can_add_agent(self):
        """Check if more agents can be added"""
        return self.get_agent_count() < self.max_agents
    
    def update_statistics(self):
        """Update campaign statistics from related calls"""
        from django.db.models import Count, Avg, Q
        
        # Import here to avoid circular imports
        try:
            from apps.calls.models import Call
            calls = Call.objects.filter(campaign=self)
            
            # Update call counts
            self.total_calls = calls.count()
            self.answered_calls = calls.filter(call_status__in=['answered', 'completed']).count()
            self.abandoned_calls = calls.filter(call_status='abandoned').count()
            
            # Calculate averages
            stats = calls.aggregate(
                avg_talk=Avg('talk_duration'),
                avg_wait=Avg('wait_duration'),
                avg_hold=Avg('hold_duration')
            )
            
            self.avg_talk_time = stats['avg_talk']
            self.avg_wait_time = stats['avg_wait']
            self.avg_hold_time = stats['avg_hold']
            
            # Calculate SLA compliance
            if self.sla_target_answer:
                sla_met_calls = calls.filter(sla_met=True).count()
                if self.total_calls > 0:
                    self.sla_compliance_rate = (sla_met_calls / self.total_calls) * 100
            
            self.save(update_fields=[
                'total_calls', 'answered_calls', 'abandoned_calls',
                'avg_talk_time', 'avg_wait_time', 'avg_hold_time',
                'sla_compliance_rate'
            ])
        except ImportError:
            # Calls app not ready yet
            pass


class CampaignMember(TimeStampedModel):
    """
    Agent assignments to campaigns.
    Tracks which agents are assigned to which campaigns and their performance.
    """
    
    MEMBER_ROLES = [
        ('agent', _('Agent')),
        ('supervisor', _('Supervisor')),
        ('team_lead', _('Team Lead')),
        ('quality_analyst', _('Quality Analyst')),
    ]
    
    campaign = models.ForeignKey(
        Campaign,
        on_delete=models.CASCADE,
        related_name='members',
        verbose_name=_("Campaign")
    )
    agent = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='campaign_memberships',
        verbose_name=_("Agent")
    )
    role = models.CharField(
        max_length=20,
        choices=MEMBER_ROLES,
        default='agent',
        verbose_name=_("Role")
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Is Active"),
        help_text=_("Whether this agent is currently active in the campaign")
    )
    
    # Assignment period
    assigned_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Assigned Date")
    )
    unassigned_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Unassigned Date")
    )
    
    # Performance tracking
    calls_handled = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Calls Handled"),
        help_text=_("Number of calls handled by this agent in this campaign")
    )
    calls_answered = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Calls Answered")
    )
    calls_successful = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Successful Calls"),
        help_text=_("Calls that resulted in successful outcomes")
    )
    
    # Time tracking
    total_talk_time = models.DurationField(
        null=True,
        blank=True,
        verbose_name=_("Total Talk Time")
    )
    avg_talk_time = models.DurationField(
        null=True,
        blank=True,
        verbose_name=_("Average Talk Time")
    )
    
    # Quality metrics
    quality_score = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_("Quality Score"),
        help_text=_("Average quality score for this agent in this campaign")
    )
    
    class Meta:
        verbose_name = _("Campaign Member")
        verbose_name_plural = _("Campaign Members")
        unique_together = ['campaign', 'agent']
        ordering = ['-assigned_date']
        indexes = [
            models.Index(fields=['campaign', 'is_active']),
            models.Index(fields=['agent', 'is_active']),
            models.Index(fields=['role', 'is_active']),
        ]
    
    def __str__(self):
        return f"{self.agent.get_full_name()} in {self.campaign.name}"
    
    @property
    def success_rate(self):
        """Calculate success rate for this agent in this campaign"""
        if self.calls_handled > 0:
            return (self.calls_successful / self.calls_handled) * 100
        return 0
    
    @property
    def answer_rate(self):
        """Calculate answer rate for this agent in this campaign"""
        if self.calls_handled > 0:
            return (self.calls_answered / self.calls_handled) * 100
        return 0
    
    def update_statistics(self):
        """Update agent statistics for this campaign"""
        from django.db.models import Count, Avg, Sum
        
        try:
            from apps.calls.models import Call
            calls = Call.objects.filter(campaign=self.campaign, agent=self.agent)
            
            # Update call counts
            self.calls_handled = calls.count()
            self.calls_answered = calls.filter(call_status__in=['answered', 'completed']).count()
            
            # Calculate time statistics
            time_stats = calls.aggregate(
                total_talk=Sum('talk_duration'),
                avg_talk=Avg('talk_duration')
            )
            
            self.total_talk_time = time_stats['total_talk']
            self.avg_talk_time = time_stats['avg_talk']
            
            # Calculate quality score
            qa_scores = calls.filter(
                quality_assessment__isnull=False
            ).aggregate(avg_quality=Avg('quality_assessment__overall_score'))
            
            self.quality_score = qa_scores['avg_quality']
            
            self.save(update_fields=[
                'calls_handled', 'calls_answered', 'calls_successful',
                'total_talk_time', 'avg_talk_time', 'quality_score'
            ])
        except ImportError:
            # Calls app not ready yet
            pass


class CampaignContact(TimeStampedModel):
    """
    Contacts assigned to outbound campaigns for calling.
    Tracks calling history and status for each contact in each campaign.
    """
    
    CONTACT_STATUSES = [
        ('pending', _('Pending')),
        ('attempted', _('Attempted')),
        ('contacted', _('Contacted')),
        ('completed', _('Completed')),
        ('do_not_call', _('Do Not Call')),
        ('invalid', _('Invalid')),
    ]
    
    campaign = models.ForeignKey(
        Campaign,
        on_delete=models.CASCADE,
        related_name='campaign_contacts',
        verbose_name=_("Campaign")
    )
    
    contact = models.ForeignKey(
        'contacts.Contact',
        on_delete=models.CASCADE,
        related_name='campaign_assignments',
        verbose_name=_("Contact")
    )
    
    # Contact status in this campaign
    status = models.CharField(
        max_length=20,
        choices=CONTACT_STATUSES,
        default='pending',
        db_index=True,
        verbose_name=_("Status")
    )
    priority = models.PositiveSmallIntegerField(
        default=1,
        verbose_name=_("Priority"),
        help_text=_("Priority level (1=highest, 5=lowest)")
    )
    
    # Attempt tracking
    attempts_made = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Attempts Made")
    )
    max_attempts = models.PositiveIntegerField(
        default=3,
        verbose_name=_("Maximum Attempts")
    )
    last_attempt = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Last Attempt")
    )
    next_attempt = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Next Attempt"),
        help_text=_("Scheduled time for next attempt")
    )
    
    # Assignment
    assigned_agent = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Assigned Agent")
    )
    
    # Results
    result = models.ForeignKey(
        'core.ReferenceData',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'category': 'call_result'},
        verbose_name=_("Call Result")
    )
    notes = models.TextField(
        blank=True,
        verbose_name=_("Notes"),
        help_text=_("Notes about this contact in this campaign")
    )
    
    class Meta:
        verbose_name = _("Campaign Contact")
        verbose_name_plural = _("Campaign Contacts")
        unique_together = ['campaign', 'contact']
        ordering = ['priority', 'next_attempt']
        indexes = [
            models.Index(fields=['campaign', 'status']),
            models.Index(fields=['status', 'next_attempt']),
            models.Index(fields=['assigned_agent', 'status']),
            models.Index(fields=['priority', 'next_attempt']),
        ]
    
    def __str__(self):
        return f"{self.contact.full_name} in {self.campaign.name}"
    
    @property
    def can_attempt(self):
        """Check if contact can be attempted again"""
        return (
            self.status in ['pending', 'attempted'] and
            self.attempts_made < self.max_attempts
        )
    
    @property
    def is_overdue(self):
        """Check if contact attempt is overdue"""
        return (
            self.next_attempt and
            self.next_attempt < timezone.now() and
            self.can_attempt
        )
    
    def schedule_next_attempt(self, delay_minutes=None):
        """Schedule the next attempt for this contact"""
        if delay_minutes is None:
            # Use campaign's retry interval
            delay_minutes = self.campaign.retry_interval // 60
        
        self.next_attempt = timezone.now() + timedelta(minutes=delay_minutes)
        self.save(update_fields=['next_attempt'])
    
    def record_attempt(self, result=None, agent=None, notes=''):
        """Record an attempt for this contact"""
        self.attempts_made += 1
        self.last_attempt = timezone.now()
        self.status = 'attempted'
        
        if result:
            self.result = result
        if agent:
            self.assigned_agent = agent
        if notes:
            self.notes = notes
        
        # Schedule next attempt if more attempts allowed
        if self.can_attempt:
            self.schedule_next_attempt()
        
        self.save()


# Signal handlers
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

@receiver(post_save, sender=CampaignMember)
def campaign_member_post_save(sender, instance, created, **kwargs):
    """Update campaign member count when member is added/changed"""
    if created or not instance.is_active:
        # Update campaign statistics
        instance.campaign.save()  # This will trigger recalculation if needed

@receiver(post_delete, sender=CampaignMember)
def campaign_member_post_delete(sender, instance, **kwargs):
    """Update campaign when member is removed"""
    instance.campaign.save()  # Trigger recalculation