<template>
  <div class="dashboard-layout">
    <button class="mobile-menu-btn" id="mobile-menu-btn" @click="toggleMobileMenu">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M3 12H21M3 6H21M3 18H21" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </button>

    <div class="sidebar" :class="{ collapsed: isSidebarCollapsed, 'mobile-open': mobileOpen }">
      <div class="toggle-btn" @click="toggleSidebar">{{ isSidebarCollapsed ? '>' : '<' }}</div>
      
      <div class="sidebar-content">
        <div class="logo-container">
          <div class="logo">
            <img src="/placeholder.svg?height=40&width=40" alt="OpenCHS Logo">
          </div>
        </div>
        
        <a href="#" class="nav-item">
          <div class="nav-icon"></div>
          <div class="nav-text">Dashboard</div>
        </a>
        
        <a href="#" class="nav-item active">
          <div class="nav-icon"></div>
          <div class="nav-text">Calls</div>
        </a>
        
        <a href="#" class="nav-item">
          <div class="nav-icon"></div>
          <div class="nav-text">Cases</div>
        </a>
        
        <a href="#" class="nav-item">
          <div class="nav-icon"></div>
          <div class="nav-text">Chats</div>
        </a>
        
        <a href="#" class="nav-item">
          <div class="nav-icon"></div>
          <div class="nav-text">QA Statistics</div>
        </a>
        
        <a href="#" class="nav-item">
          <div class="nav-icon"></div>
          <div class="nav-text">Wallboard</div>
        </a>
        
        <a href="#" class="nav-item">
          <div class="nav-icon"></div>
          <div class="nav-text">Settings</div>
        </a>
        
        <div class="user-profile">
          <a href="#" class="user-avatar">
            <svg viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 12C14.2091 12 16 10.2091 16 8C16 5.79086 14.2091 4 12 4C9.79086 4 8 5.79086 8 8C8 10.2091 9.79086 12 12 12Z"/>
              <path d="M12 14C7.58172 14 4 17.5817 4 22H20C20 17.5817 16.4183 14 12 14Z"/>
            </svg>
          </a>
        </div>
        
        <div class="status">
          <div class="status-dot"></div>
          <span>Status: Online</span>
        </div>
        
        <div class="button-container">
          <button class="join-queue-btn">Join Queue</button>
          <button class="logout-btn" @click="logout">Logout</button>
        </div>
      </div>
    </div>

    <button class="expand-btn" @click="expandSidebar" v-show="isSidebarCollapsed">></button>

    <div class="main-content">
      <div class="calls-container">
        <div class="header">
          <h1>Calls</h1>
          <button class="theme-toggle" @click="toggleTheme">
            <svg v-show="currentTheme === 'dark'" width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <svg v-show="currentTheme === 'light'" width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="12" cy="12" r="5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <line x1="12" y1="1" x2="12" y2="3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <line x1="12" y1="21" x2="12" y2="23" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <line x1="4.22" y1="4.22" x2="5.64" y2="5.64" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <line x1="18.36" y1="18.36" x2="19.78" y2="19.78" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <line x1="1" y1="12" x2="3" y2="12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <line x1="21" y1="12" x2="23" y2="12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <line x1="4.22" y1="19.78" x2="5.64" y2="18.36" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <line x1="18.36" y1="5.64" x2="19.78" y2="4.22" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <span>{{ currentTheme === 'dark' ? 'Light Mode' : 'Dark Mode' }}</span>
          </button>
        </div>
        
        <div class="view-tabs">
          <div class="view-tab" :class="{ active: activeView === 'timeline' }" @click="activeView = 'timeline'">Timeline</div>
          <div class="view-tab" :class="{ active: activeView === 'table' }" @click="activeView = 'table'">Table View</div>
        </div>
        
        <!-- Timeline View -->
        <div class="view-container" v-show="activeView === 'timeline'">
          <div class="time-section" v-for="(group, label) in groupedCalls" :key="label">
            <h2 class="time-section-title">{{ label }}</h2>
            <div class="call-list">
              <div 
                v-for="call in group" 
                :key="call.id" 
                class="call-item timeline-connector" 
                :class="{ selected: call.id === selectedCallId }" 
                @click="selectCall(call.id)"
              >
                <div class="call-icon">
                  <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07 19.5 19.5 0 01-6-6 19.79 19.79 0 01-3.07-8.67A2 2 0 014.11 2h3a2 2 0 012 1.72c.127.96.361 1.903.7 2.81a2 2 0 01-.45 2.11L8.09 9.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0122 16.92z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </div>
                <div class="call-details">
                  <div class="call-type">{{ call.title }}</div>
                  <div class="call-time">{{ call.time }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Table View -->
        <div class="view-container" v-show="activeView === 'table'">
          <div class="calls-table-container">
            <table class="calls-table">
              <thead>
                <tr>
                  <th>Call Type</th>
                  <th>Date</th>
                  <th>Time</th>
                  <th>Status</th>
                  <th>Agent</th>
                </tr>
              </thead>
              <tbody>
                <tr 
                  v-for="call in allCalls" 
                  :key="call.id" 
                  :class="{ selected: call.id === selectedCallId }" 
                  @click="selectCall(call.id)"
                >
                  <td>{{ call.title }}</td>
                  <td>{{ call.dateLabel }}</td>
                  <td>{{ call.time }}</td>
                  <td>
                    <span :class="['status-badge', call.status.toLowerCase().replace(/\s+/g, '-')]">{{ call.status }}</span>
                  </td>
                  <td>{{ call.agent || 'Unassigned' }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
      
      <div class="status-container">
        <h2 class="status-header">Status</h2>
        
        <div class="select-wrapper">
          <select class="time-range-select" v-model="selectedTimeRange">
            <option value="all">Select Time range</option>
            <option value="today">Today</option>
            <option value="week">This Week</option>
            <option value="month">This Month</option>
            <option value="30days">Last 30 Days</option>
            <option value="custom">Custom Range</option>
          </select>
          <div class="select-arrow">
            <svg width="12" height="6" viewBox="0 0 12 6" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M1 1L6 5L11 1" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
        </div>
        
        <div class="status-item" v-for="status in statusItems" :key="status.label">
          <div class="status-item-header">
            <div class="status-label">{{ status.label }}</div>
            <div class="status-count">{{ status.count }} {{ status.label === 'Unassigned' || status.label === 'In Progress' || status.label === 'Completed' ? status.label : '' }}</div>
          </div>
          <div class="progress-bar">
            <div class="progress-fill" :style="{ width: status.percentage + '%' }"></div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Call Details Panel -->
    <div class="call-details-panel" :class="{ active: showCallDetails }" id="call-details-panel">
      <div class="call-details-header">
        <div class="call-details-title">{{ selectedCallDetails?.title || 'Call Details' }}</div>
        <button class="close-details" @click="closeCallDetails">×</button>
      </div>
      <div class="call-details-content" v-if="selectedCallDetails">
        <div class="detail-item">
          <div class="detail-label">Call Title</div>
          <div class="detail-value">{{ selectedCallDetails.callTitle }}</div>
        </div>
        <div class="detail-item">
          <div class="detail-label">Call ID</div>
          <div class="detail-value">{{ selectedCallDetails.id }}</div>
        </div>
        <div class="detail-item">
          <div class="detail-label">Caller</div>
          <div class="detail-value">{{ selectedCallDetails.callerName }}</div>
        </div>
        <div class="detail-item">
          <div class="detail-label">Duration</div>
          <div class="detail-value">{{ selectedCallDetails.duration }}</div>
        </div>
        <div class="detail-item">
          <div class="detail-label">Call Start</div>
          <div class="detail-value">{{ selectedCallDetails.callStart }}</div>
        </div>
        <div class="detail-item">
          <div class="detail-label">Call End</div>
          <div class="detail-value">{{ selectedCallDetails.callEnd }}</div>
        </div>
        <div class="detail-item">
          <div class="detail-label">Disposition</div>
          <div class="detail-value">{{ selectedCallDetails.disposition }}</div>
        </div>
        <div class="detail-item">
          <div class="detail-label">Date</div>
          <div class="detail-value">{{ selectedCallDetails.date }}</div>
        </div>
        <div class="detail-item">
          <div class="detail-label">Escalated to</div>
          <div class="detail-value">{{ selectedCallDetails.escalatedTo }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const isSidebarCollapsed = ref(false)
const mobileOpen = ref(false)
const activeView = ref('timeline')
const selectedCallId = ref('1348456')
const currentTheme = ref(localStorage.getItem('theme') || 'dark')
const selectedTimeRange = ref('all')
const showCallDetails = ref(false)

// Call data
const callData = reactive({
  '1348456': {
    id: '1348456',
    title: 'Emergency Crisis: Domestic Violence',
    time: '09:00AM',
    dateLabel: 'Today',
    status: 'In Progress',
    agent: 'Sarah Davis',
    callTitle: 'Emergency call',
    callerName: 'Nelson Adega',
    duration: '3min 5 sec',
    callStart: '09:00 am',
    callEnd: '09:03 am',
    disposition: 'Abusive Call',
    date: '15th Aug 2025',
    escalatedTo: 'Ntaate Kimani',
    group: 'Today'
  },
  '1348457': {
    id: '1348457',
    title: 'Survivor Follow-Up: Safety Planning',
    time: '10:30AM',
    dateLabel: 'Today',
    status: 'Pending',
    agent: null,
    callTitle: 'Follow-up call',
    callerName: 'Maria Johnson',
    duration: '15min 20 sec',
    callStart: '10:30 am',
    callEnd: '10:45 am',
    disposition: 'Completed',
    date: '15th Aug 2025',
    escalatedTo: 'David Lee',
    group: 'Today'
  },
  '1348458': {
    id: '1348458',
    title: 'Scheduled Support: Therapy Session',
    time: '02:00PM',
    dateLabel: 'Today',
    status: 'In Progress',
    agent: 'Mark Reynolds',
    callTitle: 'Therapy Session',
    callerName: 'James Wilson',
    duration: '45min 10 sec',
    callStart: '02:00 pm',
    callEnd: '02:45 pm',
    disposition: 'Completed',
    date: '15th Aug 2025',
    escalatedTo: 'Dr. Lisa Chen',
    group: 'Today'
  },
  '1348459': {
    id: '1348459',
    title: 'Resource Request: Shelter Information',
    time: '04:45PM',
    dateLabel: 'Today',
    status: 'Unassigned',
    agent: null,
    callTitle: 'Shelter Information',
    callerName: 'Anonymous',
    duration: '8min 30 sec',
    callStart: '04:45 pm',
    callEnd: '04:53 pm',
    disposition: 'Information Provided',
    date: '15th Aug 2025',
    escalatedTo: 'Unassigned',
    group: 'Today'
  },
  '1348460': {
    id: '1348460',
    title: 'Wellness Check-In: Mental Health Support',
    time: '11:15AM',
    dateLabel: 'Yesterday',
    status: 'Completed',
    agent: 'Emily Chan',
    callTitle: 'Mental Health Support',
    callerName: 'Rebecca Taylor',
    duration: '22min 15 sec',
    callStart: '11:15 am',
    callEnd: '11:37 am',
    disposition: 'Completed',
    date: '14th Aug 2025',
    escalatedTo: 'Dr. Michael Brown',
    group: 'Yesterday'
  },
  '1348461': {
    id: '1348461',
    title: 'Appointment Booking: Legal Advocacy',
    time: '01:30PM',
    dateLabel: 'Yesterday',
    status: 'Completed',
    agent: 'David Lee',
    callTitle: 'Legal Advocacy',
    callerName: 'Thomas Garcia',
    duration: '12min 40 sec',
    callStart: '01:30 pm',
    callEnd: '01:42 pm',
    disposition: 'Appointment Scheduled',
    date: '14th Aug 2025',
    escalatedTo: 'Legal Team',
    group: 'Yesterday'
  },
  '1348462': {
    id: '1348462',
    title: 'Call Back: Housing Assistance Follow-up',
    time: '05:00PM',
    dateLabel: 'Yesterday',
    status: 'Completed',
    agent: 'Sophia Clark',
    callTitle: 'Housing Assistance',
    callerName: 'Jennifer Lopez',
    duration: '18min 22 sec',
    callStart: '05:00 pm',
    callEnd: '05:18 pm',
    disposition: 'Completed',
    date: '14th Aug 2025',
    escalatedTo: 'Housing Department',
    group: 'Yesterday'
  },
  '1348463': {
    id: '1348463',
    title: 'Wellness Check-In: Mental Health Support',
    time: '11:15AM',
    dateLabel: 'This Week',
    status: 'Completed',
    agent: 'Emily Chan',
    callTitle: 'Mental Health Support',
    callerName: 'Sarah Johnson',
    duration: '25min 05 sec',
    callStart: '11:15 am',
    callEnd: '11:40 am',
    disposition: 'Completed',
    date: '12th Aug 2025',
    escalatedTo: 'Dr. Michael Brown',
    group: 'This week'
  },
  '1348464': {
    id: '1348464',
    title: 'Appointment Booking: Legal Advocacy',
    time: '01:30PM',
    dateLabel: 'This Week',
    status: 'Completed',
    agent: 'David Lee',
    callTitle: 'Legal Advocacy',
    callerName: 'Robert Smith',
    duration: '15min 30 sec',
    callStart: '01:30 pm',
    callEnd: '01:45 pm',
    disposition: 'Appointment Scheduled',
    date: '12th Aug 2025',
    escalatedTo: 'Legal Team',
    group: 'This week'
  },
  '1348465': {
    id: '1348465',
    title: 'Call Back: Housing Assistance Follow-up',
    time: '05:00PM',
    dateLabel: 'This Week',
    status: 'Completed',
    agent: 'Sophia Clark',
    callTitle: 'Housing Assistance',
    callerName: 'Michael Brown',
    duration: '10min 45 sec',
    callStart: '05:00 pm',
    callEnd: '05:10 pm',
    disposition: 'Completed',
    date: '11th Aug 2025',
    escalatedTo: 'Housing Department',
    group: 'This week'
  },
  '1348466': {
    id: '1348466',
    title: 'Call Back: Financial Assistance Inquiry',
    time: '05:00PM',
    dateLabel: 'This Week',
    status: 'Completed',
    agent: 'Mark Reynolds',
    callTitle: 'Financial Assistance',
    callerName: 'Jessica Williams',
    duration: '14min 20 sec',
    callStart: '05:00 pm',
    callEnd: '05:14 pm',
    disposition: 'Completed',
    date: '11th Aug 2025',
    escalatedTo: 'Financial Aid Department',
    group: 'This week'
  }
})

// Status data
const statusItems = [
  { label: 'Unassigned', count: 16, percentage: 53 },
  { label: 'Pending', count: 5, percentage: 17 },
  { label: 'In Progress', count: 24, percentage: 80 },
  { label: 'Completed', count: 8, percentage: 27 }
]

// Computed properties
const allCalls = computed(() => {
  return Object.values(callData)
})

const groupedCalls = computed(() => {
  const groups = {}
  
  allCalls.value.forEach(call => {
    if (!groups[call.group]) {
      groups[call.group] = []
    }
    groups[call.group].push(call)
  })
  
  return groups
})

const selectedCallDetails = computed(() => {
  return callData[selectedCallId.value] || null
})

// Methods
function toggleSidebar() {
  isSidebarCollapsed.value = !isSidebarCollapsed.value
}

function expandSidebar() {
  isSidebarCollapsed.value = false
}

function toggleMobileMenu() {
  mobileOpen.value = !mobileOpen.value
}

function applyTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme)
  localStorage.setItem('theme', theme)
  currentTheme.value = theme
}

function toggleTheme() {
  applyTheme(currentTheme.value === 'dark' ? 'light' : 'dark')
}

function selectCall(callId) {
  selectedCallId.value = callId
  showCallDetails.value = true
}

function closeCallDetails() {
  showCallDetails.value = false
}

function logout() {
  router.push('/')
}

const handleClickOutside = (event) => {
  const sidebar = document.querySelector('.sidebar')
  const mobileMenuBtn = document.querySelector('.mobile-menu-btn')
  
  if (window.innerWidth <= 768 && 
      !sidebar?.contains(event.target) && 
      event.target !== mobileMenuBtn &&
      !mobileMenuBtn?.contains(event.target)) {
    mobileOpen.value = false
  }
}

const handleResize = () => {
  if (window.innerWidth > 768) {
    mobileOpen.value = false
  }
}

onMounted(() => {
  applyTheme(currentTheme.value)
  document.addEventListener('click', handleClickOutside)
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
:root {
  /* Dark theme variables */
  --background-color: #0a0a0a;
  --sidebar-bg: #111;
  --content-bg: #222;
  --text-color: #fff;
  --text-secondary: #aaa;
  --border-color: #333;
  --accent-color: #964B00;
  --accent-hover: #b25900;
  --danger-color: #ff3b30;
  --success-color: #4CAF50;
  --pending-color: #FFA500;
  --unassigned-color: #808080;
  --highlight-color: #ff3b30;
  --header-bg: #333;
}

[data-theme="light"] {
  --background-color: #f5f5f5;
  --sidebar-bg: #ffffff;
  --content-bg: #ffffff;
  --text-color: #333;
  --text-secondary: #666;
  --border-color: #ddd;
  --accent-color: #964B00;
  --accent-hover: #b25900;
  --danger-color: #ff3b30;
  --success-color: #4CAF50;
  --pending-color: #FFA500;
  --unassigned-color: #808080;
  --highlight-color: #ff3b30;
  --header-bg: #f0f0f0;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Inter', sans-serif;
}

.dashboard-layout {
  background-color: var(--background-color);
  color: var(--text-color);
  display: flex;
  min-height: 100vh;
  transition: background-color 0.3s, color 0.3s;
}

.sidebar {
  width: 250px;
  background-color: var(--sidebar-bg);
  color: var(--text-color);
  height: 100vh;
  position: fixed;
  transition: width 0.3s ease, transform 0.3s ease, background-color 0.3s;
  overflow-x: hidden;
  border-radius: 0 30px 30px 0;
  z-index: 100;
}

.sidebar.collapsed {
  width: 20px;
  transform: translateX(-230px);
}

.toggle-btn {
  position: absolute;
  top: 50px;
  right: -15px;
  width: 30px;
  height: 30px;
  background-color: var(--text-color);
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  z-index: 10;
  border: 1px solid var(--border-color);
  color: var(--background-color);
  font-weight: bold;
  font-size: 14px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.expand-btn {
  position: fixed;
  top: 50px;
  left: 5px;
  width: 30px;
  height: 30px;
  background-color: var(--text-color);
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  z-index: 101;
  border: 1px solid var(--border-color);
  color: var(--background-color);
  font-weight: bold;
  font-size: 14px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.sidebar-content {
  padding: 30px 0;
  width: 250px;
  height: 100%;
  overflow-y: auto;
}

.sidebar.collapsed .sidebar-content {
  opacity: 0;
  pointer-events: none;
}

.logo-container {
  display: flex;
  justify-content: center;
  margin-bottom: 30px;
}

.logo {
  width: 70px;
  height: 70px;
  border-radius: 50%;
  background-color: var(--text-color);
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
}

.logo img {
  width: 40px;
  height: 40px;
  object-fit: contain;
}

.nav-item {
  display: flex;
  align-items: center;
  padding: 12px 20px;
  cursor: pointer;
  margin-bottom: 5px;
  border-radius: 30px 0 0 30px;
  text-decoration: none;
  color: var(--text-color);
}

.nav-item.active {
  background-color: rgba(255, 255, 255, 0.1);
}

.nav-icon {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  border: 2px solid var(--text-color);
  margin-right: 15px;
}

.nav-text {
  font-size: 14px;
  font-weight: 500;
}

.user-profile {
  display: flex;
  justify-content: center;
  margin: 30px 0 20px;
}

.user-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background-color: var(--text-color);
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  overflow: hidden;
}

.user-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.user-avatar svg {
  width: 30px;
  height: 30px;
  fill: var(--background-color);
}

.status {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  margin: 0 20px 15px;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: var(--success-color);
  margin-right: 5px;
}

.button-container {
  padding: 0 20px;
}

.join-queue-btn {
  background-color: var(--accent-color);
  color: white;
  border: none;
  border-radius: 30px;
  padding: 10px;
  width: 100%;
  font-weight: 600;
  cursor: pointer;
  margin-bottom: 10px;
}

.logout-btn {
  background-color: var(--danger-color);
  color: white;
  border: none;
  border-radius: 30px;
  padding: 10px;
  width: 100%;
  font-weight: 600;
  cursor: pointer;
}

.main-content {
  flex: 1;
  padding: 20px;
  margin-left: 250px;
  min-height: 100vh;
  background-color: var(--background-color);
  transition: margin-left 0.3s ease, background-color 0.3s;
  display: flex;
}

.sidebar.collapsed ~ .main-content {
  margin-left: 20px;
}

.calls-container {
  flex: 1;
  padding-right: 20px;
}

.status-container {
  width: 300px;
  padding-left: 20px;
  border-left: 1px solid var(--border-color);
}

.header {
  margin-bottom: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header h1 {
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 5px;
}

.theme-toggle {
  background-color: var(--content-bg);
  color: var(--text-color);
  border: 1px solid var(--border-color);
  border-radius: 30px;
  padding: 8px 15px;
  font-size: 14px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
}

.theme-toggle svg {
  width: 16px;
  height: 16px;
}

.view-tabs {
  display: flex;
  border-bottom: 1px solid var(--border-color);
  margin-bottom: 20px;
  overflow-x: auto;
  white-space: nowrap;
}

.view-tab {
  padding: 10px 20px;
  cursor: pointer;
  font-size: 14px;
  color: var(--text-secondary);
  position: relative;
}

.view-tab.active {
  color: var(--text-color);
  font-weight: 500;
}

.view-tab.active::after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 0;
  width: 100%;
  height: 2px;
  background-color: var(--text-color);
}

.time-section {
  margin-bottom: 30px;
}

.time-section-title {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 15px;
}

.call-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.call-item {
  display: flex;
  align-items: flex-start;
  cursor: pointer;
  padding: 10px;
  border-radius: 10px;
  transition: background-color 0.2s;
}

.call-item:hover {
  background-color: rgba(255, 255, 255, 0.05);
}

.call-item.selected {
  background-color: rgba(255, 59, 48, 0.1);
}

.call-item.selected .call-type {
  color: var(--highlight-color);
}

.call-icon {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background-color: var(--content-bg);
  display: flex;
  justify-content: center;
  align-items: center;
  margin-right: 15px;
  margin-top: 5px;
}

.call-icon svg {
  width: 16px;
  height: 16px;
  stroke: var(--text-color);
}

.call-details {
  flex: 1;
}

.call-type {
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 5px;
}

.call-time {
  font-size: 12px;
  color: var(--text-secondary);
}

.timeline-connector {
  position: relative;
}

.timeline-connector::before {
  content: '';
  position: absolute;
  top: 30px;
  left: 15px;
  width: 1px;
  height: calc(100% - 15px);
  background-color: var(--border-color);
}

.status-header {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 20px;
}

.select-wrapper {
  position: relative;
  margin-bottom: 30px;
}

.time-range-select {
  width: 100%;
  background-color: var(--content-bg);
  color: var(--text-color);
  border: none;
  border-radius: 30px;
  padding: 12px 20px;
  font-size: 14px;
  appearance: none;
  cursor: pointer;
}

.select-arrow {
  position: absolute;
  top: 50%;
  right: 20px;
  transform: translateY(-50%);
  pointer-events: none;
  width: 12px;
  height: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.select-arrow svg {
  stroke: var(--text-color);
}

.status-item {
  margin-bottom: 20px;
}

.status-item-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}

.status-label {
  font-size: 14px;
  font-weight: 500;
}

.status-count {
  font-size: 14px;
  color: var(--text-secondary);
}

.progress-bar {
  height: 6px;
  background-color: var(--border-color);
  border-radius: 30px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background-color: var(--accent-color);
  border-radius: 30px;
}

/* Table view styles */
.calls-table-container {
  overflow-x: auto;
  border-radius: 30px;
  background-color: var(--content-bg);
  margin-bottom: 20px;
}

.calls-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
}

.calls-table th {
  text-align: left;
  padding: 15px;
  background-color: var(--header-bg);
  font-weight: 600;
  font-size: 14px;
  position: sticky;
  top: 0;
  z-index: 10;
}

.calls-table th:first-child {
  border-top-left-radius: 30px;
}

.calls-table th:last-child {
  border-top-right-radius: 30px;
}

.calls-table td {
  padding: 15px;
  border-bottom: 1px solid var(--border-color);
  font-size: 14px;
}

.calls-table tr:last-child td {
  border-bottom: none;
}

.calls-table tr:last-child td:first-child {
  border-bottom-left-radius: 30px;
}

.calls-table tr:last-child td:last-child {
  border-bottom-right-radius: 30px;
}

.calls-table tr.selected td {
  background-color: rgba(255, 59, 48, 0.1);
  color: var(--highlight-color);
}

.status-badge {
  color: #fff;
  padding: 6px 15px;
  border-radius: 30px;
  font-size: 13px;
  display: inline-block;
  font-weight: 500;
  text-align: center;
  min-width: 90px;
}

.status-badge.in-progress {
  background-color: var(--accent-color);
}

.status-badge.pending {
  background-color: var(--pending-color);
}

.status-badge.unassigned {
  background-color: var(--unassigned-color);
}

.status-badge.completed {
  background-color: var(--success-color);
}

/* Call details panel */
.call-details-panel {
  position: fixed;
  top: 0;
  right: 0;
  width: 400px;
  height: 100vh;
  background-color: var(--content-bg);
  border-left: 1px solid var(--border-color);
  z-index: 1000;
  transition: transform 0.3s ease;
  box-shadow: -5px 0 15px rgba(0, 0, 0, 0.1);
  border-radius: 30px 0 0 30px;
  transform: translateX(100%);
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}

.call-details-panel.active {
  transform: translateX(0);
}

.call-details-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid var(--border-color);
  background-color: var(--content-bg);
}

.call-details-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--highlight-color);
}

