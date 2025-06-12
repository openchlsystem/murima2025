// src/utils/sipClient.js
import JsSIP from 'jssip';

let ua = null;
let activeSession = null;
let incomingSession = null;
let eventListeners = {};
let isRegistered = false;
let iceServers = [
    { urls: 'stun:stun.l.google.com:19302' },
    { urls: 'stun:stun1.l.google.com:19302' }
];

// Test server connection - Check if Asterisk server is accessible
export const testServerConnection = async (websocketURL) => {
    return new Promise((resolve) => {
        try {
            // Create a test WebSocket connection to check if server is accessible
            const testSocket = new WebSocket(websocketURL, ['sip']);
            
            const timeout = setTimeout(() => {
                testSocket.close();
                resolve(false); // Server not accessible
            }, 5000); // 5 second timeout
            
            testSocket.onopen = () => {
                clearTimeout(timeout);
                testSocket.close();
                resolve(true); // Server is accessible
            };
            
            testSocket.onerror = () => {
                clearTimeout(timeout);
                resolve(false); // Server not accessible
            };
            
        } catch (error) {
            resolve(false); // Server not accessible
        }
    });
};

// Initialize SIP client
export function initSIP({ Desc, sipUri, password, websocketURL, debug = false }) {
    return new Promise((resolve, reject) => {
        try {
            const connectionDetails = {
                Desc,
                sipUri,
                password,
                websocketURL,
                debug
            };

            console.log('Initializing SIP client...');

            if (!connectionDetails.sipUri || !connectionDetails.password || !connectionDetails.websocketURL) {
                throw new Error('Missing required SIP connection parameters');
            }

            // Configure WebSocket
            const socket = new JsSIP.WebSocketInterface(connectionDetails.websocketURL, {
                useSipCreds: true,
                connectionTimeout: 10000,
                maxReconnectionAttempts: 5,
                reconnectionTimeout: 10000,
                binaryType: 'arraybuffer',
                keepAliveInterval: 30000
            });

            // UA configuration
            const config = {
                sockets: [socket],
                uri: connectionDetails.sipUri,
                password: connectionDetails.password,
                realm: '172.31.11.85',
                register: false, // We'll register manually
                session_timers: false,
                debug: connectionDetails.debug
            };

            ua = new JsSIP.UA(config);

            // Set up UA events
            setupUAEvents();

            // Start the UA
            ua.start();
            console.log('SIP client initialized successfully');
            resolve();

        } catch (error) {
            console.error('SIP initialization failed:', error);
            reject(error);
        }
    });
}

// Set up User Agent events
function setupUAEvents() {
    // Extension registration events
    ua.on('registered', () => {
        console.log('Extension registered - ready to receive calls');
        isRegistered = true;
        eventListeners['onRegistered']?.();
    });

    ua.on('unregistered', () => {
        console.log('Extension unregistered - no longer accessible');
        isRegistered = false;
        eventListeners['onUnregistered']?.();
    });

    ua.on('registrationFailed', (data) => {
        console.error('Extension registration failed:', data.cause);
        isRegistered = false;
        eventListeners['onRegistrationFailed']?.(data);
    });

    // Handle incoming calls
    ua.on('newRTCSession', (session) => {
        if (session.direction === 'incoming') {
            console.log('Incoming call received');
            incomingSession = session.session;
            setupCallEvents(session.session);
            eventListeners['onIncomingCall']?.(session.session);
        }
    });

    // Connection events
    ua.on('connected', () => {
        console.log('SIP UA connected to server');
        eventListeners['onConnected']?.();
    });

    ua.on('disconnected', () => {
        console.log('SIP UA disconnected from server');
        isRegistered = false;
        eventListeners['onDisconnected']?.();
    });

    // Transport error handling
    ua.on('transportError', (error) => {
        console.error('SIP transport error:', error);
        eventListeners['onTransportError']?.(error);
    });
}

