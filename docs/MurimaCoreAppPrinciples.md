# Core App Integration Guide - Design Principles & Usage

## Design Philosophy

The Murima core app is the **architectural backbone** that ensures every tenant app follows consistent patterns, maintains comprehensive audit trails, and provides unified system behavior. It's not just about code reuse—it's about creating a **cohesive platform** where all components work together seamlessly.

### Core Principles

1. **Consistency Above All** - Every app should feel like part of the same platform
2. **Audit Everything** - Complete transparency and compliance by default
3. **Fail Gracefully** - System operations never break due to audit/logging failures
4. **Security First** - Built-in permission patterns and data protection
5. **Performance Aware** - Efficient patterns that scale with usage

## Model Design Patterns

### 🎯 The BaseModel Standard

**Rule**: 95% of your business models should inherit from `BaseModel`

```python
# ✅ CORRECT - Standard pattern for business models
from apps.shared.core.models import BaseModel

class Case(BaseModel):
    case_number = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=50, default='open')
    priority = models.CharField(max_length=20, default='medium')
    
    class Meta:
        verbose_name = "Case"
        verbose_name_plural = "Cases"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['priority', 'status']),
        ]
```

**What you get automatically:**
- UUID primary key (secure, portable)
- Timestamp tracking (created_at, updated_at) 
- User tracking (created_by, updated_by)
- Soft delete capability (is_deleted, deleted_at, deleted_by)
- Automatic audit logging via signals

### 🔄 When to Use Other Base Models

```python
# Use TimestampedModel for reference/lookup data
from apps.shared.core.models import TimestampedModel

class CaseCategory(TimestampedModel):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=7)
    is_active = models.BooleanField(default=True)

# Use UUIDModel when you only need UUID primary keys
from apps.shared.core.models import UUIDModel

class ExternalAPILog(UUIDModel):
    endpoint = models.CharField(max_length=255)
    response_time = models.DurationField()
    status_code = models.IntegerField()
```

### 🚫 Model Anti-Patterns

```python
# ❌ WRONG - No audit trail, no consistency
class BadCase(models.Model):
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

# ❌ WRONG - Manual user tracking (error-prone)
class ManualCase(models.Model):
    title = models.CharField(max_length=200)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    # Missing updated_by, no soft delete, manual audit logging required

# ✅ CORRECT - Use BaseModel for consistent behavior
class GoodCase(BaseModel):
    title = models.CharField(max_length=200)
    # All tracking fields included automatically
```

## Manager and QuerySet Usage

### 🎯 Active vs All Data Pattern

Every BaseModel gets two managers automatically:

```python
class Case(BaseModel):
    title = models.CharField(max_length=200)

# Usage examples:
active_cases = Case.objects.all()  # Only non-deleted (default)
all_cases = Case.objects.with_deleted()  # Includes soft-deleted
deleted_cases = Case.objects.deleted_only()  # Only soft-deleted

# In views/APIs, always use the default manager
def list_cases(request):
    # This automatically excludes soft-deleted records
    cases = Case.objects.filter(status='open')
    return cases
```

### 🔍 Custom Manager Patterns

```python
# Build on BaseModelManager for custom behavior
from apps.shared.core.managers import BaseModelManager

class CaseManager(BaseModelManager):
    def open(self):
        return self.filter(status='open')
    
    def urgent(self):
        return self.filter(priority='high')
    
    def assigned_to_user(self, user):
        return self.filter(assigned_to=user)
    
    def recent_activity(self, days=7):
        return self.recent(days=days)  # Inherited from BaseModelManager

class Case(BaseModel):
    objects = CaseManager()  # Custom manager
    
    # Usage:
    urgent_cases = Case.objects.urgent()
    my_cases = Case.objects.assigned_to_user(request.user)
    recent_cases = Case.objects.recent_activity()
```

## Serializer Integration Patterns

### 🎯 The BaseModelSerializer Standard

**Rule**: Every business model serializer should inherit from `BaseModelSerializer`

