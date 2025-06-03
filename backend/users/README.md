# Users API Documentation
Django REST Framework (DRF) CRUD API for User & Role Management
Multi-tenant, RBAC-enabled, with audit logging

## Table of Contents
- Features
- Setup
- Authentication
- API Endpoints
- Users
- Roles
- Examples
- Error Handling

## Features
- ✅ Multi-Tenant Users: Each user belongs to a tenant (organization).
- ✅ Role-Based Access Control (RBAC): Custom roles with permissions.
- ✅ Audit Logging: Track created_by, updated_at, etc. (via BaseModel).
- ✅ JWT Authentication: Secure token-based access.

## Setup
### Prerequisites
- Django 4.x
- PostgreSQL (for multi-tenancy)
- django-rest-framework, django-tenants, djangorestframework-simplejwt

### Installation
Add users app to INSTALLED_APPS:

```python
INSTALLED_APPS = [
    'rest_framework',
    'rest_framework_simplejwt',
    'users',
]
```

Run migrations:

```bash
python manage.py makemigrations users
python manage.py migrate
```

## Authentication
All endpoints require JWT. Include this header:

```http
Authorization: Bearer <your_access_token>
```

Obtain a Token:

```bash
curl -X POST [http://localhost:8000/api/auth/login/](http://localhost:8000/api/auth/login/) \
-H "Content-Type: application/json" \
-d '{"username": "admin", "password": "admin123"}'
```

## API Endpoints
### Users
| Endpoint | Method | Description | Permissions |
|----------|--------|-------------|-------------|
| [/api/users/users/](http://localhost:8000/api/users/users/) | GET | List all users | Admin |
| [/api/users/users/](http://localhost:8000/api/users/users/) | POST | Create a user | Admin |
| /api/users/users/{id}/ | GET | Retrieve a user | Admin |
| /api/users/users/{id}/ | PUT | Update a user | Admin |
| /api/users/users/{id}/ | DELETE | Delete a user | Admin |

Fields:

```json
{
  "username": "string",
  "email": "string",
  "password": "string (write-only)",
  "tenant": "int (auto-set)",
  "is_verified": "boolean",
  "groups": "array (read-only)"
}
```

### Roles
| Endpoint | Method | Description | Permissions |
|----------|--------|-------------|-------------|
| /api/users/roles/ | GET | List all roles | Admin |
| /api/users/roles/ | POST | Create a role | Admin |
| [/api/users/roles/{id}/](http://localhost:8000/api/users/roles/1/) | GET | Retrieve a role | Admin |
| [/api/users/roles/{id}/](http://localhost:8000/api/users/roles/1/) | PUT | Update a role | Admin |
| /api/users/roles/{id}/ | DELETE | Delete a role | Admin |

Fields:

```json
{
  "name": "string",
  "permissions": "array (IDs)",
  "tenant": "int (auto-set)"
}
```

## Examples

### 1. Create a User
```bash
curl -X POST [http://localhost:8000/api/users/users/](http://localhost:8000/api/users/users/) \
-H "Content-Type: application/json" \
-H "Authorization: Bearer _token_" \
-d '{
  "username": "agent1",
  "password": "secure123",
  "email": "[agent1@tenant.com](mailto:agent1@tenant.com)",
  "is_verified": true
}'
```

### 2. Assign Permissions to a Role
```bash
curl -X PUT [http://localhost:8000/api/users/roles/1/](http://localhost:8000/api/users/roles/1/) \
-H "Authorization: Bearer _token_" \
-H "Content-Type: application/json" \
-d '{
  "name": "Case Manager",
  "permissions": [1, 2, 3]
}'
```

## Error Handling
| Code | Error | Resolution |
|------|-------|------------|
| 401 | Unauthorized | Include valid JWT token |
| 403 | Forbidden | User lacks permissions |
| 404 | Not Found | Invalid user/role ID |
| 400 | Bad Request | Validate input fields |

## License
MIT © 2023 Your Organization

## Next Steps:
- Integrate with tenants API for tenant-scoped queries.
- Add user invitation flow (email/SMS).
- Run into issues? Check DEBUG=True in settings or open a GitHub issue!

*This README.md can be placed in your users app directory or project root. Customize fields/examples as needed.*