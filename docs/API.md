# API Documentation

## 1. API Overview and Standards

### 1.1 Introduction

The Murima2025 platform provides a comprehensive set of RESTful APIs that enable integration with the system's core functionality. These APIs allow external applications to interact with case management, communication channels, authentication, and other services provided by the platform.

### 1.2 API Design Principles

The Murima2025 APIs adhere to the following design principles:

- **REST-based Architecture**: Resource-oriented design with standard HTTP methods
- **Consistency**: Uniform patterns for endpoints, parameters, and responses
- **Simplicity**: Straightforward, intuitive interfaces
- **Security**: Robust authentication and authorization
- **Performance**: Optimized for speed and efficiency
- **Versioning**: Clear versioning strategy to support evolution
- **Documentation**: Comprehensive and up-to-date documentation

### 1.3 Base URL

All API requests are made to the following base URL:

```
https://{tenant-subdomain}.murima2025.com/api/v1/
```

For on-premises deployments, the base URL will depend on your local configuration.

### 1.4 HTTP Methods

The API uses standard HTTP methods to perform operations on resources:

| Method | Description |
|--------|-------------|
| GET | Retrieve a resource or collection of resources |
| POST | Create a new resource |
| PUT | Update an existing resource (full update) |
| PATCH | Update an existing resource (partial update) |
| DELETE | Delete a resource |

### 1.5 Content Types

- Requests with a body should specify the content type using the `Content-Type` header:
  ```
  Content-Type: application/json
  ```

- Responses are returned in JSON format:
  ```
  Content-Type: application/json
  ```

### 1.6 Date and Time Format

All date and time values are returned in ISO 8601 format in UTC timezone:

```
YYYY-MM-DDTHH:MM:SSZ
```

Example: `2025-06-02T16:06:38Z`

## 2. Authentication and Authorization

### 2.1 Authentication Methods

The API supports multiple authentication methods:

#### 2.1.1 JWT Bearer Token

Most API requests should include a JWT token in the Authorization header:

```
Authorization: Bearer {token}
```

To obtain a JWT token, use the authentication endpoint:

```
POST /auth/login
```

Request body:
```json
{
  "username": "user@example.com",
  "password": "yourpassword"
}
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 3600
}
```

#### 2.1.2 API Key Authentication

For service-to-service integration, you can use API key authentication:

```
X-API-Key: your-api-key
```

API keys can be generated and managed in the administration console.

#### 2.1.3 OAuth 2.0

For third-party applications, OAuth 2.0 integration is supported:

- Authorization Code Flow: For web applications
- PKCE Flow: For mobile applications
- Client Credentials Flow: For service-to-service integration

OAuth endpoints:
```
/oauth/authorize
/oauth/token
/oauth/revoke
```

### 2.2 Authorization

Access to resources is controlled through role-based access control (RBAC):

- Each user is assigned one or more roles
- Roles are granted permissions to perform operations on resources
- API endpoints check permissions before allowing access
- Tenant isolation ensures users can only access their own tenant's data

### 2.3 Token Management

#### 2.3.1 Token Refresh

When an access token expires, you can obtain a new one using the refresh token:

```
POST /auth/refresh
```

Request body:
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 3600
}
```

#### 2.3.2 Token Invalidation

To log out and invalidate tokens:

```
POST /auth/logout
```

Request header:
```
Authorization: Bearer {token}
```

## 3. Endpoint Documentation

### 3.1 Authentication & Authorization

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/auth/login` | POST | Authenticate user credentials |
| `/auth/refresh` | POST | Refresh access token |
| `/auth/logout` | POST | Invalidate current session |
| `/auth/mfa/setup` | POST | Configure multi-factor authentication |
| `/auth/mfa/verify` | POST | Verify MFA code |
| `/users` | GET | List users |
| `/users/{id}` | GET | Get user details |
| `/users` | POST | Create new user |
| `/users/{id}` | PUT | Update user |
| `/users/{id}` | DELETE | Delete user |
| `/roles` | GET | List roles |
| `/roles/{id}` | GET | Get role details |
| `/roles` | POST | Create new role |
| `/roles/{id}` | PUT | Update role |
| `/roles/{id}` | DELETE | Delete role |
| `/permissions` | GET | List permissions |

