# apps/calls/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from apps.core.models import TimeStampedModel, SoftDeleteModel, UUIDModel
import uuid
from datetime import timedelta


class CallManager(models.Manager):
    """Custom manager for Call model with common queries"""
    
    def inbound(self):
        """Get inbound calls"""
        return self.filter(call_direction='inbound')
    
    def outbound(self):
        """Get outbound calls"""
        return self.filter(call_direction='outbound')
    
    def answered(self):
        """Get answered calls"""
        return self.filter(call_status__in=['answered', 'completed'])
    
    def abandoned(self):
        """Get abandoned calls"""
        return self.filter(call_status='abandoned')
    
    def today(self):
        """Get today's calls"""
        today = timezone.now().date()
        return self.filter(start_time__date=today)
    
    def by_agent(self, user):
        """Get calls handled by specific agent"""
        return self.filter(agent=user)
    
    def by_campaign(self, campaign):
        """Get calls for specific campaign"""
        return self.filter(campaign=campaign)
    
    def with_recordings(self):
        """Get calls that have recordings"""
        return self.filter(recording_file__isnull=False).exclude(recording_file='')
    
    def by_date_range(self, start_date, end_date):
        """Get calls within date range"""
        return self.filter(start_time__date__range=[start_date, end_date])


class Call(TimeStampedModel):
    """
    Unified call tracking model for both inbound and outbound calls.
    Maps to legacy 'chan' table with modern structure.
    """
    
    # Call Direction Choices
    CALL_DIRECTIONS = [
        ('inbound', _('Inbound')),
        ('outbound', _('Outbound')),
        ('internal', _('Internal')),
    ]
    
    # Call Status Choices  
    CALL_STATUSES = [
        ('ringing', _('Ringing')),
        ('answered', _('Answered')),
        ('busy', _('Busy')),
        ('no_answer', _('No Answer')),
        ('failed', _('Failed')),
        ('abandoned', _('Abandoned')),
        ('completed', _('Completed')),
        ('transferred', _('Transferred')),
        ('conference', _('Conference')),
        ('hold', _('On Hold')),
    ]
    
    # Hangup Reason Choices (mapped from legacy hangup_reason codes)
    HANGUP_REASONS = [
        ('normal', _('Normal Hangup')),
        ('busy', _('Busy')),
        ('noanswer', _('No Answer')),
        ('cancel', _('Cancelled')),
        ('congestion', _('Congestion')),
        ('chanunavail', _('Channel Unavailable')),
        ('timeout', _('Timeout')),
        ('rejected', _('Rejected')),
        ('unallocated', _('Unallocated Number')),
        ('normal_clearing', _('Normal Clearing')),
        ('user_busy', _('User Busy')),
        ('no_user_response', _('No User Response')),
        ('no_answer', _('No Answer')),
        ('subscriber_absent', _('Subscriber Absent')),
        ('call_rejected', _('Call Rejected')),
        ('number_changed', _('Number Changed')),
        ('destination_out_of_order', _('Destination Out of Order')),
        ('invalid_number_format', _('Invalid Number Format')),
        ('facility_rejected', _('Facility Rejected')),
        ('response_to_status_enquiry', _('Response to Status Enquiry')),
        ('normal_unspecified', _('Normal Unspecified')),
        ('normal_circuit_congestion', _('Normal Circuit Congestion')),
        ('network_out_of_order', _('Network Out of Order')),
        ('normal_temporary_failure', _('Normal Temporary Failure')),
        ('switch_congestion', _('Switch Congestion')),
        ('access_info_discarded', _('Access Info Discarded')),
        ('requested_chan_unavail', _('Requested Channel Unavailable')),
        ('pre_empted', _('Pre-empted')),
        ('facility_not_subscribed', _('Facility Not Subscribed')),
        ('outgoing_call_barred', _('Outgoing Call Barred')),
        ('incoming_call_barred', _('Incoming Call Barred')),
        ('bearercapability_notauth', _('Bearer Capability Not Authorized')),
        ('bearercapability_notavail', _('Bearer Capability Not Available')),
        ('bearercapability_notimpl', _('Bearer Capability Not Implemented')),
        ('chan_not_implemented', _('Channel Not Implemented')),
        ('facility_not_implemented', _('Facility Not Implemented')),
        ('invalid_call_reference', _('Invalid Call Reference')),
        ('incompatible_destination', _('Incompatible Destination')),
        ('invalid_msg_unspecified', _('Invalid Message Unspecified')),
        ('mandatory_ie_missing', _('Mandatory IE Missing')),
        ('message_type_nonexist', _('Message Type Non-existent')),
        ('wrong_message', _('Wrong Message')),
        ('ie_nonexist', _('IE Non-existent')),
        ('invalid_ie_contents', _('Invalid IE Contents')),
        ('wrong_call_state', _('Wrong Call State')),
        ('recovery_on_timer_expire', _('Recovery on Timer Expire')),
        ('mandatory_ie_length_error', _('Mandatory IE Length Error')),
        ('protocol_error', _('Protocol Error')),
        ('interworking', _('Interworking')),
        ('other', _('Other')),
    ]
    
    # Vector/Direction mapping from legacy system
    VECTOR_CHOICES = [
        ('0', _('Outbound')),
        ('1', _('Inbound')),
        ('2', _('Internal')),
    ]
    
    # Core Call Identification
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, db_index=True)
    unique_id = models.CharField(
        max_length=255, 
        unique=True, 
        db_index=True,
        verbose_name=_("Unique ID"),
        help_text=_("Asterisk unique call identifier")
    )
    
    # Call Numbers
    caller_number = models.CharField(
        max_length=50, 
        db_index=True,
        verbose_name=_("Caller Number"),
        help_text=_("Phone number of the caller")
    )
    caller_name = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Caller Name"),
        help_text=_("Caller ID name if available")
    )
    called_number = models.CharField(
        max_length=50,
        verbose_name=_("Called Number"),
        help_text=_("Phone number that was called")
    )
    
    # Call Direction and Type
    call_direction = models.CharField(
        max_length=10,
        choices=CALL_DIRECTIONS,
        db_index=True,
        verbose_name=_("Call Direction")
    )
    
    # Legacy vector field for migration compatibility
    vector = models.CharField(
        max_length=2,
        choices=VECTOR_CHOICES,
        blank=True,
        verbose_name=_("Vector (Legacy)"),
        help_text=_("Legacy direction indicator - to be removed post-migration")
    )
    
    # Contact Association - Commented out until contacts app is ready
    contact = models.ForeignKey(
        'contacts.Contact',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='calls',
        verbose_name=_("Contact"),
        help_text=_("Associated contact record")
    )
    
    # Campaign Association - Commented out until campaigns app is ready
    campaign = models.ForeignKey(
        'campaigns.Campaign',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='calls',
        verbose_name=_("Campaign"),
        help_text=_("Associated campaign if outbound call")
    )
    
    # Agent Assignment
    agent = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='handled_calls',
        verbose_name=_("Agent"),
        help_text=_("Agent who handled the call")
    )
    
    # Secondary agent for transfers/conferences
    secondary_agent = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='secondary_calls',
        verbose_name=_("Secondary Agent"),
        help_text=_("Second agent involved in call (transfers, conferences)")
    )
    
    # Case Association - Commented out until cases app is ready
    # case = models.ForeignKey(
    #     'cases.Case',
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     blank=True,
    #     related_name='calls',
    #     verbose_name=_("Case"),
    #     help_text=_("Associated case if call resulted in case creation")
    # )
    
    # Call Timing
    start_time = models.DateTimeField(
        db_index=True,
        verbose_name=_("Start Time"),
        help_text=_("When the call was initiated")
    )
    answer_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Answer Time"),
        help_text=_("When the call was answered")
    )
    end_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("End Time"),
        help_text=_("When the call ended")
    )
    
    # Duration Fields (calculated from timestamps)
    ring_duration = models.DurationField(
        null=True,
        blank=True,
        verbose_name=_("Ring Duration"),
        help_text=_("Time from start to answer")
    )
    talk_duration = models.DurationField(
        null=True,
        blank=True,
        verbose_name=_("Talk Duration"),
        help_text=_("Time spent talking")
    )
    hold_duration = models.DurationField(
        null=True,
        blank=True,
        verbose_name=_("Hold Duration"),
        help_text=_("Total time on hold")
    )
    wait_duration = models.DurationField(
        null=True,
        blank=True,
        verbose_name=_("Wait Duration"),
        help_text=_("Time waiting in queue")
    )
    total_duration = models.DurationField(
        null=True,
        blank=True,
        verbose_name=_("Total Duration"),
        help_text=_("Total call duration from start to end")
    )
    
    # Call Status and Outcome
    call_status = models.CharField(
        max_length=20,
        choices=CALL_STATUSES,
        default='ringing',
        db_index=True,
        verbose_name=_("Call Status")
    )
    hangup_reason = models.CharField(
        max_length=50,
        choices=HANGUP_REASONS,
        blank=True,
        verbose_name=_("Hangup Reason")
    )
    
    # Quality Metrics
    audio_quality_score = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_("Audio Quality Score"),
        help_text=_("Audio quality score (0.0 to 10.0)")
    )
    
    # Technical Details
    trunk = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_("Trunk"),
        help_text=_("Trunk used for the call")
    )
    channel = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Channel"),
        help_text=_("Asterisk channel identifier")
    )
    context = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Context"),
        help_text=_("Asterisk dialplan context")
    )
    extension = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Extension"),
        help_text=_("Extension dialed")
    )
    
    # Bridge Information (for transfers/conferences)
    bridge_id = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Bridge ID"),
        help_text=_("Asterisk bridge identifier")
    )
    peer_channel = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Peer Channel"),
        help_text=_("Connected peer channel")
    )
    
    # Recording Information
    recording_file = models.CharField(
        max_length=500,
        blank=True,
        verbose_name=_("Recording File"),
        help_text=_("Path to call recording file")
    )
    recording_duration = models.DurationField(
        null=True,
        blank=True,
        verbose_name=_("Recording Duration")
    )
    
    # SLA and Performance Metrics
    sla_target_answer = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name=_("SLA Target Answer (seconds)"),
        help_text=_("Target time to answer for SLA")
    )
    sla_target_abandon = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name=_("SLA Target Abandon (seconds)"),
        help_text=_("Target time before abandon for SLA")
    )
    sla_met = models.BooleanField(
        null=True,
        blank=True,
        verbose_name=_("SLA Met"),
        help_text=_("Whether call met SLA targets")
    )
    
    # Date-based fields for reporting (calculated)
    call_date = models.DateField(
        db_index=True,
        verbose_name=_("Call Date"),
        help_text=_("Date of the call (for reporting)")
    )
    call_hour = models.PositiveSmallIntegerField(
        verbose_name=_("Call Hour"),
        help_text=_("Hour of the call (0-23)")
    )
    call_day_of_week = models.PositiveSmallIntegerField(
        verbose_name=_("Day of Week"),
        help_text=_("Day of week (0=Monday, 6=Sunday)")
    )
    
    # AI Enhancement Fields
    ai_transcript = models.TextField(
        blank=True,
        verbose_name=_("AI Transcript"),
        help_text=_("AI-generated call transcript")
    )
    ai_sentiment_score = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_("AI Sentiment Score"),
        help_text=_("AI-analyzed sentiment score (-1.0 to 1.0)")
    )
    ai_summary = models.TextField(
        blank=True,
        verbose_name=_("AI Summary"),
        help_text=_("AI-generated call summary")
    )
    ai_categories = models.JSONField(
        default=list,
        blank=True,
        verbose_name=_("AI Categories"),
        help_text=_("AI-suggested categories for the call")
    )
    ai_keywords = models.JSONField(
        default=list,
        blank=True,
        verbose_name=_("AI Keywords"),
        help_text=_("AI-extracted keywords from the call")
    )
    ai_analysis_completed = models.BooleanField(
        default=False,
        verbose_name=_("AI Analysis Completed"),
        help_text=_("Whether AI analysis has been completed")
    )
    ai_analysis_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("AI Analysis Date"),
        help_text=_("When AI analysis was completed")
    )
    
    # Migration Helper Fields (to be removed post-migration)
    legacy_chan_id = models.IntegerField(
        null=True,
        blank=True,
        db_index=True,
        verbose_name=_("Legacy Channel ID"),
        help_text=_("Original chan table ID - for migration tracking")
    )
    legacy_uniqueid2 = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_("Legacy Unique ID 2"),
        help_text=_("Legacy uid2 field - for migration tracking")
    )
    legacy_call_data = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("Legacy Call Data"),
        help_text=_("Original call data for migration verification")
    )
    migration_notes = models.TextField(
        blank=True,
        verbose_name=_("Migration Notes"),
        help_text=_("Notes about migration process or issues")
    )
    migration_verified = models.BooleanField(
        default=False,
        verbose_name=_("Migration Verified"),
        help_text=_("Whether migration data has been verified")
    )
    
    # Manager
    objects = CallManager()
    
    class Meta:
        verbose_name = _("Call")
        verbose_name_plural = _("Calls")
        ordering = ['-start_time']
        indexes = [
            # Primary lookup indexes
            models.Index(fields=['unique_id']),
            models.Index(fields=['caller_number', '-start_time']),
            models.Index(fields=['called_number', '-start_time']),
            models.Index(fields=['call_direction', '-start_time']),
            models.Index(fields=['call_status', '-start_time']),
            models.Index(fields=['agent', '-start_time']),
            models.Index(fields=['campaign', '-start_time']),
            models.Index(fields=['contact', '-start_time']),
            # models.Index(fields=['case', '-start_time']),
            
            # Date-based indexes for reporting
            models.Index(fields=['call_date', 'call_direction']),
            models.Index(fields=['call_date', 'agent']),
            models.Index(fields=['call_date', 'campaign']),
            models.Index(fields=['call_hour', 'call_date']),
            
            # Performance indexes
            models.Index(fields=['sla_met', 'call_date']),
            models.Index(fields=['call_status', 'call_date']),
            models.Index(fields=['hangup_reason', 'call_date']),
            
            # Migration indexes (to be removed)
            models.Index(fields=['legacy_chan_id']),
            models.Index(fields=['migration_verified']),
            
            # AI analysis indexes
            models.Index(fields=['ai_analysis_completed', '-start_time']),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(audio_quality_score__gte=0.0) & models.Q(audio_quality_score__lte=10.0),
                name='valid_audio_quality_score'
            ),
            models.CheckConstraint(
                check=models.Q(ai_sentiment_score__gte=-1.0) & models.Q(ai_sentiment_score__lte=1.0),
                name='valid_sentiment_score'
            ),
        ]
    
    def __str__(self):
        return f"Call {self.unique_id}: {self.caller_number} -> {self.called_number}"
    
    def save(self, *args, **kwargs):
        """Override save to calculate derived fields"""
        if self.start_time:
            # Set date-based fields
            self.call_date = self.start_time.date()
            self.call_hour = self.start_time.hour
            self.call_day_of_week = self.start_time.weekday()
        
        # Calculate durations if we have the timestamps
        if self.start_time and self.answer_time:
            self.ring_duration = self.answer_time - self.start_time
        
        if self.start_time and self.end_time:
            self.total_duration = self.end_time - self.start_time
            
        if self.answer_time and self.end_time:
            # Talk time is total minus any hold time
            base_talk_time = self.end_time - self.answer_time
            if self.hold_duration:
                self.talk_duration = base_talk_time - self.hold_duration
            else:
                self.talk_duration = base_talk_time
        
        # Map vector to call_direction for legacy compatibility
        if self.vector and not self.call_direction:
            vector_mapping = {
                '0': 'outbound',
                '1': 'inbound', 
                '2': 'internal'
            }
            self.call_direction = vector_mapping.get(self.vector, 'inbound')
        
        # Calculate SLA compliance if targets are set
        if self.sla_target_answer and self.ring_duration:
            self.sla_met = self.ring_duration.total_seconds() <= self.sla_target_answer
        
        super().save(*args, **kwargs)
    
    @property
    def duration_seconds(self):
        """Get total duration in seconds"""
        return self.total_duration.total_seconds() if self.total_duration else 0
    
    @property
    def is_answered(self):
        """Check if call was answered"""
        return self.call_status in ['answered', 'completed']
    
    @property
    def is_abandoned(self):
        """Check if call was abandoned"""
        return self.call_status == 'abandoned'
    
    @property
    def has_recording(self):
        """Check if call has a recording"""
        return bool(self.recording_file)
    
    def calculate_cost(self, rate_per_minute=0.0):
        """Calculate call cost based on duration and rate"""
        if self.talk_duration:
            minutes = self.talk_duration.total_seconds() / 60
            return round(minutes * rate_per_minute, 2)
        return 0.0
    
    def get_quality_metrics(self):
        """Get call quality metrics"""
        return {
            'audio_quality': self.audio_quality_score,
            'sla_met': self.sla_met,
            'answered': self.is_answered,
            'abandoned': self.is_abandoned,
            'duration': self.duration_seconds,
            'sentiment': self.ai_sentiment_score,
        }


