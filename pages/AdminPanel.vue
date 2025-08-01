<template>
<div>
  <!-- Navigation Bar -->
  <nav class="navbar">
    <div class="navbar-content">
      <!-- Left side - Logo/Brand -->
      <div class="navbar-brand">
        <div class="brand-logo">
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M22 16.92V19C22 20.1046 21.1046 21 20 21C10.6112 21 3 13.3888 3 4C3 2.89543 3.89543 2 5 2H7.08C7.55607 2 7.95823 2.33718 8.02513 2.80754L8.7 7.5C8.76694 7.97036 8.53677 8.42989 8.12 8.67L6.5 9.5C7.84 12.16 11.84 16.16 14.5 17.5L15.33 15.88C15.5701 15.4632 16.0296 15.2331 16.5 15.3L21.1925 16.0249C21.6628 16.0918 22 16.4939 22 16.97V16.92Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <span class="brand-text">CallCenter</span>
        </div>
      </div>

      <!-- Center - Navigation Dropdown -->
      <div class="navbar-center">
        <div class="nav-dropdown" ref="navDropdown">
          <button class="nav-dropdown-toggle" @click="toggleNavDropdown">
            <span>{{ currentNavItem }}</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" :class="{ 'rotated': showNavDropdown }">
              <path d="M6 9L12 15L18 9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
          <div class="nav-dropdown-menu" :class="{ 'show': showNavDropdown }">
            <a href="#" class="nav-dropdown-item" @click="selectNavItem('Users')">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M17 21V19C17 17.9391 16.5786 16.9217 15.8284 16.1716C15.0783 15.4214 14.0609 15 13 15H5C3.93913 15 2.92172 15.4214 2.17157 16.1716C1.42143 16.9217 1 17.9391 1 19V21" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <circle cx="9" cy="7" r="4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M23 21V19C22.9993 18.1137 22.7044 17.2528 22.1614 16.5523C21.6184 15.8519 20.8581 15.3516 20 15.13" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M16 3.13C16.8604 3.35031 17.623 3.85071 18.1676 4.55232C18.7122 5.25392 19.0078 6.11683 19.0078 7.005C19.0078 7.89318 18.7122 8.75608 18.1676 9.45769C17.623 10.1593 16.8604 10.6597 16 10.88" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              Users
            </a>
            <a href="#" class="nav-dropdown-item" @click="selectNavItem('Reference Data')">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M14 2H6C5.46957 2 4.96086 2.21071 4.58579 2.58579C4.21071 2.96086 4 3.46957 4 4V20C4 20.5304 4.21071 21.0391 4.58579 21.4142C4.96086 21.7893 5.46957 22 6 22H18C18.5304 22 19.0391 21.7893 19.4142 21.4142C19.7893 21.0391 20 20.5304 20 20V8L14 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <polyline points="14,2 14,8 20,8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <line x1="16" y1="13" x2="8" y2="13" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <line x1="16" y1="17" x2="8" y2="17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <polyline points="10,9 9,9 8,9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              Reference Data
            </a>
            <a href="#" class="nav-dropdown-item active" @click="selectNavItem('Admin')">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 2L2 7l10 5 10-5-10-5z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M2 17l10 5 10-5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M2 12l10 5 10-5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              Admin
            </a>
            <a href="#" class="nav-dropdown-item" @click="selectNavItem('Workflow')">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <rect x="3" y="3" width="18" height="18" rx="2" ry="2" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <circle cx="9" cy="9" r="2" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M21 15L16 10L5 21" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              Workflow
            </a>
          </div>
        </div>
      </div>

      <!-- Right side - Theme toggle and Settings -->
      <div class="navbar-actions">
        <button class="theme-toggle" @click="toggleTheme">
          <svg v-if="currentTheme === 'dark'" width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <svg v-else width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
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
        </button>
        <button class="settings-btn" @click="openSettings">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M19.4 15C19.2669 15.3016 19.2272 15.6362 19.286 15.9606C19.3448 16.285 19.4995 16.5843 19.73 16.82L19.79 16.88C19.976 17.0657 20.1235 17.2863 20.2241 17.5291C20.3248 17.7719 20.3766 18.0322 20.3766 18.295C20.3766 18.5578 20.3248 18.8181 20.2241 19.0609C20.1235 19.3037 19.976 19.5243 19.71 19.71C19.6043 19.896 19.3837 20.0435 19.1409 20.1441C18.8981 20.2448 18.6378 20.2966 18.375 20.2966C18.1122 20.2966 17.8519 20.2448 17.6091 20.1441C17.3663 20.0435 17.1457 19.896 16.96 19.71L16.9 19.65C16.6643 19.4195 16.365 19.2648 16.0406 19.206C15.7162 19.1472 15.3816 19.1869 15.08 19.32C14.7842 19.4468 14.532 19.6572 14.3543 19.9255C14.1766 20.1938 14.0813 20.5082 14.08 20.83V21C14.08 21.5304 13.8693 22.0391 13.4942 22.4142C13.1191 22.7893 12.6104 23 12.08 23C11.5496 23 11.0409 22.7893 10.6658 22.4142C10.2907 22.0391 10.08 21.5304 10.08 21V20.91C10.0723 20.579 9.96512 20.2573 9.77251 19.9887C9.5799 19.7201 9.31074 19.5176 9 19.41C8.69838 19.2769 8.36381 19.2372 8.03941 19.296C7.71502 19.3548 7.41568 19.5095 7.18 19.74L7.12 19.8C6.93425 19.986 6.71368 20.1335 6.47088 20.2341C6.22808 20.3348 5.96783 20.3866 5.705 20.3866C5.44217 20.3866 5.18192 20.3348 4.93912 20.2341C4.69632 20.1335 4.47575 19.986 4.29 19.8C4.10405 19.6143 3.95653 19.3937 3.85588 19.1509C3.75523 18.9081 3.70343 18.6478 3.70343 18.385C3.70343 18.1222 3.75523 17.8619 3.85588 17.6191C3.95653 17.3763 4.10405 17.1557 4.29 16.97L4.35 16.91C4.58054 16.6743 4.73519 16.375 4.794 16.0506C4.85282 15.7262 4.81312 15.3916 4.68 15.09C4.55324 14.7942 4.34276 14.542 4.07447 14.3643C3.80618 14.1866 3.49179 14.0913 3.17 14.09H3C2.46957 14.09 1.96086 13.8793 1.58579 13.5042C1.21071 13.1291 1 12.6204 1 12.09C1 11.5596 1.21071 11.0509 1.58579 10.6758C1.96086 10.3007 2.46957 10.09 3 10.09H3.09C3.42099 10.0823 3.742 9.97512 4.01062 9.78251C4.27925 9.5899 4.48167 9.32074 4.59 9.01C4.72312 8.70838 4.76282 8.37381 4.704 8.04941C4.64519 7.72502 4.49054 7.42568 4.26 7.19L4.2 7.13C4.01405 6.94425 3.86653 6.72368 3.76588 6.48088C3.66523 6.23808 3.61343 5.97783 3.61343 5.715C3.61343 5.45217 3.66523 5.19192 3.76588 4.94912C3.86653 4.70632 4.01405 4.48575 4.2 4.3C4.38575 4.11405 4.60632 3.96653 4.84912 3.86588C5.09192 3.76523 5.35217 3.71343 5.615 3.71343C5.87783 3.71343 6.13808 3.76523 6.38088 3.86588C6.62368 3.96653 6.84425 4.11405 7.03 4.3L7.09 4.36C7.32568 4.59054 7.62502 4.74519 7.94941 4.804C8.27381 4.86282 8.60838 4.82312 8.91 4.69H9C9.29577 4.56324 9.54802 4.35276 9.72569 4.08447C9.90337 3.81618 9.99872 3.50179 10 3.18V3C10 2.46957 10.2107 1.96086 10.5858 1.58579C10.9609 1.21071 11.4696 1 12 1C12.5304 1 13.0391 1.21071 13.4142 1.58579C13.7893 1.96086 14 2.46957 14 3V3.09C14.0013 3.41179 14.0966 3.72618 14.2743 3.99447C14.452 4.26276 14.7042 4.47324 15 4.6C15.3016 4.73312 15.6362 4.77282 15.9606 4.714C16.285 4.65519 16.5843 4.50054 16.82 4.27L16.88 4.21C17.0657 4.02405 17.2863 3.87653 17.5291 3.77588C17.7719 3.67523 18.0322 3.62343 18.295 3.62343C18.5578 3.62343 18.8181 3.67523 19.0609 3.77588C19.3037 3.87653 19.5243 4.02405 19.71 4.21C19.896 4.39575 20.0435 4.61632 20.1441 4.85912C20.2448 5.10192 20.2966 5.36217 20.2966 5.625C20.2966 5.88783 20.2448 6.14808 20.1441 6.39088C20.0435 6.63368 19.896 6.85425 19.71 7.04L19.65 7.1C19.4195 7.33568 19.2648 7.63502 19.206 7.95941C19.1472 8.28381 19.1869 8.61838 19.32 8.92V9C19.4468 9.29577 19.6572 9.54802 19.9255 9.72569C20.1938 9.90337 20.5082 9.99872 20.83 10H21C21.5304 10 22.0391 10.2107 22.4142 10.5858C22.7893 10.9609 23 11.4696 23 12C23 12.5304 22.7893 13.0391 22.4142 13.4142C22.0391 13.7893 21.5304 14 21 14H20.91C20.5882 14.0013 20.2738 14.0966 20.0055 14.2743C19.7372 14.452 19.5268 14.7042 19.4 15Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
      </div>
    </div>
  </nav>

  <!-- SidePanel Component -->
  <SidePanel 
    :userRole="userRole"
    :isInQueue="isInQueue"
    :isProcessingQueue="isProcessingQueue"
    :currentCall="currentCall"
    @toggle-queue="handleQueueToggle"
    @logout="handleLogout"
    @sidebar-toggle="handleSidebarToggle"
  />

  <!-- Main Content -->
  <div class="main-content">
    <div class="calls-container">
      <div class="header">
        <h1 class="page-title">Admin</h1>
      </div>

      <!-- Status Cards - Horizontal Layout -->
      <div class="status-cards">
        <div class="status-card" v-for="status in statusItems" :key="status.label">
          <div class="status-card-header">
            <div class="status-card-label">{{ status.label }}</div>
            <div class="status-card-count">{{ status.count }}</div>
          </div>
          <div class="status-card-progress">
            <div class="status-card-progress-fill" :style="{ width: status.percentage + '%' }"></div>
          </div>
        </div>
      </div>

      <!-- Table View Only -->
      <div class="view-container">
        <div class="calls-table-container">
          <table class="calls-table">
            <thead>
              <tr>
                <th>Call ID</th>
                <th>Case ID</th>
                <th>Date</th>
                <th>Time</th>
                <th>Status</th>
                <th>Agent</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="call in allCalls"
                :key="call.id"
                :class="{ selected: call.id === selectedCallId }"
              >
                <td>
                  <span class="call-id">#{{ call.id }}</span>
                </td>
                <td>
                  <span class="case-link">#{{ call.caseId }}</span>
                </td>
                <td>{{ call.dateLabel }}</td>
                <td>{{ call.time }}</td>
                <td>
                  <span :class="['status-badge', getStatusClass(call.status)]">{{ call.status }}</span>
                </td>
                <td>{{ call.agent || 'Unassigned' }}</td>
                <td>
                  <div class="table-actions">
                    <button class="action-btn view-btn" @click.stop="viewCallDetails(call.id)" title="View Details">
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M1 12S5 4 12 4s11 8 11 8-4 8-11 8S1 12 1 12z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        <circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                      </svg>
                    </button>
                    <button class="action-btn link-btn" @click.stop="linkToCase(call.id)" title="Link to Case">
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M10 13C10.4295 13.5741 10.9774 14.0491 11.6066 14.3929C12.2357 14.7367 12.9315 14.9411 13.6467 14.9923C14.3618 15.0435 15.0796 14.9403 15.7513 14.6897C16.4231 14.4392 17.0331 14.047 17.54 13.54L20.54 10.54C21.4508 9.59695 21.9548 8.33394 21.9434 7.02296C21.932 5.71198 21.4061 4.45791 20.4791 3.53087C19.5521 2.60383 18.298 2.07799 16.987 2.0666C15.676 2.0552 14.413 2.55918 13.47 3.47L11.75 5.18" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        <path d="M14 11C13.5705 10.4259 13.0226 9.95085 12.3934 9.60706C11.7643 9.26327 11.0685 9.05885 10.3533 9.00769C9.63819 8.95653 8.92037 9.05973 8.24864 9.31028C7.5769 9.56084 6.9669 9.95303 6.46 10.46L3.46 13.46C2.54918 14.403 2.04520 15.6661 2.0566 16.9771C2.06799 18.288 2.59383 19.5421 3.52087 20.4691C4.44791 21.3962 5.70198 21.922 7.01296 21.9334C8.32394 21.9448 9.58695 21.4408 10.53 20.53L12.24 18.82" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                      </svg>
                    </button>
                    <button class="action-btn case-btn" @click.stop="viewCase(call.caseId)" title="View Case">
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M14 2H6C5.46957 2 4.96086 2.21071 4.58579 2.58579C4.21071 2.96086 4 3.46957 4 4V20C4 20.5304 4.21071 21.0391 4.58579 21.4142C4.96086 21.7893 5.46957 22 6 22H18C18.5304 22 19.0391 21.7893 19.4142 21.4142C19.7893 21.0391 20 20.5304 20 20V8L14 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        <polyline points="14,2 14,8 20,8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                      </svg>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
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
  left: 50%; /* Center horizontally */
  transform: translateX(-50%) translateY(-10px); /* Initial transform for animation */
  min-width: 180px; /* Ensure enough width */
  
  background-color: var(--content-bg);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
  opacity: 0;
  visibility: hidden;
  transition: all 0.3s ease;
  z-index: 1001;
  
  display: none; /* Initially hidden using display */
  flex-direction: column; /* Stack items vertically */
  padding: 8px; /* Internal padding for the dropdown box */
}

.nav-dropdown-menu.show {
  opacity: 1;
  visibility: visible;
  transform: translateX(-50%) translateY(0); /* Final transform for animation */
  display: flex; /* Show as flex column when active */
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