### 3.2 Case Management

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/cases` | GET | List cases |
| `/cases` | POST | Create new case |
| `/cases/{id}` | GET | Get case details |
| `/cases/{id}` | PUT | Update case |
| `/cases/{id}` | DELETE | Delete case |
| `/cases/{id}/history` | GET | Get case history |
| `/cases/{id}/documents` | GET | List case documents |
| `/cases/{id}/documents` | POST | Add document to case |
| `/cases/{id}/documents/{docId}` | GET | Get document details |
| `/cases/{id}/documents/{docId}` | DELETE | Delete document |
| `/cases/{id}/notes` | GET | List case notes |
| `/cases/{id}/notes` | POST | Add note to case |
| `/cases/{id}/notes/{noteId}` | PUT | Update note |
| `/cases/{id}/notes/{noteId}` | DELETE | Delete note |
| `/cases/{id}/tasks` | GET | List case tasks |
| `/cases/{id}/tasks` | POST | Add task to case |
| `/cases/{id}/tasks/{taskId}` | PUT | Update task |
| `/cases/{id}/tasks/{taskId}` | DELETE | Delete task |
| `/cases/{id}/related` | GET | List related cases |
| `/cases/{id}/related/{relatedId}` | POST | Link cases |
| `/cases/{id}/related/{relatedId}` | DELETE | Unlink cases |

### 3.3 Communications

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/communications` | GET | List communications |
| `/communications/voice/call` | POST | Initiate voice call |
| `/communications/voice/status` | GET | Get call status |
| `/communications/sms/send` | POST | Send SMS message |
| `/communications/whatsapp/send` | POST | Send WhatsApp message |
| `/communications/email/send` | POST | Send email |
| `/communications/chat/message` | POST | Send chat message |
| `/communications/inbox` | GET | Access unified inbox |
| `/communications/templates` | GET | List message templates |
| `/communications/templates` | POST | Create message template |
| `/communications/templates/{id}` | PUT | Update message template |
| `/communications/templates/{id}` | DELETE | Delete message template |

### 3.4 AI Services

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/ai/transcribe` | POST | Speech-to-text transcription |
| `/ai/analyze-sentiment` | POST | Sentiment analysis |
| `/ai/summarize` | POST | Text summarization |
| `/ai/translate` | POST | Language translation |
| `/ai/detect-intent` | POST | Intent classification |
| `/ai/detect-entities` | POST | Entity recognition |
| `/ai/chatbot/reply` | POST | Chatbot response generation |
| `/ai/services` | GET | List available AI services |
| `/ai/services/{id}/toggle` | PUT | Enable/disable AI service |

### 3.5 Configuration

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/config/tenants/{id}` | GET | Get tenant configuration |
| `/config/tenants/{id}` | PUT | Update tenant configuration |
| `/config/features` | GET | List feature toggles |
| `/config/features/{id}` | PUT | Update feature toggle |
| `/config/workflows` | GET | List workflows |
| `/config/workflows` | POST | Create workflow |
| `/config/workflows/{id}` | GET | Get workflow details |
| `/config/workflows/{id}` | PUT | Update workflow |
| `/config/workflows/{id}` | DELETE | Delete workflow |
| `/config/forms` | GET | List forms |
| `/config/forms` | POST | Create form |
| `/config/forms/{id}` | GET | Get form details |
| `/config/forms/{id}` | PUT | Update form |
| `/config/forms/{id}` | DELETE | Delete form |

## 4. Request/Response Formats

### 4.1 Common Request Parameters

#### 4.1.1 Pagination

List endpoints support pagination using the following query parameters:

- `page`: Page number (default: 1)
- `limit`: Items per page (default: 20, max: 100)

Example:
```
GET /cases?page=2&limit=50
```

#### 4.1.2 Sorting

- `sort`: Field to sort by
- `order`: Sort order (`asc` or `desc`)

Example:
```
GET /cases?sort=created_at&order=desc
```

#### 4.1.3 Filtering

Filters can be applied using query parameters:

Example:
```
GET /cases?status=open&priority=high
```

Complex filters can be applied using a JSON filter parameter:

