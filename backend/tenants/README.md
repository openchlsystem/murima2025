# Call Center & Case Management System API Documentation
Version: 1.0
Base URL: [https://api.yourdomain.com/v1](https://api.yourdomain.com/v1)

## Table of Contents
- Authentication
- Tenants API
- Analytics API
- Dashboards
- Widgets
- Examples
- Error Handling

## Authentication
All endpoints require JWT authentication. Include the token in the Authorization header:

```http
Authorization: Bearer <your_access_token>
```

Obtain Token:

```http
POST /api/auth/login/
Body: { "username": "admin", "password": "securepassword123" }
```

## Tenants API
Manage multi-tenant organizations.

### List/Create Tenants
```http
GET /api/tenants/tenants/
POST /api/tenants/tenants/
```

Request Body (POST):

```json
{
  "name": "Survivor Support Inc",
  "paid_until": "2025-12-31",
  "on_trial": false,
  "enable_ai": true,
  "enable_analytics": true
}
```

Response (201 Created):

```json
{
  "id": 1,
  "name": "Survivor Support Inc",
  "domains": []
}
```

### Retrieve/Update/Destroy Tenant
```http
GET|PUT|DELETE /api/tenants/tenants/{id}/
```

## Analytics API
Manage dashboards and widgets for data visualization.

### Dashboards
List/Create Dashboards:

```http
GET /api/analytics/dashboards/
POST /api/analytics/dashboards/
```

Request Body (POST):

```json
{
  "name": "Crisis Call Metrics",
  "tenant": 1,
  "description": "Track call volumes and resolutions"
}
```

Response (201 Created):

```json
{
  "id": 1,
  "name": "Crisis Call Metrics",
  "widgets": [],
  "created_at": "2023-11-20T12:00:00Z"
}
```

### Widgets (Nested Under Dashboards)
List/Create Widgets:

```http
GET /api/analytics/dashboards/{dashboard_id}/widgets/
POST /api/analytics/dashboards/{dashboard_id}/widgets/
```

Request Body (POST):

```json
{
  "title": "Calls by Region",
  "widget_type": "pie_chart",
  "data_config": {
    "labels": ["North", "South"],
    "datasets": [{"data": [30, 70]}]
  }
}
```

Response (201 Created):

```json
{
  "id": 1,
  "title": "Calls by Region",
  "widget_type": "pie_chart",
  "dashboard": 1
}
```

## Examples

1. Create a Tenant
    ```bash
    curl -X POST "https://api.yourdomain.com/v1/api/tenants/tenants/" \
      -H "Authorization: Bearer `your_token`" \
      -H "Content-Type: application/json" \
      -d '{"name": "Health Clinic LLC", "on_trial": true}'
    ```

2. Add a Widget to Dashboard
    ```bash
    curl -X POST "https://api.yourdomain.com/v1/api/analytics/dashboards/1/widgets/" \
      -H "Authorization: Bearer `your_token`" \
      -H "Content-Type: application/json" \
      -d '{"title": "Call Duration", "widget_type": "bar_chart", "data_config": {"labels": ["Jan", "Feb"], "data": [120, 180]}'
    ```

## Error Handling
| Code | Error | Description |
|------|-------|-------------|
| 400 | Bad Request | Invalid input (e.g., missing fields) |
| 401 | Unauthorized | Missing/invalid JWT token |
| 403 | Forbidden | User lacks permissions |
| 404 | Not Found | Resource doesn't exist |

Example Error Response:

```json
{
  "error": "Not Found",
  "status_code": 404,
  "detail": "Dashboard with id=99 does not exist."
}
```