class CallEvent(TimeStampedModel):
    """
    Track specific events during a call (hold, transfer, mute, etc.)
    This provides detailed call flow tracking.
    """
    
    EVENT_TYPES = [
        ('dial', _('Dial')),
        ('ring', _('Ring')),
        ('answer', _('Answer')),
        ('hold', _('Hold')),
        ('unhold', _('Unhold')),
        ('mute', _('Mute')),
        ('unmute', _('Unmute')),
        ('transfer', _('Transfer')),
        ('conference', _('Conference')),
        ('hangup', _('Hangup')),
        ('bridge', _('Bridge')),
        ('unbridge', _('Unbridge')),
        ('queue_join', _('Queue Join')),
        ('queue_leave', _('Queue Leave')),
        ('agent_connect', _('Agent Connect')),
        ('ivr_menu', _('IVR Menu')),
        ('dtmf', _('DTMF Input')),
        ('recording_start', _('Recording Start')),
        ('recording_stop', _('Recording Stop')),
    ]
    
    call = models.ForeignKey(
        Call,
        on_delete=models.CASCADE,
        related_name='events',
        verbose_name=_("Call")
    )
    event_type = models.CharField(
        max_length=20,
        choices=EVENT_TYPES,
        verbose_name=_("Event Type")
    )
    event_time = models.DateTimeField(
        verbose_name=_("Event Time"),
        help_text=_("When this event occurred")
    )
    description = models.TextField(
        blank=True,
        verbose_name=_("Description"),
        help_text=_("Additional event details")
    )
    data = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("Event Data"),
        help_text=_("Additional structured data for the event")
    )
    
    # Agent involved in this event
    agent = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Agent"),
        help_text=_("Agent involved in this event")
    )
    
    class Meta:
        verbose_name = _("Call Event")
        verbose_name_plural = _("Call Events")
        ordering = ['call', 'event_time']
        indexes = [
            models.Index(fields=['call', 'event_time']),
            models.Index(fields=['event_type', 'event_time']),
            models.Index(fields=['agent', 'event_time']),
        ]
    
    def __str__(self):
        return f"{self.call.unique_id}: {self.get_event_type_display()} at {self.event_time}"