Example:
```
GET /cases?filter={"status":{"$in":["open","pending"]},"priority":"high"}
```

#### 4.1.4 Field Selection

You can specify which fields to include in the response:

Example:
```
GET /cases?fields=id,title,status,priority
```

### 4.2 Response Format

All API responses follow a consistent format:

#### 4.2.1 Success Response (Single Resource)

```json
{
  "data": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "attribute1": "value1",
    "attribute2": "value2",
    ...
  }
}
```

#### 4.2.2 Success Response (Resource Collection)

```json
{
  "data": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "attribute1": "value1",
      "attribute2": "value2",
      ...
    },
    {
      "id": "223e4567-e89b-12d3-a456-426614174000",
      "attribute1": "value1",
      "attribute2": "value2",
      ...
    }
  ],
  "pagination": {
    "total": 100,
    "page": 2,
    "limit": 10,
    "pages": 10
  }
}
```

#### 4.2.3 Error Response

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": [
      {
        "field": "field_name",
        "message": "Field-specific error message"
      }
    ]
  }
}
```

## 5. Error Handling

### 5.1 HTTP Status Codes

The API uses standard HTTP status codes to indicate the success or failure of a request:

| Status Code | Description |
|-------------|-------------|
| 200 | OK - The request was successful |
| 201 | Created - A new resource was successfully created |
| 204 | No Content - The request was successful, but there is no representation to return |
| 400 | Bad Request - The request could not be understood or was missing required parameters |
| 401 | Unauthorized - Authentication failed or user doesn't have permissions |
| 403 | Forbidden - Access denied |
| 404 | Not Found - Resource not found |
| 409 | Conflict - Request could not be completed due to a conflict |
| 422 | Unprocessable Entity - The request was well-formed but was unable to be followed due to semantic errors |
| 429 | Too Many Requests - Rate limit exceeded |
| 500 | Internal Server Error - Something went wrong on the server |

### 5.2 Error Codes

The API returns specific error codes that provide more detail about what went wrong:

| Error Code | Description |
|------------|-------------|
| `AUTH_INVALID_CREDENTIALS` | The provided credentials are invalid |
| `AUTH_TOKEN_EXPIRED` | The authentication token has expired |
| `AUTH_INSUFFICIENT_PERMISSIONS` | The user does not have the required permissions |
| `RESOURCE_NOT_FOUND` | The requested resource was not found |
| `VALIDATION_ERROR` | The request data failed validation |
| `RATE_LIMIT_EXCEEDED` | API rate limit has been exceeded |
| `TENANT_NOT_FOUND` | The specified tenant was not found |
| `CONFLICT_ERROR` | The request conflicts with the current state of the resource |
| `INTERNAL_ERROR` | An unexpected error occurred on the server |

### 5.3 Validation Errors

Validation errors include details about which fields failed validation and why:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "The request data failed validation",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format"
      },
      {
        "field": "phone",
        "message": "Phone number is required"
      }
    ]
  }
}
```

## 6. Rate Limiting

### 6.1 Rate Limit Headers

The API includes rate limit information in the response headers:

```
X-Rate-Limit-Limit: 100
X-Rate-Limit-Remaining: 95
X-Rate-Limit-Reset: 1591234567
```

- `X-Rate-Limit-Limit`: The maximum number of requests allowed in the current time window
- `X-Rate-Limit-Remaining`: The number of requests remaining in the current time window
- `X-Rate-Limit-Reset`: The time at which the rate limit window resets, in Unix timestamp format

### 6.2 Rate Limit Tiers

Rate limits are applied based on the authentication method and subscription tier:

| Tier | Requests per Minute | Burst Capacity |
|------|---------------------|----------------|
| Basic | 60 | 100 |
| Standard | 300 | 500 |
| Premium | 1,000 | 2,000 |
| Enterprise | Custom | Custom |

### 6.3 Rate Limit Exceeded Response

When the rate limit is exceeded, the API returns a 429 Too Many Requests response:

```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "API rate limit has been exceeded",
    "details": {
      "limit": 100,
      "reset_at": 1591234567
    }
  }
}
```

### 6.4 Best Practices for Rate Limit Management

