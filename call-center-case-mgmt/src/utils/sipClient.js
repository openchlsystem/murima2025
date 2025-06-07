// src/utils/sipClient.js
import JsSIP from 'jssip';

let ua = null;
let activeSession = null;
let incomingSession = null;
let eventListeners = {};
let isInQueue = false;
let iceServers = [
    { urls: 'stun:stun.l.google.com:19302' },
    { urls: 'stun:stun1.l.google.com:19302' }
];


// Initialize SIP client with WebRTC support
export function initSIP({ Desc,sipUri, password, websocketURL, debug = false }) {
    try {
        // Validate parameters first
      
        const connectionDetails = {
            Desc,
            sipUri,
            password,
            websocketURL,
            debug
        };

        console.log('Initializing SIP with:', connectionDetails);

        if (!connectionDetails.sipUri || !connectionDetails.password || !connectionDetails.websocketURL) {
            throw new Error('Missing required SIP connection parameters');
        }

        console.log('Initializing SIP with:', {
            uri: connectionDetails.sipUri,
            ws: connectionDetails.websocketURL
        });

        // Configure WebSocket with error handling
        const socket = new JsSIP.WebSocketInterface(connectionDetails.websocketURL, {
            useSipCreds: true,
            connectionTimeout: 10000, // Increased timeout
            maxReconnectionAttempts: 5,
            reconnectionTimeout: 10000,
            // Add these for better error handling:
            binaryType: 'arraybuffer',
            keepAliveInterval: 30000
        });

        // Enhanced UA configuration
        const config = {
            sockets: [socket],
            uri: connectionDetails.sipUri,
            password: connectionDetails.password,
            realm: '172.31.11.85', // Explicit realm
            // ... rest of your config
        };

        ua = new JsSIP.UA(config);

        // Add transport-level error handling
        ua.on('transportError', (error) => {
            console.error('Transport Error:', error);
            eventListeners['onTransportError']?.(error);
        });

        // ... rest of your event handlers

        return true;
    } catch (error) {
        console.error('SIP Init Failed:', error);
        // Add recovery logic here
        setTimeout(() => initSIP({ sipUri, password, websocketURL, debug }), 5000);
        throw error;
    }
}

// Enhanced queue management
export function joinQueue(queueNumber = '') {
   
    if (!ua) {
        throw new Error('SIP client not initialized');
    }

    try {
        const options = {
            extraHeaders: queueNumber ? [`X-Queue: ${queueNumber}`] : []
        };

        ua.register(options)
            .then(() => {
                isInQueue = true;
                console.log('Joined queue successfully');
                eventListeners['onQueueJoined']?.();
            })
            .catch(error => {
                console.error('Failed to join queue:', error);
                eventListeners['onQueueJoinFailed']?.(error);
                throw error;
            });
    } catch (error) {
        console.error('Error joining queue:', error);
        eventListeners['onQueueJoinFailed']?.(error);
        throw error;
    }
}

export function leaveQueue() {
    if (!ua) {
        throw new Error('SIP client not initialized');
    }

    try {
        ua.unregister()
            .then(() => {
                isInQueue = false;
                console.log('Left queue successfully');
                eventListeners['onQueueLeft']?.();
            })
            .catch(error => {
                console.error('Failed to leave queue:', error);
                eventListeners['onQueueLeaveFailed']?.(error);
                throw error;
            });
    } catch (error) {
        console.error('Error leaving queue:', error);
        eventListeners['onQueueLeaveFailed']?.(error);
        throw error;
    }
}

// Enhanced call control with WebRTC options
export function answerCall() {
    if (!incomingSession) {
        throw new Error('No incoming call to answer');
    }

    try {
        const options = {
            mediaConstraints: { audio: true, video: false },
            pcConfig: {
                iceServers: iceServers,
                iceTransportPolicy: 'all'
            },
            rtcConstraints: {
                optional: [{ googDscp: true }]
            },
            rtcOfferConstraints: {
                offerToReceiveAudio: true,
                offerToReceiveVideo: false
            }
        };

        incomingSession.answer(options);
        activeSession = incomingSession;
        incomingSession = null;
        console.log('Call answered successfully');
        eventListeners['onCallAnswered']?.(activeSession);
    } catch (error) {
        console.error('Failed to answer call:', error);
        eventListeners['onCallAnswerFailed']?.(error);
        throw error;
    }
}

