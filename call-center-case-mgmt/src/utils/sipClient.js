// src/utils/sipClient.js
import JsSIP from 'jssip'

let ua = null
let session = null
let incomingSession = null
let eventListeners = {}

export function initSIP({ uri, password, websocketURL }) {
    try {
        if (!uri || !password || !websocketURL) {
            throw new Error('Missing required parameters: uri, password, or websocketURL')
        }

        const socket = new JsSIP.WebSocketInterface(websocketURL)
        const config = {
            sockets: [socket],
            uri,
            password,
            session_timers: false
        }

        try {
            ua = new JsSIP.UA(config)
        } catch (error) {
            eventListeners['onRegistrationFailed']?.({ reason: 'UA initialization failed', error })
            throw error
        }

        ua.on('registered', () => eventListeners['onRegistered']?.())
        ua.on('registrationFailed', e => eventListeners['onRegistrationFailed']?.(e))
        ua.on('disconnected', () => eventListeners['onDisconnected']?.())

        ua.on('newRTCSession', e => {
            try {
                const incoming = e.originator === 'remote'
                if (incoming) {
                    incomingSession = e.session
                    setupCallEvents(incomingSession)
                    eventListeners['onIncomingCall']?.(incomingSession)
                }
            } catch (error) {
                eventListeners['onRegistrationFailed']?.({ reason: 'Failed to handle incoming call', error })
            }
        })
    } catch (error) {
        eventListeners['onRegistrationFailed']?.({ reason: 'SIP initialization failed', error })
        throw error
    }
}
export function joinQueue() {
    try {
        if (ua) {
            alert('Joining queue...')
            ua.start()
            alert('Successfully joined queue')
        } else {
            alert('Error: SIP User Agent not initialized')
            throw new Error('SIP User Agent not initialized')
        }
    } catch (error) {
        alert(`Failed to join queue: ${error.message}`)
        eventListeners['onRegistrationFailed']?.({ reason: 'Failed to join queue', error })
        throw error
    }
}
export function leaveQueue() {
    if (ua) ua.stop()
    session = null
    incomingSession = null
}

export function answerCall() {
    if (incomingSession) {
        incomingSession.answer({
            mediaConstraints: { audio: true, video: false }
        })
        session = incomingSession
        incomingSession = null
    }
}

export function cancelCall() {
    if (incomingSession) {
        incomingSession.terminate()
        incomingSession = null
    }
}

export function hangupCall() {
    if (session) {
        session.terminate()
        session = null
    }
}

export function transferCall(targetExtension) {
    if (session && session.isEstablished()) {
        session.refer(`sip:${targetExtension}@${ua.configuration.uri.split('@')[1]}`)
        eventListeners['onTransferred']?.(targetExtension)
    }
}

function setupCallEvents(sess) {
    sess.on('progress', () => eventListeners['onProgress']?.())
    sess.on('confirmed', () => eventListeners['onConfirmed']?.())
    sess.on('ended', () => {
        eventListeners['onEnded']?.()
        session = null
    })
    sess.on('failed', () => {
        eventListeners['onFailed']?.()
        session = null
    })
}

export function on(event, callback) {
    eventListeners[event] = callback
}

export function getSessionStatus() {
    return {
        isInCall: !!session,
        isIncoming: !!incomingSession,
        isRegistered: ua?.isRegistered() ?? false
    }
}

