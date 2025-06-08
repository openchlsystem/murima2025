<template>
  <div>
    <!-- Mobile Menu Button -->
    <button class="mobile-menu-btn" id="mobile-menu-btn" @click="toggleMobileMenu">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M3 12H21M3 6H21M3 18H21" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </button>

    <!-- Sidebar -->
    <div class="sidebar" :class="{ collapsed: isSidebarCollapsed, 'mobile-open': mobileOpen }" id="sidebar">
      <div class="toggle-btn" @click="toggleSidebar">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M3 12H21M3 6H21M3 18H21" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </div>

      <div class="sidebar-content">
        <!-- Header with Logo -->
        <div class="sidebar-header">
          <div class="logo-container">
            <div class="logo">
              <img src="/Openchs logo-1.png" alt="OpenCHS Logo">
            </div>
          </div>
        </div>
        
        <!-- Navigation Links -->
        <div class="nav-section">
          <router-link to="/dashboard" class="nav-item" :class="{ active: $route.path === '/dashboard' }">
            <div class="nav-icon">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M3 9L12 2L21 9V20C21 20.5304 20.7893 21.0391 20.4142 21.4142C20.0391 21.7893 19.5304 22 19 22H5C4.46957 22 3.96086 21.7893 3.58579 21.4142C3.21071 21.0391 3 20.5304 3 20V9Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <polyline points="9,22 9,12 15,12 15,22" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <div class="nav-text">Dashboard</div>
          </router-link>
          
          <router-link to="/calls" class="nav-item" :class="{ active: $route.path === '/calls' }">
            <div class="nav-icon">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M22 16.92V19C22 20.1046 21.1046 21 20 21C10.6112 21 3 13.3888 3 4C3 2.89543 3.89543 2 5 2H7.08C7.55607 2 7.95823 2.33718 8.02513 2.80754L8.7 7.5C8.76694 7.97036 8.53677 8.42989 8.12 8.67L6.5 9.5C7.84 12.16 11.84 16.16 14.5 17.5L15.33 15.88C15.5701 15.4632 16.0296 15.2331 16.5 15.3L21.1925 16.0249C21.6628 16.0918 22 16.4939 22 16.97V16.92Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <div class="nav-text">Calls</div>
          </router-link>
          
          <router-link to="/cases" class="nav-item" :class="{ active: $route.path === '/cases' }">
            <div class="nav-icon">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M14 2H6C5.46957 2 4.96086 2.21071 4.58579 2.58579C4.21071 2.96086 4 3.46957 4 4V20C4 20.5304 4.21071 21.0391 4.58579 21.4142C4.96086 21.7893 5.46957 22 6 22H18C18.5304 22 19.0391 21.7893 19.4142 21.4142C19.7893 21.0391 20 20.5304 20 20V8L14 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <polyline points="14,2 14,8 20,8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <line x1="16" y1="13" x2="8" y2="13" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <line x1="16" y1="17" x2="8" y2="17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <polyline points="10,9 9,9 8,9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <div class="nav-text">Cases</div>
          </router-link>
          
          <router-link to="/chats" class="nav-item" :class="{ active: $route.path === '/chats' }">
            <div class="nav-icon">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M21 15C21 15.5304 20.7893 16.0391 20.4142 16.4142C20.0391 16.7893 19.5304 17 19 17H7L3 21V5C3 4.46957 3.21071 3.96086 3.58579 3.58579C3.96086 3.21071 4.46957 3 5 3H19C19.5304 3 20.0391 3.21071 20.4142 3.58579C20.7893 3.96086 21 4.46957 21 5V15Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M8 9H16" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M8 13H14" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <div class="nav-text">Chats</div>
          </router-link>
          
          <router-link to="/qa-statistics" class="nav-item" :class="{ active: $route.path === '/qa-statistics' }">
            <div class="nav-icon">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <line x1="18" y1="20" x2="18" y2="10" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <line x1="12" y1="20" x2="12" y2="4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <line x1="6" y1="20" x2="6" y2="14" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <div class="nav-text">QA Statistics</div>
          </router-link>
          
          <router-link to="/wallboard" class="nav-item" :class="{ active: $route.path === '/wallboard' }">
            <div class="nav-icon">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <rect x="2" y="3" width="20" height="14" rx="2" ry="2" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <line x1="8" y1="21" x2="16" y2="21" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <line x1="12" y1="17" x2="12" y2="21" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <div class="nav-text">Wallboard</div>
          </router-link>
          
          <router-link to="/settings" class="nav-item" :class="{ active: $route.path === '/settings' }">
            <div class="nav-icon">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M19.4 15C19.2669 15.3016 19.2272 15.6362 19.286 15.9606C19.3448 16.285 19.4995 16.5843 19.73 16.82L19.79 16.88C19.976 17.0657 20.1235 17.2863 20.2241 17.5291C20.3248 17.7719 20.3766 18.0322 20.3766 18.295C20.3766 18.5578 20.3248 18.8181 20.2241 19.0609C20.1235 19.3037 19.976 19.5243 19.71 19.71C19.6043 19.896 19.3837 20.0435 19.1409 20.1441C18.8981 20.2448 18.6378 20.2966 18.375 20.2966C18.1122 20.2966 17.8519 20.2448 17.6091 20.1441C17.3663 20.0435 17.1457 19.896 16.96 19.71L16.9 19.65C16.6643 19.4195 16.365 19.2648 16.0406 19.206C15.7162 19.1472 15.3816 19.1869 15.08 19.32C14.7842 19.4468 14.532 19.6572 14.3543 19.9255C14.1766 20.1938 14.0813 20.5082 14.08 20.83V21C14.08 21.5304 13.8693 22.0391 13.4942 22.4142C13.1191 22.7893 12.6104 23 12.08 23C11.5496 23 11.0409 22.7893 10.6658 22.4142C10.2907 22.0391 10.08 21.5304 10.08 21V20.91C10.0723 20.579 9.96512 20.2573 9.77251 19.9887C9.5799 19.7201 9.31074 19.5176 9 19.41C8.69838 19.2769 8.36381 19.2372 8.03941 19.296C7.71502 19.3548 7.41568 19.5095 7.18 19.74L7.12 19.8C6.93425 19.986 6.71368 20.1335 6.47088 20.2341C6.22808 20.3348 5.96783 20.3866 5.705 20.3866C5.44217 20.3866 5.18192 20.3348 4.93912 20.2341C4.69632 20.1335 4.47575 19.986 4.29 19.8C4.10405 19.6143 3.95653 19.3937 3.85588 19.1509C3.75523 18.9081 3.70343 18.6478 3.70343 18.385C3.70343 18.1222 3.75523 17.8619 3.85588 17.6191C3.95653 17.3763 4.10405 17.1557 4.29 16.97L4.35 16.91C4.58054 16.6743 4.73519 16.375 4.794 16.0506C4.85282 15.7262 4.81312 15.3916 4.68 15.09C4.55324 14.7942 4.34276 14.542 4.07447 14.3643C3.80618 14.1866 3.49179 14.0913 3.17 14.09H3C2.46957 14.09 1.96086 13.8793 1.58579 13.5042C1.21071 13.1291 1 12.6204 1 12.09C1 11.5596 1.21071 11.0509 1.58579 10.6758C1.96086 10.3007 2.46957 10.09 3 10.09H3.09C3.42099 10.0823 3.742 9.97512 4.01062 9.78251C4.27925 9.5899 4.48167 9.32074 4.59 9.01C4.72312 8.70838 4.76282 8.37381 4.704 8.04941C4.64519 7.72502 4.49054 7.42568 4.26 7.19L4.2 7.13C4.01405 6.94425 3.86653 6.72368 3.76588 6.48088C3.66523 6.23808 3.61343 5.97783 3.61343 5.715C3.61343 5.45217 3.66523 5.19192 3.76588 4.94912C3.86653 4.70632 4.01405 4.48575 4.2 4.3C4.38575 4.11405 4.60632 3.96653 4.84912 3.86588C5.09192 3.76523 5.35217 3.71343 5.615 3.71343C5.87783 3.71343 6.13808 3.76523 6.38088 3.86588C6.62368 3.96653 6.84425 4.11405 7.03 4.3L7.09 4.36C7.32568 4.59054 7.62502 4.74519 7.94941 4.804C8.27381 4.86282 8.60838 4.82312 8.91 4.69H9C9.29577 4.56324 9.54802 4.35276 9.72569 4.08447C9.90337 3.81618 9.99872 3.50179 10 3.18V3C10 2.46957 10.2107 1.96086 10.5858 1.58579C10.9609 1.21071 11.4696 1 12 1C12.5304 1 13.0391 1.21071 13.4142 1.58579C13.7893 1.96086 14 2.46957 14 3V3.09C14.0013 3.41179 14.0966 3.72618 14.2743 3.99447C14.452 4.26276 14.7042 4.47324 15 4.6C15.3016 4.73312 15.6362 4.77282 15.9606 4.714C16.285 4.65519 16.5843 4.50054 16.82 4.27L16.88 4.21C17.0657 4.02405 17.2863 3.87653 17.5291 3.77588C17.7719 3.67523 18.0322 3.62343 18.295 3.62343C18.5578 3.62343 18.8181 3.67523 19.0609 3.77588C19.3037 3.87653 19.5243 4.02405 19.71 4.21C19.896 4.39575 20.0435 4.61632 20.1441 4.85912C20.2448 5.10192 20.2966 5.36217 20.2966 5.625C20.2966 5.88783 20.2448 6.14808 20.1441 6.39088C20.0435 6.63368 19.896 6.85425 19.71 7.04L19.65 7.1C19.4195 7.33568 19.2648 7.63502 19.206 7.95941C19.1472 8.28381 19.1869 8.61838 19.32 8.92V9C19.4468 9.29577 19.6572 9.54802 19.9255 9.72569C20.1938 9.90337 20.5082 9.99872 20.83 10H21C21.5304 10 22.0391 10.2107 22.4142 10.5858C22.7893 10.9609 23 11.4696 23 12C23 12.5304 22.7893 13.0391 22.4142 13.4142C22.0391 13.7893 21.5304 14 21 14H20.91C20.5882 14.0013 20.2738 14.0966 20.0055 14.2743C19.7372 14.452 19.5268 14.7042 19.4 15Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <div class="nav-text">Settings</div>
          </router-link>

          <!-- Super Admin Dashboard Button (conditional) -->
          <router-link to="/superadmin" class="nav-item" :class="{ active: $route.path === '/superadmin' }" v-if="userRole === 'super-admin'">
            <div class="nav-icon">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 22S8 18 8 12V5L12 2L16 5V12C16 18 12 22 12 22Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M9 12L11 14L15 10" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <div class="nav-text">Super Admin</div>
          </router-link>
        </div>
        
        <!-- Bottom Section with Server Connection and Queue Controls -->
        <div class="sidebar-bottom">
          <!-- User Profile -->
          <div class="user-profile">
            <router-link to="/edit-profile" class="user-avatar">
              <svg viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 12C14.2091 12 16 10.2091 16 8C16 5.79086 14.2091 4 12 4C9.79086 4 8 5.79086 8 8C8 10.2091 9.79086 12 12 12Z"/>
                <path d="M12 14C7.58172 14 4 17.5817 4 22H20C20 17.5817 16.4183 14 12 14Z"/>
              </svg>
            </router-link>
          </div>
          
          <!-- Server Connection Status -->
          <div class="connection-section">
            <div class="connection-status">
              <span :class="['connection-indicator', connectionStatus.class]"></span>
              <span class="connection-text">{{ connectionStatus.text }}</span>
            </div>
            
            <!-- Show error and retry if connection failed -->
            <div v-if="serverStatus.connectionError" class="error-section">
              <p class="error-message">{{ serverStatus.connectionError }}</p>
              <button @click="retryConnection" class="retry-btn">Retry</button>
            </div>
          </div>
          
          <!-- Queue Status -->
          <div class="status">
            <div class="status-dot" :class="{ 'in-queue': sipStatus.isInQueue }"></div>
            <span>{{ queueStatus }}</span>
          </div>
          
          <!-- Queue Control Button -->
          <div class="button-container">
            <button 
              class="join-queue-btn" 
              :class="{ 
                'in-queue': sipStatus.isInQueue, 
                'has-call': sipStatus.hasActiveCall || sipStatus.hasIncomingCall 
              }"
              @click="handleQueueToggle"
              :disabled="!canJoinQueue || isProcessingQueue"
            >
              {{ queueButtonText }}
            </button>
            
            <!-- Queue Help Text -->
            <div class="queue-help-text">
              <p v-if="serverStatus.isTestingConnection" class="help-text">
                Testing server connection...
              </p>
              <p v-else-if="!serverStatus.isServerAccessible" class="help-text">
                Server must be accessible to join queue
              </p>
              <p v-else-if="sipStatus.isInQueue && sipStatus.isRegistered" class="help-text success">
                ✓ Ready to receive calls
              </p>
              <p v-else-if="sipStatus.isInQueue && !sipStatus.isRegistered" class="help-text">
                Registering extension...
              </p>
              <p v-else-if="canJoinQueue && !sipStatus.isInQueue" class="help-text">
                Click to register extension and receive calls
              </p>
            </div>
            
            <button class="logout-btn" @click="handleLogout">Logout</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Expand Button (for collapsed sidebar) -->
    <button class="expand-btn" @click="expandSidebar" id="expand-btn">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M3 12H21M3 6H21M3 18H21" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </button>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import {
  testServerConnection,
  initSIP,
  joinQueue,
  leaveQueue,
  answerCall,
  rejectCall,
  hangupCall,
  muteCall,
  sendDTMF,
  on,
  off,
  cleanup,
  getCallStatus,
  getRegistrationStatus
} from '@/utils/sipClient'

