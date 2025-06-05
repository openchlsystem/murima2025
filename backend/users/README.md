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
- UI Screens
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
curl -X POST http://localhost:8000/api/auth/register/ \
-H "Content-Type: application/json" \
-d '{"username": "admin", "password": "admin123"}'
```

## API Endpoints

### Users

| Endpoint | Method | Description | Permissions |
|----------|--------|-------------|-------------|
| /api/auth/register/ | POST | Register new user | Public |
| /api/auth/otp/request/ | POST | Request OTP | Public |
| /api/auth/otp/verify/ | POST | Verify OTP | Public |
| /api/auth/token/refresh/ | POST | Refresh token | Public |
| /api/auth/token/verify/ | POST | Verify token | Public |
| /api/auth/users/ | GET | List all users | Admin |
| /api/auth/users/ | POST | Create a user | Admin |
| /api/auth/users/{id}/ | GET | Retrieve a user | Admin |
| /api/auth/users/{id}/ | PUT | Update a user | Admin |
| /api/auth/users/{id}/ | DELETE | Delete a user | Admin |

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
| /api/auth/roles/ | GET | List all roles | Admin |
| /api/auth/roles/ | POST | Create a role | Admin |
| /api/auth/roles/{id}/ | GET | Retrieve a role | Admin |
| /api/auth/roles/{id}/ | PUT | Update a role | Admin |
| /api/auth/roles/{id}/ | DELETE | Delete a role | Admin |

Fields:

```json
{
 "name": "string",
 "permissions": "array (IDs)",
 "tenant": "int (auto-set)"
}
```
## UI Screens

The front-end Vue 3 interface should provide the following key screens to interact with the Users API:

**1. Login Screen**
  - Allow users to authenticate with username/email/phone and password, triggering OTP if enabled.
  - Key components: Input fields for username and password, login button, forgot password link.

**2. OTP Verification Screen**
  - Prompt users to enter OTP sent via Email, SMS, or WhatsApp. Includes resend OTP option.
  - Key components: OTP input, delivery method notice, verify and resend buttons.

**3. Registration Screen**
  - Register new users with fields for username, email, phone, password, tenant selection, and role assignment.
  - Key components: Form inputs for user details and role/tenant selectors, submit button.

**4. Forgot Password + Reset OTP Screen**
  - Request password reset by entering email or phone, then verify OTP and set new password.
  - Key components: Input for email/phone, OTP entry, new password input, reset button.

**5. User Management Screen (Admin Panel)**
  - Admins can list, filter, create, edit, and deactivate users.
  - Key components: User table, filters by role and tenant, active status toggle, edit and add user modals.

**6. Role Management Screen**
  - Admins can create and assign roles with specific permissions.
  - Key components: Roles list, multi-select permissions, add/edit role forms.

**7. Profile & Settings Screen**
  - Users can view and update their profile and change passwords.
  - Key components: Display user info, edit profile form, password change inputs.

**8. Session Management Screen (Optional)**
  - View active sessions and allow users to terminate other sessions.
  - Key components: List active sessions with device info, logout buttons.
## Examples

1. Create a User

```bash
curl -X POST http://localhost:8000/api/auth/users/ \
-H "Content-Type: application/json" \
-H "Authorization: Bearer _token_" \
-d '{
 "username": "agent1",
 "password": "secure123",
 "email": "agent1@tenant.com",
 "is_verified": true
}'
```

2. Assign Permissions to a Role

```bash
curl -X PUT http://localhost:8000/api/auth/roles/1/ \
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
