# Database Design Document

## 1. Database Overview

### 1.1 Introduction

The Murima2025 system employs a hybrid data storage approach to effectively handle different types of data and access patterns. This document outlines the database architecture, data models, optimization strategies, and other important aspects of the data layer design.

### 1.2 Database Technology Stack

The system uses the following database technologies:

| Database Type | Technology | Primary Use |
|---------------|------------|-------------|
| Relational Database | PostgreSQL 14+ | Structured transactional data, complex relationships |
| Document Database | MongoDB 6.0+ | Unstructured data, custom fields, document storage |
| Cache Layer | Redis 7.0+ | Session data, frequently accessed data, real-time counters |
| Search Engine | Elasticsearch 8.0+ | Full-text search, analytics, log storage |
| Message Queue | RabbitMQ 3.10+ / Kafka 3.3+ | Event messaging, asynchronous processing |

### 1.3 Multi-Tenancy Approach

The system implements a multi-tenant architecture with tenant isolation at the data level:

- **Shared Database, Separate Schemas**: Each tenant has its own schema within a shared PostgreSQL database
- **Collection Prefixing**: For MongoDB, collections use tenant-specific prefixes
- **Tenant Identifier**: All data includes a tenant identifier field
- **Row-Level Security**: PostgreSQL row-level security policies enforce tenant isolation
- **Query Filtering**: Application-level tenant filtering as an additional security layer

### 1.4 High-Level Data Flow

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Client Apps    │────▶│  API Services   │────▶│ Data Access Layer│
└─────────────────┘     └─────────────────┘     └────────┬────────┘
                                                         │
                                                         ▼
┌──────────────────────────────────────────────────────────────────────┐
│                        Data Storage Layer                             │
│                                                                      │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌──────────┐  │
│  │ PostgreSQL  │   │   MongoDB   │   │    Redis    │   │Elasticsearch│
│  │(Structured) │   │(Document)   │   │  (Cache)    │   │ (Search)  │  │
│  └─────────────┘   └─────────────┘   └─────────────┘   └──────────┘  │
└──────────────────────────────────────────────────────────────────────┘
```

## 2. Data Models and Schemas

### 2.1 PostgreSQL Schema

#### 2.1.1 Tenant Schema

Each tenant has a dedicated schema in PostgreSQL named after their tenant ID (e.g., `tenant_123456`). The system also maintains a global schema for shared data.

```sql
-- Create tenant schema
CREATE SCHEMA tenant_123456;

-- Enable row-level security
ALTER TABLE tenant_123456.cases ENABLE ROW LEVEL SECURITY;

-- Create policy for tenant isolation
CREATE POLICY tenant_isolation ON tenant_123456.cases
    USING (tenant_id = current_setting('app.current_tenant_id')::uuid);
```

#### 2.1.2 Core Tables

The following tables are created for each tenant:

**Users Table**
```sql
CREATE TABLE tenant_123456.users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES public.tenants(id),
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    role VARCHAR(50) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'active',
    last_login TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    permissions JSONB,
    preferences JSONB,
    metadata JSONB,
    CONSTRAINT users_email_tenant_unique UNIQUE (email, tenant_id),
    CONSTRAINT users_username_tenant_unique UNIQUE (username, tenant_id)
);

CREATE INDEX idx_users_tenant_id ON tenant_123456.users(tenant_id);
CREATE INDEX idx_users_email ON tenant_123456.users(email);
CREATE INDEX idx_users_status ON tenant_123456.users(status);
```

**Teams Table**
```sql
CREATE TABLE tenant_123456.teams (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES public.tenants(id),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    metadata JSONB,
    CONSTRAINT teams_name_tenant_unique UNIQUE (name, tenant_id)
);

CREATE INDEX idx_teams_tenant_id ON tenant_123456.teams(tenant_id);
```

**Team Members Table**
```sql
CREATE TABLE tenant_123456.team_members (
    team_id UUID NOT NULL REFERENCES tenant_123456.teams(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES tenant_123456.users(id) ON DELETE CASCADE,
    role VARCHAR(50) NOT NULL DEFAULT 'member',
    joined_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    PRIMARY KEY (team_id, user_id)
);

CREATE INDEX idx_team_members_user_id ON tenant_123456.team_members(user_id);
```

**Case Types Table**
```sql
CREATE TABLE tenant_123456.case_types (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES public.tenants(id),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    form_definition JSONB NOT NULL,
    validation_rules JSONB,
    workflow_id UUID,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    CONSTRAINT case_types_name_tenant_unique UNIQUE (name, tenant_id)
);

CREATE INDEX idx_case_types_tenant_id ON tenant_123456.case_types(tenant_id);
CREATE INDEX idx_case_types_is_active ON tenant_123456.case_types(is_active);
```

**Cases Table**
```sql
CREATE TABLE tenant_123456.cases (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES public.tenants(id),
    case_number VARCHAR(50) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(50) NOT NULL DEFAULT 'open',
    priority VARCHAR(20) NOT NULL DEFAULT 'medium',
    case_type_id UUID NOT NULL REFERENCES tenant_123456.case_types(id),
    workflow_id UUID,
    current_stage_id UUID,
    created_by UUID NOT NULL REFERENCES tenant_123456.users(id),
    assigned_to UUID REFERENCES tenant_123456.users(id),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    due_date TIMESTAMP WITH TIME ZONE,
    custom_fields JSONB,
    tags TEXT[],
    metadata JSONB,
    CONSTRAINT cases_case_number_unique UNIQUE (case_number, tenant_id)
);

CREATE INDEX idx_cases_tenant_id ON tenant_123456.cases(tenant_id);
CREATE INDEX idx_cases_status ON tenant_123456.cases(status);
CREATE INDEX idx_cases_priority ON tenant_123456.cases(priority);
CREATE INDEX idx_cases_case_type_id ON tenant_123456.cases(case_type_id);
CREATE INDEX idx_cases_assigned_to ON tenant_123456.cases(assigned_to);
CREATE INDEX idx_cases_created_at ON tenant_123456.cases(created_at);
CREATE INDEX idx_cases_due_date ON tenant_123456.cases(due_date);
CREATE INDEX idx_cases_tags ON tenant_123456.cases USING GIN(tags);
CREATE INDEX idx_cases_custom_fields ON tenant_123456.cases USING GIN(custom_fields);
```

**Channels Table**
```sql
CREATE TABLE tenant_123456.channels (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES public.tenants(id),
    name VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL,
    configuration JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    CONSTRAINT channels_name_tenant_unique UNIQUE (name, tenant_id)
);

CREATE INDEX idx_channels_tenant_id ON tenant_123456.channels(tenant_id);
CREATE INDEX idx_channels_type ON tenant_123456.channels(type);
CREATE INDEX idx_channels_is_active ON tenant_123456.channels(is_active);
```

**Interactions Table**
```sql
CREATE TABLE tenant_123456.interactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES public.tenants(id),
    case_id UUID NOT NULL REFERENCES tenant_123456.cases(id),
    channel_id UUID NOT NULL REFERENCES tenant_123456.channels(id),
    user_id UUID REFERENCES tenant_123456.users(id),
    direction VARCHAR(20) NOT NULL,
    content TEXT,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    metadata JSONB,
    external_id VARCHAR(255),
    tags TEXT[]
);

