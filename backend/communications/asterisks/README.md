# Asterisk WebRTC Setup Guide

This guide will help you configure your Asterisk server to enable WebRTC calls.

---

## Prerequisites

- Asterisk installed with PJSIP support (Asterisk 13+ recommended)
- Root or sudo access to the server
- Valid TLS certificate (self-signed or Let's Encrypt)
- Open ports 8088 (HTTP) and 8089 (HTTPS/WSS)
- Optional: TURN/STUN server for NAT traversal

---

## Step 1: Configure `http.conf`

Edit `/etc/asterisk/http.conf` to enable HTTP and HTTPS with TLS:

```markdown
[general]
enabled=yes
bindaddr=0.0.0.0
bindport=8088

tlsenable=yes
tlsbindaddr=0.0.0.0:8089
tlscertfile=/etc/asterisk/keys/asterisk.pem
tlsprivatekey=/etc/asterisk/keys/asterisk.key
```

Note: Replace asterisk.pem and asterisk.key with your TLS certificate and private key paths.

## Step 2: Configure PJSIP Transport (pjsip.conf)

Add the WebSocket transport for WebRTC:

```markdown
[transport-wss]
type=transport
protocol=ws
bind=0.0.0.0
```

## Step 3: Configure WebRTC User Endpoint (pjsip.conf)

Add the following:

```markdown
[webrtc_user]
type=endpoint
transport=transport-wss
context=internal
disallow=all
allow=opus,ulaw,vp8,h264
webrtc=yes
aors=webrtc_user
auth=webrtc_auth
dtls_auto_generate_cert=yes
media_encryption=dtls
ice_support=yes
use_avpf=yes
rtcp_mux=yes

[webrtc_auth]
type=auth
auth_type=userpass
username=webrtc_user
password=your_secure_password

[webrtc_user]
type=aor
max_contacts=1
```

Replace your_secure_password with a strong password.

## Step 4: Configure Dialplan (extensions.conf)

Create or update your dialplan to handle calls:

```markdown
[internal]
exten => 1000,1,Answer()
 same => n,Playback(hello-world)
 same => n,Hangup()
```

## Step 5: Restart Asterisk

```markdown
sudo systemctl restart asterisk
```

## Optional: Configure STUN/TURN Server

For NAT traversal, edit the pjsip.conf or sip.conf:

```markdown
icesupport=yes
stunaddr=stun.l.google.com:19302
```

Set up a TURN server such as coturn if needed.

## Notes

- Use a valid TLS certificate trusted by browsers to avoid connection errors.
- WebRTC requires secure WebSocket (wss), so HTTPS on port 8089 must be enabled.
- Ports 8088 (HTTP) and 8089 (HTTPS/WSS) should be open on your firewall.
