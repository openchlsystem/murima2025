# Murima Backend Design Document

## Project Architecture Overview

**Technology Stack**: Django + django-tenants for multi-tenant SaaS with on-premises capability
**Database**: PostgreSQL (primary), MongoDB (documents), Redis (cache), Elasticsearch (search - future)
**API**: RESTful API with versioning support
**Authentication**: JWT-based with multi-factor authentication support

## Folder Structure

```
murima2025/
├── apps/
│   ├── shared/                     # SHARED_APPS (platform-level)
│   │   ├── accounts/              # User management & authentication
│   │   ├── api/                   # Centralized API management
│   │   ├── core/                  # Base models & utilities
│   │   ├── platform/              # Platform administration
│   │   └── tenants/               # Tenant management
│   └── tenant/                    # TENANT_APPS (business logic)
│       ├── calls/                 # Call center operations
│       ├── cases/                 # Case management
│       ├── communications/        # Omnichannel communications
│       ├── contacts/              # CRM functionality
│       ├── documents/             # Document management
│       ├── notifications/         # Notification system
│       ├── reference_data/        # Lookup data
│       ├── tasks/                 # Task management
│       └── workflows/             # Workflow automation
├── config/                        # Django settings
├── deployment/                    # Docker, K8s configs
├── frontend/                      # Vue.js, Flutter, Electron
└── requirements/                  # Python dependencies
```

## Django Settings Configuration

### SHARED_APPS (Platform Level)
```python
SHARED_APPS = [
    'django_tenants',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Custom shared apps
    'accounts',        # User management, authentication, RBAC
    'tenants',         # Tenant management, domains
    'platform',        # Platform administration tools
    'core',           # Abstract models, utilities, audit logs
    'api',            # Centralized API management
]
```

### TENANT_APPS (Organization Level)
```python
TENANT_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.admin',
    
    # Core business apps
    'cases',           # Case management
    'communications',  # Omnichannel communications
    'calls',          # Call center operations
    'contacts',        # CRM functionality
    'reference_data',  # Tenant-specific lookup data
    'workflows',       # Custom workflows
    'documents',       # Document management
    'tasks',          # Task management
    'notifications',   # Notification system
]
```

## Shared Apps (Platform Level)

### 1. accounts/ (SHARED)
**Purpose**: User authentication, tenant membership, platform-wide user management

#### Key Models:
```python
class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    is_platform_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class TenantMembership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tenant = models.ForeignKey('tenants.Tenant', on_delete=models.CASCADE)
    role = models.ForeignKey('TenantRole', on_delete=models.PROTECT)
    is_active = models.BooleanField(default=True)
    joined_at = models.DateTimeField(auto_now_add=True)
    invited_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

class TenantRole(models.Model):
    tenant = models.ForeignKey('tenants.Tenant', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)  # 'admin', 'supervisor', 'agent', 'viewer'
    display_name = models.CharField(max_length=100)
    permissions = models.JSONField(default=dict)
    is_system_role = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

class PlatformRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=50)  # 'super_admin', 'admin', 'support'
    permissions = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
```

### 2. tenants/ (SHARED)
**Purpose**: Tenant/organization management and domain routing

#### Key Models:
```python
class Tenant(TenantMixin):
    name = models.CharField(max_length=100)
    subdomain = models.CharField(max_length=100, unique=True)
    owner = models.ForeignKey(User, on_delete=models.PROTECT)
    sector = models.CharField(max_length=50, default='general')
    is_active = models.BooleanField(default=True)
    subscription_plan = models.CharField(max_length=50, default='basic')
    created_at = models.DateTimeField(auto_now_add=True)
    settings = models.JSONField(default=dict)

class Domain(DomainMixin):
    pass

class TenantInvitation(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    email = models.EmailField()
    role = models.ForeignKey('accounts.TenantRole', on_delete=models.CASCADE)
    invited_by = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    expires_at = models.DateTimeField()
    is_accepted = models.BooleanField(default=False)
```

