<template>
  <div>
    <!-- Navigation Bar -->


    <!-- SidePanel Component -->
    <SidePanel :userRole="userRole" :isInQueue="isInQueue" :isProcessingQueue="isProcessingQueue"
      :currentCall="currentCall" @toggle-queue="handleQueueToggle" @logout="handleLogout"
      @sidebar-toggle="handleSidebarToggle" />


    <Navbar brandText="CallCenter" :currentTheme="currentTheme"
      @toggle-theme="currentTheme = currentTheme === 'light' ? 'dark' : 'light'"
      @open-settings="console.log('Settings opened')">
    </Navbar>
    <!-- Main Content -->
    <div class="main-content">
      <div class="calls-container">
        <div class="header">
          <h1 class="page-title">Admin</h1>

          <DropdownMenu v-model="selectedNav" :items="dropdownItems" />
        </div>

        <ReferenceData v-if="selectedNav === 'referral_services'" />
        <ImportCSV v-if="selectedNav === 'import_data'" />

        
    </div>
  </div>

    <!-- Settings Modal -->
    <div v-if="showSettings" class="modal-overlay" @click="closeSettings">
      <div class="modal-content settings-modal" @click.stop>
        <div class="modal-header">
          <h3>Settings</h3>
          <button class="modal-close" @click="closeSettings">×</button>
        </div>
        <div class="modal-body">
          <div class="settings-section">
            <h4>Appearance</h4>
            <div class="setting-item">
              <label>Theme</label>
              <select v-model="currentTheme" @change="applyTheme(currentTheme)" class="form-control">
                <option value="light">Light</option>
                <option value="dark">Dark</option>
              </select>
            </div>
          </div>
          <div class="settings-section">
            <h4>Notifications</h4>
            <div class="setting-item">
              <label>
                <input type="checkbox" v-model="notificationsEnabled">
                Enable notifications
              </label>
            </div>
          </div>
          <div class="settings-section">
            <h4>Call Settings</h4>
            <div class="setting-item">
              <label>Auto-refresh interval (seconds)</label>
              <input type="number" v-model="refreshInterval" min="5" max="300" class="form-control">
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn-secondary" @click="closeSettings">Cancel</button>
          <button class="btn-primary" @click="saveSettings">Save Settings</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
  import { ref, computed, onMounted, onUnmounted } from 'vue'
  import { useRouter } from 'vue-router'
  import SidePanel from '@/components/SidePanel.vue'
  import Navbar from '@/components/nav/Navbar.vue'
  import DropdownMenu from '@/components/dropdown/DropdownMenu.vue'
  import ReferenceData from '../components/referancedata/ReferenceData.vue'
  import ImportCSV from '../components/referancedata/ImportCSV.vue'


  const router = useRouter()
  const isSidebarCollapsed = ref(false)

  function handleSidebarToggle(collapsed) {
    isSidebarCollapsed.value = collapsed
  }

  // Navigation state
  const showNavDropdown = ref(false)
  const currentNavItem = ref('Admin')
  const navDropdown = ref(null)

  // Settings state
  const showSettings = ref(false)
  const notificationsEnabled = ref(true)
  const refreshInterval = ref(30)

  // Reactive state
  const selectedCallId = ref('1348456')
  const currentTheme = ref('dark')
  const userRole = ref('super-admin')

  // Queue management state (simplified)
  const isInQueue = ref(false)
  const isProcessingQueue = ref(false)
  const currentCall = ref(null)

  const selected = ref(null)

  const selectedNav = ref('')

  const dropdownItems = [
    // Profile & Session
    { label: 'My Profile', value: 'profile' },
    { label: 'Change Password', value: 'change_password' },
    { label: 'Logout', value: 'logout' },

    // User & Role Management
    { label: 'Manage Users', value: 'manage_users' },
    { label: 'Roles & Permissions', value: 'manage_roles' },

    // Reference Data
    { label: 'Case Categories', value: 'case_categories' },
    { label: 'Referral Services', value: 'referral_services' },
    { label: 'Locations / Sub-counties', value: 'locations' },
    { label: 'Contact Sources', value: 'contact_sources' },
    { label: 'Communication Types', value: 'communication_types' },

    // Workflow & Case Setup
    { label: 'Case Types & Subtypes', value: 'case_types' },
    { label: 'Workflows & Statuses', value: 'workflow_config' },
    { label: 'Auto-assignment Rules', value: 'auto_assignment' },
    { label: 'Risk Assessment Templates', value: 'risk_templates' },

    // Call Center Config
    { label: 'Call Routing Rules', value: 'call_routing' },
    { label: 'Agent Availability', value: 'agent_availability' },

    // Communication Templates
    { label: 'SMS / Email Templates', value: 'message_templates' },
    { label: 'Automated Messages', value: 'automated_messages' },

    // Data Tools
    { label: 'Import Data (CSV)', value: 'import_data' },
    { label: 'Export Reports', value: 'export_reports' },

    // Logs & Monitoring
    { label: 'Audit Logs', value: 'audit_logs' },
    { label: 'User Activity Logs', value: 'user_logs' },

    // System Config
    { label: 'Tenant Branding', value: 'branding' },
    { label: 'Time & Locale Settings', value: 'tenant_settings' },

    // Privacy & Consent
    { label: 'Consent Settings', value: 'consent_settings' },
    { label: 'Data Retention Rules', value: 'data_retention' },

    // Dashboards
    { label: 'Reporting Dashboard', value: 'dashboard' },
  ];




  // Call data with auto-generated case IDs
  const callData = ref({
    '1348456': {
      id: '1348456',
      title: 'Emergency Crisis: Domestic Violence',
      time: '09:00AM',
      dateLabel: 'Today',
      status: 'In Progress',
      agent: 'Sarah Davis',
      caseId: 'CASE-2025-1001',
      priority: 'critical'
    },
    '1348457': {
      id: '1348457',
      title: 'Survivor Follow-Up: Safety Planning',
      time: '10:30AM',
      dateLabel: 'Today',
      status: 'Pending',
      agent: null,
      caseId: 'CASE-2025-1002',
      priority: 'high'
    },
    '1348458': {
      id: '1348458',
      title: 'Scheduled Support: Therapy Session',
      time: '02:00PM',
      dateLabel: 'Today',
      status: 'In Progress',
      agent: 'Mark Reynolds',
      caseId: 'CASE-2025-1003',
      priority: 'medium'
    },
    '1348459': {
      id: '1348459',
      title: 'Resource Request: Shelter Information',
      time: '04:45PM',
      dateLabel: 'Today',
      status: 'Unassigned',
      agent: null,
      caseId: 'CASE-2025-1004',
      priority: 'low'
    },
    '1348460': {
      id: '1348460',
      title: 'Wellness Check-In: Mental Health Support',
      time: '11:15AM',
      dateLabel: 'Yesterday',
      status: 'Completed',
      agent: 'Emily Chan',
      caseId: 'CASE-2025-1005',
      priority: 'medium'
    },
    '1348461': {
      id: '1348461',
      title: 'Appointment Booking: Legal Advocacy',
      time: '01:30PM',
      dateLabel: 'Yesterday',
      status: 'Completed',
      agent: 'David Lee',
      caseId: 'CASE-2025-1006',
      priority: 'high'
    },
    '1348462': {
      id: '1348462',
      title: 'Call Back: Housing Assistance Follow-up',
      time: '05:00PM',
      dateLabel: 'Yesterday',
      status: 'Completed',
      agent: 'Sophia Clark',
      caseId: 'CASE-2025-1007',
      priority: 'medium'
    }
  })

  // Status data
  const statusItems = ref([
    { label: 'Unassigned', count: 16, percentage: 53 },
    { label: 'Pending', count: 5, percentage: 17 },
    { label: 'In Progress', count: 24, percentage: 80 },
    { label: 'Completed', count: 8, percentage: 27 }
  ])

  // Computed properties
  const allCalls = computed(() => {
    return Object.values(callData.value)
  })

  // Navigation methods
  const toggleNavDropdown = () => {
    showNavDropdown.value = !showNavDropdown.value
  }

  const selectNavItem = (item) => {
    currentNavItem.value = item
    showNavDropdown.value = false
    console.log('Navigating to:', item)
  }

  // Settings methods
  const openSettings = () => {
    showSettings.value = true
  }

  const closeSettings = () => {
    showSettings.value = false
  }

  const saveSettings = () => {
    localStorage.setItem('notificationsEnabled', notificationsEnabled.value)
    localStorage.setItem('refreshInterval', refreshInterval.value)
    localStorage.setItem('theme', currentTheme.value)
    closeSettings()
    console.log('Settings saved')
  }

  // Simplified methods
  const handleQueueToggle = async () => {
    isProcessingQueue.value = true
    try {
      isInQueue.value = !isInQueue.value
      console.log(isInQueue.value ? 'Joined queue' : 'Left queue')
    } finally {
      isProcessingQueue.value = false
    }
  }

  const handleLogout = () => {
    console.log('Logging out...')
    alert('Logged out successfully!')
  }

  const viewCallDetails = (callId) => {
    selectedCallId.value = callId
    console.log('Viewing call details for:', callId)
  }

  const linkToCase = (callId) => {
    console.log('Linking call to case:', callId)
  }

  const viewCase = (caseId) => {
    console.log('Viewing case:', caseId)
    router.push('/cases')
  }

  const getStatusClass = (status) => {
    return status.toLowerCase().replace(/\s+/g, '-')
  }

  const applyTheme = (theme) => {
    const root = document.documentElement
    if (theme === 'light') {
      root.style.setProperty('--background-color', '#f5f5f5')
      root.style.setProperty('--sidebar-bg', '#ffffff')
      root.style.setProperty('--content-bg', '#ffffff')
      root.style.setProperty('--text-color', '#333')
      root.style.setProperty('--text-secondary', '#666')
      root.style.setProperty('--border-color', '#ddd')
      root.style.setProperty('--card-bg', '#ffffff')
      root.style.setProperty('--navbar-bg', '#ffffff')
      root.style.setProperty('--navbar-border', '#e0e0e0')
      root.setAttribute('data-theme', 'light')
    } else {
      root.style.setProperty('--background-color', '#0a0a0a')
      root.style.setProperty('--sidebar-bg', '#111')
      root.style.setProperty('--content-bg', '#222')
      root.style.setProperty('--text-color', '#fff')
      root.style.setProperty('--text-secondary', '#aaa')
      root.style.setProperty('--border-color', '#333')
      root.style.setProperty('--card-bg', '#222')
      root.style.setProperty('--navbar-bg', '#1a1a1a')
      root.style.setProperty('--navbar-border', '#333')
      root.setAttribute('data-theme', 'dark')
    }

    // Set common variables
    root.style.setProperty('--accent-color', '#FF8C00')
    root.style.setProperty('--accent-hover', '#b25900')
    root.style.setProperty('--danger-color', '#ff3b30')
    root.style.setProperty('--success-color', '#4CAF50')
    root.style.setProperty('--pending-color', '#FFA500')
    root.style.setProperty('--unassigned-color', '#808080')
    root.style.setProperty('--highlight-color', '#ff3b30')
    root.style.setProperty('--critical-color', '#ff3b30')
    root.style.setProperty('--high-color', '#ff9500')
    root.style.setProperty('--medium-color', '#007aff')
    root.style.setProperty('--low-color', '#34c759')
  }

  const toggleTheme = () => {
    currentTheme.value = currentTheme.value === 'dark' ? 'light' : 'dark'
    localStorage.setItem('theme', currentTheme.value)
    applyTheme(currentTheme.value)
  }

  // Click outside handler
  const handleClickOutside = (event) => {
    if (navDropdown.value && !navDropdown.value.contains(event.target)) {
      showNavDropdown.value = false
    }
  }

  // Lifecycle
  onMounted(() => {
    // Load saved theme and settings
    const savedTheme = localStorage.getItem('theme')
    if (savedTheme) {
      currentTheme.value = savedTheme
    }

    const savedNotifications = localStorage.getItem('notificationsEnabled')
    if (savedNotifications !== null) {
      notificationsEnabled.value = JSON.parse(savedNotifications)
    }

    const savedRefreshInterval = localStorage.getItem('refreshInterval')
    if (savedRefreshInterval) {
      refreshInterval.value = parseInt(savedRefreshInterval)
    }

    // Apply theme immediately
    applyTheme(currentTheme.value)

    // Add click outside listener
    document.addEventListener('click', handleClickOutside)
  })

  onUnmounted(() => {
    document.removeEventListener('click', handleClickOutside)
  })
