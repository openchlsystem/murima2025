# Analytics API Documentation

Base URL: [http://localhost:8000/api/analytics/](http://localhost:8000/api/analytics/)

## Table of Contents
- Authentication
- Dashboards
- List/Create Dashboards
- Retrieve/Update/Delete Dashboard
- Widgets
- List/Create Widgets
- Retrieve/Update/Delete Widget
- Models
- Error Handling

## Authentication
All endpoints require JWT authentication. Include the token in headers:

```http
Authorization: Bearer <your_access_token>
```

## Dashboards

### List or Create Dashboards
Endpoint: GET/POST /dashboards/

#### Request (POST)
```http
POST /dashboards/
Content-Type: application/json
{
    "name": "Survivor Metrics",
    "tenant": 1,
    "description": "Tracking survivor support cases",
    "is_active": true
}
```

#### Response (201 Created)
```json
{
    "id": 1,
    "name": "Survivor Metrics",
    "tenant": {
        "id": 1,
        "name": "SafeHaven NGO"
    },
    "description": "Tracking survivor support cases",
    "is_active": true,
    "created_at": "2023-10-25T14:30:00Z",
    "updated_at": "2023-10-25T14:30:00Z",
    "created_by": 1,
    "updated_by": 1,
    "widgets": []
}
```

#### Response (GET - List)
```json
{
    "count": 2,
    "results": [
        {
            "id": 1,
            "name": "Survivor Metrics",
            "tenant": {"id": 1, "name": "SafeHaven NGO"},
            "is_active": true
        },
        {
            "id": 2,
            "name": "Call Volume",
            "tenant": {"id": 1, "name": "SafeHaven NGO"},
            "is_active": true
        }
    ]
}
```

### Retrieve, Update, or Delete Dashboard
Endpoint: GET/PUT/PATCH/DELETE /dashboards/{id}/

#### Request (PATCH)
```http
PATCH /dashboards/1/
Content-Type: application/json
{
    "is_active": false
}
```

#### Response (200 OK)
```json
{
    "id": 1,
    "name": "Survivor Metrics",
    "is_active": false,
    "updated_at": "2023-10-25T15:00:00Z"
}
```

#### DELETE Response
```http
HTTP 204 No Content
```

## Widgets

### List or Create Widgets
Endpoint: GET/POST /dashboards/{dashboard_id}/widgets/

#### Request (POST)
```http
POST /dashboards/1/widgets/
Content-Type: application/json
{
    "title": "Calls by Region",
    "widget_type": "pie_chart",
    "data_config": {
        "labels": ["North", "South"],
        "data": [30, 70]
    }
}
```

#### Response (201 Created)
```json
{
    "id": 1,
    "title": "Calls by Region",
    "widget_type": "pie_chart",
    "data_config": {
        "labels": ["North", "South"],
        "data": [30, 70]
    },
    "dashboard": 1,
    "created_at": "2023-10-25T15:30:00Z"
}
```

### Retrieve, Update, or Delete Widget
Endpoint: GET/PUT/PATCH/DELETE /dashboards/{dashboard_id}/widgets/{widget_id}/

#### Request (PUT)
```http
PUT /dashboards/1/widgets/1/
Content-Type: application/json
{
    "title": "Calls by Region (Updated)",
    "data_config": {
        "labels": ["North", "South", "East"],
        "data": [25, 60, 15]
    }
}
```

#### Response (200 OK)
```json
{
    "id": 1,
    "title": "Calls by Region (Updated)",
    "widget_type": "pie_chart",
    "data_config": {
        "labels": ["North", "South", "East"],
        "data": [25, 60, 15]
    },
    "updated_at": "2023-10-25T16:00:00Z"
}
```

## Models

### Dashboard
| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Auto-generated PK |
| tenant | ForeignKey | Linked Tenant |
| name | CharField | Dashboard name (max 100 chars) |
| description | TextField | Optional details |
| is_active | Boolean | Toggle visibility |
| created_at | DateTime | Auto-set on creation |
| updated_at | DateTime | Auto-updated |

### Widget
| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Auto-generated PK |
| dashboard | ForeignKey | Parent dashboard |
| title | CharField | Widget title (max 100 chars) |
| widget_type | CharField | Chart type (e.g., pie_chart) |
| data_config | JSONField | Chart data/configuration |

## Error Handling
| Code | Error | Resolution |
|------|-------|------------|
| 401 | Unauthorized | Include valid JWT token |
| 403 | Forbidden | Check user permissions |
| 404 | Not Found | Verify object ID exists |
| 400 | Bad Request | Validate request body JSON |

Example (404):
```json
{
    "detail": "Not found."
}
```

## Usage Examples

### Python (Requests)
```python
import requests

headers = {"Authorization": "Bearer <your_token>"}

# Create a widget
response = requests.post(
    "http://localhost:8000/api/analytics/dashboards/1/widgets/",
    json={
        "title": "Case Status",
        "widget_type": "bar_chart",
        "data_config": {"labels": ["Open", "Closed"], "data": [20, 80]}
    },
    headers=headers
)
print(response.json())
```

### cURL
```bash
# Get all dashboards
curl -H "Authorization: Bearer <your_token>" http://localhost:8000/api/analytics/dashboards/
```

> 📌 Note: Replace `<your_token>` and `localhost:8000` with your actual credentials and domain.

For further assistance, contact the development team.