CREATE INDEX idx_interactions_tenant_id ON tenant_123456.interactions(tenant_id);
CREATE INDEX idx_interactions_case_id ON tenant_123456.interactions(case_id);
CREATE INDEX idx_interactions_channel_id ON tenant_123456.interactions(channel_id);
CREATE INDEX idx_interactions_user_id ON tenant_123456.interactions(user_id);
CREATE INDEX idx_interactions_timestamp ON tenant_123456.interactions(timestamp);
CREATE INDEX idx_interactions_tags ON tenant_123456.interactions USING GIN(tags);
```

**Documents Table**
```sql
CREATE TABLE tenant_123456.documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES public.tenants(id),
    case_id UUID NOT NULL REFERENCES tenant_123456.cases(id),
    filename VARCHAR(255) NOT NULL,
    mime_type VARCHAR(100) NOT NULL,
    size BIGINT NOT NULL,
    storage_path VARCHAR(1024) NOT NULL,
    uploaded_by UUID NOT NULL REFERENCES tenant_123456.users(id),
    uploaded_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    metadata JSONB
);

CREATE INDEX idx_documents_tenant_id ON tenant_123456.documents(tenant_id);
CREATE INDEX idx_documents_case_id ON tenant_123456.documents(case_id);
CREATE INDEX idx_documents_uploaded_by ON tenant_123456.documents(uploaded_by);
CREATE INDEX idx_documents_is_deleted ON tenant_123456.documents(is_deleted);
```

**Tasks Table**
```sql
CREATE TABLE tenant_123456.tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES public.tenants(id),
    case_id UUID NOT NULL REFERENCES tenant_123456.cases(id),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    priority VARCHAR(20) NOT NULL DEFAULT 'medium',
    assigned_to UUID REFERENCES tenant_123456.users(id),
    created_by UUID NOT NULL REFERENCES tenant_123456.users(id),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    due_date TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    metadata JSONB
);

CREATE INDEX idx_tasks_tenant_id ON tenant_123456.tasks(tenant_id);
CREATE INDEX idx_tasks_case_id ON tenant_123456.tasks(case_id);
CREATE INDEX idx_tasks_status ON tenant_123456.tasks(status);
CREATE INDEX idx_tasks_assigned_to ON tenant_123456.tasks(assigned_to);
CREATE INDEX idx_tasks_due_date ON tenant_123456.tasks(due_date);
```

**Workflows Table**
```sql
CREATE TABLE tenant_123456.workflows (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES public.tenants(id),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    stages JSONB NOT NULL,
    transitions JSONB NOT NULL,
    actions JSONB,
    sla_definitions JSONB,
    CONSTRAINT workflows_name_tenant_unique UNIQUE (name, tenant_id)
);

CREATE INDEX idx_workflows_tenant_id ON tenant_123456.workflows(tenant_id);
CREATE INDEX idx_workflows_active ON tenant_123456.workflows(active);
```

### 2.2 MongoDB Collections

MongoDB is used for storing unstructured and semi-structured data with flexible schemas.

#### 2.2.1 Collection Naming Convention

Collections follow a naming convention that includes the tenant ID: `tenant_{tenant_id}_{collection_name}`

#### 2.2.2 Core Collections

**Custom Field Definitions**
```javascript
// tenant_123456_custom_field_definitions
{
  "_id": ObjectId("..."),
  "tenant_id": "UUID",
  "entity_type": "case", // case, interaction, user, etc.
  "field_name": "customer_satisfaction",
  "display_name": "Customer Satisfaction",
  "field_type": "select",
  "required": true,
  "default_value": "neutral",
  "options": [
    {"label": "Very Satisfied", "value": "very_satisfied"},
    {"label": "Satisfied", "value": "satisfied"},
    {"label": "Neutral", "value": "neutral"},
    {"label": "Unsatisfied", "value": "unsatisfied"},
    {"label": "Very Unsatisfied", "value": "very_unsatisfied"}
  ],
  "validation": {
    "type": "in",
    "values": ["very_satisfied", "satisfied", "neutral", "unsatisfied", "very_unsatisfied"]
  },
  "visibility_rules": {
    "case_type_ids": ["UUID1", "UUID2"],
    "roles": ["agent", "supervisor"]
  },
  "order": 1,
  "section": "feedback",
  "description": "Overall satisfaction level of the customer",
  "created_at": ISODate("2025-06-02T16:06:38Z"),
  "updated_at": ISODate("2025-06-02T16:06:38Z"),
  "is_active": true
}
```

**Case Notes**
```javascript
// tenant_123456_case_notes
{
  "_id": ObjectId("..."),
  "tenant_id": "UUID",
  "case_id": "UUID",
  "user_id": "UUID",
  "content": "Customer called to follow up on their request. I informed them that we're still investigating the issue.",
  "created_at": ISODate("2025-06-02T16:06:38Z"),
  "updated_at": ISODate("2025-06-02T16:06:38Z"),
  "is_internal": true,
  "tags": ["follow-up", "customer-contact"],
  "attachments": [
    {
      "id": "UUID",
      "filename": "call_recording.mp3",
      "mime_type": "audio/mpeg",
      "size": 2048576,
      "storage_path": "tenant_123456/case_xyz/recordings/call_2025_06_02.mp3"
    }
  ]
}
```

**Audit Logs**
```javascript
// tenant_123456_audit_logs
{
  "_id": ObjectId("..."),
  "tenant_id": "UUID",
  "entity_type": "case",
  "entity_id": "UUID",
  "action": "update",
  "user_id": "UUID",
  "timestamp": ISODate("2025-06-02T16:06:38Z"),
  "changes": [
    {
      "field": "status",
      "old_value": "open",
      "new_value": "in_progress"
    },
    {
      "field": "assigned_to",
      "old_value": null,
      "new_value": "UUID"
    }
  ],
  "ip_address": "192.168.1.1",
  "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...",
  "context": {
    "session_id": "UUID",
    "request_id": "UUID"
  }
}
```

**Message Templates**
```javascript
// tenant_123456_message_templates
{
  "_id": ObjectId("..."),
  "tenant_id": "UUID",
  "name": "Case Resolution Confirmation",
  "description": "Email template sent when a case is marked as resolved",
  "channel_type": "email",
  "subject": "Your case #{{case_number}} has been resolved",
  "content": "Dear {{customer_name}},\n\nWe're pleased to inform you that your case #{{case_number}} regarding \"{{case_title}}\" has been resolved.\n\nIf you have any further questions, please don't hesitate to contact us.\n\nThank you,\n{{agent_name}}\n{{company_name}}",
  "variables": ["customer_name", "case_number", "case_title", "agent_name", "company_name"],
  "created_by": "UUID",
  "created_at": ISODate("2025-06-02T16:06:38Z"),
  "updated_at": ISODate("2025-06-02T16:06:38Z"),
  "is_active": true,
  "tags": ["resolution", "email"],
  "category": "case_status"
}
```

**AI Results Cache**
```javascript
// tenant_123456_ai_results_cache
{
  "_id": ObjectId("..."),
  "tenant_id": "UUID",
  "service_type": "sentiment_analysis",
  "input_hash": "a1b2c3d4e5f6g7h8i9j0...",
  "result": {
    "sentiment": "negative",
    "confidence": 0.92,
    "scores": {
      "positive": 0.02,
      "neutral": 0.06,
      "negative": 0.92
    }
  },
  "provider": "azure",
  "created_at": ISODate("2025-06-02T16:06:38Z"),
  "expires_at": ISODate("2025-06-09T16:06:38Z")
}
```

### 2.3 Redis Data Structures

Redis is used for caching, session management, and real-time features.

#### 2.3.1 Key Naming Convention

Redis keys follow a consistent naming pattern: `{tenant_id}:{entity_type}:{entity_id}:{purpose}`

#### 2.3.2 Key Types and TTLs

| Key Pattern | Type | TTL | Purpose |
|-------------|------|-----|---------|
| `{tenant_id}:session:{session_id}` | Hash | 24 hours | User session data |
| `{tenant_id}:user:{user_id}:permissions` | Hash | 1 hour | User permissions cache |
| `{tenant_id}:case:{case_id}` | Hash | 30 minutes | Case data cache |
| `{tenant_id}:config:{config_key}` | String | 1 hour | Tenant configuration |
| `{tenant_id}:rate_limit:{ip_address}` | Sorted Set | 1 minute | API rate limiting |
| `{tenant_id}:online_users` | Sorted Set | N/A | Currently online users |
| `{tenant_id}:case:{case_id}:viewers` | Set | 5 minutes | Current case viewers |
| `{tenant_id}:notifications:{user_id}` | List | 30 days | User notifications |
| `{tenant_id}:locks:{resource_id}` | String | 30 seconds | Distributed locks |

#### 2.3.3 Sample Redis Structures

**User Session**
```
HMSET tenant_123456:session:abcd1234 
  user_id "98765432-1234-5678-9012-345678901234" 
  username "john.doe" 
  role "agent" 
  permissions "{"cases":["view","create","update"]}" 
  last_activity "2025-06-02T16:06:38Z"