// ==========================================
// ROUTER SETUP
// ==========================================
const router = useRouter()
const route = useRoute()

// ==========================================
// PROPS (Data coming from parent component)
// ==========================================
const props = defineProps({
  userRole: {
    type: String,
    default: 'user'  // Can be 'user' or 'super-admin'
  },
  isInQueue: {
    type: Boolean,
    default: false   // Whether user is currently in queue
  },
  isProcessingQueue: {
    type: Boolean,
    default: false   // Whether queue operation is in progress
  },
  currentCall: {
    type: Object,
    default: null    // Current call information
  }
})

// ==========================================
// EMITS (Events sent to parent component)
// ==========================================
const emit = defineEmits([
  'toggle-queue',     // When queue button is clicked
  'logout',          // When logout button is clicked
  'sidebar-toggle',  // When sidebar is collapsed/expanded
  'incoming-call',   // When there's an incoming call
  'call-answered',   // When call is answered
  'call-ended'       // When call ends
])

// ==========================================
// LOCAL REACTIVE STATE
// ==========================================

// UI state for sidebar behavior
const isSidebarCollapsed = ref(false)  // Is sidebar collapsed?
const mobileOpen = ref(false)          // Is mobile menu open?

// Server connection state (same as TestCall component)
const serverStatus = ref({
  isTestingConnection: false,  // Currently testing connection?
  isServerAccessible: false,   // Is Asterisk server reachable?
  connectionError: null        // Error message if connection failed
})

