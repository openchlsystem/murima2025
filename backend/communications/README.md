# Communications API Documentation

**Last Updated**: {DATE}  
**Base URL**: `https://yourdomain.com/api/communications/`

## Table of Contents

1. [Overview](#overview)
2. [Authentication](#authentication)
3. [Endpoints](#endpoints)
   - [Channels](#channels)
   - [Messages](#messages)
4. [Webhooks](#webhooks)
5. [Error Handling](#error-handling)
6. [Rate Limiting](#rate-limiting)
7. [Examples](#examples)

## Overview

The Communications API enables multi-channel messaging (SMS, WhatsApp, Voice, etc.) with:

- Tenant isolation
- Full audit trails
- CRUD operations for channels/messages
- Webhook integrations

## Authentication

```http
Authorization: Bearer <your_jwt_token>
```

Requires JWT token from /api/auth/login/

All endpoints are tenant-scoped automatically

## Endpoints

### Channels

Manage communication channels (Twilio, WhatsApp Business, etc.)

#### List/Create Channels

```http
GET|POST /channels/
```

Request (Create)

```json
{
  "name": "Twilio SMS",
  "channel_type": "SMS",
  "is_active": true,
  "config": {
    "account_sid": "AC...",
    "auth_token": "..." 
  }
}
```

Response (201 Created)

```json
{
  "id": 1,
  "name": "Twilio SMS",
  "channel_type": "SMS",
  "is_active": true,
  "tenant_name": "Acme Corp",
  "config": {
    "account_sid": "AC...",
    "auth_token": "***" 
  }
}
```

#### Retrieve/Update/Delete Channel

```http
GET|PUT|PATCH|DELETE /channels/{id}/
```

Response (200 OK)

```json
{
  "id": 1,
  "name": "Updated Name",
  "channel_type": "SMS",
  "is_active": false,
  "tenant_name": "Acme Corp"
}
```

### Messages

Send and track messages across channels

#### List/Create Messages

```http
GET|POST /messages/
```

Query Params:
- channel_id: Filter by channel
- direction: IN (inbound) or OUT (outbound)

Request (Create SMS)

```json
{
  "channel": 1,
  "content": "Hello survivor!",
  "direction": "OUT",
  "metadata": {
    "to": "+1234567890"
  }
}
```

Response (201 Created)

```json
{
  "id": 101,
  "channel": 1,
  "external_id": "SM...",
  "direction": "OUT",
  "content": "Hello survivor!",
  "status": "queued",
  "created_at": "2023-11-20T14:30:00Z"
}
```

## Webhooks

### Incoming Message Webhook (Twilio Example)

```http
POST /webhooks/twilio/
```

Sample Payload

```json
{
  "MessageSid": "SM...",
  "From": "+1234567890",
  "Body": "Need help",
  "Status": "received"
}
```

Response (200 OK)

```json
{
  "success": true,
  "message_id": 102
}
```

## Error Handling

Common Status Codes

| Code | Description |
|------|-------------|
| 400  | Invalid request data |
| 401  | Unauthenticated |
| 403  | Tenant mismatch |
| 404  | Channel/message not found |
| 429  | Rate limit exceeded |

Sample Error

```json
{
  "error": "Invalid channel_type",
  "detail": "Valid options: CALL, SMS, WHATSAPP, EMAIL, SOCIAL"
}
```

## Rate Limiting

100 requests/minute per tenant

Headers included in responses:

```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 99
```

## Examples

### Python (Requests)

```python
import requests

headers = {
    "Authorization": "Bearer <token>",
    "Content-Type": "application/json"
}

# Create SMS channel
data = {
    "name": "Twilio Prod",
    "channel_type": "SMS",
    "config": {"account_sid": "AC..."}
}
response = requests.post(
    "https://yourdomain.com/api/communications/channels/",
    json=data,
    headers=headers
)
```

### cURL (Send Message)

```bash
curl -X POST https://yourdomain.com/api/communications/messages/ \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"channel":1,"content":"Test","direction":"OUT"}'
```

Note: Replace all {variables} and $TOKEN with actual values.
For production, use HTTPS and rotate API keys regularly.

This document includes:
1. Clear endpoint documentation
2. Sample requests/responses
3. Webhook integration guide
4. Error handling reference
5. Ready-to-use code snippets

Let me know if you'd like to add:
- SDK examples (JavaScript/Java)
- Postman collection link
- Detailed field-by-field specifications