### 3. core/ (SHARED)
**Purpose**: Common utilities, abstract models, and cross-cutting concerns

#### Abstract Base Models:
```python
class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

class UUIDModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    class Meta:
        abstract = True

class UserTrackingModel(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='%(class)s_created')
    updated_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='%(class)s_updated', null=True, blank=True)
    
    class Meta:
        abstract = True

class SoftDeleteModel(models.Model):
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='%(class)s_deleted')
    
    class Meta:
        abstract = True

class BaseModel(UUIDModel, TimestampedModel, UserTrackingModel, SoftDeleteModel):
    """Complete base model with all common functionality"""
    
    class Meta:
        abstract = True
```

#### Audit and System Models:
```python
class AuditLog(TimestampedModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    tenant = models.ForeignKey('tenants.Tenant', on_delete=models.CASCADE)
    action = models.CharField(max_length=20)  # CREATE, UPDATE, DELETE, VIEW
    object_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=255)
    object_repr = models.CharField(max_length=255)
    changes = models.JSONField(default=dict, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
```

### 4. api/ (SHARED)
**Purpose**: Centralized API management, versioning, and common API functionality

#### Key Models:
```python
class APIKey(BaseModel):
    tenant = models.ForeignKey('tenants.Tenant', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    key = models.CharField(max_length=255, unique=True)
    permissions = models.JSONField(default=dict)
    rate_limit = models.IntegerField(default=1000)
    is_active = models.BooleanField(default=True)
    last_used = models.DateTimeField(null=True, blank=True)

class APIRequestLog(BaseModel):
    tenant = models.ForeignKey('tenants.Tenant', on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    endpoint = models.CharField(max_length=255)
    method = models.CharField(max_length=10)
    status_code = models.IntegerField()
    response_time = models.DurationField()
    ip_address = models.GenericIPAddressField()
```

### 5. platform/ (SHARED)
**Purpose**: Platform administration, monitoring, and support tools

#### Key Models:
```python
class SystemHealth(models.Model):
    component = models.CharField(max_length=50)  # 'database', 'cache', 'queue'
    status = models.CharField(max_length=20)  # 'healthy', 'warning', 'critical'
    metrics = models.JSONField(default=dict)
    checked_at = models.DateTimeField(auto_now_add=True)

class TenantUsage(models.Model):
    tenant = models.ForeignKey('tenants.Tenant', on_delete=models.CASCADE)
    date = models.DateField()
    active_users = models.IntegerField(default=0)
    api_requests = models.IntegerField(default=0)
    storage_used = models.BigIntegerField(default=0)  # bytes
    cases_created = models.IntegerField(default=0)
```

## Tenant Apps (Organization Level)

### 1. cases/ (TENANT)
**Purpose**: Core case management functionality

#### Key Models:
```python
class Case(BaseModel):
    case_number = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=50, default='open')
    priority = models.CharField(max_length=20, default='medium')
    case_type = models.ForeignKey('reference_data.CaseCategory', on_delete=models.PROTECT)
    workflow = models.ForeignKey('workflows.Workflow', on_delete=models.PROTECT, null=True, blank=True)
    current_stage = models.CharField(max_length=50, blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    custom_fields = models.JSONField(default=dict, blank=True)
    tags = models.JSONField(default=list, blank=True)

class CaseHistory(BaseModel):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='history')
    field_name = models.CharField(max_length=100)
    old_value = models.TextField(blank=True)
    new_value = models.TextField(blank=True)
    change_reason = models.TextField(blank=True)

class CaseLink(BaseModel):
    from_case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='linked_from')
    to_case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='linked_to')
    link_type = models.CharField(max_length=50)  # 'related', 'duplicate', 'parent', 'child'
    description = models.TextField(blank=True)
```

### 2. communications/ (TENANT)
**Purpose**: Omnichannel communication management (non-voice)