// SIP and call state (same as TestCall component)
const sipStatus = ref({
  isRegistered: false,    // Is SIP extension registered?
  isInQueue: false,       // Is user in queue (extension registered)?
  hasActiveCall: false,   // Is there an active call?
  hasIncomingCall: false, // Is there an incoming call?
  callDuration: '00:00:00' // Current call duration
})

// ==========================================
// COMPUTED PROPERTIES (Calculated values)
// ==========================================

// Server connection status text and CSS class
const connectionStatus = computed(() => {
  if (serverStatus.value.isTestingConnection) {
    return { text: 'Testing Connection...', class: 'testing' }
  }
  if (serverStatus.value.isServerAccessible) {
    return { text: 'Server Connected', class: 'connected' }
  }
  if (serverStatus.value.connectionError) {
    return { text: 'Connection Failed', class: 'error' }
  }
  return { text: 'Not Connected', class: 'disconnected' }
})

// Can user join queue? (only if server is accessible)
const canJoinQueue = computed(() => {
  return serverStatus.value.isServerAccessible && !serverStatus.value.isTestingConnection
})

// Current queue/call status text
const queueStatus = computed(() => {
  if (sipStatus.value.hasIncomingCall) {
    return 'Incoming Call'
  }
  if (sipStatus.value.hasActiveCall) {
    return 'On Call'
  }
  return sipStatus.value.isInQueue ? 'In Queue' : 'Offline'
})