class CallDisposition(TimeStampedModel):
    """
    Call outcome and disposition tracking.
    Maps to legacy disposition system.
    """
    
    call = models.OneToOneField(
        Call,
        on_delete=models.CASCADE,
        related_name='disposition',
        verbose_name=_("Call")
    )
    
    # Disposition from reference data
    disposition = models.ForeignKey(
        'core.ReferenceData',
        on_delete=models.PROTECT,
        limit_choices_to={'category': 'disposition'},
        verbose_name=_("Disposition"),
        help_text=_("Call outcome disposition")
    )
    
    # Additional notes
    notes = models.TextField(
        blank=True,
        verbose_name=_("Notes"),
        help_text=_("Additional disposition notes")
    )
    
    # Outcome tracking
    case_created = models.BooleanField(
        default=False,
        verbose_name=_("Case Created"),
        help_text=_("Whether this call resulted in a case")
    )
    follow_up_required = models.BooleanField(
        default=False,
        verbose_name=_("Follow-up Required")
    )
    follow_up_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Follow-up Date")
    )
    callback_requested = models.BooleanField(
        default=False,
        verbose_name=_("Callback Requested")
    )
    callback_number = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_("Callback Number")
    )
    
    # AI Enhancement
    ai_suggested_disposition = models.ForeignKey(
        'core.ReferenceData',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'category': 'disposition'},
        related_name='ai_suggested_dispositions',
        verbose_name=_("AI Suggested Disposition"),
        help_text=_("AI-suggested disposition")
    )
    ai_confidence_score = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_("AI Confidence Score"),
        help_text=_("Confidence score for AI suggestion (0.0 to 1.0)")
    )
    
    # Migration tracking
    legacy_disposition_id = models.IntegerField(
        null=True,
        blank=True,
        db_index=True,
        verbose_name=_("Legacy Disposition ID"),
        help_text=_("Original disposition table ID")
    )
    
    class Meta:
        verbose_name = _("Call Disposition")
        verbose_name_plural = _("Call Dispositions")
        indexes = [
            models.Index(fields=['disposition', '-created_at']),
            models.Index(fields=['case_created', '-created_at']),
            models.Index(fields=['follow_up_required', 'follow_up_date']),
            models.Index(fields=['callback_requested', '-created_at']),
            models.Index(fields=['legacy_disposition_id']),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(ai_confidence_score__gte=0.0) & models.Q(ai_confidence_score__lte=1.0),
                name='valid_ai_confidence_score'
            ),
        ]
    
    def __str__(self):
        return f"{self.call.unique_id}: {self.disposition.name}"


