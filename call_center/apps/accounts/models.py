# apps/accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.utils import timezone as django_timezone
from django.core.exceptions import ValidationError
from apps.core.models import TimeStampedModel, SoftDeleteModel
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    """Custom user model for call center system."""
    
    # Role choices
    ROLE_CHOICES = [
        ('admin', _('Administrator')),
        ('agent', _('Agent')),
        ('supervisor', _('Supervisor')),
        ('manager', _('Manager')),
        ('qa', _('Quality Assurance')),
        ('reporting', _('Reporting Analyst')),
        ('it_support', _('IT Support')),
    ]
    
    # Status choices
    STATUS_CHOICES = [
        ('active', _('Active')),
        ('inactive', _('Inactive')),
        ('suspended', _('Suspended')),
        ('terminated', _('Terminated')),
    ]
    
    # Agent status choices
    AGENT_STATUS_CHOICES = [
        ('available', _('Available')),
        ('busy', _('Busy')),
        ('on_call', _('On Call')),
        ('on_break', _('On Break')),
        ('in_meeting', _('In Meeting')),
        ('offline', _('Offline')),
        ('away', _('Away')),
    ]
    
    # Basic Information
    username = models.CharField(
        max_length=100, 
        unique=True, 
        verbose_name=_("Username"),
        help_text=_("Required. 100 characters or fewer. Letters, digits and @/./+/-/_ only."),
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+$',
                message=_('Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters.')
            )
        ]
    )
    email = models.EmailField(
        max_length=255, 
        unique=True, 
        verbose_name=_("Email"),
        help_text=_("Required. Valid email address.")
    )
    employee_id = models.CharField(
        max_length=50,
        unique=True,
        blank=True,
        null=True,
        verbose_name=_("Employee ID"),
        help_text=_("Unique employee identifier")
    )
    
    # Personal Information
    first_name = models.CharField(
        max_length=100, 
        blank=True, 
        verbose_name=_("First name")
    )
    last_name = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Last name")
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name=_("Phone number"),
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message=_("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
            )
        ]
    )
    
    # Work-related Information
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='agent',
        verbose_name=_("Role"),
        help_text=_("User's primary role in the system")
    )
    department = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Department"),
        help_text=_("Department or team the user belongs to")
    )
    manager = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subordinates',
        verbose_name=_("Manager"),
        help_text=_("Direct manager/supervisor")
    )
    
    # Call Center Specific Fields
    extension = models.CharField(
        max_length=20, 
        blank=True, 
        null=True, 
        verbose_name=_("Extension"),
        help_text=_("Phone extension number")
    )
    agent_number = models.CharField(
        max_length=20, 
        blank=True, 
        null=True, 
        verbose_name=_("Agent number"),
        help_text=_("Unique agent identifier for call routing")
    )
    
    # Status and Availability
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active',
        verbose_name=_("Status")
    )
    agent_status = models.CharField(
        max_length=20,
        choices=AGENT_STATUS_CHOICES,
        default='offline',
        verbose_name=_("Agent status"),
        help_text=_("Current availability status")
    )
    is_online = models.BooleanField(
        default=False,
        verbose_name=_("Is online"),
        help_text=_("Whether the user is currently logged in")
    )
    last_login_ip = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name=_("Last login IP")
    )
    last_activity = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Last activity"),
        help_text=_("Last time user performed any action")
    )
    
    # Break and Time Tracking
    last_break_type = models.CharField(
        max_length=32,
        blank=True,
        null=True,
        verbose_name=_("Last break type"),
        help_text=_("Type of last break taken")
    )
    last_break_time = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_("Last break time"),
        help_text=_("When the last break was taken")
    )
    break_start_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Break start time"),
        help_text=_("When current break started")
    )
    shift_start_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Shift start time"),
        help_text=_("When current shift started")
    )
    
    # Contact Information Link (will be added after contacts app is created)
    # contact = models.ForeignKey(
    #     'contacts.Contact',
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     blank=True,
    #     related_name="user_profile",
    #     verbose_name=_("Contact"),
    #     help_text=_("Associated contact record")
    # )
    
    # Permissions and Access
    is_active = models.BooleanField(
        default=True, 
        verbose_name=_("Is active"),
        help_text=_("Designates whether this user should be treated as active.")
    )
    is_staff = models.BooleanField(
        default=False, 
        verbose_name=_("Is staff"),
        help_text=_("Designates whether the user can log into admin site.")
    )
    
    # Settings and Preferences
    timezone = models.CharField(
        max_length=50,
        default='UTC',
        verbose_name=_("Timezone")
    )
    language = models.CharField(
        max_length=10,
        default='en',
        verbose_name=_("Language")
    )
    
    # Date fields
    date_joined = models.DateTimeField(
        default=django_timezone.now,
        verbose_name=_("Date joined")
    )
    date_terminated = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Date terminated")
    )
    
    objects = UserManager()
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    
    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        indexes = [
            models.Index(fields=['username']),
            models.Index(fields=['email']),
            models.Index(fields=['role', 'is_active']),
            models.Index(fields=['agent_status']),
            models.Index(fields=['department', 'is_active']),
            models.Index(fields=['manager']),
            models.Index(fields=['employee_id']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['employee_id'],
                condition=models.Q(employee_id__isnull=False),
                name='unique_employee_id'
            ),
            models.UniqueConstraint(
                fields=['agent_number'],
                condition=models.Q(agent_number__isnull=False),
                name='unique_agent_number'
            ),
            models.UniqueConstraint(
                fields=['extension'],
                condition=models.Q(extension__isnull=False),
                name='unique_extension'
            ),
        ]
    
    def __str__(self):
        return self.get_full_name() or self.username
    
    def clean(self):
        """Validate the model"""
        if self.manager == self:
            raise ValidationError(_("A user cannot be their own manager"))
        
        if self.role in ['agent', 'supervisor'] and not self.extension:
            raise ValidationError(_("Agents and supervisors must have an extension"))
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def get_full_name(self):
        """Return the full name"""
        return f"{self.first_name} {self.last_name}".strip() or self.username
    
    def get_short_name(self):
        """Return the short name"""
        return self.first_name or self.username
    
    def get_display_name(self):
        """Return display name with role"""
        full_name = self.get_full_name()
        return f"{full_name} ({self.get_role_display()})"
    
    @property
    def is_agent(self):
        """Check if user is an agent"""
        return self.role == 'agent'
    
    @property
    def is_supervisor(self):
        """Check if user is a supervisor"""
        return self.role == 'supervisor'
    
    @property
    def is_manager(self):
        """Check if user is a manager"""
        return self.role == 'manager'
    
    @property
    def is_admin(self):
        """Check if user is an admin"""
        return self.role == 'admin'
    
    @property
    def can_supervise(self):
        """Check if user can supervise others"""
        return self.role in ['supervisor', 'manager', 'admin']
    
    @property
    def is_available_for_calls(self):
        """Check if user is available to receive calls"""
        return (
            self.is_active and 
            self.is_online and 
            self.agent_status in ['available', 'busy'] and
            self.role in ['agent', 'supervisor']
        )
    
    @property
    def is_on_break(self):
        """Check if user is currently on break"""
        return self.agent_status == 'on_break' and self.break_start_time is not None
    
    def set_status(self, status, break_type=None):
        """Set agent status with proper time tracking"""
        old_status = self.agent_status
        self.agent_status = status
        self.last_activity = django_timezone.now()
        
        if status == 'on_break':
            self.break_start_time = django_timezone.now()
            if break_type:
                self.last_break_type = break_type
        elif old_status == 'on_break' and status != 'on_break':
            # Ending break
            if self.break_start_time:
                self.last_break_time = self.break_start_time
            self.break_start_time = None
        
        self.save(update_fields=['agent_status', 'last_activity', 'break_start_time', 'last_break_time', 'last_break_type'])
    
    def start_shift(self):
        """Mark the start of a shift"""
        self.shift_start_time = django_timezone.now()
        self.set_status('available')
    
    def end_shift(self):
        """Mark the end of a shift"""
        self.set_status('offline')
        self.shift_start_time = None
        self.save(update_fields=['shift_start_time'])
    
    def get_subordinates(self):
        """Get all users who report to this user"""
        return User.objects.filter(manager=self, is_active=True)
    
    def get_team_members(self):
        """Get all team members (same manager)"""
        if self.manager:
            return User.objects.filter(manager=self.manager, is_active=True).exclude(pk=self.pk)
        return User.objects.none()


