# Asterisk PBX Configuration for Call Center with WebRTC Phones

**Document Version:** 1.0  
**Last Updated:** [Current Date]

---

## Table of Contents

1. Introduction  
2. System Architecture Overview  
3. Prerequisites  
4. Asterisk PBX Configuration  
    - 4.1 Installing Asterisk  
    - 4.2 Configuring SIP/WebRTC (PJSIP)  
    - 4.3 Setting Up IVR (Dialplan)  
    - 4.4 Implementing Call Queues (Agent Hunting)  
    - 4.5 Call Recording Setup  
    - 4.6 Database Integration for Call Logging  
5. WebRTC Phone Configuration  
6. Monitoring & Reporting  
7. Troubleshooting & Best Practices  
8. Appendix: Sample Configuration Files  

---

## 1. Introduction

This document provides a step-by-step guide to configuring Asterisk PBX for a call center with:

- Inbound call flow (Welcome message, IVR, Agent hunting)  
- Outbound call routing  
- Call recording  
- WebRTC-based softphones  
- Database storage for call events  

---

## 2. System Architecture Overview

### System Components

- Inbound Calls → Asterisk PBX → IVR → Queue → Agent (WebRTC)  
- Outbound Calls → Agent (WebRTC) → Asterisk PBX → PSTN/Trunk  
- Call Recording → Storage (Local/Cloud)  
- Call Logging → Database (MySQL/PostgreSQL)  

---

## 3. Prerequisites

- Server: Ubuntu/CentOS (Recommended: 4GB RAM, 2 vCPU)  
- Asterisk 18+ (LTS Version)  
- WebRTC Phones (Zoiper, Linphone, or custom web-based SIP clients)  
- Database (MySQL/PostgreSQL for call logging)  
- SSL Certificates (For secure WebRTC)  

---

## 4. Asterisk PBX Configuration

### 4.1 Installing Asterisk

```bash
# On Ubuntu/Debian
sudo apt update
sudo apt install -y asterisk asterisk-pjsip asterisk-mysql

# Enable and start Asterisk
sudo systemctl enable asterisk
sudo systemctl start asterisk
```

### 4.2 Configuring SIP/WebRTC (PJSIP)

Edit `/etc/asterisk/pjsip.conf`:

```ini
[transport-udp]
type=transport
protocol=udp
bind=0.0.0.0

[transport-wss]
type=transport
protocol=wss
bind=0.0.0.0

[6001] ; Agent 1
type=endpoint
context=agents
disallow=all
allow=ulaw,opus
auth=6001
aors=6001
webrtc=yes

[6001]
type=auth
auth_type=userpass
password=agentpass
username=6001

[6001]
type=aor
max_contacts=1
```

### 4.3 Setting Up IVR (Dialplan)

Edit `/etc/asterisk/extensions.conf`:

```ini
[inbound-calls]
exten => s,1,Answer()
same => n,Playback(welcome-message)
same => n,Background(enter-ext-of-person)
same => n,WaitExten(5)

exten => 1,1,Queue(sales-q,,,10)
exten => 2,1,Queue(support-q,,,10)

[agents]
exten => 6001,1,Dial(PJSIP/6001,20)
```

### 4.4 Implementing Call Queues (Agent Hunting)

Edit `/etc/asterisk/queues.conf`:

```ini
[sales-q]
strategy=ringall
timeout=30
musicclass=default
member => PJSIP/6001
member => PJSIP/6002
```

### 4.5 Call Recording Setup

Edit `/etc/asterisk/extensions.conf` (add to dialplan as needed):

```ini
exten => _X.,1,MixMonitor(/var/spool/asterisk/monitor/${UNIQUEID}.wav)
```

### 4.6 Database Integration for Call Logging

Install MySQL ODBC:

```bash
sudo apt install -y unixodbc unixodbc-dev mysql-connector-odbc
```

Configure `/etc/asterisk/res_odbc.conf`:

```ini
[asterisk]
enabled => yes
dsn => asterisk-connector
username => asteriskuser
password => securepassword
```

Create a CDR table in your MySQL/PostgreSQL database:

```sql
CREATE TABLE cdr (
    call_id VARCHAR(255),
    caller_id VARCHAR(50),
    agent_id VARCHAR(50),
    status VARCHAR(20),
    duration INT,
    recording_path VARCHAR(255),
    timestamp DATETIME
);
```

## 5. WebRTC Phone Configuration

Zoiper: Use SIP credentials (e.g., 6001@your-asterisk-ip)

Web Client: Use WebSocket URL wss://your-asterisk-ip:8089/ws (Secure WebSocket)

## 6. Monitoring & Reporting

Use AMI (Asterisk Manager Interface) for real-time event monitoring

Custom scripts can query CDR data for dashboards

## 7. Troubleshooting & Best Practices

✅ Check SIP Registration: asterisk -rvvvvv → pjsip show endpoints

✅ Test IVR: Dial into the system and verify menu options

✅ Verify Call Recording: Check /var/spool/asterisk/monitor/

✅ Secure WebRTC: Use HTTPS/WSS (not plain WS)

## 8. Appendix: Sample Configuration Files

pjsip.conf (Full SIP/WebRTC setup)

extensions.conf (Complete dialplan)

queues.conf (Advanced queue settings)