EXPIRE tenant_123456:session:abcd1234 86400
```

**Rate Limiting**
```
ZADD tenant_123456:rate_limit:192.168.1.1 1685723198 "api_call_1"
ZADD tenant_123456:rate_limit:192.168.1.1 1685723199 "api_call_2"
ZCOUNT tenant_123456:rate_limit:192.168.1.1 1685723138 1685723198  # Count requests in the last minute
EXPIRE tenant_123456:rate_limit:192.168.1.1 60
```

**Online Users Tracking**
```
ZADD tenant_123456:online_users 1685723198 "98765432-1234-5678-9012-345678901234"
ZREMRANGEBYSCORE tenant_123456:online_users 0 1685723138  # Remove users inactive for more than 1 minute
ZRANGE tenant_123456:online_users 0 -1  # Get all online users
```

### 2.4 Elasticsearch Indices

Elasticsearch is used for full-text search, analytics, and log storage.

#### 2.4.1 Index Naming Convention

Indices follow a naming convention: `tenant-{tenant_id}-{entity_type}-{YYYY-MM}`

#### 2.4.2 Core Indices

**Cases Index**
```json
PUT /tenant-123456-cases-2025-06
{
  "settings": {
    "number_of_shards": 3,
    "number_of_replicas": 1,
    "analysis": {
      "analyzer": {
        "case_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": ["lowercase", "asciifolding", "stop", "snowball"]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "tenant_id": { "type": "keyword" },
      "id": { "type": "keyword" },
      "case_number": { "type": "keyword" },
      "title": { 
        "type": "text",
        "analyzer": "case_analyzer",
        "fields": {
          "keyword": { "type": "keyword", "ignore_above": 256 }
        }
      },
      "description": { "type": "text", "analyzer": "case_analyzer" },
      "status": { "type": "keyword" },
      "priority": { "type": "keyword" },
      "case_type_id": { "type": "keyword" },
      "case_type_name": { "type": "keyword" },
      "created_by": { "type": "keyword" },
      "assigned_to": { "type": "keyword" },
      "created_at": { "type": "date" },
      "updated_at": { "type": "date" },
      "due_date": { "type": "date" },
      "custom_fields": { "type": "object", "dynamic": true },
      "tags": { "type": "keyword" }
    }
  }
}
```

**Interactions Index**
```json
PUT /tenant-123456-interactions-2025-06
{
  "settings": {
    "number_of_shards": 3,
    "number_of_replicas": 1,
    "analysis": {
      "analyzer": {
        "interaction_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": ["lowercase", "asciifolding", "stop", "snowball"]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "tenant_id": { "type": "keyword" },
      "id": { "type": "keyword" },
      "case_id": { "type": "keyword" },
      "channel_id": { "type": "keyword" },
      "channel_type": { "type": "keyword" },
      "user_id": { "type": "keyword" },
      "direction": { "type": "keyword" },
      "content": { 
        "type": "text",
        "analyzer": "interaction_analyzer"
      },
      "sentiment_score": { "type": "float" },
      "timestamp": { "type": "date" },
      "tags": { "type": "keyword" }
    }
  }
}
```

**Audit Logs Index**
```json
PUT /tenant-123456-audit-logs-2025-06
{
  "settings": {
    "number_of_shards": 3,
    "number_of_replicas": 1
  },
  "mappings": {
    "properties": {
      "tenant_id": { "type": "keyword" },
      "entity_type": { "type": "keyword" },
      "entity_id": { "type": "keyword" },
      "action": { "type": "keyword" },
      "user_id": { "type": "keyword" },
      "timestamp": { "type": "date" },
      "changes": {
        "type": "nested",
        "properties": {
          "field": { "type": "keyword" },
          "old_value": { "type": "text", "fields": { "keyword": { "type": "keyword", "ignore_above": 256 } } },
          "new_value": { "type": "text", "fields": { "keyword": { "type": "keyword", "ignore_above": 256 } } }
        }
      },
      "ip_address": { "type": "ip" },
      "user_agent": { "type": "text" },
      "context": { "type": "object", "dynamic": true }
    }
  }
}
```

## 3. Entity Relationships

### 3.1 Entity Relationship Diagram

The following diagram illustrates the key entity relationships in the system:

```
┌────────────┐       ┌─────────────┐       ┌───────────┐
│   TENANT   │◄──1:n─┤    USER     │◄──n:n─┤   TEAM    │
└────────────┘       └─────────────┘       └───────────┘
      │1:n                 │n:1                │n:1
      │                    │                   │
      │                    │                   │
      ▼                    ▼                   ▼
┌────────────┐       ┌─────────────┐       ┌───────────┐
│ CASE_TYPE  │◄──1:n─┤    CASE     │──n:1──┤ WORKFLOW  │
└────────────┘       └─────────────┘       └───────────┘
                           │1:n                 │1:n
                           │                    │
                           │                    │
                           ▼                    ▼
┌────────────┐       ┌─────────────┐       ┌───────────┐
│  CHANNEL   │◄──1:n─┤ INTERACTION │       │   STAGE   │
└────────────┘       └─────────────┘       └───────────┘
                           │n:1                 │1:n
                           │                    │
                           │                    │
┌────────────┐       ┌─────────────┐       ┌───────────┐
│ ATTACHMENT │◄──n:1─┤  DOCUMENT   │       │ TRANSITION│
└────────────┘       └─────────────┘       └───────────┘
                           │n:1
                           │
                           │
                     ┌─────────────┐
                     │    TASK     │
                     └─────────────┘
```

### 3.2 Key Relationships

#### 3.2.1 Tenant to User
- A tenant has many users
- Each user belongs to exactly one tenant
- Tenant deletion cascades to users

#### 3.2.2 User to Team
- A user can belong to multiple teams
- A team can have multiple users
- This is a many-to-many relationship handled through the team_members junction table

#### 3.2.3 Case Type to Case
- A case type has many cases
- Each case belongs to exactly one case type
- Case types determine the form structure and workflow for cases

#### 3.2.4 Workflow to Case
- A workflow has many cases
- Each case follows one workflow
- Workflows define the stages and transitions a case can go through

#### 3.2.5 Case to Interaction
- A case has many interactions
- Each interaction belongs to exactly one case
- Interactions represent communications related to a case

#### 3.2.6 Channel to Interaction
- A channel has many interactions
- Each interaction occurs through exactly one channel
- Channels represent communication methods (email, SMS, voice, etc.)

#### 3.2.7 Case to Document
- A case has many documents
- Each document belongs to exactly one case
- Documents store files related to a case

#### 3.2.8 Case to Task
- A case has many tasks
- Each task belongs to exactly one case
- Tasks represent actionable items related to a case

### 3.3 Integrity Constraints

#### 3.3.1 Foreign Key Constraints
- All relationships are enforced through foreign key constraints
- Deletion of parent records is handled according to business rules (e.g., prevent, cascade, set null)

#### 3.3.2 Unique Constraints
- Tenant-scoped uniqueness (e.g., usernames must be unique within a tenant)
- Business identifiers (e.g., case numbers) must be unique

#### 3.3.3 Check Constraints
- Status and priority fields have check constraints to ensure valid values
- Date range validations (e.g., due_date > created_at)

## 4. Indexing Strategy

### 4.1 PostgreSQL Indexing

#### 4.1.1 Primary Keys
- All tables use UUID primary keys generated using `gen_random_uuid()` function
- UUID keys provide better distribution for sharding and avoid sequence hotspots

#### 4.1.2 Foreign Keys
- All foreign key columns are indexed to improve join performance
- Foreign keys referencing frequently accessed tables get composite indexes

#### 4.1.3 Common Query Patterns
The following indexes support common query patterns:

**Case Filtering Indexes**
```sql
-- For filtering cases by status and priority
CREATE INDEX idx_cases_status_priority ON tenant_123456.cases(tenant_id, status, priority);

-- For date range queries
CREATE INDEX idx_cases_created_at ON tenant_123456.cases(tenant_id, created_at);
CREATE INDEX idx_cases_due_date ON tenant_123456.cases(tenant_id, due_date);

-- For assignment queries
CREATE INDEX idx_cases_assigned_to ON tenant_123456.cases(tenant_id, assigned_to);
```

**Reporting Indexes**
```sql
-- For status reports by case type
CREATE INDEX idx_cases_case_type_status ON tenant_123456.cases(tenant_id, case_type_id, status);

-- For time-based metrics
CREATE INDEX idx_cases_created_at_status ON tenant_123456.cases(tenant_id, created_at, status);
```

#### 4.1.4 JSONB Indexing
For JSONB columns storing custom fields:

```sql
-- GIN index for full jsonb querying
CREATE INDEX idx_cases_custom_fields ON tenant_123456.cases USING GIN(custom_fields);

-- For commonly queried specific fields
CREATE INDEX idx_cases_custom_fields_customer_id ON tenant_123456.cases ((custom_fields->>'customer_id'));
```

#### 4.1.5 Full Text Search
```sql
-- Create a tsvector column for full text search
ALTER TABLE tenant_123456.cases ADD COLUMN search_vector tsvector;

-- Create a function to update the search vector
CREATE FUNCTION tenant_123456.cases_search_vector_update() RETURNS trigger AS $$
BEGIN
  NEW.search_vector := 
    setweight(to_tsvector('english', COALESCE(NEW.title, '')), 'A') ||
    setweight(to_tsvector('english', COALESCE(NEW.description, '')), 'B');
  RETURN NEW;
END
$$ LANGUAGE plpgsql;

-- Create a trigger to maintain the search vector
CREATE TRIGGER cases_search_vector_update
BEFORE INSERT OR UPDATE ON tenant_123456.cases
FOR EACH ROW EXECUTE FUNCTION tenant_123456.cases_search_vector_update();

-- Create an index on the search vector
CREATE INDEX idx_cases_search_vector ON tenant_123456.cases USING GIN(search_vector);
```

### 4.2 MongoDB Indexing

#### 4.2.1 Default Indexes
Each collection has the following default indexes:

```javascript
// Create a compound index on tenant_id and created_at
db.tenant_123456_case_notes.createIndex({ "tenant_id": 1, "created_at": -1 });

// Create an index on the case_id field
db.tenant_123456_case_notes.createIndex({ "tenant_id": 1, "case_id": 1 });
```

#### 4.2.2 Text Search Indexes
For collections that require text search capabilities:

```javascript
// Create a text index on content field
db.tenant_123456_case_notes.createIndex({ 
  "content": "text" 
}, {
  default_language: "english",
  weights: {
    "content": 1
  },
  name: "text_index"
});
```

#### 4.2.3 TTL Indexes
For collections with automatic document expiration:

```javascript
// Create a TTL index for the AI results cache
db.tenant_123456_ai_results_cache.createIndex({ "expires_at": 1 }, { expireAfterSeconds: 0 });
```

### 4.3 Elasticsearch Indexing

#### 4.3.1 Index Templates
Index templates are used to automatically apply settings and mappings to new indices:

```json
PUT _index_template/tenant_cases_template
{
  "index_patterns": ["tenant-*-cases-*"],
  "template": {
    "settings": {
      "number_of_shards": 3,
      "number_of_replicas": 1,
      "analysis": {
        "analyzer": {
          "case_analyzer": {
            "type": "custom",
            "tokenizer": "standard",
            "filter": ["lowercase", "asciifolding", "stop", "snowball"]
          }
        }
      }
    }
  }
}
```

#### 4.3.2 Search Optimization
- Custom analyzers for different entity types
- Multi-field mappings for exact and fuzzy matching
- Completion suggester for typeahead search
- Nested field mappings for structured searches

## 5. Partitioning Strategy

### 5.1 PostgreSQL Partitioning

#### 5.1.1 Table Partitioning Approach
The system uses table partitioning for large tables to improve query performance and maintenance operations:

**Tenant-Based Partitioning**
For multi-tenant deployments with many tenants, the cases table is partitioned by tenant_id:

```sql
-- Create partitioned cases table
CREATE TABLE cases (
    id UUID NOT NULL,
    tenant_id UUID NOT NULL,
    -- other columns
    PRIMARY KEY (tenant_id, id)
) PARTITION BY LIST (tenant_id);

-- Create partitions for each tenant
CREATE TABLE cases_tenant_123456 PARTITION OF cases
    FOR VALUES IN ('123456-1234-5678-9012-345678901234');
```

**Time-Based Partitioning**
For time-series data like interactions and audit logs:

```sql
-- Create partitioned interactions table
CREATE TABLE interactions (
    id UUID NOT NULL,
    tenant_id UUID NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    -- other columns
    PRIMARY KEY (tenant_id, timestamp, id)
) PARTITION BY RANGE (timestamp);

-- Create monthly partitions
CREATE TABLE interactions_y2025m06 PARTITION OF interactions
    FOR VALUES FROM ('2025-06-01') TO ('2025-07-01');
```

#### 5.1.2 Partition Maintenance
Automated partition management procedures:

```sql
-- Create a function to add next month's partition
CREATE OR REPLACE FUNCTION create_next_month_partition()
RETURNS void AS $$
DECLARE
    next_month date;
    partition_name text;
    start_date text;
    end_date text;
BEGIN
    next_month := date_trunc('month', now()) + interval '1 month';
    partition_name := 'interactions_y' || to_char(next_month, 'YYYY') || 'm' || to_char(next_month, 'MM');
    start_date := to_char(next_month, 'YYYY-MM-01');
    end_date := to_char(next_month + interval '1 month', 'YYYY-MM-01');
    
    EXECUTE format('CREATE TABLE IF NOT EXISTS %I PARTITION OF interactions FOR VALUES FROM (%L) TO (%L)', 
                  partition_name, start_date, end_date);
                  
    RAISE NOTICE 'Created partition % for range % to %', partition_name, start_date, end_date;
END;
$$ LANGUAGE plpgsql;
```

### 5.2 MongoDB Partitioning

#### 5.2.1 Sharding Strategy
For large MongoDB deployments, collections are sharded based on the following strategies:

**Tenant-Based Sharding**
```javascript
// Enable sharding for the database
sh.enableSharding("murima2025")

// Shard the case notes collection by tenant_id
sh.shardCollection(
  "murima2025.tenant_123456_case_notes",
  { "tenant_id": 1 }
)
```

**Time-Based Sharding**
For time-series data with high write volume:

```javascript
// Shard the audit logs collection by timestamp
sh.shardCollection(
  "murima2025.tenant_123456_audit_logs",
  { "tenant_id": 1, "timestamp": 1 }
)
```

#### 5.2.2 Time-Based Collections
For high-volume collections, time-based collection naming is used:

```javascript
// Collection naming pattern: tenant_123456_audit_logs_2025_06
```

### 5.3 Elasticsearch Partitioning

#### 5.3.1 Time-Based Indices
Elasticsearch uses time-based indices for efficient data lifecycle management:

```
tenant-123456-cases-2025-06
tenant-123456-interactions-2025-06
tenant-123456-audit-logs-2025-06
```

#### 5.3.2 Index Lifecycle Management
ILM policies define the lifecycle of indices:

```json
PUT _ilm/policy/case_logs_policy
{
  "policy": {
    "phases": {
      "hot": {
        "actions": {
          "rollover": {
            "max_age": "30d",
            "max_size": "50gb"
          }
        }
      },
      "warm": {
        "min_age": "30d",
        "actions": {
          "shrink": {
            "number_of_shards": 1
          },
          "forcemerge": {
            "max_num_segments": 1
          }
        }
      },
      "cold": {
        "min_age": "90d",
        "actions": {
          "freeze": {}
        }
      },
      "delete": {
        "min_age": "365d",
        "actions": {
          "delete": {}
        }
      }
    }
  }
}
```

## 6. Caching Strategy

### 6.1 Multi-Level Caching

The system implements a multi-level caching strategy:

#### 6.1.1 Application-Level Cache
- First-level cache using in-memory structures
- Request-scoped caching to avoid duplicate database calls within a request
- Thread-local storage for context-specific data

#### 6.1.2 Distributed Cache (Redis)
- Second-level cache for cross-service data sharing
- Consistent hashing for Redis Cluster deployments
- Key categories with appropriate TTLs

#### 6.1.3 Database-Level Cache
- PostgreSQL query cache
- MongoDB read preference configuration
- Elasticsearch query cache

### 6.2 Cache Invalidation Strategies

#### 6.2.1 Time-Based Invalidation
- TTL-based expiration for cached items
- Sliding expiration for frequently accessed items
- Staggered expiration to prevent cache stampedes

#### 6.2.2 Event-Based Invalidation
- Publisher-subscriber model for cache invalidation events
- Entity-specific invalidation channels
- Hierarchical invalidation (e.g., updating a case invalidates related caches)

#### 6.2.3 Version-Based Invalidation
- Entity versioning for optimistic concurrency control
- Cache keys incorporate entity version
- Compare-and-swap operations for atomic updates

### 6.3 Cache Implementation Examples

#### 6.3.1 Case Data Caching
```javascript
// Cache a case record in Redis
function cacheCase(tenantId, caseId, caseData) {
  const key = `${tenantId}:case:${caseId}`;
  const serializedData = JSON.stringify(caseData);
  return redisClient.setex(key, 1800, serializedData); // 30 minute TTL
}

// Retrieve a case from cache
async function getCaseFromCache(tenantId, caseId) {
  const key = `${tenantId}:case:${caseId}`;
  const cachedData = await redisClient.get(key);
  
  if (cachedData) {
    return JSON.parse(cachedData);
  }
  
  // Cache miss, fetch from database
  const caseData = await fetchCaseFromDatabase(tenantId, caseId);
  
  if (caseData) {
    // Store in cache for future requests
    await cacheCase(tenantId, caseId, caseData);
  }
  
  return caseData;
}

// Invalidate case cache on update
function invalidateCaseCache(tenantId, caseId) {
  const key = `${tenantId}:case:${caseId}`;
  return redisClient.del(key);
}
```

#### 6.3.2 User Permissions Caching
```javascript
// Cache user permissions
function cacheUserPermissions(tenantId, userId, permissions) {
  const key = `${tenantId}:user:${userId}:permissions`;
  const serializedData = JSON.stringify(permissions);
  return redisClient.setex(key, 3600, serializedData); // 1 hour TTL
}

// Check if user has a specific permission
async function hasPermission(tenantId, userId, permission) {
  const key = `${tenantId}:user:${userId}:permissions`;
  
  // Try to get permissions from cache
  let permissions = await redisClient.get(key);
  
  if (!permissions) {
    // Cache miss, fetch from database
    permissions = await fetchUserPermissionsFromDatabase(tenantId, userId);
    
    if (permissions) {
      // Store in cache for future requests
      await cacheUserPermissions(tenantId, userId, permissions);
    } else {
      return false;
    }
  } else {
    permissions = JSON.parse(permissions);
  }
  
  // Check if the user has the requested permission
  return permissions.includes(permission);
}
```

#### 6.3.3 Configuration Caching
```javascript
// Cache tenant configuration
function cacheTenantConfig(tenantId, config) {
  const key = `${tenantId}:config`;
  const serializedData = JSON.stringify(config);
  return redisClient.setex(key, 3600, serializedData); // 1 hour TTL
}

// Get tenant configuration
async function getTenantConfig(tenantId) {
  const key = `${tenantId}:config`;
  
  // Try to get configuration from cache
  let config = await redisClient.get(key);
  
  if (!config) {
    // Cache miss, fetch from database
    config = await fetchTenantConfigFromDatabase(tenantId);
    
    if (config) {
      // Store in cache for future requests
      await cacheTenantConfig(tenantId, config);
    }
  } else {
    config = JSON.parse(config);
  }
  
  return config;
}
```

## 7. Data Migration and Versioning

### 7.1 Schema Migration

#### 7.1.1 PostgreSQL Migrations
The system uses a migration framework to manage database schema changes:

```sql
-- Migration: 20250601123456_add_case_priority_index

-- Up Migration
CREATE INDEX idx_cases_priority ON tenant_123456.cases(priority);

-- Down Migration
DROP INDEX IF EXISTS tenant_123456.idx_cases_priority;
```

Migration versioning follows a timestamp-based approach (YYYYMMDDHHMMSS_description).

#### 7.1.2 MongoDB Schema Evolution
For MongoDB collections, schema changes are managed through application-level validation:

```javascript
// Update MongoDB schema validation
db.runCommand({
  collMod: "tenant_123456_case_notes",
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["tenant_id", "case_id", "content", "created_at"],
      properties: {
        tenant_id: { bsonType: "string" },
        case_id: { bsonType: "string" },
        content: { bsonType: "string" },
        created_at: { bsonType: "date" },
        // New field added in this migration
        is_internal: { bsonType: "bool", description: "Flag indicating if the note is internal" }
      }
    }
  },
  validationLevel: "moderate"
});
```

#### 7.1.3 Elasticsearch Mapping Updates
For Elasticsearch, mapping updates are applied using the reindex API:

```json
// Create a new index with updated mappings
PUT /tenant-123456-cases-2025-06-v2
{
  "mappings": {
    "properties": {
      // Existing fields...
      
      // New field
      "resolution_time": { "type": "integer" }
    }
  }
}

