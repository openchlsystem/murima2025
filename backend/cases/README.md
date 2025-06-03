# Case Management API Documentation

Base URL: [https://yourdomain.com/api/cases/](https://yourdomain.com/api/cases/)
Authentication: Bearer Token (JWT)
Required Headers:

```http
Authorization: Bearer <your_jwt_token>
Content-Type: application/json
```

## Endpoints

1. List All Cases / Create a Case

Endpoint: /cases/
Method: GET (List) | POST (Create)

### GET Response (200 OK)
```json
{
  "count": 2,
  "results": [
    {
      "id": 1,
      "title": "Urgent Housing Need",
      "description": "Survivor requires immediate shelter.",
      "status": "OPEN",
      "assigned_to": 3,
      "tenant": 1,
      "created_at": "2023-10-25T14:30:00Z",
      "updated_at": "2023-10-25T14:30:00Z",
      "created_by": 1,
      "updated_by": null
    }
  ]
}
```

### POST Request (201 Created)
```json
{
  "title": "Legal Assistance",
  "description": "Survivor needs help filing a protection order.",
  "status": "OPEN",
  "assigned_to": 3
}
```

### Errors
| Code | Scenario | Response Example |
|------|----------|------------------|
| 401 | Missing/invalid JWT | `{"detail": "Authentication required"}` |
| 403 | User not in tenant | `{"detail": "Permission denied"}` |
| 400 | Invalid data | `{"title": ["This field is required."]}` |

2. Retrieve/Update/Delete a Case

Endpoint: /cases/`id`/
Method: GET (Retrieve) | PUT/PATCH (Update) | DELETE (Destroy)

### GET Response (200 OK)
```json
{
  "id": 1,
  "title": "Urgent Housing Need",
  "status": "IN_PROGRESS",
  "...": "..."
}
```

### PATCH Request (200 OK)
```json
{
  "status": "CLOSED",
  "assigned_to": null
}
```

### DELETE Response (204 No Content)
Empty body on success.

### Errors
| Code | Scenario | Response Example |
|------|----------|------------------|
| 404 | Case not found | `{"detail": "Not found"}` |
| 403 | User doesn't own case | `{"detail": "Permission denied"}` |

## Filtering & Searching
Endpoint: /cases/?field=value

### Examples
Filter by status:

```http
GET /cases/?status=OPEN
```

Filter by assignee:

```http
GET /cases/?assigned_to=3
```

## Pagination
Responses are paginated (default: 20 items/page).

### Query Params
| Param | Description | Example |
|-------|-------------|---------|
| page | Page number | ?page=2 |
| limit | Items per page | ?limit=50 |

### Response Header
```http
Link: <https://yourdomain.com/api/cases/?page=2>; rel="next"
```

## Status Codes
| Code | Meaning | Typical Use Case |
|------|---------|------------------|
| 200 | OK | Successful GET/PUT |
| 201 | Created | Successful POST |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Invalid input data |
| 401 | Unauthorized | Missing JWT |
| 403 | Forbidden | Tenant/user mismatch |
| 404 | Not Found | Invalid case ID |

## Sample Workflow

### Create a Case:
```bash
curl -X POST https://yourdomain.com/api/cases/ -d '{"title": "Test"}' -H "Authorization: Bearer <token>"
```

### Update Status:
```bash
curl -X PATCH https://yourdomain.com/api/cases/1/ -d '{"status": "CLOSED"}' -H "Authorization: Bearer <token>"
```

### Delete:
```bash
curl -X DELETE https://yourdomain.com/api/cases/1/ -H "Authorization: Bearer <token>"
```

## Notes
- All endpoints are tenant-scoped (users only see their organization's cases).
- Timestamps (created_at, updated_at) are in UTC.
- Assign a user ID to assigned_to or null to unassign.

## Need more details?
- For authentication, see the Auth API Docs.
- For errors, check the Error Reference.
