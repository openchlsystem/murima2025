# Part 2: Vue 3 WebRTC Client Setup with JsSIP

## Prerequisites

- Vue 3 project setup

### Install JsSIP

```bash
npm install jssip
```

## Step 1: Vue Component (src/components/WebRTCCall.vue)

```vue
<template>
  <div>
    <h2>WebRTC SIP Call</h2>
    <input v-model="target" placeholder="Enter extension to call" />
    <button @click="makeCall">Call</button>
    <button @click="hangupCall" :disabled="!session">Hangup</button>

    <p v-if="status">{{ status }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import JsSIP from 'jssip'

const target = ref('')
const status = ref('')
let ua = null
let session = null

const socket = new JsSIP.WebSocketInterface('wss://your-server-domain:8089/ws')
const configuration = {
  sockets: [socket],
  uri: 'sip:webrtc_user@your-server-domain',
  password: 'your_secure_password',
  session_timers: false
}

ua = new JsSIP.UA(configuration)
ua.start()

ua.on('registrationFailed', e => {
  status.value = 'Registration failed: ' + e.cause
})

ua.on('registered', () => {
  status.value = 'Registered successfully'
})

ua.on('newRTCSession', e => {
  if (session) session.terminate()
  session = e.session

  session.on('ended', () => {
    status.value = 'Call ended'
    session = null
  })

  session.on('failed', () => {
    status.value = 'Call failed'
    session = null
  })

  session.on('confirmed', () => {
    status.value = 'Call connected'
  })
})

function makeCall() {
  if (!target.value) {
    status.value = 'Please enter a target extension'
    return
  }
  const eventHandlers = {
    progress: () => { status.value = 'Call in progress...' },
    failed: () => { status.value = 'Call failed' },
    ended: () => { status.value = 'Call ended' },
    confirmed: () => { status.value = 'Call confirmed' }
  }
  const options = {
    eventHandlers,
    mediaConstraints: { audio: true, video: false }
  }
  session = ua.call(`sip:${target.value}@your-server-domain`, options)
  status.value = 'Calling ' + target.value
}

function hangupCall() {
  if (session) session.terminate()
}
</script>
```

## Step 2: Replace placeholders

- `wss://your-server-domain:8089/ws` → Your Asterisk WSS URL
- `sip:webrtc_user@your-server-domain` → Your SIP user URI
- `your_secure_password` → Your SIP user password

## Step 3: Run Vue app

```bash
npm run dev
```

Open the app, enter extension (e.g. 1000), and click Call.

## Notes

- Ensure TLS certificates are valid to avoid browser security issues
- WebRTC requires HTTPS/WSS for browsers
- Microphone permission must be allowed in browser
- Open firewall ports 8088/8089 on Asterisk server
- Use TURN/STUN servers for NAT traversal if needed