// Queue button text based on current state
const queueButtonText = computed(() => {
  if (props.isProcessingQueue) return 'Processing...'
  if (sipStatus.value.hasActiveCall || sipStatus.value.hasIncomingCall) return 'End Call'
  return sipStatus.value.isInQueue ? 'Leave Queue' : 'Join Queue'
})

// ==========================================
// SERVER CONNECTION FUNCTIONS
// ==========================================

// Test if Asterisk server is accessible (same as TestCall)
const testAsteriskConnection = async () => {
  try {
    // Set testing state
    serverStatus.value.isTestingConnection = true
    serverStatus.value.connectionError = null
    
    // Get SIP connection details from localStorage
    const sipDetails = JSON.parse(localStorage.getItem('sipConnectionDetails'))
    
    if (!sipDetails?.websocketURL) {
      throw new Error('Missing Asterisk server details')
    }

    console.log('Testing Asterisk server connection...')
    
    // Test server accessibility using WebSocket
    const isAccessible = await testServerConnection(sipDetails.websocketURL)
    
    if (isAccessible) {
      serverStatus.value.isServerAccessible = true
      console.log('Asterisk server is accessible')
    } else {
      throw new Error('Asterisk server is not responding')
    }

  } catch (error) {
    console.error('Server connection test failed:', error)
    serverStatus.value.connectionError = error.message
    serverStatus.value.isServerAccessible = false
  } finally {
    // Always stop testing state
    serverStatus.value.isTestingConnection = false
  }
}