class CallQualityAssessment(TimeStampedModel):
    """
    Quality assessment for calls (QA scoring).
    """
    
    call = models.OneToOneField(
        Call,
        on_delete=models.CASCADE,
        related_name='quality_assessment',
        verbose_name=_("Call")
    )
    
    assessor = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_("Assessor"),
        help_text=_("QA assessor who evaluated this call")
    )
    
    # Overall scores
    overall_score = models.FloatField(
        verbose_name=_("Overall Score"),
        help_text=_("Overall quality score (0.0 to 100.0)")
    )
    
    # Individual criteria scores
    opening_score = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_("Opening Score")
    )
    listening_score = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_("Listening Score")
    )
    resolution_score = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_("Resolution Score")
    )
    closing_score = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_("Closing Score")
    )
    professionalism_score = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_("Professionalism Score")
    )
    
    # Detailed feedback
    strengths = models.TextField(
        blank=True,
        verbose_name=_("Strengths"),
        help_text=_("Positive aspects of the call")
    )
    improvements = models.TextField(
        blank=True,
        verbose_name=_("Areas for Improvement"),
        help_text=_("Areas where agent can improve")
    )
    comments = models.TextField(
        blank=True,
        verbose_name=_("Comments"),
        help_text=_("Additional assessor comments")
    )
    
    # Assessment status
    is_calibrated = models.BooleanField(
        default=False,
        verbose_name=_("Is Calibrated"),
        help_text=_("Whether this assessment was calibrated with other assessors")
    )
    
    # Migration tracking
    legacy_qa_id = models.IntegerField(
        null=True,
        blank=True,
        db_index=True,
        verbose_name=_("Legacy QA ID"),
        help_text=_("Original qa table ID")
    )
    
    class Meta:
        verbose_name = _("Call Quality Assessment")
        verbose_name_plural = _("Call Quality Assessments")
        indexes = [
            models.Index(fields=['assessor', '-created_at']),
            models.Index(fields=['overall_score', '-created_at']),
            models.Index(fields=['is_calibrated', '-created_at']),
            models.Index(fields=['legacy_qa_id']),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(overall_score__gte=0.0) & models.Q(overall_score__lte=100.0),
                name='valid_overall_score'
            ),
            models.CheckConstraint(
                check=models.Q(opening_score__gte=0.0) & models.Q(opening_score__lte=100.0),
                name='valid_opening_score'
            ),
            models.CheckConstraint(
                check=models.Q(listening_score__gte=0.0) & models.Q(listening_score__lte=100.0),
                name='valid_listening_score'
            ),
            models.CheckConstraint(
                check=models.Q(resolution_score__gte=0.0) & models.Q(resolution_score__lte=100.0),
                name='valid_resolution_score'
            ),
            models.CheckConstraint(
                check=models.Q(closing_score__gte=0.0) & models.Q(closing_score__lte=100.0),
                name='valid_closing_score'
            ),
            models.CheckConstraint(
                check=models.Q(professionalism_score__gte=0.0) & models.Q(professionalism_score__lte=100.0),
                name='valid_professionalism_score'
            ),
        ]
    
    def __str__(self):
        return f"QA for {self.call.unique_id}: {self.overall_score}%"


