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

---

## **Key Features**

| Feature | Description | Endpoint |
|---------|-------------|----------|
| **System Configuration** | Enable maintenance mode, control signups, set AI defaults | `GET/PATCH /api/admin/system-config/` |
| **Tenant Management** | Override tenant-specific settings (domains, enabled modules) | `GET/PUT /api/tenants/<id>/config/` |
| **Audit Logs** | Track all admin actions with filters | `GET /api/admin/audit-logs/?user_id=<id>` |
| **Role Escalation** | Temporarily assume tenant admin roles | `POST /api/admin/impersonate/<tenant_id>/` |

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
  "maintenance_mode": true,
  "default_ai_provider": "HUGGINGFACE"
}
```

### **2. Audit Logs (Filterable)**

```http
GET /api/admin/audit-logs/?model_name=Tenant&action=DELETE
```

Response:

```json
{
  "count": 3,
  "results": [
    {
      "id": 1,
      "user_email": "admin@org.com",
      "action": "DELETE",
      "model_name": "Tenant",
      "timestamp": "2023-11-20T12:34:56Z",
      "metadata": {"deleted_id": 42}
    }
  ]
}
```

## **Admin Panel Usage**

Access at `/admin/` after setup:

### **System Config**

- Toggle maintenance mode
- Configure default AI services

### **Tenant Overrides**

- Assign custom domains
- Enable/disable modules per tenant:

```json
["ai_chatbot", "advanced_analytics"]
```

### **Audit Logs**

- Filter by: User, Action Type, Date Range

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

## **Development Roadmap**

- Real-time system health dashboard
- Bulk tenant onboarding (CSV upload)
- Integration with SIEM tools (Splunk, Datadog)

---

### **Key Sections Explained**

1. **Visual Preview**: Dashboard screenshot for quick orientation  
2. **Feature Matrix**: Clear endpoint mapping for developers  
3. **Security Focus**: Highlights protection mechanisms  
4. **Troubleshooting**: Quick-reference table for common issues  

**Pro Tip**: Add a `docker-compose-admin.yml` snippet if admins need isolated services (e.g., pgAdmin).