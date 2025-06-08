// src/utils/sipClient.js
import JsSIP from 'jssip';

let ua = null;
let activeSession = null;
let incomingSession = null;
let eventListeners = {};
let isInQueue = false;
let isRegistered = false;
let iceServers = [
    { urls: 'stun:stun.l.google.com:19302' },
    { urls: 'stun:stun1.l.google.com:19302' }
];

// Test server connection
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

// Initialize SIP client with WebRTC support
export function initSIP({ Desc, sipUri, password, websocketURL, debug = false }) {
    return new Promise((resolve, reject) => {
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
                connectionTimeout: 10000,
                maxReconnectionAttempts: 5,
                reconnectionTimeout: 10000,
                binaryType: 'arraybuffer',
                keepAliveInterval: 30000
            });

            // Enhanced UA configuration
            const config = {
                sockets: [socket],
                uri: connectionDetails.sipUri,
                password: connectionDetails.password,
                realm: '172.31.11.85',
                register: false, // We'll register manually when joining queue
                session_timers: false,
                debug: connectionDetails.debug
            };

            ua = new JsSIP.UA(config);

            // Set up registration events
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

            ua.on('connected', () => {
                console.log('SIP UA connected');
                eventListeners['onConnected']?.();
            });

            ua.on('disconnected', () => {
                console.log('SIP UA disconnected');
                isRegistered = false;
                isInQueue = false;
                eventListeners['onDisconnected']?.();
            });

            // Add transport-level error handling
            ua.on('transportError', (error) => {
                console.error('Transport Error:', error);
                eventListeners['onTransportError']?.(error);
            });

            // Start the UA
            ua.start();
            resolve();

        } catch (error) {
            console.error('SIP Init Failed:', error);
            reject(error);
        }
    });
}

// Join Queue = Register Extension (Ready to Receive Calls)
export function joinQueue(queueNumber = '') {
    return new Promise((resolve, reject) => {
        if (!ua) {
            reject(new Error('SIP client not initialized'));
            return;
        }

        try {
            console.log('Registering extension to receive calls...');
            
            // Register the extension - makes it accessible
            const options = {
                extraHeaders: queueNumber ? [`X-Queue: ${queueNumber}`] : []
            };

            // Wait for registration success
            if (isRegistered) {
                isInQueue = true;
                console.log('Extension already registered - ready to receive calls');
                eventListeners['onQueueJoined']?.();
                resolve();
                return;
            }

            const onRegistered = () => {
                isInQueue = true;
                console.log('Extension registered successfully - ready to receive calls');
                eventListeners['onQueueJoined']?.();
                eventListeners['onRegistered'] = null; // Remove temp listener
                resolve();
            };

            const onFailed = (error) => {
                console.error('Failed to register extension:', error);
                eventListeners['onQueueJoinFailed']?.(error);
                eventListeners['onRegistrationFailed'] = null; // Remove temp listener
                reject(error);
            };

            // Set temporary event listeners for this registration attempt
            const originalOnRegistered = eventListeners['onRegistered'];
            const originalOnFailed = eventListeners['onRegistrationFailed'];

            eventListeners['onRegistered'] = () => {
                onRegistered();
                if (originalOnRegistered) eventListeners['onRegistered'] = originalOnRegistered;
            };

            eventListeners['onRegistrationFailed'] = (error) => {
                onFailed(error);
                if (originalOnFailed) eventListeners['onRegistrationFailed'] = originalOnFailed;
            };

            // Trigger registration
            ua.register(options);

        } catch (error) {
            console.error('Error joining queue:', error);
            eventListeners['onQueueJoinFailed']?.(error);
            reject(error);
        }
    });
}

// Leave Queue = Unregister Extension (No Longer Accessible)
export function leaveQueue() {
    return new Promise((resolve, reject) => {
        if (!ua) {
            reject(new Error('SIP client not initialized'));
            return;
        }

        try {
            console.log('Unregistering extension...');
            
            if (!isRegistered) {
                isInQueue = false
                console.log('Extension already unregistered');
                eventListeners['onQueueLeft']?.();
                resolve();
                return;
            }

            const onUnregistered = () => {
                isInQueue = false;
                console.log('Extension unregistered - no longer accessible');
                eventListeners['onQueueLeft']?.();
                resolve();
            };

            const onFailed = (error) => {
                console.error('Failed to unregister extension:', error);
                eventListeners['onQueueLeaveFailed']?.(error);
                reject(error);
            };

            // Set temporary event listener
            const originalOnUnregistered = eventListeners['onUnregistered'];
            eventListeners['onUnregistered'] = () => {
                onUnregistered();
                if (originalOnUnregistered) eventListeners['onUnregistered'] = originalOnUnregistered;
            };

            // Trigger unregistration
            ua.unregister();

        } catch (error) {
            console.error('Error leaving queue:', error);
            eventListeners['onQueueLeaveFailed']?.(error);
            reject(error);
        }
    });
}

// Get Registration Status
export function getRegistrationStatus() {
    return {
        isRegistered: isRegistered,
        isInQueue: isInQueue,
        canReceiveCalls: isRegistered,
        sipUA: ua ? 'initialized' : 'not initialized'
    };
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
            .find(sender => sender.track && sender.track.kind === 'audio');

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
        isRegistered: isRegistered,
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
        .find(sender => sender.track && sender.track.kind === 'audio');
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
        isRegistered = false;
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