#### Key Models:
```python
class Channel(BaseModel):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50, choices=[
        ('sms', 'SMS'),
        ('whatsapp', 'WhatsApp'),
        ('email', 'Email'),
        ('webchat', 'Web Chat'),
        ('facebook', 'Facebook Messenger'),
        ('twitter', 'Twitter DM'),
        ('instagram', 'Instagram DM'),
    ])
    configuration = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)

class Interaction(BaseModel):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    contact = models.ForeignKey('contacts.Contact', on_delete=models.CASCADE)
    case = models.ForeignKey('cases.Case', on_delete=models.SET_NULL, null=True, blank=True)
    direction = models.CharField(max_length=20)  # 'inbound', 'outbound'
    content = models.TextField()
    timestamp = models.DateTimeField()
    external_id = models.CharField(max_length=255, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    attachments = models.JSONField(default=list, blank=True)

class MessageTemplate(BaseModel):
    name = models.CharField(max_length=100)
    channel_type = models.CharField(max_length=50)
    subject = models.CharField(max_length=255, blank=True)  # For email
    content = models.TextField()
    variables = models.JSONField(default=list, blank=True)
    is_active = models.BooleanField(default=True)

class Conversation(BaseModel):
    contact = models.ForeignKey('contacts.Contact', on_delete=models.CASCADE)
    case = models.ForeignKey('cases.Case', on_delete=models.SET_NULL, null=True, blank=True)
    last_interaction = models.DateTimeField()
    status = models.CharField(max_length=20, default='active')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
```

### 3. calls/ (TENANT)
**Purpose**: Call center specific functionality

#### Key Models:
```python
class Call(BaseModel):
    call_id = models.CharField(max_length=100, unique=True)  # Asterisk call ID
    case = models.ForeignKey('cases.Case', on_delete=models.SET_NULL, null=True, blank=True)
    contact = models.ForeignKey('contacts.Contact', on_delete=models.SET_NULL, null=True, blank=True)
    caller_number = models.CharField(max_length=50)
    caller_name = models.CharField(max_length=200, blank=True)
    agent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    direction = models.CharField(max_length=20)  # 'inbound', 'outbound', 'internal'
    status = models.CharField(max_length=20)  # 'ringing', 'answered', 'completed', 'failed'
    started_at = models.DateTimeField()
    answered_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    disposition = models.ForeignKey('CallDisposition', on_delete=models.PROTECT, null=True, blank=True)
    recording_path = models.CharField(max_length=500, blank=True)

class CallEvent(BaseModel):
    call = models.ForeignKey(Call, on_delete=models.CASCADE, related_name='events')
    event_type = models.CharField(max_length=50)  # 'answered', 'transferred', 'held', 'ended'
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    details = models.JSONField(default=dict, blank=True)

class CallTransfer(BaseModel):
    call = models.ForeignKey(Call, on_delete=models.CASCADE, related_name='transfers')
    transfer_type = models.CharField(max_length=20)  # 'warm', 'cold', 'blind'
    from_agent = models.ForeignKey(User, on_delete=models.PROTECT, related_name='transfers_made')
    to_agent = models.ForeignKey(User, on_delete=models.PROTECT, related_name='transfers_received', null=True)
    reason = models.TextField(blank=True)
    status = models.CharField(max_length=20, default='initiated')

class CallDisposition(BaseModel):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    category = models.CharField(max_length=50)
    requires_follow_up = models.BooleanField(default=False)
    requires_case_creation = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

class CallQueue(BaseModel):
    name = models.CharField(max_length=100)
    asterisk_queue_name = models.CharField(max_length=50, unique=True)
    max_wait_time = models.DurationField(default=timezone.timedelta(minutes=5))
    ring_strategy = models.CharField(max_length=20, default='leastrecent')
    is_active = models.BooleanField(default=True)
```

### 4. contacts/ (TENANT)
**Purpose**: CRM and contact management