// Retry server connection when it fails
const retryConnection = () => {
  testAsteriskConnection()
}

// ==========================================
// QUEUE MANAGEMENT FUNCTIONS
// ==========================================

// Handle join/leave queue (same logic as TestCall)
const handleQueueToggle = async () => {
  // Don't proceed if server not accessible
  if (!canJoinQueue.value) return
  
  try {
    if (sipStatus.value.isInQueue) {
      // LEAVE QUEUE = Unregister SIP extension
      console.log('Leaving queue - unregistering extension...')
      await leaveQueue()
      sipStatus.value.isInQueue = false
      sipStatus.value.isRegistered = false
      console.log('Left queue and unregistered extension')
      
    } else {
      // JOIN QUEUE = Initialize SIP and register extension
      console.log('Joining queue - initializing SIP and registering extension...')
      
      // Get SIP credentials from localStorage
      const sipDetails = JSON.parse(localStorage.getItem('sipConnectionDetails'))
      
      // Initialize SIP client
      await initSIP({
        Desc: sipDetails.Desc || 'Agent Extension',
        sipUri: sipDetails.uri,
        password: sipDetails.password,
        websocketURL: sipDetails.websocketURL,
        debug: true
      })
      
      // Set up SIP event listeners
      setupSipEventListeners()
      
      // Register extension (this makes it accessible for calls)
      await joinQueue()
      sipStatus.value.isInQueue = true
      console.log('Successfully joined queue - extension registered')
    }
    
    // Notify parent component about queue change
    emit('toggle-queue')
    
  } catch (error) {
    console.error('Queue operation failed:', error)
    // Reset states on error
    sipStatus.value.isInQueue = false
    sipStatus.value.isRegistered = false
  }
}

// ==========================================
// SIP EVENT LISTENERS SETUP
// ==========================================

// Set up all SIP event listeners (same as TestCall)
const setupSipEventListeners = () => {
  
  // EXTENSION REGISTRATION EVENTS
  on('onRegistered', () => {
    console.log('Extension registered - ready to receive calls')
    sipStatus.value.isRegistered = true
  })

  on('onUnregistered', () => {
    console.log('Extension unregistered - no longer accessible')
    sipStatus.value.isRegistered = false
    sipStatus.value.isInQueue = false
  })

  on('onRegistrationFailed', (error) => {
    console.error('Extension registration failed:', error)
    sipStatus.value.isRegistered = false
    sipStatus.value.isInQueue = false
  })

  // INCOMING CALL EVENTS
  on('onIncomingCall', (session) => {
    console.log('Incoming call received from:', session.remote_identity.uri.user)
    sipStatus.value.hasIncomingCall = true
    
    // Notify parent component about incoming call
    emit('incoming-call', {
      session,
      callerId: session.remote_identity.uri.user,
      callerName: session.remote_identity.display_name || session.remote_identity.uri.user
    })
  })

  // CALL ANSWER/START EVENTS
  on('onCallAnswered', (session) => {
    console.log('Call answered successfully')
    sipStatus.value.hasActiveCall = true
    sipStatus.value.hasIncomingCall = false
    
    // Notify parent component about answered call
    emit('call-answered', session)
  })

  // CALL END EVENTS
  on('onCallEnded', () => {
    console.log('Call ended')
    sipStatus.value.hasActiveCall = false
    sipStatus.value.hasIncomingCall = false
    
    // Notify parent component about call ending
    emit('call-ended')
  })

  on('onCallRejected', () => {
    console.log('Call rejected')
    sipStatus.value.hasIncomingCall = false
  })

  // CONNECTION EVENTS
  on('onDisconnected', () => {
    console.log('SIP disconnected')
    sipStatus.value.isRegistered = false
    sipStatus.value.isInQueue = false
  })

  // QUEUE EVENTS
  on('onQueueJoined', () => {
    console.log('Successfully joined queue')
    sipStatus.value.isInQueue = true
  })

  on('onQueueLeft', () => {
    console.log('Successfully left queue')
    sipStatus.value.isInQueue = false
  })
}