// Reindex data from the old index to the new one
POST /_reindex
{
  "source": {
    "index": "tenant-123456-cases-2025-06"
  },
  "dest": {
    "index": "tenant-123456-cases-2025-06-v2"
  },
  "script": {
    "source": "if (ctx._source.status == 'resolved' && ctx._source.containsKey('resolved_at') && ctx._source.containsKey('created_at')) { ctx._source.resolution_time = (ctx._source.resolved_at.getMillis() - ctx._source.created_at.getMillis()) / 60000; }",
    "lang": "painless"
  }
}

// Create an alias that points to the new index
POST /_aliases
{
  "actions": [
    { "remove": { "index": "tenant-123456-cases-2025-06", "alias": "tenant-123456-cases-current" }},
    { "add": { "index": "tenant-123456-cases-2025-06-v2", "alias": "tenant-123456-cases-current" }}
  ]
}
```

### 7.2 Data Migration

#### 7.2.1 Batch Processing
For large data migrations, the system uses batch processing to minimize impact:

```javascript
// Batch migration of cases to add a new field
async function migrateAddResolutionTime(tenantId, batchSize = 100) {
  let processed = 0;
  let hasMore = true;
  let lastId = null;
  
  while (hasMore) {
    // Fetch a batch of cases
    let query = `
      SELECT id, created_at, resolved_at
      FROM tenant_${tenantId}.cases
      WHERE status = 'resolved' AND resolution_time IS NULL
    `;
    
    if (lastId) {
      query += ` AND id > '${lastId}'`;
    }
    
    query += ` ORDER BY id LIMIT ${batchSize}`;
    
    const cases = await db.query(query);
    
    if (cases.length === 0) {
      hasMore = false;
      continue;
    }
    
    // Process the batch
    for (const caseRecord of cases) {
      if (caseRecord.resolved_at && caseRecord.created_at) {
        const resolutionTimeMinutes = Math.floor(
          (new Date(caseRecord.resolved_at) - new Date(caseRecord.created_at)) / 60000
        );
        
        await db.query(`
          UPDATE tenant_${tenantId}.cases
          SET resolution_time = ${resolutionTimeMinutes}
          WHERE id = '${caseRecord.id}'
        `);
        
        processed++;
      }
      
      lastId = caseRecord.id;
    }
    
    console.log(`Processed ${processed} cases so far`);
  }
  
  return processed;
}
```

#### 7.2.2 Online Schema Changes
For high-availability requirements, online schema changes are performed:

1. Add a new column as nullable
2. Deploy application code that populates the column
3. Backfill existing data
4. Make the column non-nullable (if required)

```sql
-- Step 1: Add new column as nullable
ALTER TABLE tenant_123456.cases ADD COLUMN resolution_time INTEGER;

