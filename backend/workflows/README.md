# Workflows App

A modular workflow engine for multi-tenant call center & case management systems
Built with Django REST Framework (DRF) & PostgreSQL

## Features

✅ Multi-tenant workflows (isolated per organization)

✅ CRUD APIs for workflows and steps

✅ Reusable BaseModel with audit fields (created_by, updated_at)

✅ Nested steps with order priority

✅ Role-Based Access Control (RBAC) integration

✅ Django Generic Views for clean, maintainable code

## Table of Contents

- Requirements
- Installation
- Models
- API Endpoints
- Permissions
- Examples
- Testing
- Contributing

## Requirements

- Python 3.8+
- Django 4.0+
- Django REST Framework
- PostgreSQL (with django-tenants for multi-tenancy)
- JWT Authentication (recommended: djangorestframework-simplejwt)

## Installation

Add to INSTALLED_APPS in settings.py:

```python
INSTALLED_APPS = [
    ...,
    'core',      # For BaseModel
    'tenants',   # For Tenant model
    'workflows',
]
```

Run migrations:

```bash
python manage.py makemigrations workflows
python manage.py migrate
```

## Models

### 1. Workflow

| Field | Type | Description |
|-------|------|-------------|
| tenant | ForeignKey | Linked to Tenant model |
| name | CharField | Workflow name (e.g., "Survivor Intake") |
| description | TextField | Optional details |
| is_active | Boolean | Toggle workflow on/off |

### 2. Step

| Field | Type | Description |
|-------|------|-------------|
| workflow | ForeignKey | Parent workflow |
| name | CharField | Step name (e.g., "Verify Contact") |
| order | Integer | Execution priority (0=first) |
| action | CharField | Action key (e.g., "send_email") |

## API Endpoints

### Workflows

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/tenants/{tenant_id}/workflows/` | GET | List all workflows for a tenant |
| | POST | Create a new workflow |
| `/api/tenants/{tenant_id}/workflows/{id}/` | GET | Get workflow details |
| | PUT | Update workflow |
| | DELETE | Delete workflow |

### Steps

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/workflows/{workflow_id}/steps/` | GET | List all steps in a workflow |
| | POST | Add a step to workflow |
| `/api/workflows/{workflow_id}/steps/{step_id}/` | GET | Get step details |
| | PUT | Update step |
| | DELETE | Remove step |

## Permissions

By default, endpoints require:

- Authentication: JWT token (IsAuthenticated)
- Tenant Scope: Users can only access workflows for their tenant.

To customize, override in views.py:

```python
from rest_framework.permissions import BasePermission

class IsTenantAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'ADMIN'  # Custom logic
```

## Examples

### 1. Create a Workflow

```bash
curl -X POST /api/tenants/1/workflows/ \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{"name": "Crisis Response", "description": "For survivor support"}'
```

### 2. Add a Step

```bash
curl -X POST /api/workflows/1/steps/ \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{"name": "Assess Risk", "order": 1, "action": "check_safety"}'
```

## Testing

Run tests with:

```bash
python manage.py test workflows.tests
```

Sample Test Case:

```python
from django.test import TestCase
from rest_framework.test import APIClient

class WorkflowAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {test_token}')

    def test_create_workflow(self):
        response = self.client.post(
            '/api/tenants/1/workflows/',
            {'name': 'Test', 'description': 'Test workflow'},
            format='json'
        )
        self.assertEqual(response.status_code, 201)
```

## Contributing

1. Fork the repository.
2. Create a branch: `git checkout -b feature/new-workflow-type`
3. Commit changes: `git commit -m "Add X feature"`
4. Push to branch: `git push origin feature/new-workflow-type`
5. Submit a PR.

## License

MIT

## Need More?

- For multi-tenancy setup, see django-tenants docs.
- For JWT authentication, use DRF SimpleJWT.