class CallNote(TimeStampedModel):
    """
    Notes added to calls by agents or supervisors.
    """
    
    NOTE_TYPES = [
        ('agent', _('Agent Note')),
        ('supervisor', _('Supervisor Note')),
        ('system', _('System Note')),
        ('quality', _('Quality Note')),
        ('follow_up', _('Follow-up Note')),
    ]
    
    call = models.ForeignKey(
        Call,
        on_delete=models.CASCADE,
        related_name='notes',
        verbose_name=_("Call")
    )
    
    note_type = models.CharField(
        max_length=20,
        choices=NOTE_TYPES,
        default='agent',
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
        verbose_name=_("Content"),
        help_text=_("Note content")
    )
    
    is_private = models.BooleanField(
        default=False,
        verbose_name=_("Is Private"),
        help_text=_("Whether this note is private to supervisors only")
    )
    
    is_important = models.BooleanField(
        default=False,
        verbose_name=_("Is Important"),
        help_text=_("Mark this note as important")
    )
    
    class Meta:
        verbose_name = _("Call Note")
        verbose_name_plural = _("Call Notes")
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['call', '-created_at']),
            models.Index(fields=['author', '-created_at']),
            models.Index(fields=['note_type', '-created_at']),
            models.Index(fields=['is_important', '-created_at']),
        ]
    
    def __str__(self):
        return f"Note on {self.call.unique_id}: {self.title or self.content[:50]}"


