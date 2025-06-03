# AI Integrations API Documentation

Base URL: [https://yourdomain.com/api/ai/](https://yourdomain.com/api/ai/)
Authentication: Bearer Token (JWT)
Required Headers:

```json
{
  "Authorization": "Bearer <your_jwt_token>",
  "Content-Type": "application/json"
}
```

## 1. AI Services

### List/Create AI Services
Endpoint: GET/POST /services/
Description: List all AI services or create a new one.

#### Query Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| tenant_id | int  | Yes      | Filter services by tenant |

#### Request Body (POST)
```json
{
  "name": "Survivor Support NLP",
  "service_type": "OPENAI",
  "api_key": "sk-your-openai-key",
  "is_active": true,
  "tenant_id": 1,
  "config": {"temperature": 0.7}
}
```

#### Response (200 OK)
```json
{
  "id": 1,
  "name": "Survivor Support NLP",
  "service_type": "OPENAI",
  "is_active": true,
  "tenant": {"id": 1, "name": "Test Org"},
  "models": [],
  "created_at": "2023-11-20T12:00:00Z",
  "updated_at": "2023-11-20T12:00:00Z"
}
```

### Retrieve/Update/Delete AI Service
Endpoint: GET/PUT/DELETE /services/{id}/

#### Response (200 OK - GET)
Same as POST /services/, but includes nested models.

#### Request Body (PUT)
```json
{
  "is_active": false,
  "config": {"max_tokens": 1000}
}
```

#### Response (204 No Content - DELETE)

## 2. AI Models

### List/Create AI Models
Endpoint: GET/POST /services/{service_id}/models/
Description: List or add models to an AI service.

#### Request Body (POST)
```json
{
  "model_name": "gpt-4",
  "is_default": true
}
```

#### Response (201 Created)
```json
{
  "id": 1,
  "model_name": "gpt-4",
  "is_default": true,
  "service": 1,
  "created_at": "2023-11-20T12:05:00Z",
  "updated_at": "2023-11-20T12:05:00Z"
}
```

## 3. Example Use Cases

### Enable OpenAI for a Tenant

#### Create Service:
```bash
POST /api/ai/services/
```
```json
{
  "name": "Crisis Chatbot",
  "service_type": "OPENAI",
  "api_key": "sk-...",
  "tenant_id": 1
}
```

#### Add Models:
```bash
POST /api/ai/services/1/models/
```
```json
{
  "model_name": "gpt-4",
  "is_default": true
}
```

#### Activate Service:
```bash
PUT /api/ai/services/1/
```
```json
{"is_active": true}
```

## 4. Error Responses
| Code | Error | Description |
|------|-------|-------------|
| 400 | Bad Request | Invalid service_type or missing fields |
| 403 | Forbidden | User lacks permissions for the tenant |
| 404 | Not Found | Tenant or service not found |

## 5. OpenAPI (Swagger) Integration

Add to your settings.py:

```python
INSTALLED_APPS += ['drf_spectacular']
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}
```

Generate schema:

```bash
python manage.py spectacular --file schema.yml
```

View docs at /api/docs/ (after setting up drf-spectacular).