// ==========================================
// SIDEBAR UI FUNCTIONS
// ==========================================

// Toggle sidebar collapsed/expanded state
const toggleSidebar = () => {
  isSidebarCollapsed.value = !isSidebarCollapsed.value
  emit('sidebar-toggle', isSidebarCollapsed.value)
}

// Expand sidebar (from collapsed state)
const expandSidebar = () => {
  isSidebarCollapsed.value = false
  emit('sidebar-toggle', isSidebarCollapsed.value)
}

// Toggle mobile menu open/closed
const toggleMobileMenu = () => {
  mobileOpen.value = !mobileOpen.value
}

// Handle logout - clean up SIP and notify parent
const handleLogout = () => {
  // Clean up SIP connections before logout
  cleanup()
  emit('logout')
}

// ==========================================
// LIFECYCLE HOOKS
// ==========================================

// When component is mounted (appears on screen)
onMounted(() => {
  // Test server accessibility immediately
  testAsteriskConnection()
  
  // Set up router behavior for mobile
  router.afterEach(() => {
    // Close mobile menu after navigation on small screens
    if (window.innerWidth <= 1024) {
      mobileOpen.value = false
    }
  })
})

// When component is about to be destroyed
onBeforeUnmount(() => {
  // Clean up SIP connections
  cleanup()
  
  // Remove all SIP event listeners to prevent memory leaks
  off('onRegistered')
  off('onUnregistered')
  off('onRegistrationFailed')
  off('onIncomingCall')
  off('onCallAnswered')
  off('onCallEnded')
  off('onCallRejected')
  off('onDisconnected')
  off('onQueueJoined')
  off('onQueueLeft')
})
</script>

<style scoped>
/* ==========================================
   MAIN SIDEBAR CONTAINER
   ========================================== */
.sidebar {
  width: 250px;                          /* Fixed width */
  background-color: var(--sidebar-bg);   /* Uses CSS custom property */
  color: var(--text-color);              /* Text color from theme */
  height: 100vh;                         /* Full viewport height */
  position: fixed;                       /* Stays in place when scrolling */
  transition: width 0.3s ease, transform 0.3s ease, background-color 0.3s;
  overflow: hidden;                      /* Hide overflow content */
  border-radius: 0 30px 30px 0;         /* Rounded right corners */
  z-index: 100;                          /* Layer above other content */
  display: flex;
  flex-direction: column;                /* Stack items vertically */
}

/* Sidebar content wrapper */
.sidebar-content {
  width: 250px;                          /* Match sidebar width */
  height: 100%;
  display: flex;
  flex-direction: column;                /* Header, nav, bottom sections */
  overflow: hidden;
}

/* ==========================================
   SIDEBAR HEADER (Logo area)
   ========================================== */
.sidebar-header {
  flex-shrink: 0;                        /* Don't shrink when space is tight */
  padding: 20px;
  text-align: center;
}

.logo-container {
  display: flex;
  justify-content: center;
}

.logo {
  width: 50px;
  height: 50px;
  border-radius: 50%;                    /* Make it circular */
  background-color: var(--logo-bg);
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;                      /* Crop image if too big */
}

.logo img {
  width: 30px;
  height: 30px;
  object-fit: contain;                   /* Maintain aspect ratio */
}

/* ==========================================
   NAVIGATION SECTION
   ========================================== */
.nav-section {
  flex: 1;                               /* Take up remaining space */
  overflow-y: auto;                      /* Scroll if too many items */
  overflow-x: hidden;                    /* No horizontal scroll */
  padding: 0 15px;
  margin-bottom: 0;
  min-height: 0;                         /* Allow shrinking */
  scrollbar-width: none;                 /* Hide scrollbar (Firefox) */
  -ms-overflow-style: none;              /* Hide scrollbar (IE/Edge) */
}

/* Hide scrollbar for WebKit browsers */
.nav-section::-webkit-scrollbar {
  display: none;
}

/* Individual navigation items */
.nav-item {
  display: flex;
  align-items: center;
  padding: 10px 12px;
  cursor: pointer;
  margin-bottom: 4px;
  border-radius: 12px;
  text-decoration: none;                 /* Remove link underline */
  color: var(--text-color);
  transition: all 0.3s ease;             /* Smooth hover effects */
  min-height: 44px;                      /* Minimum touch target */
}