```python
# ✅ CORRECT - Inherit from BaseModelSerializer
from apps.shared.core.serializers import BaseModelSerializer

class CaseSerializer(BaseModelSerializer):
    # Add computed/related fields
    assigned_to_name = serializers.CharField(
        source='assigned_to.get_full_name', read_only=True
    )
    days_open = serializers.SerializerMethodField()
    
    class Meta(BaseModelSerializer.Meta):
        model = Case
        fields = BaseModelSerializer.Meta.fields + [
            'case_number', 'title', 'description', 'status', 'priority',
            'assigned_to', 'assigned_to_name', 'days_open'
        ]
    
    def get_days_open(self, obj):
        if obj.status == 'closed':
            return 0
        return (timezone.now() - obj.created_at).days
```

**What you get automatically:**
- User tracking fields set from `request.user`
- Timestamp fields as read-only
- Soft delete fields (hidden unless requested)
- Consistent API response format

### 🔧 Custom Validation Patterns

```python
class CaseSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = Case
        fields = BaseModelSerializer.Meta.fields + [
            'title', 'description', 'priority', 'assigned_to'
        ]
    
    def validate_title(self, value):
        """Custom field validation."""
        if len(value.strip()) < 5:
            raise serializers.ValidationError(
                "Case title must be at least 5 characters long"
            )
        return value.strip()
    
    def validate(self, data):
        """Cross-field validation."""
        data = super().validate(data)
        
        # Business rule: High priority cases must be assigned
        if data.get('priority') == 'high' and not data.get('assigned_to'):
            raise serializers.ValidationError(
                "High priority cases must be assigned to a user"
            )
        
        return data
```

## Audit Trail Integration

### 🎯 Automatic Audit Logging

The beauty of the core app is that audit logging happens **automatically**:

```python
# This code automatically creates audit logs:
case = Case.objects.create(
    title="Customer complaint",
    created_by=request.user,
    updated_by=request.user
)
# → AuditLog entry created: action='CREATE'

case.status = 'in_progress'
case.assigned_to = some_user
case.save()
# → AuditLog entry created: action='UPDATE' with field changes

case.soft_delete(user=request.user)
# → AuditLog entry created: action='DELETE' (soft)
```

### 🔍 Manual Audit Logging for Special Events

For business events that aren't simple CRUD operations:

```python
from apps.shared.core.models import AuditLog
from django.contrib.contenttypes.models import ContentType

def transfer_case(case, from_user, to_user, reason, request):
    """Transfer case between users with audit trail."""
    old_user = case.assigned_to
    case.assigned_to = to_user
    case.updated_by = request.user
    case.save()
    
    # Manual audit log for business event
    AuditLog.objects.create(
        user=request.user,
        tenant=request.tenant,
        action='TRANSFER',
        object_type=ContentType.objects.get_for_model(Case),
        object_id=str(case.id),
        object_repr=str(case),
        description=f"Case transferred from {old_user} to {to_user}: {reason}",
        changes={
            'assigned_to': {
                'old': str(old_user) if old_user else None,
                'new': str(to_user)
            }
        },
        metadata={
            'transfer_reason': reason,
            'from_user_id': str(old_user.id) if old_user else None,
            'to_user_id': str(to_user.id),
        },
        ip_address=get_client_ip(request),
        user_agent=request.META.get('HTTP_USER_AGENT', '')
    )
```

## System Configuration Usage

### 🎯 Reading Configuration Values

```python
from apps.shared.core.models import SystemConfiguration

class FileUploadView(APIView):
    def post(self, request):
        # Get configuration values with defaults
        max_size = SystemConfiguration.objects.get_value(
            'max_file_upload_size', 
            default=5242880  # 5MB default
        )
        
        if request.FILES['file'].size > max_size:
            return Response(
                {'error': f'File size exceeds limit of {max_size} bytes'},
                status=400
            )
        
        # Process file upload...
```

### 🔧 Configuration-Driven Features

```python
class NotificationService:
    def send_notification(self, user, message, channel='email'):
        # Check if notifications are enabled
        notifications_enabled = SystemConfiguration.objects.get_value(
            'enable_notifications', default=True
        )
        
        if not notifications_enabled:
            return False
        
        # Get rate limiting configuration
        rate_limit = SystemConfiguration.objects.get_value(
            'notification_rate_limit_per_hour', default=100
        )
        
        # Implement rate limiting...
        # Send notification...
```

## ViewSet Integration Patterns

### 🎯 Standard CRUD ViewSet