class UserProfile(SoftDeleteModel):
    """Extended user profile information"""
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name=_("User")
    )
    
    # Personal Information
    avatar = models.ImageField(
        upload_to='avatars/%Y/%m/',
        blank=True,
        null=True,
        verbose_name=_("Avatar")
    )
    date_of_birth = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Date of birth")
    )
    emergency_contact_name = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Emergency contact name")
    )
    emergency_contact_phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name=_("Emergency contact phone")
    )
    
    # Preferences
    email_notifications = models.BooleanField(
        default=True,
        verbose_name=_("Email notifications")
    )
    browser_notifications = models.BooleanField(
        default=True,
        verbose_name=_("Browser notifications")
    )
    sms_notifications = models.BooleanField(
        default=False,
        verbose_name=_("SMS notifications")
    )
    
    # Skills and Qualifications
    skills = models.JSONField(
        default=list,
        blank=True,
        verbose_name=_("Skills"),
        help_text=_("List of skills and competencies")
    )
    certifications = models.JSONField(
        default=list,
        blank=True,
        verbose_name=_("Certifications"),
        help_text=_("Professional certifications")
    )
    languages_spoken = models.JSONField(
        default=list,
        blank=True,
        verbose_name=_("Languages spoken"),
        help_text=_("Languages the user can communicate in")
    )
    
    # Performance Settings
    call_queue_limit = models.IntegerField(
        default=5,
        verbose_name=_("Call queue limit"),
        help_text=_("Maximum number of calls in queue for this agent")
    )
    auto_answer_calls = models.BooleanField(
        default=False,
        verbose_name=_("Auto answer calls")
    )
    wrap_up_time_seconds = models.IntegerField(
        default=30,
        verbose_name=_("Wrap-up time (seconds)"),
        help_text=_("Time required after each call for notes")
    )
    
    class Meta:
        verbose_name = _("User Profile")
        verbose_name_plural = _("User Profiles")
    
    def __str__(self):
        return f"Profile for {self.user.get_full_name()}"