class CallTransfer(TimeStampedModel):
    """
    Track call transfers between agents/departments.
    """
    
    TRANSFER_TYPES = [
        ('blind', _('Blind Transfer')),
        ('attended', _('Attended Transfer')),
        ('conference', _('Conference Transfer')),
    ]
    
    TRANSFER_REASONS = [
        ('escalation', _('Escalation')),
        ('expertise', _('Requires Expertise')),
        ('department', _('Wrong Department')),
        ('supervisor', _('Supervisor Request')),
        ('technical', _('Technical Issue')),
        ('language', _('Language Barrier')),
        ('other', _('Other')),
    ]
    
    call = models.ForeignKey(
        Call,
        on_delete=models.CASCADE,
        related_name='transfers',
        verbose_name=_("Call")
    )
    
    transfer_type = models.CharField(
        max_length=20,
        choices=TRANSFER_TYPES,
        verbose_name=_("Transfer Type")
    )
    
    transfer_reason = models.CharField(
        max_length=20,
        choices=TRANSFER_REASONS,
        verbose_name=_("Transfer Reason")
    )
    
    from_agent = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='transfers_from',
        verbose_name=_("From Agent")
    )
    
    to_agent = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='transfers_to',
        verbose_name=_("To Agent")
    )
    
    to_queue = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("To Queue"),
        help_text=_("Queue transferred to if not to specific agent")
    )
    
    transfer_time = models.DateTimeField(
        verbose_name=_("Transfer Time")
    )
    
    success = models.BooleanField(
        default=True,
        verbose_name=_("Transfer Successful")
    )
    
    notes = models.TextField(
        blank=True,
        verbose_name=_("Transfer Notes")
    )
    
    class Meta:
        verbose_name = _("Call Transfer")
        verbose_name_plural = _("Call Transfers")
        ordering = ['-transfer_time']
        indexes = [
            models.Index(fields=['call', 'transfer_time']),
            models.Index(fields=['from_agent', '-transfer_time']),
            models.Index(fields=['to_agent', '-transfer_time']),
            models.Index(fields=['transfer_reason', '-transfer_time']),
        ]
    
    def __str__(self):
        if self.to_agent:
            return f"Transfer {self.call.unique_id}: {self.from_agent} -> {self.to_agent}"
        return f"Transfer {self.call.unique_id}: {self.from_agent} -> {self.to_queue}"