```python
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.shared.core.serializers import SoftDeleteActionSerializer

class CaseViewSet(ModelViewSet):
    serializer_class = CaseSerializer
    permission_classes = [IsAuthenticated]  # Add TenantPermission when available
    
    def get_queryset(self):
        # Only show active (non-deleted) cases for current tenant
        return Case.objects.filter(
            # Add tenant filtering when tenants app is ready
        ).select_related('assigned_to', 'category')
    
    def perform_create(self, serializer):
        # BaseModelSerializer automatically sets created_by/updated_by
        serializer.save()
    
    def perform_update(self, serializer):
        # BaseModelSerializer automatically sets updated_by
        serializer.save()
    
    @action(detail=True, methods=['post'])
    def soft_delete(self, request, pk=None):
        """Soft delete a case with reason."""
        case = self.get_object()
        serializer = SoftDeleteActionSerializer(data=request.data)
        
        if serializer.is_valid():
            reason = serializer.validated_data.get('reason', '')
            case.soft_delete(user=request.user)
            
            # Optional: Add manual audit log with reason
            # log_soft_delete(case, user=request.user, reason=reason)
            
            return Response({'status': 'deleted', 'reason': reason})
        
        return Response(serializer.errors, status=400)
    
    @action(detail=True, methods=['post'])
    def restore(self, request, pk=None):
        """Restore a soft-deleted case."""
        case = self.get_object()
        case.restore()
        
        return Response({'status': 'restored'})
```

## Real-World App Examples

### 📞 Call Center App Integration

```python
# apps/tenant/calls/models.py
from apps.shared.core.models import BaseModel

class Call(BaseModel):
    call_id = models.CharField(max_length=100, unique=True)
    caller_number = models.CharField(max_length=50)
    agent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    duration = models.DurationField(null=True)
    
    # Inherits: id, created_at, updated_at, created_by, updated_by,
    #          is_deleted, deleted_at, deleted_by

# apps/tenant/calls/serializers.py
from apps.shared.core.serializers import BaseModelSerializer

class CallSerializer(BaseModelSerializer):
    agent_name = serializers.CharField(source='agent.get_full_name', read_only=True)
    
    class Meta(BaseModelSerializer.Meta):
        model = Call
        fields = BaseModelSerializer.Meta.fields + [
            'call_id', 'caller_number', 'agent', 'agent_name', 'duration'
        ]
```

### 💬 Communication App Integration

```python
# apps/tenant/communications/models.py
from apps.shared.core.models import BaseModel

class Interaction(BaseModel):
    channel = models.CharField(max_length=50)  # 'email', 'sms', 'whatsapp'
    direction = models.CharField(max_length=20)  # 'inbound', 'outbound'
    content = models.TextField()
    metadata = models.JSONField(default=dict)
    
    class Meta:
        ordering = ['-created_at']

# Usage in views:
def recent_interactions(request):
    # Automatically excludes soft-deleted, includes audit trail
    interactions = Interaction.objects.recent(days=30)
    return interactions
```

### 👥 Contact Management Integration

```python
# apps/tenant/contacts/models.py
from apps.shared.core.models import BaseModel
from apps.shared.core.managers import BaseModelManager

class ContactManager(BaseModelManager):
    def search(self, query):
        return self.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query)
        )

class Contact(BaseModel):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    
    objects = ContactManager()
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
```

## Performance Optimization Patterns

### 🎯 Efficient Querysets

```python
# ✅ GOOD - Optimized queries
def list_cases_with_details(request):
    cases = Case.objects.select_related(
        'assigned_to', 'category', 'created_by'
    ).prefetch_related(
        'documents', 'comments'
    ).filter(
        status='open'
    )[:50]  # Limit results
    
    return cases

# ❌ BAD - N+1 queries
def list_cases_inefficient(request):
    cases = Case.objects.filter(status='open')
    for case in cases:
        print(case.assigned_to.name)  # Database hit for each case
        print(case.created_by.email)  # Another database hit
```

### 🔍 Smart Filtering

