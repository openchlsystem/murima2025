<script>
    import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
    import {
        testServerConnection,
        initSIP,
        // joinQueue,
        // leaveQueue,
        answerCall,
        rejectCall,
        hangupCall,
        transferCall,
        muteCall,
        sendDTMF,
        on,
        off,
        cleanup,
        getCallStatus,
        getRegistrationStatus
    } from '@/utils/sipClient';

    export default {
        setup() {
            // Component state
            const sipStatus = ref({
                isRegistered: false,
                isInQueue: false,
                hasActiveCall: false,
                hasIncomingCall: false,
                callDuration: '00:00:00'
            });
    // Component state
    const serverStatus = ref({
        isTestingConnection: false,
        isServerAccessible: false,
        connectionError: null
    });

    const sipStatus = ref({
        isRegistered: false,
        isInQueue: false,
        hasActiveCall: false,
        hasIncomingCall: false,
        callDuration: '00:00:00'
    });

            const callInfo = ref({
                active: null,
                incoming: null
            });

            const isMuted = ref(false);

    // Computed properties
    const connectionStatus = computed(() => {
        if (serverStatus.value.isTestingConnection) {
            return { text: 'Testing Connection...', class: 'testing' };
        }
        if (serverStatus.value.isServerAccessible) {
            return { text: 'Server Connected', class: 'connected' };
        }
        if (serverStatus.value.connectionError) {
            return { text: 'Connection Failed', class: 'error' };
        }
        return { text: 'Not Connected', class: 'disconnected' };
    });

    const canJoinQueue = computed(() => {
        return serverStatus.value.isServerAccessible && !serverStatus.value.isTestingConnection;
    });

    // Test Asterisk server accessibility
    const testAsteriskConnection = async () => {
        try {
            serverStatus.value.isTestingConnection = true;
            serverStatus.value.connectionError = null;
            
            const sipDetails = JSON.parse(localStorage.getItem('sipConnectionDetails'));
            
            if (!sipDetails?.websocketURL) {
                throw new Error('Missing Asterisk server details');
            }

            console.log('Testing Asterisk server connection...');
            
            // Test if Asterisk server is accessible
            const isAccessible = await testServerConnection(sipDetails.websocketURL);
            
            if (isAccessible) {
                serverStatus.value.isServerAccessible = true;
                console.log('Asterisk server is accessible');
            } else {
                throw new Error('Asterisk server is not responding');
            }

        } catch (error) {
            console.error('Server connection test failed:', error);
            serverStatus.value.connectionError = error.message;
            serverStatus.value.isServerAccessible = false;
        } finally {
            serverStatus.value.isTestingConnection = false;
        }
    };

    // Retry server connection test
    const retryConnection = () => {
        testAsteriskConnection();
    };

    // Queue management - Extension Registration
    const toggleQueue = async () => {
        if (!canJoinQueue.value) return;
        
        try {
            if (sipStatus.value.isInQueue) {
                // Leave queue = Unregister extension
                console.log('Leaving queue - unregistering extension...');
                await leaveQueue();
                sipStatus.value.isInQueue = false;
                sipStatus.value.isRegistered = false;
                console.log('Left queue and unregistered extension');
            } else {
                // Join queue = Initialize SIP and register extension
                console.log('Joining queue - initializing SIP and registering extension...');
                const sipDetails = JSON.parse(localStorage.getItem('sipConnectionDetails'));
                
                // Initialize SIP client
                await initSIP({
                    Desc: sipDetails.Desc || 'Agent Extension',
                    sipUri: sipDetails.uri,
                    password: sipDetails.password,
                    websocketURL: sipDetails.websocketURL,
                    debug: true
                });
                
                // Set up event listeners
                setupSipEventListeners();
                
                // Register extension (join queue)
                await joinQueue();
                sipStatus.value.isInQueue = true;
                console.log('Successfully joined queue - extension registered');
            }
        } catch (error) {
            console.error('Queue operation failed:', error);
            sipStatus.value.isInQueue = false;
            sipStatus.value.isRegistered = false;
        }
    };

    // Set up SIP event listeners
    const setupSipEventListeners = () => {
        // Extension Registration events
        on('onRegistered', () => {
            console.log('Extension registered - ready to receive calls');
            sipStatus.value.isRegistered = true;
        });

        on('onUnregistered', () => {
            console.log('Extension unregistered - no longer accessible');
            sipStatus.value.isRegistered = false;
            sipStatus.value.isInQueue = false;
        });

        on('onRegistrationFailed', (error) => {
            console.error('Extension registration failed:', error);
            sipStatus.value.isRegistered = false;
            sipStatus.value.isInQueue = false;
        });

        // Incoming call events
        on('onIncomingCall', (session) => {
            console.log('Incoming call received from:', session.remote_identity.uri.user);
            callInfo.value.incoming = {
                session,
                callerId: session.remote_identity.uri.user,
                callerName: session.remote_identity.display_name || session.remote_identity.uri.user
            };
            sipStatus.value.hasIncomingCall = true;
        });

        // Call answer/start events
        on('onCallAnswered', (session) => {
            console.log('Call answered successfully');
            callInfo.value.active = {
                session,
                callerId: session.remote_identity.uri.user,
                callerName: session.remote_identity.display_name || session.remote_identity.uri.user
            };
            sipStatus.value.hasActiveCall = true;
            sipStatus.value.hasIncomingCall = false;
            callInfo.value.incoming = null;
            startCallTimer();
        });

        // Call end events
        on('onCallEnded', () => {
            console.log('Call ended');
            sipStatus.value.hasActiveCall = false;
            sipStatus.value.hasIncomingCall = false;
            callInfo.value.active = null;
            callInfo.value.incoming = null;
            isMuted.value = false;
            stopCallTimer();
        });

        on('onCallRejected', () => {
            console.log('Call rejected');
            sipStatus.value.hasIncomingCall = false;
            callInfo.value.incoming = null;
        });

        // Connection events
        on('onDisconnected', () => {
            console.log('SIP disconnected');
            sipStatus.value.isRegistered = false;
            sipStatus.value.isInQueue = false;
        });

        // Queue events
        on('onQueueJoined', () => {
            console.log('Successfully joined queue');
            sipStatus.value.isInQueue = true;
        });

        on('onQueueLeft', () => {
            console.log('Successfully left queue');
            sipStatus.value.isInQueue = false;
        });
    };

    // Call control functions
    const answerIncomingCall = async () => {
        try {
            console.log('Answering incoming call...');
            await answerCall();
        } catch (error) {
            console.error('Failed to answer call:', error);
        }
    };

    const rejectIncomingCall = async () => {
        try {
            console.log('Rejecting incoming call...');
            await rejectCall();
            sipStatus.value.hasIncomingCall = false;
            callInfo.value.incoming = null;
        } catch (error) {
            console.error('Failed to reject call:', error);
        }
    };

    const hangupActiveCall = async () => {
        try {
            console.log('Hanging up active call...');
            await hangupCall();
        } catch (error) {
            console.error('Failed to hangup call:', error);
        }
    };

    const toggleMute = async () => {
        try {
            const newMuteState = !isMuted.value;
            await muteCall(newMuteState);
            isMuted.value = newMuteState;
            console.log(newMuteState ? 'Call muted' : 'Call unmuted');
        } catch (error) {
            console.error('Failed to toggle mute:', error);
        }
    };

    const sendDTMFTone = (tone) => {
        try {
            sendDTMF(tone);
            console.log('DTMF tone sent:', tone);
        } catch (error) {
            console.error('Failed to send DTMF:', error);
        }
    };

    // Call timer management
    let callTimer = null;
    let callStartTime = null;

    const startCallTimer = () => {
        callStartTime = Date.now();
        callTimer = setInterval(() => {
            const elapsed = Date.now() - callStartTime;
            const hours = Math.floor(elapsed / 3600000);
            const minutes = Math.floor((elapsed % 3600000) / 60000);
            const seconds = Math.floor((elapsed % 60000) / 1000);
            
            sipStatus.value.callDuration = 
                `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        }, 1000);
    };

    const stopCallTimer = () => {
        if (callTimer) {
            clearInterval(callTimer);
            callTimer = null;
        }
        sipStatus.value.callDuration = '00:00:00';
    };

    // Lifecycle hooks
    onMounted(() => {
        // Test server accessibility first
        testAsteriskConnection();
    });

    onBeforeUnmount(() => {
        stopCallTimer();
        cleanup();
        
        // Clean up event listeners
        off('onRegistered');
        off('onUnregistered');
        off('onRegistrationFailed');
        off('onIncomingCall');
        off('onCallAnswered');
        off('onCallEnded');
        off('onCallRejected');
        off('onDisconnected');
        off('onQueueJoined');
        off('onQueueLeft');
    });
</script>

<template>
    <div class="sip-phone">
        <!-- Server Connection Status -->
        <div class="status-section">
            <div class="connection-status">
                <span :class="['indicator', connectionStatus.class]"></span>
                <span class="status-text">{{ connectionStatus.text }}</span>
            </div>
            
            <!-- Show error and retry if connection failed -->
            <div v-if="serverStatus.connectionError" class="error-section">
                <p class="error-message">{{ serverStatus.connectionError }}</p>
                <button @click="retryConnection" class="retry-btn">Retry Connection</button>
            </div>
        </div>

        <!-- Queue Control - Extension Registration -->
        <div class="queue-section">
            <button 
                @click="toggleQueue" 
                :disabled="!canJoinQueue"
                class="queue-btn"
                :class="{ 'in-queue': sipStatus.isInQueue }"
            >
                {{ sipStatus.isInQueue ? 'Leave Queue' : 'Join Queue' }}
            </button>
            
            <div class="queue-status">
                <p v-if="serverStatus.isTestingConnection" class="queue-help">
                    Testing server connection...
                </p>
                <p v-else-if="!serverStatus.isServerAccessible" class="queue-help">
                    Server must be accessible to join queue
                </p>
                <p v-else-if="sipStatus.isInQueue && sipStatus.isRegistered" class="queue-help success">
                    ✓ Ready to receive calls
                </p>
                <p v-else-if="sipStatus.isInQueue && !sipStatus.isRegistered" class="queue-help">
                    Registering extension...
                </p>
                <p v-else-if="canJoinQueue && !sipStatus.isInQueue" class="queue-help">
                    Click to register extension and receive calls
                </p>
            </div>
        </div>

        <!-- Incoming Call -->
        <div v-if="sipStatus.hasIncomingCall" class="incoming-call">
            <h3>📞 Incoming Call</h3>
            <div class="caller-info">
                <p class="caller-name">{{ callInfo.incoming.callerName }}</p>
                <p class="caller-id">{{ callInfo.incoming.callerId }}</p>
            </div>
            <div class="call-actions">
                <button @click="answerIncomingCall" class="btn-answer">📞 Answer</button>
                <button @click="rejectIncomingCall" class="btn-reject">❌ Reject</button>
            </div>
        </div>

        <!-- Active Call -->
        <div v-if="sipStatus.hasActiveCall" class="active-call">
            <h3>📞 Active Call</h3>
            <div class="caller-info">
                <p class="caller-name">{{ callInfo.active.callerName }}</p>
                <p class="caller-id">{{ callInfo.active.callerId }}</p>
                <p class="call-time">⏱️ {{ sipStatus.callDuration }}</p>
            </div>

            <div class="call-controls">
                <button @click="toggleMute" class="btn-mute" :class="{ muted: isMuted }">
                    {{ isMuted ? '🔇 Unmute' : '🔊 Mute' }}
                </button>
                <button @click="hangupActiveCall" class="btn-hangup">📞 Hang Up</button>
            </div>

            <!-- DTMF Pad -->
            <div class="dtmf-pad">
                <h4>Keypad</h4>
                <div class="keypad">
                    <button 
                        v-for="key in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '*', '0', '#']" 
                        :key="key"
                        @click="sendDTMFTone(key)"
                        class="key-btn"
                    >
                        {{ key }}
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.sip-phone {
    max-width: 350px;
    margin: 20px auto;
    padding: 20px;
    background: white;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

/* Status Section */
.status-section {
    text-align: center;
    margin-bottom: 25px;
    padding: 15px;
    background: #f8f9fa;
    border-radius: 8px;
}

.connection-status {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
}

.indicator {
    width: 16px;
    height: 16px;
    border-radius: 50%;
    flex-shrink: 0;
}

.indicator.testing {
    background: #ffc107;
    animation: pulse 1s infinite;
}

.indicator.connected {
    background: #28a745;
    box-shadow: 0 0 0 3px rgba(40, 167, 69, 0.2);
}

.indicator.disconnected {
    background: #6c757d;
}

.indicator.error {
    background: #dc3545;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.4; }
}

.status-text {
    font-size: 18px;
    font-weight: 600;
    color: #2c3e50;
}

.error-section {
    margin-top: 15px;
    padding: 10px;
    background: #f8d7da;
    border: 1px solid #f5c6cb;
    border-radius: 6px;
}

.error-message {
    color: #721c24;
    font-size: 14px;
    margin: 0 0 10px 0;
}

.retry-btn {
    padding: 6px 12px;
    background: #dc3545;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
}

.retry-btn:hover {
    background: #c82333;
}

/* Queue Section */
.queue-section {
    margin-bottom: 25px;
}

.queue-btn {
    width: 100%;
    padding: 15px;
    font-size: 16px;
    font-weight: 600;
    border: 2px solid #007bff;
    background: white;
    color: #007bff;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.2s ease;
}

.queue-btn:hover:not(:disabled) {
    background: #007bff;
    color: white;
    transform: translateY(-1px);
}

.queue-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    border-color: #dee2e6;
    color: #6c757d;
}

.queue-btn.in-queue {
    background: #28a745;
    border-color: #28a745;
    color: white;
}

.queue-status {
    margin-top: 10px;
}

.queue-help {
    text-align: center;
    font-size: 14px;
    color: #6c757d;
    margin: 0;
    font-style: italic;
}

.queue-help.success {
    color: #28a745;
    font-weight: 600;
    font-style: normal;
}

/* Incoming Call */
.incoming-call {
    background: linear-gradient(135deg, #d4edda, #c3e6cb);
    border: 2px solid #28a745;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 20px;
    animation: slideIn 0.3s ease, callPulse 2s infinite;
}

@keyframes callPulse {
    0%, 100% { 
        box-shadow: 0 0 0 0 rgba(40, 167, 69, 0.4);
    }
    50% { 
        box-shadow: 0 0 0 10px rgba(40, 167, 69, 0);
    }
}

/* Active Call */
.active-call {
    background: #f8f9fa;
    border: 2px solid #007bff;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 20px;
}

.incoming-call h3, .active-call h3 {
    margin: 0 0 15px 0;
    text-align: center;
    color: #2c3e50;
}

.caller-info {
    text-align: center;
    margin-bottom: 20px;
}

.caller-name {
    font-size: 20px;
    font-weight: 600;
    margin: 0 0 5px 0;
    color: #2c3e50;
}

.caller-id {
    font-size: 14px;
    color: #6c757d;
    margin: 0;
}

.call-time {
    font-size: 18px;
    font-weight: 600;
    color: #007bff;
    margin: 10px 0 0 0;
}

/* Call Actions */
.call-actions, .call-controls {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    margin-top: 15px;
}

.btn-answer, .btn-reject, .btn-mute, .btn-hangup {
    padding: 12px;
    border: none;
    border-radius: 8px;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
}

.btn-answer {
    background: #28a745;
    color: white;
}

.btn-answer:hover {
    background: #218838;
    transform: translateY(-1px);
}

.btn-reject, .btn-hangup {
    background: #dc3545;
    color: white;
}

.btn-reject:hover, .btn-hangup:hover {
    background: #c82333;
    transform: translateY(-1px);
}

.btn-mute {
    background: #6c757d;
    color: white;
}

.btn-mute.muted {
    background: #ffc107;
    color: #212529;
}

.btn-mute:hover {
    background: #5a6268;
}

/* DTMF Pad */
.dtmf-pad {
    margin-top: 20px;
    padding-top: 20px;
    border-top: 1px solid #dee2e6;
}

.dtmf-pad h4 {
    text-align: center;
    margin-bottom: 15px;
    color: #2c3e50;
}

.keypad {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 8px;
}

.key-btn {
    aspect-ratio: 1;
    border: 1px solid #dee2e6;
    background: white;
    border-radius: 8px;
    font-size: 18px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.1s ease;
}

.key-btn:hover {
    background: #e9ecef;
    transform: scale(0.95);
}

.key-btn:active {
    background: #007bff;
    color: white;
}

@keyframes slideIn {
    from {
        opacity: 0;
        transform: translateY(-20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
</style>