export function rejectCall() {
    if (!incomingSession) {
        throw new Error('No incoming call to reject');
    }

    try {
        incomingSession.terminate({
            status_code: 486,
            reason_phrase: 'Busy Here'
        });
        incomingSession = null;
        console.log('Call rejected successfully');
        eventListeners['onCallRejected']?.();
    } catch (error) {
        console.error('Failed to reject call:', error);
        eventListeners['onCallRejectFailed']?.(error);
        throw error;
    }
}

export function hangupCall() {
    if (!activeSession) {
        throw new Error('No active call to hang up');
    }

    try {
        activeSession.terminate();
        activeSession = null;
        console.log('Call ended successfully');
        eventListeners['onCallEnded']?.();
    } catch (error) {
        console.error('Failed to hang up call:', error);
        eventListeners['onCallEndFailed']?.(error);
        throw error;
    }
}

// Enhanced call features
export function muteCall(mute = true) {
    if (!activeSession) {
        throw new Error('No active call to mute');
    }

    try {
        const audioTrack = activeSession.connection.getSenders()
            .find(sender => sender.track.kind === 'audio');

        if (audioTrack) {
            audioTrack.track.enabled = !mute;
            console.log(mute ? 'Call muted successfully' : 'Call unmuted successfully');
            eventListeners['onCallMuted']?.(mute);
        }
    } catch (error) {
        console.error('Failed to toggle mute:', error);
        eventListeners['onCallMuteFailed']?.(error);
        throw error;
    }
}

export function sendDTMF(tone, duration = 100, interToneGap = 500) {
    if (!activeSession) {
        throw new Error('No active call to send DTMF');
    }

    try {
        activeSession.sendDTMF(tone, {
            duration,
            interToneGap
        });
        console.log('DTMF tone sent successfully:', tone);
        eventListeners['onDTMFSent']?.(tone);
    } catch (error) {
        console.error('Failed to send DTMF:', error);
        eventListeners['onDTMFSendFailed']?.(error);
        throw error;
    }
}

// Enhanced status information
export function getCallStatus() {
    const status = {
        isInCall: !!activeSession,
        hasIncomingCall: !!incomingSession,
        isInQueue: isInQueue,
        isRegistered: ua?.isRegistered() || false,
        registrationState: ua?.registrationState || 'unregistered',
        connectionState: ua?.connectionState || 'disconnected'
    };

    if (activeSession) {
        status.callDirection = activeSession.direction;
        status.remoteIdentity = activeSession.remote_identity.display_name || activeSession.remote_identity.uri.toString();
        status.startTime = activeSession.start_time;
        status.isMuted = isCallMuted();
    }

    return status;
}

function isCallMuted() {
    if (!activeSession) return false;
    const audioTrack = activeSession.connection.getSenders()
        .find(sender => sender.track.kind === 'audio');
    return audioTrack ? !audioTrack.track.enabled : false;
}

// Enhanced event management
export function on(event, callback) {
    if (typeof callback !== 'function') {
        throw new Error('Callback must be a function');
    }
    eventListeners[event] = callback;
}

export function off(event) {
    delete eventListeners[event];
}