</script>

<style scoped>

  /* Navigation Bar Styles */
  .navbar {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: 60px;
    background-color: var(--navbar-bg, #1a1a1a);
    border-bottom: 1px solid var(--navbar-border, #333);
    z-index: 1000;
    backdrop-filter: blur(10px);
  }

  .navbar-content {
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 100%;
    padding: 0 24px;
    max-width: 1400px;
    margin: 0 auto;
  }

  .navbar-brand {
    display: flex;
    align-items: center;
  }

  .brand-logo {
    display: flex;
    align-items: center;
    gap: 12px;
    color: var(--text-color);
  }

  .brand-logo svg {
    color: var(--accent-color);
  }

  .brand-text {
    font-size: 20px;
    font-weight: 700;
    color: var(--text-color);
  }

  .navbar-center {
    flex: 1;
    display: flex;
    justify-content: center;
  }

  .nav-dropdown {
    position: relative;
  }

  .nav-dropdown-toggle {
    display: flex;
    align-items: center;
    gap: 8px;
    background-color: var(--content-bg);
    color: var(--text-color);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 10px 16px;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    min-width: 140px;
  }

  .nav-dropdown-toggle:hover {
    background-color: var(--accent-color);
    color: white;
    border-color: var(--accent-color);
  }

  .nav-dropdown-toggle svg {
    transition: transform 0.3s ease;
  }

  .nav-dropdown-toggle svg.rotated {
    transform: rotate(180deg);
  }

  .nav-dropdown-menu {
    position: absolute;
    top: calc(100% + 8px);
    left: 50%;
    /* Center horizontally */
    transform: translateX(-50%) translateY(-10px);
    /* Initial transform for animation */
    min-width: 180px;
    /* Ensure enough width */

    background-color: var(--content-bg);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
    opacity: 0;
    visibility: hidden;
    transition: all 0.3s ease;
    z-index: 1001;

    display: none;
    /* Initially hidden using display */
    flex-direction: column;
    /* Stack items vertically */
    padding: 8px;
    /* Internal padding for the dropdown box */
  }

  .nav-dropdown-menu.show {
    opacity: 1;
    visibility: visible;
    transform: translateX(-50%) translateY(0);
    /* Final transform for animation */
    display: flex;
    /* Show as flex column when active */
  }

  .nav-dropdown-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 16px;
    color: var(--text-color);
    text-decoration: none;
    font-size: 14px;
    font-weight: 600;
    transition: all 0.3s ease;
    border-radius: 8px;
    margin: 4px;
  }

  .nav-dropdown-item:hover {
    background-color: var(--accent-color);
    color: white;
  }

  .nav-dropdown-item.active {
    background-color: rgba(255, 140, 0, 0.1);
    color: var(--accent-color);
  }

  .nav-dropdown-item svg {
    width: 16px;
    height: 16px;
  }

  .navbar-actions {
    display: flex;
    align-items: center;
    gap: 12px;
  }

  .theme-toggle,
  .settings-btn {
    background-color: var(--content-bg);
    color: var(--text-color);
    border: 1px solid var(--border-color);
    border-radius: 10px;
    padding: 10px;
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .theme-toggle:hover,
  .settings-btn:hover {
    background-color: var(--accent-color);
    color: white;
    border-color: var(--accent-color);
    transform: translateY(-1px);
  }

  /* Adjust main content for navbar */
  .main-content {
    margin-top: 60px;
    transition: margin-left 0.3s, width 0.3s;
    margin-left: 250px;
    width: calc(100% - 250px);
  }

  .main-content.sidebar-collapsed {
    margin-left: 20px;
    width: calc(100% - 20px);
  }

  /* Settings Modal Styles */
  .settings-modal {
    max-width: 600px;
  }

  .settings-section {
    margin-bottom: 24px;
    padding-bottom: 20px;
    border-bottom: 1px solid var(--border-color);
  }

  .settings-section:last-child {
    border-bottom: none;
    margin-bottom: 0;
  }

  .settings-section h4 {
    font-size: 16px;
    font-weight: 700;
    color: var(--text-color);
    margin-bottom: 16px;
  }

  .setting-item {
    margin-bottom: 16px;
  }

  .setting-item:last-child {
    margin-bottom: 0;
  }

  .setting-item label {
    display: block;
    font-size: 14px;
    font-weight: 600;
    color: var(--text-color);
    margin-bottom: 8px;
  }

  .setting-item input[type="checkbox"] {
    margin-right: 8px;
  }

  .modal-footer {
    display: flex;
    gap: 12px;
    justify-content: flex-end;
    padding: 20px 25px;
    border-top: 1px solid var(--border-color);
  }

  /* Rest of the existing styles remain the same */
  :root {
    --accent-color: #FF8C00;
  }

  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: 'Inter', sans-serif;
  }

  body {
    background-color: var(--background-color);
    color: var(--text-color);
    display: flex;
    min-height: 100vh;
    transition: background-color 0.3s, color 0.3s;
    overflow: hidden;
  }

  .calls-container {
    flex: 1;
    padding: 20px;
    overflow-y: auto;
    overflow-x: hidden;
    scrollbar-width: thin;
    scrollbar-color: rgba(255, 255, 255, 0.3) transparent;
    background: var(--background-color);
  }

  .calls-container::-webkit-scrollbar {
    width: 8px;
  }

  .calls-container::-webkit-scrollbar-track {
    background: transparent;
  }

  .calls-container::-webkit-scrollbar-thumb {
    background-color: rgba(255, 255, 255, 0.3);
    border-radius: 4px;
  }

  .calls-container::-webkit-scrollbar-thumb:hover {
    background-color: rgba(255, 255, 255, 0.5);
  }

  .header {
    margin-bottom: 25px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-shrink: 0;
  }

  .page-title {
    font-size: 28px;
    font-weight: 700;
  }

  /* Status Cards - Horizontal Layout */
  .status-cards {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
    margin-bottom: 25px;
    padding: 0;
  }

  .status-card {
    background-color: var(--content-bg);
    border-radius: 15px;
    padding: 20px;
    border: 1px solid var(--border-color);
    transition: all 0.3s ease;
  }

  .status-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  }

  .status-card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
  }

  .status-card-label {
    font-size: 14px;
    font-weight: 700;
    color: var(--text-color);
  }

  .status-card-count {
    font-size: 24px;
    font-weight: 800;
    color: var(--accent-color);
  }

  .status-card-progress {
    height: 6px;
    background-color: var(--border-color);
    border-radius: 3px;
    overflow: hidden;
  }

  .status-card-progress-fill {
    height: 100%;
    background-color: var(--accent-color);
    border-radius: 3px;
    transition: width 0.3s ease;
  }

  .view-container {
    flex: 1;
    overflow-y: auto;
    overflow-x: hidden;
    scrollbar-width: thin;
    scrollbar-color: rgba(255, 255, 255, 0.3) transparent;
  }

  .view-container::-webkit-scrollbar {
    width: 8px;
  }

  .view-container::-webkit-scrollbar-track {
    background: transparent;
  }

  .view-container::-webkit-scrollbar-thumb {
    background-color: rgba(255, 255, 255, 0.3);
    border-radius: 4px;
  }

  .view-container::-webkit-scrollbar-thumb:hover {
    background-color: rgba(255, 255, 255, 0.5);
  }

  /* Table view styles */
  .calls-table-container {
    overflow-x: auto;
    border-radius: 30px;
    background-color: var(--content-bg);
    margin-bottom: 20px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }

  .calls-table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
  }

  .calls-table th {
    text-align: left;
    padding: 18px 20px;
    background-color: var(--header-bg, var(--content-bg));
    font-weight: 700;
    font-size: 14px;
    position: sticky;
    top: 0;
    z-index: 10;
    color: var(--text-color);
  }

  .calls-table th:first-child {
    border-top-left-radius: 30px;
  }

  .calls-table th:last-child {
    border-top-right-radius: 30px;
  }

  .calls-table td {
    padding: 18px 20px;
    border-bottom: 1px solid var(--border-color);
    font-size: 14px;
    font-weight: 600;
    transition: all 0.3s ease;
  }

  .calls-table tr:hover td {
    background-color: rgba(255, 59, 48, 0.05);
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
    font-weight: 700;
  }

  .call-id {
    font-size: 14px;
    font-weight: 700;
    color: var(--text-color);
  }

  .case-link {
    font-size: 12px;
    font-weight: 600;
    color: var(--accent-color);
    text-decoration: none;
    padding: 2px 8px;
    background-color: rgba(150, 75, 0, 0.1);
    border-radius: 8px;
  }

  .case-link:hover {
    text-decoration: underline;
  }

  .status-badge {
    color: #fff;
    padding: 6px 16px;
    border-radius: 30px;
    font-size: 12px;
    display: inline-block;
    font-weight: 700;
    text-align: center;
    min-width: 100px;
    transition: all 0.3s ease;
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

  .table-actions {
    display: flex;
    gap: 8px;
  }

  .action-btn {
    background-color: var(--accent-color);
    color: white;
    border: none;
    border-radius: 6px;
    padding: 6px 8px;
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .action-btn:hover {
    background-color: var(--accent-hover);
    transform: scale(1.1);
  }

  .action-btn.view-btn {
    background-color: var(--medium-color);
  }

  .action-btn.link-btn {
    background-color: var(--high-color);
  }

  .action-btn.case-btn {
    background-color: var(--success-color);
  }

  /* Modal Styles */
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 2000;
  }

  .modal-content {
    background-color: var(--content-bg);
    border-radius: 20px;
    width: 90%;
    max-width: 500px;
    max-height: 80vh;
    overflow-y: auto;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  }

  .modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px 25px;
    border-bottom: 1px solid var(--border-color);
  }

  .modal-header h3 {
    font-size: 18px;
    font-weight: 700;
    color: var(--text-color);
  }

  .modal-close {
    background: none;
    border: none;
    color: var(--text-color);
    cursor: pointer;
    font-size: 24px;
    font-weight: 700;
    width: 32px;
    height: 32px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s ease;
  }

  .modal-close:hover {
    background-color: rgba(255, 255, 255, 0.1);
  }

  .modal-body {
    padding: 25px;
  }

  .form-group {
    margin-bottom: 20px;
  }

  .form-group label {
    display: block;
    font-size: 14px;
    font-weight: 600;
    color: var(--text-color);
    margin-bottom: 8px;
  }

  .form-control {
    width: 100%;
    background-color: var(--input-bg, var(--content-bg));
    color: var(--text-color);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 12px 16px;
    font-size: 14px;
    font-weight: 600;
    transition: all 0.3s ease;
  }

  .form-control:focus {
    outline: none;
    border-color: var(--accent-color);
  }

  .btn-primary {
    background-color: var(--accent-color);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 12px 24px;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .btn-primary:hover {
    background-color: var(--accent-hover);
    transform: translateY(-1px);
  }

  .btn-secondary {
    background-color: var(--border-color);
    color: var(--text-color);
    border: none;
    border-radius: 12px;
    padding: 12px 24px;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
  }

  .btn-secondary:hover {
    background-color: var(--text-secondary);
    transform: translateY(-1px);
  }

  /* Responsive Styles */
  @media (max-width: 768px) {
    .navbar-content {
      padding: 0 16px;
    }

    .brand-text {
      display: none;
    }

    .navbar-actions {
      gap: 8px;
    }

    .main-content {
      margin-left: 0;
      width: 100vw;
    }

    .calls-container {
      padding: 10px 2vw;
    }
  }

  @media (max-width: 1024px) {
    .main-content {
      margin-left: 0;
      width: 100vw;
    }

    .calls-container {
      padding: 10px 2vw;
    }
  }
</style>