.close-details {
  background: none;
  border: none;
  color: var(--text-color);
  cursor: pointer;
  font-size: 20px;
}

.call-details-content {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 5px;
  background-color: var(--background-color);
  padding: 15px;
  border-radius: 15px;
}

.detail-label {
  font-size: 12px;
  color: var(--text-secondary);
}

.detail-value {
  font-size: 14px;
  font-weight: 500;
}

.mobile-menu-btn {
  position: fixed;
  top: 20px;
  left: 20px;
  z-index: 101;
  background-color: var(--content-bg);
  color: var(--text-color);
  border: none;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  display: none;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

/* Responsive styles */
@media (max-width: 1024px) {
  .main-content {
    flex-direction: column;
  }
  
  .calls-container {
    padding-right: 0;
    margin-bottom: 30px;
  }
  
  .status-container {
    width: 100%;
    padding-left: 0;
    border-left: none;
    border-top: 1px solid var(--border-color);
    padding-top: 20px;
  }
  
  .call-details-panel {
    width: 100%;
    border-radius: 30px 30px 0 0;
    height: 80vh;
    bottom: 0;
    top: auto;
    transform: translateY(100%);
  }
  
  .call-details-panel.active {
    transform: translateY(0);
  }
}

@media (max-width: 768px) {
  .sidebar {
    transform: translateX(-250px);
  }
  
  .sidebar.mobile-open {
    transform: translateX(0);
  }
  
  .main-content {
    margin-left: 0;
    padding: 15px;
  }
  
  .view-tabs {
    overflow-x: auto;
  }
  
  .mobile-menu-btn {
    display: flex;
  }
  
  .expand-btn {
    display: none !important;
  }
}

@media (min-width: 769px) {
  .mobile-menu-btn {
    display: none;
  }
}
</style>