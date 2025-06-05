# 🔐 Authentication Architecture for Django Backend (Mobile, Web, API)

## Overview

This document outlines the authentication strategy for a Django-based backend designed to support:

- Mobile applications
- Web applications
- API integrations

The system uses **OTP-based login** and **JWT (JSON Web Tokens)** for secure, token-based authentication across platforms.

---

## 🔧 Stack Components

| Component | Technology |
|----------|------------|
| Framework | Django |
| Auth Method | OTP (via phone/email) |
| Token Type | JWT |
| Token Transport | HTTP Authorization Header (`Bearer <token>`) |
| Token Expiry | 15 minutes (Access), 7 days (Refresh) |
| Storage (Mobile) | Secure Storage (Keychain, EncryptedSharedPrefs) |
| Storage (Web) | HTTP-only Secure Cookies or localStorage |
| 3rd-Party API Auth | API Keys or OAuth2 (optional) |

---

## 🔁 Authentication Flow

### 1. Request OTP

- Endpoint: `POST /api/auth/request-otp/`
- Input: Phone number or email
- Action: Backend generates and sends OTP via SMS/email

### 2. Verify OTP

- Endpoint: `POST /api/auth/verify-otp/`
- Input: Phone/email + OTP code
- Output: Access Token (JWT) + Refresh Token
- Action: Validates OTP and issues tokens

### 3. Use Token for Authenticated Requests

- Client includes token in headers:
  Authorization: Bearer <access_token>

- Backend validates the token on each request

### 4. Refresh Token (Optional)

- Endpoint: `POST /api/auth/token/refresh/`
- Input: Refresh token
- Output: New access token

---

## 🔐 Security Considerations

- Access tokens are **short-lived** (15 minutes)
- Refresh tokens are **long-lived** (7 days) and stored securely
- Web apps should use **HTTP-only cookies** to prevent XSS attacks
- OTPs should expire in 5–10 minutes and be single-use
- Rate-limit OTP requests to prevent abuse

---

## ✅ API Summary

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/auth/request-otp/` | `POST` | Sends OTP to user |
| `/api/auth/verify-otp/` | `POST` | Verifies OTP and returns tokens |
| `/api/auth/token/refresh/` | `POST` | Issues new access token |
| `/api/auth/logout/` | `POST` | (Optional) Invalidates refresh token |

---

## 📱 Token Storage Recommendations

**Mobile**:

- Use Keychain (iOS) or EncryptedSharedPreferences (Android)

**Web**:

- HTTP-only, Secure Cookies (preferred)
- `localStorage` (fallback with CSRF protections)

**API Clients**:

- Store and use tokens in request headers

---

## 🛠 Libraries & Packages

- [`djangorestframework`](https://www.django-rest-framework.org/)
- [`djangorestframework-simplejwt`](https://github.com/SimpleJWT/django-rest-framework-simplejwt)

OTP Options:

- [`django-otp`](https://github.com/django-otp/django-otp)
- Custom OTP logic using Twilio, email, or SMS APIs

---

## 🧪 Testing

- Ensure OTP is sent and expires correctly
- Simulate token expiration and refresh flows
- Validate secure storage and CSRF protections on web

---

## 🔄 Future Additions

- Support for social login (Google, Facebook)
- API key-based integration for external systems
- Role-based access control (RBAC)