class CallCallback(TimeStampedModel):
    """
    Track callback requests and scheduled callbacks.
    """
    
    CALLBACK_STATUSES = [
        ('requested', _('Requested')),
        ('scheduled', _('Scheduled')),
        ('attempted', _('Attempted')),
        ('completed', _('Completed')),
        ('failed', _('Failed')),
        ('cancelled', _('Cancelled')),
    ]
    
    original_call = models.ForeignKey(
        Call,
        on_delete=models.CASCADE,
        related_name='callback_requests',
        verbose_name=_("Original Call")
    )
    
    callback_call = models.OneToOneField(
        Call,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='callback_origin',
        verbose_name=_("Callback Call"),
        help_text=_("The actual callback call when made")
    )
    
    requested_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='callback_requests',
        verbose_name=_("Requested By")
    )
    
    assigned_to = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='callback_assignments',
        verbose_name=_("Assigned To")
    )
    
    contact = models.ForeignKey(
        'contacts.Contact',
        on_delete=models.CASCADE,
        verbose_name=_("Contact")
    )
    
    callback_number = models.CharField(
        max_length=50,
        verbose_name=_("Callback Number")
    )
    
    scheduled_time = models.DateTimeField(
        verbose_name=_("Scheduled Time")
    )
    
    status = models.CharField(
        max_length=20,
        choices=CALLBACK_STATUSES,
        default='requested',
        verbose_name=_("Status")
    )
    
    notes = models.TextField(
        blank=True,
        verbose_name=_("Notes")
    )
    
    reason = models.TextField(
        blank=True,
        verbose_name=_("Reason"),
        help_text=_("Reason for callback request")
    )
    
    attempted_count = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Attempt Count"),
        help_text=_("Number of callback attempts made")
    )
    
    max_attempts = models.PositiveIntegerField(
        default=3,
        verbose_name=_("Max Attempts"),
        help_text=_("Maximum number of callback attempts")
    )
    
    last_attempt = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Last Attempt")
    )
    
    completed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Completed At")
    )
    
    class Meta:
        verbose_name = _("Call Callback")
        verbose_name_plural = _("Call Callbacks")
        ordering = ['scheduled_time']
        indexes = [
            models.Index(fields=['status', 'scheduled_time']),
            models.Index(fields=['assigned_to', 'status']),
            models.Index(fields=['contact', '-created_at']),
            models.Index(fields=['scheduled_time', 'status']),
        ]
    
    def __str__(self):
        return f"Callback for {self.contact}: {self.scheduled_time}"
    
    @property
    def is_overdue(self):
        """Check if callback is overdue"""
        return (
            self.status in ['requested', 'scheduled'] and
            self.scheduled_time < timezone.now()
        )
    
    @property
    def can_attempt(self):
        """Check if callback can still be attempted"""
        return (
            self.status in ['requested', 'scheduled', 'attempted'] and
            self.attempted_count < self.max_attempts
        )