class AgentShift(SoftDeleteModel):
    """Agent shift schedule"""
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="shifts",
        verbose_name=_("User")
    )
    day_of_week = models.IntegerField(
        choices=[
            (0, _('Sunday')),
            (1, _('Monday')),
            (2, _('Tuesday')),
            (3, _('Wednesday')),
            (4, _('Thursday')),
            (5, _('Friday')),
            (6, _('Saturday')),
        ],
        verbose_name=_("Day of week")
    )
    start_time = models.TimeField(verbose_name=_("Start time"))
    end_time = models.TimeField(verbose_name=_("End time"))
    break_duration_minutes = models.IntegerField(
        default=60,
        verbose_name=_("Break duration (minutes)")
    )
    timezone = models.CharField(
        max_length=50,
        default='UTC',
        verbose_name=_("Timezone")
    )
    
    # Effective date range
    effective_from = models.DateField(
        default=django_timezone.now,
        verbose_name=_("Effective from")
    )
    effective_to = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Effective to")
    )
    
    class Meta:
        verbose_name = _("Agent Shift")
        verbose_name_plural = _("Agent Shifts")
        ordering = ['user', 'day_of_week', 'start_time']
        indexes = [
            models.Index(fields=['user', 'day_of_week', 'is_active']),
            models.Index(fields=['effective_from', 'effective_to']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'day_of_week', 'start_time'],
                condition=models.Q(is_active=True),
                name='unique_active_user_shift'
            )
        ]
        
    def __str__(self):
        day_names = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        return f"{self.user.get_full_name()} - {day_names[self.day_of_week]} {self.start_time} to {self.end_time}"
    
    def clean(self):
        """Validate shift times"""
        if self.start_time >= self.end_time:
            raise ValidationError(_("Start time must be before end time"))
        
        if self.effective_to and self.effective_from >= self.effective_to:
            raise ValidationError(_("Effective from date must be before effective to date"))
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    @property
    def duration_hours(self):
        """Calculate shift duration in hours"""
        from datetime import datetime, timedelta
        start = datetime.combine(datetime.today(), self.start_time)
        end = datetime.combine(datetime.today(), self.end_time)
        
        if end < start:
            end += timedelta(days=1)
        
        duration = end - start
        return duration.total_seconds() / 3600
    
    @property
    def is_current(self):
        """Check if shift is currently effective"""
        today = django_timezone.now().date()
        return (
            self.effective_from <= today and
            (self.effective_to is None or self.effective_to >= today)
        )


class UserSession(TimeStampedModel):
    """Track user login sessions"""
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sessions',
        verbose_name=_("User")
    )
    session_key = models.CharField(
        max_length=40,
        unique=True,
        verbose_name=_("Session key")
    )
    ip_address = models.GenericIPAddressField(verbose_name=_("IP address"))
    user_agent = models.TextField(verbose_name=_("User agent"))
    login_time = models.DateTimeField(
        default=django_timezone.now,
        verbose_name=_("Login time")
    )
    logout_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Logout time")
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Is active")
    )
    
    class Meta:
        verbose_name = _("User Session")
        verbose_name_plural = _("User Sessions")
        ordering = ['-login_time']
        indexes = [
            models.Index(fields=['user', '-login_time']),
            models.Index(fields=['session_key']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.login_time}"
    
    @property
    def duration(self):
        """Get session duration"""
        end_time = self.logout_time or django_timezone.now()
        return end_time - self.login_time
    
    def end_session(self):
        """End the session"""
        self.logout_time = django_timezone.now()
        self.is_active = False
        self.save(update_fields=['logout_time', 'is_active'])