#### Key Models:
```python
class Contact(BaseModel):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    organization = models.CharField(max_length=200, blank=True)
    title = models.CharField(max_length=100, blank=True)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    preferred_language = models.CharField(max_length=10, default='en')
    preferred_contact_method = models.CharField(max_length=20, blank=True)
    custom_fields = models.JSONField(default=dict, blank=True)
    tags = models.JSONField(default=list, blank=True)
    is_active = models.BooleanField(default=True)

class ContactRelationship(BaseModel):
    from_contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='relationships_from')
    to_contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='relationships_to')
    relationship_type = models.CharField(max_length=50)  # 'parent', 'child', 'spouse', 'guardian'
    description = models.TextField(blank=True)

class ContactGroup(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    contacts = models.ManyToManyField(Contact, related_name='groups')
    is_active = models.BooleanField(default=True)
```

### 5. reference_data/ (TENANT)
**Purpose**: Tenant-specific lookup data and hierarchical reference information

#### Key Models:
```python
class CaseCategory(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    code = models.CharField(max_length=20, unique=True)
    color = models.CharField(max_length=7, default='#0066CC')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)

class Priority(BaseModel):
    name = models.CharField(max_length=50)
    level = models.PositiveIntegerField(unique=True)
    color = models.CharField(max_length=7)
    sla_hours = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

class Location(BaseModel):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20)  # 'country', 'state', 'district', 'area'
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    code = models.CharField(max_length=10, blank=True)
    is_active = models.BooleanField(default=True)

# Generic reference data for flexible lookup tables
class ReferenceDataCategory(BaseModel):
    name = models.CharField(max_length=50, unique=True)
    display_name = models.CharField(max_length=100)
    category_type = models.CharField(max_length=20, default='LIST')
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

class ReferenceData(BaseModel):
    category = models.ForeignKey(ReferenceDataCategory, on_delete=models.CASCADE)
    code = models.CharField(max_length=50, blank=True)
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    sort_order = models.IntegerField(default=0)
    metadata = models.JSONField(default=dict, blank=True)
    is_active = models.BooleanField(default=True)
```

### 6. workflows/ (TENANT)
**Purpose**: Custom workflow and automation engine

#### Key Models:
```python
class Workflow(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    entity_type = models.CharField(max_length=50, default='case')  # 'case', 'task', etc.
    stages = models.JSONField(default=list)  # List of stage definitions
    transitions = models.JSONField(default=list)  # Allowed transitions between stages
    actions = models.JSONField(default=list)  # Automated actions
    is_active = models.BooleanField(default=True)

class WorkflowInstance(BaseModel):
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE)
    entity_type = models.CharField(max_length=50)
    entity_id = models.UUIDField()  # Generic foreign key to any entity
    current_stage = models.CharField(max_length=50)
    data = models.JSONField(default=dict)  # Instance-specific data
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

class BusinessRule(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    entity_type = models.CharField(max_length=50)
    conditions = models.JSONField(default=dict)
    actions = models.JSONField(default=list)
    is_active = models.BooleanField(default=True)
```

### 7. documents/ (TENANT)
**Purpose**: Document and file management

#### Key Models:
```python
class Document(BaseModel):
    case = models.ForeignKey('cases.Case', on_delete=models.CASCADE, null=True, blank=True)
    contact = models.ForeignKey('contacts.Contact', on_delete=models.CASCADE, null=True, blank=True)
    filename = models.CharField(max_length=255)
    original_filename = models.CharField(max_length=255)
    file_path = models.CharField(max_length=500)
    mime_type = models.CharField(max_length=100)
    size = models.BigIntegerField()
    description = models.TextField(blank=True)
    tags = models.JSONField(default=list, blank=True)
    is_public = models.BooleanField(default=False)

class DocumentAccess(BaseModel):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    access_type = models.CharField(max_length=20)  # 'view', 'edit', 'download'
    granted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='document_access_granted')
    expires_at = models.DateTimeField(null=True, blank=True)
```

### 8. tasks/ (TENANT)
**Purpose**: Task and assignment management

