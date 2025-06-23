# Murima Core Models - Developer Guide

## Overview

The `core` app provides abstract base models and system utilities that should be used consistently across all tenant apps in the Murima platform. This ensures data consistency, audit trails, and proper multi-tenant architecture.

## Abstract Base Models - When to Use What

### 🎯 Quick Decision Tree

```
Need UUID primary key + timestamps + user tracking + soft delete? 
├─ YES → Use BaseModel (recommended for most cases)
└─ NO → Choose specific combinations:
    ├─ Just timestamps? → TimestampedModel
    ├─ Just UUID PK? → UUIDModel  
    ├─ Just user tracking? → UserTrackingModel
    └─ Just soft delete? → SoftDeleteModel
```

### BaseModel (Recommended Default)

**Use for**: 95% of your business models (cases, contacts, calls, etc.)

```python
from apps.shared.core.models import BaseModel

class Case(BaseModel):
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=50, default='open')
    
    class Meta:
        verbose_name = "Case"
        verbose_name_plural = "Cases"
```

**What you get automatically**:
- UUID primary key (`id`)
- Timestamps (`created_at`, `updated_at`) 
- User tracking (`created_by`, `updated_by`)
- Soft delete (`is_deleted`, `deleted_at`, `deleted_by`)

### Individual Base Models

**TimestampedModel** - Use for lookup/reference data that doesn't need user tracking:
```python
from apps.shared.core.models import TimestampedModel

class SystemSetting(TimestampedModel):
    key = models.CharField(max_length=100)
    value = models.TextField()
```

**UUIDModel** - Use when you only need UUID primary key:
```python
from apps.shared.core.models import UUIDModel

class ExternalAPILog(UUIDModel):
    endpoint = models.CharField(max_length=255)
    response_data = models.JSONField()
```

## 🔧 Implementation Guidelines

### 1. Setting User Fields Automatically

**In your views/serializers, always set the user fields**:

```python
# In Django views
def create_case(request):
    case = Case.objects.create(
        title=request.data['title'],
        created_by=request.user,  # Always set this
        updated_by=request.user   # Always set this
    )

# In DRF serializers
class CaseSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        validated_data['updated_by'] = self.context['request'].user
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        validated_data['updated_by'] = self.context['request'].user
        return super().update(instance, validated_data)
```

### 2. Using Soft Delete

```python
# Instead of: case.delete()
case.soft_delete(user=request.user)

# To restore:
case.restore()

# Query only non-deleted records:
active_cases = Case.objects.filter(is_deleted=False)

# Or create a manager:
class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

class Case(BaseModel):
    title = models.CharField(max_length=200)
    
    objects = models.Manager()  # Default manager (includes deleted)
    active_objects = ActiveManager()  # Only non-deleted
```

### 3. Foreign Key Best Practices

**Always use PROTECT for user fields to maintain audit trails**:

```python
class Case(BaseModel):
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,  # Use SET_NULL for optional references
        null=True,
        blank=True
    )
    category = models.ForeignKey(
        'CaseCategory',
        on_delete=models.PROTECT,  # Use PROTECT for required references
        help_text="Case category - cannot be deleted while cases exist"
    )
```

## 📋 System Models Usage

### AuditLog - Automatic Usage

The audit log is typically populated automatically via signals or middleware. You rarely create entries manually:

```python
# This happens automatically when you save models
# But if you need manual logging:
from apps.shared.core.models import AuditLog

AuditLog.objects.create(
    user=request.user,
    tenant=request.tenant,
    action='ASSIGN',
    object_type=ContentType.objects.get_for_model(Case),
    object_id=str(case.id),
    object_repr=str(case),
    description=f"Case assigned to {assigned_user.get_full_name()}",
    ip_address=get_client_ip(request)
)
```

### SystemConfiguration - Runtime Settings