- Implement exponential backoff retry logic
- Cache responses where appropriate
- Use bulk operations instead of multiple single-resource operations
- Monitor rate limit headers and adjust request rates accordingly
- Consider upgrading your subscription tier if you consistently hit rate limits

## 7. Versioning Strategy

### 7.1 API Versioning Approach

The Murima2025 API uses URL path versioning to ensure backward compatibility as the API evolves:

```
https://{tenant-subdomain}.murima2025.com/api/v1/cases
```

New major versions will be introduced when there are breaking changes:

```
https://{tenant-subdomain}.murima2025.com/api/v2/cases
```

### 7.2 Version Lifecycle

Each API version goes through the following lifecycle stages:

1. **Preview**: Early access for testing and feedback
2. **General Availability**: Fully supported and recommended for production use
3. **Deprecated**: Still available but no longer recommended for use
4. **Sunset**: No longer available

### 7.3 Version Support Policy

- Major versions are supported for a minimum of 24 months after the release of the next major version
- When a version is deprecated, a migration guide will be provided
- At least 6 months notice will be given before a version is sunset

### 7.4 API Changelog

Changes to the API are documented in the changelog available at:

```
https://{tenant-subdomain}.murima2025.com/api/changelog
```

## 8. Examples and Usage Guidelines

### 8.1 Authentication Example

#### Request:
```http
POST /api/v1/auth/login HTTP/1.1
Host: example.murima2025.com
Content-Type: application/json

{
  "username": "user@example.com",
  "password": "yourpassword"
}
```

#### Response:
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 3600
}
```

### 8.2 Create a Case Example

#### Request:
```http
POST /api/v1/cases HTTP/1.1
Host: example.murima2025.com
Content-Type: application/json
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

{
  "title": "Customer unable to access account",
  "description": "Customer reports being unable to log in to their account after password reset.",
  "priority": "medium",
  "case_type_id": "5f8b5a6c-d431-4b6e-a4c1-c5c08c2f5d1b",
  "custom_fields": {
    "customer_id": "CUS-12345",
    "platform": "mobile_app",
    "version": "2.3.1"
  }
}
```

#### Response:
```http
HTTP/1.1 201 Created
Content-Type: application/json

{
  "data": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "case_number": "CS-2025-06-02-1234",
    "title": "Customer unable to access account",
    "description": "Customer reports being unable to log in to their account after password reset.",
    "status": "open",
    "priority": "medium",
    "case_type_id": "5f8b5a6c-d431-4b6e-a4c1-c5c08c2f5d1b",
    "created_by": "98765432-1234-5678-9012-345678901234",
    "assigned_to": null,
    "created_at": "2025-06-02T16:06:38Z",
    "updated_at": "2025-06-02T16:06:38Z",
    "custom_fields": {
      "customer_id": "CUS-12345",
      "platform": "mobile_app",
      "version": "2.3.1"
    }
  }
}
```

### 8.3 Send a WhatsApp Message Example

#### Request:
```http
POST /api/v1/communications/whatsapp/send HTTP/1.1
Host: example.murima2025.com
Content-Type: application/json
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

{
  "case_id": "123e4567-e89b-12d3-a456-426614174000",
  "to": "+15551234567",
  "message": "Hello, this is regarding your recent support request. How may I assist you today?",
  "template_id": "welcome_message",
  "variables": {
    "name": "John"
  }
}
```

#### Response:
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "data": {
    "id": "223e4567-e89b-12d3-a456-426614174000",
    "case_id": "123e4567-e89b-12d3-a456-426614174000",
    "to": "+15551234567",
    "message": "Hello, this is regarding your recent support request. How may I assist you today?",
    "status": "sent",
    "channel": "whatsapp",
    "external_id": "wamid.HBgLMTU1NTEyMzQ1NjcVAgASGBQzRUE3NTYwQjM1N0JFOTk5OTk5OQA=",
    "created_at": "2025-06-02T16:10:38Z"
  }
}
```

### 8.4 AI Sentiment Analysis Example

#### Request:
```http
POST /api/v1/ai/analyze-sentiment HTTP/1.1
Host: example.murima2025.com
Content-Type: application/json
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

{
  "text": "I am extremely frustrated with the poor service I received. My issue has not been resolved for weeks!",
  "language": "en",
  "provider": "azure"
}
```

