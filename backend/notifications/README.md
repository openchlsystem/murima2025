# Notifications API Documentation
Version: 1.0
Last Updated: {{date}}

## Table of Contents
- [Overview](#overview)
- [API Endpoints](#api-endpoints)
- [Authentication](#authentication)
- [Request & Response Examples](#request--response-examples)
- [Error Handling](#error-handling)
- [Webhooks](#webhooks)
- [Rate Limits](#rate-limits)
- [Setup & Deployment](#setup--deployment)

## Overview
The Notifications API enables multi-channel (email, SMS, WhatsApp, in-app) notification management within a multi-tenant system. Key features:

- Tenant Isolation: Notifications are scoped to the tenant making the request.
- Audit Trails: Tracks created_by, updated_at, etc.
- Real-Time Support: Integrates with WebSockets for in-app alerts.

## API Endpoints
All endpoints are prefixed with `/api/notifications/`.

| Endpoint | Method | Description | Permissions |
|----------|--------|-------------|-------------|
| / | GET | List all notifications | IsAuthenticated |
| / | POST | Create a notification | IsAuthenticated |
| /{id}/ | GET | Retrieve a notification | IsAuthenticated |
| /{id}/ | PUT | Update a notification | IsOwnerOrAdmin |
| /{id}/ | DELETE | Delete a notification | IsOwnerOrAdmin |
| /mark-as-read/{id}/ | PATCH | Mark as read | IsOwnerOrAdmin |

## Authentication
Required Headers:

```http
Authorization: Bearer <access_token>  
X-Tenant-ID: <tenant_id>  # For multi-tenancy
```

Authentication Flow:

1. Obtain JWT token via `/api/auth/login/`.
2. Include token in Authorization header for all requests.

## Request & Response Examples
### Create a Notification
Request:

```http
POST /api/notifications/  
Content-Type: application/json  
Authorization: Bearer <token>  

{
  "title": "Case Escalation",
  "message": "Case #1234 requires urgent attention.",
  "channel": "whatsapp",
  "recipient_id": 5,
  "is_read": false
}
```

Response: 201 Created

```json
{
  "id": 101,
  "title": "Case Escalation",
  "message": "Case #1234 requires urgent attention.",
  "channel": "whatsapp",
  "is_read": false,
  "sent_at": null,
  "created_at": "2023-11-20T14:30:00Z",
  "updated_at": "2023-11-20T14:30:00Z",
  "recipient": {
    "id": 5,
    "email": "[social.worker@example.com](mailto:social.worker@example.com)"
  }
}
```

### Mark as Read
Request:

```http
PATCH /api/notifications/mark-as-read/101/  
Authorization: Bearer <token>  
```

Response: 200 OK

```json
{
  "id": 101,
  "is_read": true,
  "updated_at": "2023-11-20T14:35:00Z"
}
```

## Error Handling
| Code | Error | Resolution |
|------|-------|------------|
| 400 | Invalid channel | Use email, sms, whatsapp, in_app |
| 403 | Permission denied | Check tenant/role permissions |
| 404 | Notification not found | Validate notification_id |

## Webhooks
Configure endpoints to receive delivery statuses:

- Event Types: delivered, failed, read

Sample Payload:

```json
{
  "notification_id": 101,
  "status": "delivered",
  "timestamp": "2023-11-20T14:40:00Z"
}
```

## Rate Limits
- Default: 100 requests/minute per tenant.
- Exceeded Response: 429 Too Many Requests

## Setup & Deployment
### Prerequisites
Python 3.10+, Django 4.2+, Django REST Framework.

### Installation
```bash
pip install -r requirements.txt  # Includes django-tenants, djangorestframework
```

### Environment Variables
```env
# .env
DATABASE_URL=postgres://user:pass@localhost:5432/tenant_db
TWILIO_ACCOUNT_SID=your_sid  # For SMS/WhatsApp
```

### Run Migrations
```bash
python manage.py migrate_schemas --shared
python manage.py migrate_schemas --tenant
```

### Support
For issues, contact [api-support@yourdomain.com](mailto:api-support@yourdomain.com)