```python
class CaseFilter:
    def __init__(self, queryset, request):
        self.queryset = queryset
        self.request = request
    
    def filter(self):
        # Start with active records (automatic via manager)
        qs = self.queryset
        
        # Add filters based on request parameters
        if self.request.GET.get('status'):
            qs = qs.filter(status=self.request.GET['status'])
        
        if self.request.GET.get('assigned_to_me'):
            qs = qs.filter(assigned_to=self.request.user)
        
        if self.request.GET.get('created_after'):
            date = parse_date(self.request.GET['created_after'])
            qs = qs.filter(created_at__gte=date)
        
        return qs
```

## Common Mistakes and Solutions

### ❌ Forgetting User Tracking

```python
# BAD - Missing user context
case = Case.objects.create(title="New case")  # created_by will be None!

# GOOD - Use serializer or set manually
serializer = CaseSerializer(data=data, context={'request': request})
if serializer.is_valid():
    case = serializer.save()  # User tracking automatic

# Or set manually:
case = Case.objects.create(
    title="New case",
    created_by=request.user,
    updated_by=request.user
)
```

### ❌ Bypassing Soft Delete

```python
# BAD - Hard delete loses audit trail
case.delete()  # Permanently removes from database

# GOOD - Use soft delete
case.soft_delete(user=request.user)  # Maintains audit trail
```

### ❌ Inconsistent Model Inheritance

```python
# BAD - Mixing inheritance patterns
class Case(models.Model):  # No audit trail
    title = models.CharField(max_length=200)

class Contact(BaseModel):  # Has audit trail
    name = models.CharField(max_length=200)

# GOOD - Consistent patterns
class Case(BaseModel):     # Audit trail
    title = models.CharField(max_length=200)

class Contact(BaseModel):  # Audit trail
    name = models.CharField(max_length=200)
```

## Testing with Core Models

```python
# tests/test_models.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.tenant.cases.models import Case

User = get_user_model()

class CaseModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com'
        )
    
    def test_case_creation_with_audit_trail(self):
        """Test that creating a case generates audit logs."""
        case = Case.objects.create(
            title="Test Case",
            created_by=self.user,
            updated_by=self.user
        )
        
        # Verify BaseModel functionality
        self.assertIsNotNone(case.id)  # UUID assigned
        self.assertIsNotNone(case.created_at)
        self.assertEqual(case.created_by, self.user)
        self.assertFalse(case.is_deleted)
        
        # Verify audit log created (if signals are connected)
        # audit_logs = AuditLog.objects.filter(object_id=str(case.id))
        # self.assertEqual(audit_logs.count(), 1)
    
    def test_soft_delete(self):
        """Test soft delete functionality."""
        case = Case.objects.create(
            title="Test Case",
            created_by=self.user,
            updated_by=self.user
        )
        
        case.soft_delete(user=self.user)
        
        # Verify soft delete
        self.assertTrue(case.is_deleted)
        self.assertIsNotNone(case.deleted_at)
        self.assertEqual(case.deleted_by, self.user)
        
        # Verify not in default queryset
        self.assertNotIn(case, Case.objects.all())
        
        # Verify in deleted queryset
        self.assertIn(case, Case.objects.with_deleted())
```

## Success Checklist

### ✅ Model Implementation
- [ ] Inherits from appropriate base model (usually BaseModel)
- [ ] Includes proper Meta class with ordering and indexes
- [ ] Custom manager if needed (inherits from BaseModelManager)
- [ ] Proper foreign key relationships with correct on_delete
- [ ] String representation (__str__) method

### ✅ Serializer Implementation  
- [ ] Inherits from BaseModelSerializer
- [ ] Extends Meta.fields properly
- [ ] Custom validation methods if needed
- [ ] Computed fields for API responses
- [ ] Proper field ordering and read-only settings

### ✅ ViewSet Implementation
- [ ] Uses optimized querysets (select_related, prefetch_related)
- [ ] Proper permission classes
- [ ] Custom actions for soft delete/restore if needed
- [ ] Error handling and validation
- [ ] Consistent response formats

### ✅ Testing
- [ ] Model tests for BaseModel functionality
- [ ] Serializer tests for user tracking
- [ ] ViewSet tests for CRUD operations
- [ ] Audit trail verification
- [ ] Soft delete behavior testing

---

**Remember**: The core app isn't just about inheritance—it's about creating a **unified platform experience**. Every decision should prioritize consistency, auditability, and maintainability over convenience.