# 🧱 Core Django Application

The **`core`** app provides foundational building blocks for the entire platform. It includes abstract models, audit logging mechanisms, system utilities, and reusable components used across other apps.

---

## ✨ Features

- **🧩 Base Models** – Abstract classes for consistent model architecture
- **🕵️ Audit Logging** – Track all create/update/delete operations with user/IP metadata
- **🛠️ Utilities** – Common functions shared across multiple modules
- **🔌 API Endpoints** – Expose core functionality via RESTful endpoints

---

## ⚙️ Installation

1. Add `'core'` to your `INSTALLED_APPS` in `settings.py`:

    ```python
    INSTALLED_APPS = [
        ...
        'core',
    ]
    ```

2. Run database migrations:

    ```bash
    python manage.py makemigrations core
    python manage.py migrate
    ```

---

## 🧬 Base Models

These abstract models provide composable features for other Django models.

| Model               | Description                                                       |
|--------------------|-------------------------------------------------------------------|
| `BaseModel`         | Combines UUID, timestamps, user tracking, soft delete            |
| `TimestampedModel` | Adds `created_at` and `updated_at` fields                         |
| `UUIDModel`         | Uses UUID as the primary key                                     |
| `UserTrackingModel`| Tracks `created_by` and `updated_by` users                        |
| `SoftDeleteModel`   | Provides logical deletion (`is_deleted`) instead of hard delete  |
| `OwnedModel`        | Associates models with an owning user                            |
| `TenantModel`       | Enables multi-tenant isolation                                   |

### Example Usage

```python
from core.models import BaseModel

class Product(BaseModel):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
```
# 📜 Audit Logging

## 🔐 Key Features

- Automatic logging of all create, update, and delete operations
- Captures user, action type, IP address, timestamp, and object metadata
- Filterable via API or Django Admin
- Configurable and extensible


```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "timestamp": "2023-01-01T12:00:00Z",
  "user": {
    "id": 1,
    "username": "admin"
  },
  "action": "CREATE",
  "object_type": "Product",
  "object_id": "123e4567-e89b-12d3-a456-426614174000",
  "ip_address": "192.168.1.1",
  "metadata": {
    "field": "value"
  }
}
```


## Viewing Logs
Admin Panel: via Django Admin

API: GET /api/v1/core/audit-logs/

## API Endpoints
| Endpoint | Method | Description | Permissions |
| --- | --- | --- | --- |
| /core/audit-logs/ | GET | List all audit logs | Admin only |
| /core/audit-logs/<uuid>/ | GET | Retrieve specific audit log | Admin only |
| /core/health/ | GET | System health check | Public |
| /core/example-models/ | CRUD | Sample endpoints (for testing) | Authenticated users |

### Parameters

- `request` (HttpRequest, optional): The request object
- `user` (User, optional): Performing user  
- `obj` (Model instance, optional): Target object
- `metadata` (dict, optional): Additional data

## Testing

Run the test suite:

```bash
python manage.py test core.tests --verbosity=2
```

### Coverage Areas

- Base model behaviors
- Signal handling and audit log creation
- Serializer validation and constraints  
- View and API access controls
- Utility function outputs


### Directory  Structure



```
core
├── README.md
├── __init__.py
├── __pycache__
│   ├── __init__.cpython-310.pyc
│   ├── admin.cpython-310.pyc
│   ├── apps.cpython-310.pyc
│   └── models.cpython-310.pyc
├── admin.py
├── apps.py
├── middleware.py
├── migrations
│   ├── __init__.py
│   └── __pycache__
├── models.py
├── serializers.py
├── signals.py
├── tests
│   ├── test_models.py
│   ├── test_serializers.py
│   ├── test_signals.py
│   ├── test_utils.py
│   └── test_views.py
├── tests.py
├── urls.py
├── utils.py
└── views.py

```