-- Step 2: Deploy application code that sets the column

-- Step 3: Backfill existing data
UPDATE tenant_123456.cases
SET resolution_time = EXTRACT(EPOCH FROM (resolved_at - created_at))/60
WHERE status = 'resolved' AND resolved_at IS NOT NULL;

-- Step 4: Add not-null constraint (if needed)
ALTER TABLE tenant_123456.cases ALTER COLUMN resolution_time SET NOT NULL;
```

### 7.3 Data Versioning

#### 7.3.1 Optimistic Concurrency Control
The system uses optimistic concurrency control to prevent lost updates:

```sql
-- Add a version column to the cases table
ALTER TABLE tenant_123456.cases ADD COLUMN version INTEGER NOT NULL DEFAULT 1;

-- Update with version check
UPDATE tenant_123456.cases
SET 
  status = 'in_progress',
  assigned_to = '98765432-1234-5678-9012-345678901234',
  updated_at = NOW(),
  version = version + 1
WHERE 
  id = '123e4567-e89b-12d3-a456-426614174000'
  AND version = 1;
```

In the application code:

```javascript
async function updateCase(tenantId, caseId, caseData, expectedVersion) {
  // Start a transaction
  const tx = await db.beginTransaction();
  
  try {
    // Update the case with version check
    const result = await tx.query(`
      UPDATE tenant_${tenantId}.cases
      SET 
        status = $1,
        assigned_to = $2,
        updated_at = NOW(),
        version = version + 1
      WHERE 
        id = $3
        AND version = $4
      RETURNING *
    `, [caseData.status, caseData.assigned_to, caseId, expectedVersion]);
    
    if (result.rowCount === 0) {
      // Concurrent modification detected
      await tx.rollback();
      throw new ConcurrentModificationError("The case was modified by another user");
    }
    
    // Commit the transaction
    await tx.commit();
    return result.rows[0];
  } catch (error) {
    await tx.rollback();
    throw error;
  }
}
```

#### 7.3.2 Audit Trail
All data changes are recorded in the audit trail:

```sql
-- Function to record audit events
CREATE OR REPLACE FUNCTION tenant_123456.record_audit_event()
RETURNS TRIGGER AS $$
DECLARE
  changes jsonb;