```python
from apps.shared.core.models import SystemConfiguration

# Create configuration
SystemConfiguration.objects.create(
    key='max_file_upload_size',
    name='Maximum File Upload Size',
    value=10485760,  # 10MB in bytes
    data_type='integer',
    description='Maximum size for file uploads in bytes',
    category='file_management',
    created_by=admin_user
)

# Use in code
def get_max_upload_size():
    try:
        config = SystemConfiguration.objects.get(
            key='max_file_upload_size', 
            is_active=True
        )
        return config.value
    except SystemConfiguration.DoesNotExist:
        return 5242880  # Default 5MB
```

### ErrorLog - Exception Tracking

```python
from apps.shared.core.models import ErrorLog
import traceback

# In exception handlers
try:
    # Some operation
    process_payment(case)
except Exception as e:
    ErrorLog.objects.create(
        level='ERROR',
        message=str(e),
        exception_type=type(e).__name__,
        stack_trace=traceback.format_exc(),
        user=request.user,
        tenant=request.tenant,
        request_path=request.path,
        request_method=request.method,
        context={'case_id': case.id}
    )
    raise  # Re-raise the exception
```

## 🚫 Common Mistakes to Avoid

### ❌ DON'T: Forget to set user fields
```python
# Bad - missing user tracking
case = Case.objects.create(title="New Case")
```

### ✅ DO: Always set user fields
```python
# Good - proper user tracking
case = Case.objects.create(
    title="New Case",
    created_by=request.user,
    updated_by=request.user
)
```

### ❌ DON'T: Use hard delete for business data
```python
# Bad - permanently deletes data
case.delete()
```

### ✅ DO: Use soft delete for business data
```python
# Good - maintains audit trail
case.soft_delete(user=request.user)
```

### ❌ DON'T: Create models without inheriting from base models
```python
# Bad - no audit trail, no consistency
class Case(models.Model):
    title = models.CharField(max_length=200)
```

### ✅ DO: Inherit from appropriate base model
```python
# Good - full audit trail and consistency
class Case(BaseModel):
    title = models.CharField(max_length=200)
```

## 📊 Model Inheritance Hierarchy

```
models.Model
├── TimestampedModel (created_at, updated_at)
├── UUIDModel (id as UUID)
├── UserTrackingModel (created_by, updated_by)
├── SoftDeleteModel (is_deleted, deleted_at, deleted_by)
└── BaseModel (combines all above) ← Use this for most models

models.Model (direct inheritance)
├── AuditLog (system audit trail)
├── SystemConfiguration (runtime settings)
└── ErrorLog (error tracking)
```

## 🔄 Migration Considerations

When adding core model inheritance to existing models:

1. **Create migration carefully**: May require data migration for existing records
2. **Set default values**: For required fields like `created_by`
3. **Update queries**: Add `.filter(is_deleted=False)` where needed

```python
# Example migration for adding BaseModel to existing model
from django.db import migrations

def set_default_users(apps, schema_editor):
    Case = apps.get_model('cases', 'Case')
    User = apps.get_model('auth', 'User')
    admin_user = User.objects.filter(is_superuser=True).first()
    
    Case.objects.filter(created_by__isnull=True).update(
        created_by=admin_user,
        updated_by=admin_user
    )

class Migration(migrations.Migration):
    operations = [
        # Add fields
        migrations.AddField(...),
        # Set default data
        migrations.RunPython(set_default_users),
    ]
```

## 🎯 Team Standards

1. **Always use BaseModel** for business entities unless you have a specific reason not to
2. **Set user fields** in all create/update operations
3. **Use soft delete** for business data, hard delete only for truly temporary data
4. **Add indexes** on frequently queried fields in your model's Meta class
5. **Write tests** that verify audit trails and soft delete behavior
6. **Document** any deviation from these patterns in code comments

## 📚 Next Steps

1. Review existing models in your app and migrate to BaseModel
2. Update views/serializers to set user fields properly
3. Add soft delete support to your querysets
4. Test audit trail functionality
5. Configure any needed SystemConfiguration entries

---

**Questions?** Check with the team lead or refer to the full design document for more context.