// Enhanced internal call event setup
function setupCallEvents(session) {
    session.on('progress', (data) => {
        console.log('Call progress:', data);
        eventListeners['onCallProgress']?.(session, data);
    });

    session.on('accepted', (data) => {
        console.log('Call accepted:', data);
        eventListeners['onCallAccepted']?.(session, data);
    });

    session.on('confirmed', (data) => {
        console.log('Call confirmed:', data);
        eventListeners['onCallConfirmed']?.(session, data);
    });

    session.on('ended', (data) => {
        console.log('Call ended:', data);
        if (session === activeSession) {
            activeSession = null;
        }
        if (session === incomingSession) {
            incomingSession = null;
        }
        eventListeners['onCallEnded']?.(session, data);
    });

    session.on('failed', (data) => {
        console.error('Call failed:', data);
        if (session === activeSession) {
            activeSession = null;
        }
        if (session === incomingSession) {
            incomingSession = null;
        }
        eventListeners['onCallFailed']?.(session, data);
    });

    session.on('peerconnection', (data) => {
        console.log('WebRTC peer connection event:', data);
        eventListeners['onPeerConnection']?.(session, data);
    });

    session.on('sending', (data) => {
        console.log('Sending media:', data);
        eventListeners['onMediaSending']?.(session, data);
    });

    session.on('addstream', (data) => {
        console.log('Remote stream added:', data);
        eventListeners['onRemoteStreamAdded']?.(session, data);
    });

    session.on('icecandidate', (data) => {
        console.log('ICE candidate:', data);
        eventListeners['onIceCandidate']?.(session, data);
    });

    session.on('iceconnectionstatechange', (data) => {
        console.log('ICE connection state changed:', data);
        eventListeners['onIceStateChange']?.(session, data);
    });
}

// Enhanced transfer functionality
export function transferCall(targetExtension, isBlind = true) {
    if (!activeSession || !activeSession.isEstablished()) {
        throw new Error('No active call to transfer');
    }

    try {
        const domain = ua.configuration.uri.split('@')[1];
        const targetUri = `sip:${targetExtension}@${domain}`;

        if (isBlind) {
            activeSession.terminate({
                status_code: 302,
                reason_phrase: 'Moved Temporarily',
                extraHeaders: [`Refer-To: <${targetUri}>`]
            });
        } else {
            activeSession.refer(targetUri);
        }

        console.log(`Call ${isBlind ? 'blind' : 'attended'} transferred to:`, targetExtension);
        eventListeners['onCallTransferred']?.(targetExtension, isBlind);
    } catch (error) {
        console.error('Failed to transfer call:', error);
        eventListeners['onCallTransferFailed']?.(error);
        throw error;
    }
}

// Enhanced cleanup
export function cleanup() {
    try {
        if (activeSession) {
            activeSession.terminate();
            activeSession = null;
        }

        if (incomingSession) {
            incomingSession.terminate();
            incomingSession = null;
        }

        if (ua) {
            ua.unregister()
                .then(() => ua.stop())
                .catch(err => console.error('Error during cleanup:', err));
            ua = null;
        }

        isInQueue = false;
        eventListeners = {};
        console.log('SIP client cleaned up successfully');
    } catch (error) {
        console.error('Error during cleanup:', error);
        throw error;
    }
}

// Additional utility functions
export function makeCall(target, options = {}) {
    if (!ua) {
        throw new Error('SIP client not initialized');
    }

    try {
        const domain = ua.configuration.uri.split('@')[1];
        const targetUri = target.includes('@') ? target : `sip:${target}@${domain}`;

        const callOptions = {
            mediaConstraints: { audio: true, video: false },
            pcConfig: {
                iceServers: iceServers,
                iceTransportPolicy: 'all'
            },
            rtcConstraints: {
                optional: [{ googDscp: true }]
            },
            rtcOfferConstraints: {
                offerToReceiveAudio: true,
                offerToReceiveVideo: false
            },
            ...options
        };

        const session = ua.call(targetUri, callOptions);
        activeSession = session;
        setupCallEvents(session);
        console.log('Outgoing call initiated to:', target);
        return session;
    } catch (error) {
        console.error('Failed to make call:', error);
        eventListeners['onCallFailed']?.(error);
        throw error;
    }
}

export function updateIceServers(newIceServers) {
    if (!Array.isArray(newIceServers)) {
        throw new Error('ICE servers must be an array');
    }
    iceServers = newIceServers;
    console.log('ICE servers updated:', iceServers);
}