BEGIN
  IF (TG_OP = 'UPDATE') THEN
    changes = jsonb_object(array_agg(key), array_agg(value))
    FROM (
      SELECT 
        key,
        CASE
          WHEN OLD.key IS DISTINCT FROM NEW.key THEN 
            jsonb_build_object('old', OLD.key, 'new', NEW.key)
          ELSE NULL
        END as value
      FROM jsonb_object_keys(to_jsonb(NEW)) key
      WHERE OLD.key IS DISTINCT FROM NEW.key
    ) changed_fields;
    
    INSERT INTO tenant_123456.audit_logs (
      entity_type, 
      entity_id, 
      action, 
      user_id, 
      changes
    ) VALUES (
      TG_TABLE_NAME,
      NEW.id,
      'update',
      current_setting('app.current_user_id', true)::uuid,
      changes
    );
  ELSIF (TG_OP = 'INSERT') THEN
    INSERT INTO tenant_123456.audit_logs (
      entity_type, 
      entity_id, 
      action, 
      user_id
    ) VALUES (
      TG_TABLE_NAME,
      NEW.id,
      'create',
      current_setting('app.current_user_id', true)::uuid
    );
  ELSIF (TG_OP = 'DELETE') THEN
    INSERT INTO tenant_123456.audit_logs (
      entity_type, 
      entity_id, 
      action, 
      user_id
    ) VALUES (
      TG_TABLE_NAME,
      OLD.id,
      'delete',
      current_setting('app.current_user_id', true)::uuid
    );
  END IF;
  
  RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- Create triggers for audit logging