// Register Extension - Make it accessible to receive calls
export function registerExtension() {
    return new Promise((resolve, reject) => {
        if (!ua) {
            reject(new Error('SIP client not initialized'));
            return;
        }

        try {
            console.log('Registering extension to receive calls...');
            
            if (isRegistered) {
                console.log('Extension already registered');
                resolve();
                return;
            }

            // Set up temporary event listeners for this registration attempt
            const onRegistered = () => {
                console.log('Extension registration successful');
                cleanup();
                resolve();
            };

            const onFailed = (error) => {
                console.error('Extension registration failed:', error);
                cleanup();
                reject(new Error(`Registration failed: ${error.cause || error}`));
            };

            const cleanup = () => {
                clearTimeout(timeout);
                eventListeners['onRegistered'] = originalOnRegistered;
                eventListeners['onRegistrationFailed'] = originalOnFailed;
            };

            // Store original listeners
            const originalOnRegistered = eventListeners['onRegistered'];
            const originalOnFailed = eventListeners['onRegistrationFailed'];

            // Set temporary listeners
            eventListeners['onRegistered'] = onRegistered;
            eventListeners['onRegistrationFailed'] = onFailed;

            // Set timeout for registration
            const timeout = setTimeout(() => {
                cleanup();
                reject(new Error('Registration timeout'));
            }, 15000);

            // Trigger registration
            ua.register();

        } catch (error) {
            console.error('Error during extension registration:', error);
            reject(error);
        }
    });
}

// Unregister Extension - Make it no longer accessible
export function unregisterExtension() {
    return new Promise((resolve, reject) => {
        if (!ua) {
            reject(new Error('SIP client not initialized'));
            return;
        }

        try {
            console.log('Unregistering extension...');
            
            if (!isRegistered) {
                console.log('Extension already unregistered');
                resolve();
                return;
            }

            // Set up temporary event listener
            const onUnregistered = () => {
                console.log('Extension unregistered successfully');
                clearTimeout(timeout);
                eventListeners['onUnregistered'] = originalOnUnregistered;
                resolve();
            };

            // Store original listener
            const originalOnUnregistered = eventListeners['onUnregistered'];
            eventListeners['onUnregistered'] = onUnregistered;

            // Set timeout
            const timeout = setTimeout(() => {
                eventListeners['onUnregistered'] = originalOnUnregistered;
                resolve(); // Don't reject on timeout for unregister
            }, 10000);

            // Trigger unregistration
            ua.unregister();

        } catch (error) {
            console.error('Error during extension unregistration:', error);
            reject(error);
        }
    });
}

// Get Registration Status
export function getRegistrationStatus() {
    return {
        isRegistered: isRegistered,
        canReceiveCalls: isRegistered,
        sipUA: ua ? 'initialized' : 'not initialized',
        connectionState: ua?.connectionState || 'disconnected'
    };
}

// Answer incoming call
export function answerCall() {
    if (!incomingSession) throw new Error('No incoming call to answer');

    const options = {
        mediaConstraints: { audio: true, video: false },
        pcConfig: { iceServers, iceTransportPolicy: 'all' },
        rtcConstraints: { optional: [{ googDscp: true }] },
        rtcOfferConstraints: { offerToReceiveAudio: true, offerToReceiveVideo: false }
    };

    incomingSession.answer(options);
    activeSession = incomingSession;
    incomingSession = null;
    console.log('Call answered successfully');
    eventListeners['onCallAnswered']?.(activeSession);
}

// Reject incoming call
export function rejectCall() {
    if (!incomingSession) throw new Error('No incoming call to reject');

    incomingSession.terminate({
        status_code: 486,
        reason_phrase: 'Busy Here'
    });

    incomingSession = null;
    console.log('Call rejected successfully');
    eventListeners['onCallRejected']?.();
}

// Hang up active call
export function hangupCall() {
    if (!activeSession) throw new Error('No active call to hang up');

    activeSession.terminate();
    activeSession = null;
    console.log('Call ended successfully');
    eventListeners['onCallEnded']?.();
}