#### Key Models:
```python
class Task(BaseModel):
    case = models.ForeignKey('cases.Case', on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=50, default='pending')
    priority = models.CharField(max_length=20, default='medium')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    estimated_hours = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    actual_hours = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

class TaskComment(BaseModel):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    is_internal = models.BooleanField(default=True)

class TaskDependency(BaseModel):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='dependencies')
    depends_on = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='dependents')
    dependency_type = models.CharField(max_length=20, default='finish_to_start')
```

### 9. notifications/ (TENANT)
**Purpose**: Notification and alert management

#### Key Models:
```python
class NotificationRule(BaseModel):
    name = models.CharField(max_length=100)
    trigger_event = models.CharField(max_length=50)  # 'case_created', 'task_overdue', etc.
    conditions = models.JSONField(default=dict)
    recipients = models.JSONField(default=list)  # List of user IDs or roles
    channels = models.JSONField(default=list)  # 'email', 'sms', 'in_app'
    template = models.TextField()
    is_active = models.BooleanField(default=True)

class Notification(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=50)
    entity_type = models.CharField(max_length=50, blank=True)
    entity_id = models.UUIDField(null=True, blank=True)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    channel = models.CharField(max_length=20)  # 'email', 'sms', 'in_app'
    delivery_status = models.CharField(max_length=20, default='pending')
```

## API Structure

### URL Pattern
```
/api/v1/auth/                    # Authentication endpoints
/api/v1/cases/                   # Case management
/api/v1/communications/          # Omnichannel communications
/api/v1/calls/                   # Call center operations
/api/v1/contacts/                # CRM functionality
/api/v1/workflows/               # Workflow management
/api/v1/reference-data/          # Lookup data
/api/v1/documents/               # Document management
/api/v1/tasks/                   # Task management
/api/v1/notifications/           # Notifications

/api/platform/tenants/           # Platform admin - tenant management
/api/platform/users/             # Platform admin - user management
/api/platform/analytics/         # Platform admin - cross-tenant analytics
```

## Development Phases

### MVP Phase (Core Apps)
**Focus**: Essential functionality for basic operations
- ✅ accounts, tenants, core, api (shared)
- ✅ cases, communications, calls, contacts, reference_data, workflows (tenant)
- ✅ Basic documents, tasks, notifications (simplified)

### Phase 2 (Enhanced Features)
**Focus**: Advanced functionality and optimization
- 📊 analytics/ (advanced reporting)
- 🤖 ai_services/ (AI integration)
- 📚 knowledge/ (knowledge base)
- 📋 surveys/ (feedback collection)

### Phase 3 (Advanced Features)
**Focus**: Enterprise and specialized features
- 📅 scheduling/ (appointment management)
- 🔌 integrations/ (third-party integrations)
- 🔍 search/ (Elasticsearch integration)
- 🏥 Sector-specific modules

## Key Design Decisions

1. **Multi-Tenancy**: Django-tenants for schema-based isolation
2. **Authentication**: Shared users with tenant membership model
3. **API Management**: Centralized API app for versioning and consistency
4. **Data Models**: Base model inheritance for common functionality
5. **Flexibility**: Generic reference data model alongside specific models
6. **Scalability**: Designed for both SaaS and on-premises deployment
7. **Standards**: Industry-standard Django patterns and best practices

## Development Guidelines

1. **Model Naming**: Use descriptive names, avoid abbreviations
2. **Foreign Keys**: Always use `on_delete` parameter explicitly
3. **JSON Fields**: Use for flexible data, define schema where possible
4. **Indexing**: Add database indexes for frequently queried fields
5. **Migrations**: Keep migrations small and reversible
6. **Testing**: Each app should have comprehensive test coverage
7. **Documentation**: Document complex business logic and API endpoints

This design provides a solid foundation for building a professional, scalable multi-tenant call center and case management system while maintaining flexibility for future enhancements and sector-specific customizations.