#### Response:
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "data": {
    "sentiment": "negative",
    "confidence": 0.92,
    "scores": {
      "positive": 0.02,
      "neutral": 0.06,
      "negative": 0.92
    },
    "entities": [
      {
        "text": "service",
        "sentiment": "negative",
        "confidence": 0.88
      },
      {
        "text": "issue",
        "sentiment": "negative",
        "confidence": 0.90
      }
    ],
    "provider": "azure",
    "language": "en"
  }
}
```

### 8.5 List Cases with Filtering and Pagination Example

#### Request:
```http
GET /api/v1/cases?status=open&priority=high&page=2&limit=10 HTTP/1.1
Host: example.murima2025.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

#### Response:
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "data": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "case_number": "CS-2025-06-02-1234",
      "title": "Customer unable to access account",
      "status": "open",
      "priority": "high",
      "created_at": "2025-06-02T16:06:38Z",
      "assigned_to": "98765432-1234-5678-9012-345678901234"
    },
    // More cases...
  ],
  "pagination": {
    "total": 45,
    "page": 2,
    "limit": 10,
    "pages": 5
  }
}
```

### 8.6 Error Handling Example

#### Request:
```http
POST /api/v1/cases HTTP/1.1
Host: example.murima2025.com
Content-Type: application/json
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

{
  "title": "",
  "priority": "super-high",
  "case_type_id": "invalid"
}
```

#### Response:
```http
HTTP/1.1 422 Unprocessable Entity
Content-Type: application/json

{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "The request data failed validation",
    "details": [
      {
        "field": "title",
        "message": "Title is required"
      },
      {
        "field": "priority",
        "message": "Invalid priority value. Valid values are: low, medium, high"
      },
      {
        "field": "case_type_id",
        "message": "Invalid case type ID"
      }
    ]
  }
}
```

### 8.7 Best Practices

#### 8.7.1 API Usage Guidelines

- Always use HTTPS for API calls
- Implement proper error handling and retry logic
- Store API keys and tokens securely
- Minimize the number of API calls by using filtering, pagination, and field selection
- Respect rate limits and implement backoff strategies
- Keep authentication tokens up to date

#### 8.7.2 Performance Optimization

- Use batch operations where available
- Cache responses when appropriate
- Use compression for large payloads
- Implement conditional requests with ETags when supported
- Request only the fields you need using the fields parameter

#### 8.7.3 Security Recommendations

- Rotate API keys regularly
- Use the principle of least privilege for API permissions
- Implement IP restrictions for sensitive operations
- Monitor API usage for suspicious activity
- Keep client libraries and dependencies up to date

## 9. SDKs and Client Libraries

### 9.1 Official SDKs

The following official SDKs are available:

- JavaScript/TypeScript: [npm package](https://www.npmjs.com/package/murima2025-sdk)
- Python: [PyPI package](https://pypi.org/project/murima2025/)
- Java: [Maven repository](https://mvnrepository.com/artifact/com.murima2025/api-client)
- C#: [NuGet package](https://www.nuget.org/packages/Murima2025.Client/)

### 9.2 Community Libraries

- PHP: [GitHub repository](https://github.com/community/murima2025-php)
- Ruby: [RubyGems](https://rubygems.org/gems/murima2025)
- Go: [GitHub repository](https://github.com/community/murima2025-go)

## 10. Support and Resources

### 10.1 Developer Portal

Visit our developer portal for additional resources, tutorials, and tools:

```
https://developers.murima2025.com
```

### 10.2 API Status

Check the current API status and any ongoing incidents:

```
https://status.murima2025.com
```

### 10.3 Support Channels

- Developer Support: [developers@murima2025.com](mailto:developers@murima2025.com)
- Community Forum: [https://community.murima2025.com](https://community.murima2025.com)
- Stack Overflow: Tag your questions with [murima2025-api](https://stackoverflow.com/questions/tagged/murima2025-api)

### 10.4 Feature Requests and Bug Reports

Submit feature requests and bug reports through our GitHub repository:

```
https://github.com/murima2025/api-feedback/issues
```