// Mute/unmute call
export function muteCall(mute = true) {
    if (!activeSession) throw new Error('No active call to mute');

    try {
        const audioTrack = activeSession.connection.getSenders()
            .find(sender => sender.track && sender.track.kind === 'audio');

    if (audioTrack) {
        audioTrack.track.enabled = !mute;
        console.log(mute ? 'Call muted' : 'Call unmuted');
        eventListeners['onCallMuted']?.(mute);
    }
}

// Send DTMF tone
export function sendDTMF(tone, duration = 100, interToneGap = 500) {
    if (!activeSession) throw new Error('No active call to send DTMF');

    activeSession.sendDTMF(tone, { duration, interToneGap });
    console.log('DTMF tone sent:', tone);
    eventListeners['onDTMFSent']?.(tone);
}

// Get call status
export function getCallStatus() {
    return {
        isInCall: !!activeSession,
        hasIncomingCall: !!incomingSession,
        isRegistered: isRegistered,
        registrationState: isRegistered ? 'registered' : 'unregistered',
        connectionState: ua?.connectionState || 'disconnected',
        activeCall: activeSession ? {
            direction: activeSession.direction,
            remoteIdentity: activeSession.remote_identity.display_name || activeSession.remote_identity.uri.toString(),
            startTime: activeSession.start_time,
            isMuted: isCallMuted()
        } : null
    };
}

// Check if call is muted
function isCallMuted() {
    if (!activeSession) return false;
    const audioTrack = activeSession.connection.getSenders()
        .find(sender => sender.track && sender.track.kind === 'audio');
    return audioTrack ? !audioTrack.track.enabled : false;
}

// Set up call event listeners
function setupCallEvents(session) {
    session.on('progress', data => eventListeners['onCallProgress']?.(session, data));
    session.on('accepted', data => eventListeners['onCallAccepted']?.(session, data));
    session.on('confirmed', data => eventListeners['onCallConfirmed']?.(session, data));
    session.on('ended', data => {
        if (session === activeSession) activeSession = null;
        if (session === incomingSession) incomingSession = null;
        eventListeners['onCallEnded']?.(session, data);
    });
    session.on('failed', data => {
        if (session === activeSession) activeSession = null;
        if (session === incomingSession) incomingSession = null;
        eventListeners['onCallFailed']?.(session, data);
    });

    session.on('peerconnection', (data) => {
        console.log('WebRTC peer connection event:', data);
        eventListeners['onPeerConnection']?.(session, data);
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

// Make outgoing call
export function makeCall(target, options = {}) {
    if (!ua) {
        throw new Error('SIP client not initialized');
    }

    if (!isRegistered) {
        throw new Error('Extension not registered - cannot make calls');
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

// Transfer call
export function transferCall(targetExtension, isBlind = true) {
    if (!activeSession || !activeSession.isEstablished()) {
        throw new Error('No active call to transfer');
    }

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

    console.log(`Call transferred to ${targetExtension} (${isBlind ? 'blind' : 'attended'})`);
    eventListeners['onCallTransferred']?.(targetExtension, isBlind);
}

// Event management
export function on(event, callback) {
    if (typeof callback !== 'function') {
        throw new Error('Callback must be a function');
    }
    eventListeners[event] = callback;
}

export function off(event) {
    delete eventListeners[event];
}

// Clean up
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
            if (isRegistered) {
                ua.unregister();
            }
            ua.stop();
            ua = null;
        }

        isRegistered = false;
        eventListeners = {};
        console.log('SIP client cleaned up successfully');
    } catch (error) {
        console.error('Error during cleanup:', error);
        throw error;
    }
}

// Update ICE servers
export function updateIceServers(newIceServers) {
    if (!Array.isArray(newIceServers)) {
        throw new Error('ICE servers must be an array');
    }
    iceServers = newIceServers;
    console.log('ICE servers updated:', iceServers);
}