CREATE TRIGGER cases_audit_trigger
AFTER INSERT OR UPDATE OR DELETE ON tenant_123456.cases
FOR EACH ROW EXECUTE FUNCTION tenant_123456.record_audit_event();
```

## 8. Performance Optimization

### 8.1 Query Optimization

#### 8.1.1 PostgreSQL Query Optimization
- Use of `EXPLAIN ANALYZE` to identify slow queries
- Creation of appropriate indexes for common query patterns
- Query rewriting for performance improvement
- Proper use of joins and subqueries

Example of a query optimization:

```sql
-- Original query
SELECT c.*, u.username as assigned_to_username
FROM tenant_123456.cases c
LEFT JOIN tenant_123456.users u ON c.assigned_to = u.id
WHERE c.status = 'open'
ORDER BY c.created_at DESC;

-- Optimized query with LIMIT and specific columns
SELECT c.id, c.case_number, c.title, c.status, c.priority, c.created_at, 
       u.username as assigned_to_username
FROM tenant_123456.cases c
LEFT JOIN tenant_123456.users u ON c.assigned_to = u.id
WHERE c.status = 'open'
ORDER BY c.created_at DESC
LIMIT 100;

-- Create supporting index
CREATE INDEX idx_cases_status_created_at ON tenant_123456.cases(status, created_at DESC);
```

#### 8.1.2 MongoDB Query Optimization
- Use of the MongoDB Query Profiler to identify slow queries
- Creation of compound indexes for common query patterns
- Use of projection to limit returned fields

Example of a MongoDB query optimization:

```javascript
// Original query
db.tenant_123456_case_notes.find({
  tenant_id: "123456-1234-5678-9012-345678901234",
  case_id: "123e4567-e89b-12d3-a456-426614174000"
}).sort({ created_at: -1 });

// Optimized query with projection and limit
db.tenant_123456_case_notes.find({
  tenant_id: "123456-1234-5678-9012-345678901234",
  case_id: "123e4567-e89b-12d3-a456-426614174000"
}, {
  content: 1,
  created_at: 1,
  user_id: 1,
  is_internal: 1
}).sort({ created_at: -1 }).limit(20);

// Create supporting index
db.tenant_123456_case_notes.createIndex({
  tenant_id: 1,
  case_id: 1,
  created_at: -1
});
```

#### 8.1.3 Elasticsearch Query Optimization
- Use of filters instead of queries when possible
- Implementation of query result caching
- Proper selection of analyzers and tokenizers

Example of an Elasticsearch query optimization:

```json
// Original query
GET /tenant-123456-cases-2025-06/_search
{
  "query": {
    "bool": {
      "must": [
        { "match": { "title": "account access" }},
        { "match": { "status": "open" }}
      ]
    }
  },
  "sort": [
    { "created_at": { "order": "desc" }}
  ]
}

// Optimized query with filter context
GET /tenant-123456-cases-2025-06/_search
{
  "query": {
    "bool": {
      "must": [
        { "match": { "title": "account access" }}
      ],
      "filter": [
        { "term": { "status": "open" }}
      ]
    }
  },
  "sort": [
    { "created_at": { "order": "desc" }}
  ],
  "_source": ["id", "title", "status", "priority", "created_at"],
  "size": 100
}
```

### 8.2 Database Optimization

#### 8.2.1 PostgreSQL Configuration
Key PostgreSQL configuration parameters for performance:

```ini
# Memory Configuration
shared_buffers = 4GB                  # 25% of available RAM
effective_cache_size = 12GB           # 75% of available RAM
work_mem = 64MB                       # Per-query work memory
maintenance_work_mem = 512MB          # For maintenance operations

# Write-Ahead Log
wal_buffers = 16MB                    # WAL buffer size
synchronous_commit = off              # For performance over durability when appropriate

# Query Planning
random_page_cost = 1.1                # For SSD storage
effective_io_concurrency = 200        # For SSD storage
max_parallel_workers_per_gather = 4   # Parallel query workers