/* Hover effects for nav items */
.nav-item:hover {
  background-color: rgba(255, 255, 255, 0.05);  /* Subtle highlight */
  transform: translateX(3px);                    /* Slide right slightly */
}

/* Active/current page styling */
.nav-item.active {
  background-color: rgba(255, 255, 255, 0.1);   /* More prominent highlight */
}

/* Icon container for nav items */
.nav-icon {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 12px;
  border-radius: 8px;
  background-color: rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
  flex-shrink: 0;                        /* Don't shrink icon */
}

/* Hover effect for icons */
.nav-item:hover .nav-icon {
  background-color: rgba(255, 255, 255, 0.2);
  transform: scale(1.05);                /* Slightly larger on hover */
}

/* SVG styling inside icons */
.nav-icon svg {
  color: var(--text-color);
  stroke: var(--text-color);
  width: 18px;
  height: 18px;
}

/* Text styling for nav items */
.nav-text {
  font-size: 14px;
  font-weight: 600;
  white-space: nowrap;                   /* Don't wrap text */
  overflow: hidden;                      /* Hide overflow */
  text-overflow: ellipsis;               /* Show ... if text too long */
}

/* ==========================================
   SIDEBAR BOTTOM SECTION
   ========================================== */
.sidebar-bottom {
  padding: 15px;
  flex-shrink: 0;                        /* Don't shrink this section */
  background-color: var(--sidebar-bg);
  border-top: 1px solid rgba(255, 255, 255, 0.1);  /* Subtle separator */
}

/* ==========================================
   USER PROFILE SECTION
   ========================================== */
.user-profile {
  display: flex;
  justify-content: center;
  margin-bottom: 12px;
}

.user-avatar {
  width: 44px;
  height: 44px;
  border-radius: 50%;                    /* Circular avatar */
  background-color: var(--text-color);
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  overflow: hidden;
  text-decoration: none;
  transition: all 0.3s ease;
}

.user-avatar:hover {
  transform: scale(1.05);                /* Slightly larger on hover */
}

.user-avatar svg {
  width: 24px;
  height: 24px;
  fill: var(--background-color);
}

/* ==========================================
   SERVER CONNECTION STATUS (NEW!)
   ========================================== */
.connection-section {
  margin-bottom: 10px;
  padding: 8px;
  background: rgba(255, 255, 255, 0.05); /* Subtle background */
  border-radius: 8px;
}

.connection-status {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-bottom: 5px;
}

/* Connection indicator dot */
.connection-indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}

/* Different states for connection indicator */
.connection-indicator.testing {
  background: #ffc107;                   /* Yellow for testing */
  animation: pulse 1s infinite;          /* Pulsing animation */
}

.connection-indicator.connected {
  background: #28a745;                   /* Green for connected */
  box-shadow: 0 0 0 2px rgba(40, 167, 69, 0.2);  /* Glow effect */
}

.connection-indicator.disconnected {
  background: #6c757d;                   /* Gray for disconnected */
}

.connection-indicator.error {
  background: #dc3545;                   /* Red for error */
}

/* Pulsing animation for testing state */
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}

.connection-text {
  font-size: 11px;
  font-weight: 600;
  color: var(--text-color);
}

/* Error section styling */
.error-section {
  margin-top: 5px;
  padding: 5px;
  background: rgba(220, 53, 69, 0.1);    /* Light red background */
  border: 1px solid rgba(220, 53, 69, 0.3);  /* Red border */
  border-radius: 4px;
}

.error-message {
  color: #ff6b6b;                        /* Red text */
  font-size: 10px;
  margin: 0 0 5px 0;
  text-align: center;
}

.retry-btn {
  padding: 3px 8px;
  background: #dc3545;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 10px;
  width: 100%;
}

.retry-btn:hover {
  background: #c82333;                   /* Darker red on hover */
}

/* ==========================================
   QUEUE STATUS SECTION
   ========================================== */
.status {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 600;
  margin-bottom: 12px;
  color: var(--text-secondary);
}

/* Status indicator dot */
.status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background-color: var(--unassigned-color);  /* Default gray */
  margin-right: 6px;
  transition: all 0.3s ease;
}

