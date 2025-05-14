# System Design Document: Survivor-Based Call Center & Case Management System

## 1. Introduction

### 1.1 Purpose
This document outlines the system design for a Call Center & Case Management System tailored for managing survivor-based cases. The system will handle incoming calls, case documentation, multi-channel communication (WhatsApp, Messenger, etc.), quality assurance, administrative controls, and analytics.

### 1.2 Scope
The system will support:

- **Call Management** (Inbound/outbound call logging)
- **Case Management** (Survivor, reporter, perpetrator details, assessments, narratives)
- **Multi-Channel Logging** (WhatsApp, Messenger, etc.)
- **Quality Assurance** (Supervisor review & feedback)
- **Admin Portal** (User management & system customization)
- **Analytics & Reporting** (Metrics, dashboards, exports)

## 2. System Architecture

### 2.1 High-Level Overview
The system follows a three-tier architecture:

- **Frontend**: Web-based UI (React/Angular)
- **Backend**: REST API (Node.js/Django/Spring Boot)
- **Database**: Relational (PostgreSQL/MySQL) + Optional NoSQL for logs

### 2.2 Technology Stack

| Component    | Technology Options                              |
|-------------|--------------------------------------------------|
| Frontend     | React.js, Angular, Vue.js                        |
| Backend      | Node.js (Express), Django, Spring Boot           |
| Database     | PostgreSQL (structured data), MongoDB (logs)     |
| Analytics    | Power BI, Metabase, Elasticsearch                |
| Telephony    | Twilio, Plivo, or custom VoIP integration        |

## 3. Core Modules & Features

### 3.1 Call Management

**Features:**
- Pop-up Call Form: Auto-fetches caller details (if available)
- Call Logging: Records call duration, timestamps, agent notes
- Call Disposition: Tags (e.g., "New Case," "Follow-up," "Referral")

**Data Model:**

```plaintext
CallLogs {
  id: UUID,
  caller_number: String,
  agent_id: UUID (Foreign Key),
  start_time: DateTime,
  end_time: DateTime,
  disposition: Enum,
  notes: Text,
  case_linked: UUID (Nullable, Foreign Key to Cases)
}
