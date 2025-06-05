# Admin Module Documentation

![Admin Dashboard Preview](https://i.imgur.com/xyz4567.png)  
*Screenshot: System Configuration Panel*

---

## **Overview**

Centralized control panel for super-admins to manage:

- Global system settings
- Tenant configurations
- Audit logs
- Module toggles
- Category management
- System notifications

---

## **Key Features**

| Feature | Description | Endpoint |
|---------|-------------|----------|
| **System Configuration** | Enable maintenance mode, control signups, set AI defaults | `GET/PATCH /api/admin/system-config/` |
| **Tenant Management** | Override tenant-specific settings (domains, enabled modules) | `GET/PUT /api/tenants/<id>/config/` |
| **Audit Logs** | Track all admin actions with filters | `GET /api/admin/audit-logs/?user_id=<id>` |
| **Role Escalation** | Temporarily assume tenant admin roles | `POST /api/admin/impersonate/<tenant_id>/` |
| **Category Management** | Manage system and tenant-specific categories | `GET/POST /api/admin/categories/` |
| **System Notifications** | Broadcast system-wide alerts | `GET/POST /api/admin/notifications/` |

---

## **Setup Guide**

### **Prerequisites**

- Django admin privileges (`is_superuser=True`)
- Access to PostgreSQL and Redis

### **Installation**

1. Add to `INSTALLED_APPS`:

   ```python
   INSTALLED_APPS += ['admin_module']
   ```

2. Run migrations:

   ```bash
   python manage.py makemigrations admin_module
   python manage.py migrate
   ```

3. Create initial config:

   ```bash
   python manage.py shell -c "from admin_module.models import SystemConfiguration; SystemConfiguration.objects.create()"
   ```

## **API Reference**

### **1. System Configuration**

```http
PATCH /api/admin/system-config/
```

Request Body:

```json
{
  "id": 1,
  "maintenance_mode": false,
  "allow_new_signups": true,
  "default_ai_provider": "OPENAI",
  "case_number_prefix": "CASE",
  "case_number_counter": 102,
  "default_case_priority": "MEDIUM"
}
```

### **2. Tenant Configuration**

```http
PATCH /api/admin/tenant-config/
```

Request Body:

```json
{
  "id": 1,
  "tenant": 2,
  "custom_domain": "client.yourapp.com",
  "enabled_modules": ["ai_chatbot", "case_management"],
  "custom_categories": {
    "violence_types": ["Physical", "Emotional", "Neglect"]
  },
  "case_workflow": ["Intake", "Assessment", "Closure"],
  "default_assignee": 5
}
```

### **3. Audit Logs (Filterable)**

```http
GET /api/admin/audit-logs/?model_name=Case&action=CREATE
```

Response:

```json
{
  "id": 1,
  "user": 3,
  "action": "CREATE",
  "model_name": "Case",
  "object_id": "abc123",
  "timestamp": "2025-06-05T14:30:00Z",
  "metadata": {
    "field_changed": "status",
    "old_value": "open",
    "new_value": "closed"
  },
  "ip_address": "192.168.1.100",
  "user_agent": "Mozilla/5.0"
}
```

### **4. Category Types**

```http
POST /api/admin/category-types/
```

Request Body:

```json
{
  "id": 1,
  "name": "Violence Type",
  "description": "Types of violence experienced",
  "is_active": true,
  "tenant_specific": true,
  "system_managed": false
}
```

### **5. Categories**

```http
POST /api/admin/categories/
```

Request Body:

```json
{
  "id": 5,
  "category_type": 1,
  "name": "Physical Abuse",
  "description": "Involves bodily harm",
  "is_active": true,
  "sort_order": 1,
  "metadata": {
    "color": "#FF0000"
  },
  "parent": null
}
```

### **6. System Notifications**

```http
POST /api/admin/notifications/
```

Request Body:

```json
{
  "id": 1,
  "title": "System Maintenance",
  "message": "We will be down from 10 PM to 12 AM.",
  "severity": "WARNING",
  "is_active": true,
  "start_date": "2025-06-10T22:00:00Z",
  "end_date": "2025-06-11T00:00:00Z",
  "created_by": 1,
  "affected_tenants": [1, 2]
}
```

## **Admin Panel Usage**

Access at `/admin/` after setup:

### **System Config**

Components:
- Toggle switches for maintenance mode and signup control
- Dropdown for AI provider selection
- Text/number inputs for case numbering
- Priority selection dropdown

### **Tenant Management**

Components:
- Tenant selector dropdown
- Domain configuration
- Module enablement multi-select
- Category and workflow customization
- Default assignee selection

### **Audit Logs**

Components:
- Search and filter interface
- Sortable log table
- Detailed log viewer modal

### **Category Management**

Components:
- Type creation/management
- Category hierarchy editor
- Metadata configuration
- Active status toggles

### **System Notifications**

Components:
- Notification composer
- Scheduling interface
- Tenant targeting
- Severity selection

## **Security Protocols**

- Authentication: JWT with is_superuser requirement
- Rate Limiting: 50 requests/minute for admin endpoints
- Data Protection:
  - Audit logs are immutable
  - Sensitive operations require 2FA

## **Troubleshooting**

| Issue | Solution |
|-------|----------|
| 403 Forbidden | Ensure user has is_superuser=True |
| Missing audit logs | Check signals.py hooks in other apps |
| Tenant config not applying | Verify tenant_id in request headers |
| Category sync issues | Check tenant_specific flag |
| Notification delivery | Verify tenant subscription status |

## **Development Roadmap**

- Real-time system health dashboard
- Bulk tenant onboarding (CSV upload)
- Integration with SIEM tools (Splunk, Datadog)
- Advanced category management features
- Multi-channel notification delivery

---

### **Key Sections Explained**

1. **Visual Preview**: Dashboard screenshot for quick orientation  
2. **Feature Matrix**: Clear endpoint mapping for developers  
3. **Security Focus**: Highlights protection mechanisms  
4. **Troubleshooting**: Quick-reference table for common issues  
5. **Component Overview**: Detailed UI element descriptions

**Pro Tip**: Add a `docker-compose-admin.yml` snippet if admins need isolated services (e.g., pgAdmin).