/* Green pulsing dot when in queue */
.status-dot.in-queue {
  background-color: var(--success-color);
  animation: statusPulse 2s infinite;
}

@keyframes statusPulse {
  0% { opacity: 1; }
  50% { opacity: 0.5; }
  100% { opacity: 1; }
}

/* ==========================================
   BUTTON CONTAINER AND BUTTONS
   ========================================== */
.button-container {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

/* Main queue join/leave button */
.join-queue-btn {
  background-color: var(--accent-color);  /* Default blue */
  color: white;
  border: none;
  border-radius: 25px;                   /* Rounded pill shape */
  padding: 10px 14px;
  width: 100%;
  font-weight: 700;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.join-queue-btn:hover:not(:disabled) {
  background-color: var(--accent-hover);
  transform: translateY(-1px);           /* Lift up slightly on hover */
}

/* Green when in queue */
.join-queue-btn.in-queue {
  background-color: var(--success-color);
}

/* Red when on a call */
.join-queue-btn.has-call {
  background-color: var(--danger-color);
}

/* Disabled state */
.join-queue-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;                       /* No hover effect when disabled */
}

/* Queue help text section */
.queue-help-text {
  margin-bottom: 8px;
}

.help-text {
  text-align: center;
  font-size: 10px;
  color: #999;                           /* Light gray */
  margin: 0;
  font-style: italic;
  line-height: 1.2;
}

/* Success state for help text */
.help-text.success {
  color: #28a745;                        /* Green */
  font-weight: 600;
  font-style: normal;                    /* Not italic */
}

/* Logout button */
.logout-btn {
  background-color: var(--danger-color);
  color: white;
  border: none;
  border-radius: 25px;
  padding: 10px 14px;
  width: 100%;
  font-weight: 700;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.logout-btn:hover {
  background-color: #e60000;             /* Darker red on hover */
  transform: translateY(-1px);
}

/* ==========================================
   TOGGLE BUTTONS (Collapse/Expand)
   ========================================== */
.toggle-btn {
  position: absolute;
  top: 50px;
  right: -15px;                          /* Positioned outside sidebar */
  width: 30px;
  height: 30px;
  background-color: #ffffff;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  z-index: 10;
  border: none;
  color: #333333;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
  transition: all 0.3s ease;
}

.toggle-btn:hover {
  transform: scale(1.1);
  box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

.expand-btn {
  position: fixed;
  top: 50px;
  left: 5px;
  width: 30px;
  height: 30px;
  background-color: #ffffff;
  border-radius: 50%;
  display: none;                         /* Hidden by default */
  justify-content: center;
  align-items: center;
  cursor: pointer;
  z-index: 101;
  border: none;
  color: #333333;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
  transition: all 0.3s ease;
}

.expand-btn:hover {
  transform: scale(1.1);
  box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

/* Show expand button when sidebar is collapsed */
.sidebar.collapsed ~ .expand-btn {
  display: flex;
}

/* ==========================================
   SIDEBAR COLLAPSED STATE
   ========================================== */
.sidebar.collapsed {
  width: 20px;                           /* Very narrow when collapsed */
  transform: translateX(-230px);         /* Slide mostly off-screen */
}

.sidebar.collapsed .sidebar-content {
  opacity: 0;                            /* Hide content when collapsed */
  pointer-events: none;                  /* Disable interactions */
}

/* ==========================================
   MOBILE MENU BUTTON
   ========================================== */
.mobile-menu-btn {
  display: none;                         /* Hidden on desktop */
  position: fixed;
  top: 20px;
  left: 20px;
  width: 40px;
  height: 40px;
  background-color: var(--content-bg);
  border: 1px solid var(--border-color);
  border-radius: 50%;
  color: var(--text-color);
  cursor: pointer;
  z-index: 102;                          /* Above sidebar */
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.mobile-menu-btn:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

/* ==========================================
   RESPONSIVE DESIGN (Mobile/Tablet)
   ========================================== */
@media (max-width: 1024px) {
  /* Show mobile menu button */
  .mobile-menu-btn {
    display: flex;
  }
  
  /* Hide sidebar by default on mobile */
  .sidebar {
    transform: translateX(-100%);        /* Completely off-screen */
    z-index: 200;                        /* Above other content */
  }
  
  /* Show sidebar when mobile menu is open */
  .sidebar.mobile-open {
    transform: translateX(0);            /* Slide back into view */
  }
  
  /* Hide expand button on mobile */
  .expand-btn {
    display: none !important;
  }
}
</style>