# Autovacuum Settings
autovacuum_vacuum_scale_factor = 0.05 # Vacuum when 5% of rows are dead
autovacuum_analyze_scale_factor = 0.025 # Analyze when 2.5% of rows change
```

#### 8.2.2 MongoDB Configuration
Key MongoDB configuration for performance:

```yaml
storage:
  wiredTiger:
    engineConfig:
      cacheSizeGB: 8  # Adjust based on available RAM
      journalCompressor: snappy
    collectionConfig:
      blockCompressor: snappy
  
operationProfiling:
  mode: slowOp
  slowOpThresholdMs: 100

replication:
  oplogSizeMB: 10240  # 10GB oplog size

net:
  maxIncomingConnections: 2000
```

#### 8.2.3 Elasticsearch Configuration
Key Elasticsearch configuration for performance:

```yaml
cluster.name: murima2025
node.name: node-1

path.data: /var/lib/elasticsearch
path.logs: /var/log/elasticsearch

bootstrap.memory_lock: true

http.port: 9200
network.host: 0.0.0.0

# JVM Heap Size (set to 50% of available RAM, but no more than 32GB)
# Configure in jvm.options:
# -Xms16g
# -Xmx16g

# Threadpools
thread_pool:
  search:
    size: 12
    queue_size: 1000
  write:
    size: 8
    queue_size: 1000

# Cache settings
indices.queries.cache.size: 10%
indices.memory.index_buffer_size: 20%
```

### 8.3 Connection Pooling

#### 8.3.1 PostgreSQL Connection Pooling
The system uses PgBouncer for PostgreSQL connection pooling:

```ini
[databases]
* = host=localhost port=5432 dbname=murima2025

[pgbouncer]
listen_port = 6432
listen_addr = *
auth_type = md5
auth_file = /etc/pgbouncer/userlist.txt
pool_mode = transaction
default_pool_size = 100
max_client_conn = 5000
max_db_connections = 200
```

#### 8.3.2 MongoDB Connection Pooling
MongoDB connection pooling configuration:

```javascript
// Configure MongoDB connection pool
const mongoClient = new MongoClient(uri, {
  maxPoolSize: 100,
  minPoolSize: 10,
  maxIdleTimeMS: 30000,
  connectTimeoutMS: 5000,
  socketTimeoutMS: 30000
});
```

### 8.4 Data Access Patterns

#### 8.4.1 Read-Heavy Optimization
For read-heavy workloads:

- Implementation of read replicas
- Query result caching
- Materialized views for complex reports

```sql
-- Create a materialized view for case statistics
CREATE MATERIALIZED VIEW tenant_123456.case_statistics AS
SELECT 
  c.case_type_id,
  ct.name as case_type_name,
  c.status,
  COUNT(*) as case_count,
  AVG(EXTRACT(EPOCH FROM (COALESCE(c.resolved_at, NOW()) - c.created_at))/3600)::NUMERIC(10,2) as avg_time_hours
FROM 
  tenant_123456.cases c
JOIN 
  tenant_123456.case_types ct ON c.case_type_id = ct.id
WHERE 
  c.created_at >= DATE_TRUNC('month', NOW())
GROUP BY 
  c.case_type_id, ct.name, c.status;

-- Create a refresh function
CREATE OR REPLACE FUNCTION tenant_123456.refresh_case_statistics()
RETURNS void AS $$
BEGIN
  REFRESH MATERIALIZED VIEW CONCURRENTLY tenant_123456.case_statistics;
END;
$$ LANGUAGE plpgsql;

-- Schedule refresh using pg_cron
SELECT cron.schedule('0 * * * *', 'SELECT tenant_123456.refresh_case_statistics()');
```

#### 8.4.2 Write-Heavy Optimization
For write-heavy workloads:

- Use of bulk operations
- Asynchronous processing for non-critical writes
- Write-behind caching

```javascript
// Example of bulk insert for audit logs
async function bulkInsertAuditLogs(tenantId, auditLogs) {
  // Prepare bulk operation
  const bulkOp = db.collection(`tenant_${tenantId}_audit_logs`).initializeUnorderedBulkOp();
  
  // Add operations to bulk
  for (const log of auditLogs) {
    bulkOp.insert(log);
  }
  
  // Execute bulk operation
  return await bulkOp.execute();
}
```

#### 8.4.3 Denormalization
Strategic denormalization for performance:

```sql
-- Add denormalized fields to the cases table
ALTER TABLE tenant_123456.cases 
ADD COLUMN case_type_name VARCHAR(255),
ADD COLUMN assigned_to_username VARCHAR(255);

-- Create a trigger to maintain denormalized data
CREATE OR REPLACE FUNCTION tenant_123456.update_case_denormalized_fields()
RETURNS TRIGGER AS $$
BEGIN
  -- Update case_type_name
  IF NEW.case_type_id IS NOT NULL THEN
    SELECT name INTO NEW.case_type_name
    FROM tenant_123456.case_types
    WHERE id = NEW.case_type_id;
  END IF;
  
  -- Update assigned_to_username
  IF NEW.assigned_to IS NOT NULL THEN
    SELECT username INTO NEW.assigned_to_username
    FROM tenant_123456.users
    WHERE id = NEW.assigned_to;
  ELSE
    NEW.assigned_to_username = NULL;
  END IF;
  
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create the trigger
CREATE TRIGGER update_case_denormalized_fields_trigger
BEFORE INSERT OR UPDATE ON tenant_123456.cases
FOR EACH ROW EXECUTE FUNCTION tenant_123456.update_case_denormalized_fields();
```

### 8.5 Monitoring and Performance Tuning

#### 8.5.1 Database Monitoring
Key metrics monitored for each database:

**PostgreSQL Metrics**
- Query execution time
- Index usage statistics
- Buffer cache hit ratio
- Lock contention
- Vacuum effectiveness

**MongoDB Metrics**
- Query execution time
- Collection scan vs. index scan ratio
- Write lock percentage
- Connection pool utilization
- Operation counts

**Elasticsearch Metrics**
- Query latency
- Indexing throughput
- Segment merge times
- JVM heap usage
- Search queue size

#### 8.5.2 Performance Tuning Process
1. Establish performance baselines
2. Identify bottlenecks through monitoring
3. Implement targeted optimizations
4. Measure impact of changes
5. Iterate until performance goals are met

## 9. Conclusion

The database design for the Murima2025 system provides a robust, scalable, and efficient foundation for the application. By leveraging a hybrid approach with multiple database technologies, the system can effectively handle different types of data and access patterns while maintaining data integrity, security, and performance.

Key design considerations include:

- Multi-tenant data isolation
- Comprehensive indexing strategy
- Efficient partitioning for high-volume data
- Multi-level caching for performance optimization
- Robust data migration and versioning approach
- Performance optimization at all levels

This design supports the system's requirements for:

- Handling diverse data types (structured, semi-structured, unstructured)
- Supporting high transaction volumes
- Ensuring data security and privacy
- Enabling flexible customization
- Providing comprehensive search capabilities
- Maintaining high performance and scalability

