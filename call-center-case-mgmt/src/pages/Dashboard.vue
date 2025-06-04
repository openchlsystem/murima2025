<template>
  <div class="dashboard-layout">
    <!-- Mobile Menu Button -->
    <button class="mobile-menu-btn" @click="toggleMobileMenu" :class="{ 'active': mobileOpen }">
      <svg v-if="!mobileOpen" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <line x1="3" y1="6" x2="21" y2="6"></line>
        <line x1="3" y1="12" x2="21" y2="12"></line>
        <line x1="3" y1="18" x2="21" y2="18"></line>
      </svg>
      <svg v-if="mobileOpen" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <line x1="18" y1="6" x2="6" y2="18"></line>
        <line x1="6" y1="6" x2="18" y2="18"></line>
      </svg>
    </button>
  
    <!-- Sidebar -->
    <div class="sidebar" :class="{ 'collapsed': isSidebarCollapsed, 'mobile-open': mobileOpen }">
      <div class="sidebar-content">
        <!-- Logo Section -->
        <div class="logo-container">
          <div class="logo">
            <img src="/Openchs logo-1.png" alt="OpenCHS Logo">
          </div>
          <div class="brand-text" v-show="!isSidebarCollapsed">
            <h2>OpenCHS</h2>
            <span>Child Protection</span>
          </div>
        </div>
        
        <!-- Navigation -->
        <nav class="nav-menu">
          <router-link to="/dashboard" class="nav-item active">
            <svg class="nav-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
              <polyline points="9,22 9,12 15,12 15,22"></polyline>
            </svg>
            <span class="nav-text">Dashboard</span>
          </router-link>
          
          <router-link to="/calls" class="nav-item">
            <svg class="nav-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path>
            </svg>
            <span class="nav-text">Calls</span>
          </router-link>
          
          <router-link to="/cases" class="nav-item">
            <svg class="nav-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path>
            </svg>
            <span class="nav-text">Cases</span>
          </router-link>
          
          <router-link to="/chats" class="nav-item">
            <svg class="nav-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
            </svg>
            <span class="nav-text">Chats</span>
          </router-link>
          
          <router-link to="/qa-statistics" class="nav-item">
            <svg class="nav-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M3 3v18h18"></path>
              <path d="m19 9-5 5-4-4-3 3"></path>
            </svg>
            <span class="nav-text">QA Statistics</span>
          </router-link>
          
          <router-link to="/wallboard" class="nav-item">
            <svg class="nav-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <rect width="20" height="14" x="2" y="3" rx="2"></rect>
              <line x1="8" y1="21" x2="16" y2="21"></line>
              <line x1="12" y1="17" x2="12" y2="21"></line>
            </svg>
            <span class="nav-text">Wallboard</span>
          </router-link>
          
          <router-link to="/settings" class="nav-item">
            <svg class="nav-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="3"></circle>
              <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1 1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
            </svg>
            <span class="nav-text">Settings</span>
          </router-link>
  
          <!-- Admin Access -->
          <button @click="navigateToSuperAdmin" class="nav-item admin-item" v-if="userRole === 'super-admin'">
            <svg class="nav-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
            </svg>
            <span class="nav-text">Super Admin</span>
          </button>
        </nav>
        
        <!-- User Profile -->
        <div class="user-section">
          <div class="user-profile">
            <div class="user-avatar">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                <circle cx="12" cy="7" r="4"></circle>
              </svg>
            </div>
            <div class="user-info" v-show="!isSidebarCollapsed">
              <span class="user-name">{{ userName }}</span>
              <span class="user-role">{{ userRole }}</span>
            </div>
          </div>
          
          <div class="status-indicator" v-show="!isSidebarCollapsed">
            <div class="status-dot online"></div>
            <span>Online</span>
          </div>
          
          <div class="action-buttons">
            <button class="join-queue-btn" v-show="!isSidebarCollapsed">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polygon points="5,3 19,12 5,21 5,3"></polygon>
              </svg>
              Join Queue
            </button>
            <button class="logout-btn" @click="logout">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
                <polyline points="16,17 21,12 16,7"></polyline>
                <line x1="21" y1="12" x2="9" y2="12"></line>
              </svg>
              <span v-show="!isSidebarCollapsed">Logout</span>
            </button>
          </div>
        </div>
      </div>
      
      <!-- Sidebar Toggle -->
      <button class="sidebar-toggle" @click="toggleSidebar">
        <svg v-if="!isSidebarCollapsed" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="15,18 9,12 15,6"></polyline>
        </svg>
        <svg v-if="isSidebarCollapsed" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="9,18 15,12 9,6"></polyline>
        </svg>
      </button>
    </div>
  
    <!-- Main Content -->
    <div class="main-content" :class="{ 'sidebar-collapsed': isSidebarCollapsed }">
      <!-- Header -->
      <header class="header">
        <div class="header-left">
          <h1>Dashboard</h1>
          <p class="header-subtitle">Welcome back, {{ userName }}</p>
        </div>
        <div class="header-right">
          <button class="theme-toggle" @click="toggleTheme">
            <svg v-if="currentTheme === 'dark'" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="5"></circle>
              <line x1="12" y1="1" x2="12" y2="3"></line>
              <line x1="12" y1="21" x2="12" y2="23"></line>
              <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
              <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
              <line x1="1" y1="12" x2="3" y2="12"></line>
              <line x1="21" y1="12" x2="23" y2="12"></line>
              <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
              <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
            </svg>
            <svg v-if="currentTheme === 'light'" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
            </svg>
          </button>
          <div class="notification-btn">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"></path>
              <path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
            </svg>
            <span class="notification-badge">3</span>
          </div>
        </div>
      </header>
  
      <!-- Dashboard Content -->
      <div class="dashboard-content">
        <!-- Metrics Grid -->
        <div class="metrics-grid">
          <div v-for="(metric, index) in metrics" :key="index" class="metric-card">
            <div class="metric-header">
              <div class="metric-icon" :class="metric.iconClass">
                <component :is="metric.icon" />
              </div>
              <div class="metric-trend" :class="metric.trendClass">
                <svg v-if="metric.trend > 0" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <polyline points="23,6 13.5,15.5 8.5,10.5 1,18"></polyline>
                  <polyline points="17,6 23,6 23,12"></polyline>
                </svg>
                <svg v-if="metric.trend < 0" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <polyline points="23,18 13.5,8.5 8.5,13.5 1,6"></polyline>
                  <polyline points="17,18 23,18 23,12"></polyline>
                </svg>
                <span>{{ Math.abs(metric.trend) }}%</span>
              </div>
            </div>
            <div class="metric-content">
              <h3 class="metric-value">{{ metric.value }}</h3>
              <p class="metric-label">{{ metric.label }}</p>
              <span class="metric-subtitle">{{ metric.subtitle }}</span>
            </div>
          </div>
        </div>
  
        <!-- Quick Actions -->
        <div class="quick-actions">
          <h2 class="section-title">Quick Actions</h2>
          <div class="actions-grid">
            <button class="action-card" @click="startEmergencyCall">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path>
              </svg>
              <span>Emergency Call</span>
            </button>
            <button class="action-card" @click="createNewCase">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M5 12h14"></path>
                <path d="M12 5v14"></path>
              </svg>
              <span>New Case</span>
            </button>
            <button class="action-card" @click="viewReports">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                <polyline points="14,2 14,8 20,8"></polyline>
                <line x1="16" y1="13" x2="8" y2="13"></line>
                <line x1="16" y1="17" x2="8" y2="17"></line>
                <polyline points="10,9 9,9 8,9"></polyline>
              </svg>
              <span>View Reports</span>
            </button>
            <button class="action-card" @click="accessResources">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path>
                <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path>
              </svg>
              <span>Resources</span>
            </button>
          </div>
        </div>
  
        <!-- Recent Activity -->
        <div class="activity-section">
          <div class="activity-header">
            <h2 class="section-title">Recent Activity</h2>
            <router-link to="/calls" class="view-all">View All</router-link>
          </div>
          
          <div class="activity-grid">
            <!-- Recent Calls -->
            <div class="activity-card">
              <h3 class="card-title">Recent Calls</h3>
              <div class="call-list">
                <div v-for="call in recentCalls" :key="call.id" class="call-item">
                  <div class="call-icon">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path>
                    </svg>
                  </div>
                  <div class="call-details">
                    <h4>{{ call.type }}</h4>
                    <p>{{ call.time }}</p>
                  </div>
                  <div class="call-status" :class="call.statusClass">
                    {{ call.status }}
                  </div>
                </div>
              </div>
            </div>
  
            <!-- Queue Status -->
            <div class="activity-card">
              <h3 class="card-title">Queue Status</h3>
              <div class="queue-stats">
                <div class="queue-item">
                  <div class="queue-number">{{ queueStats.waiting }}</div>
                  <div class="queue-label">Waiting</div>
                </div>
                <div class="queue-item">
                  <div class="queue-number">{{ queueStats.active }}</div>
                  <div class="queue-label">Active</div>
                </div>
                <div class="queue-item">
                  <div class="queue-number">{{ queueStats.agents }}</div>
                  <div class="queue-label">Agents Online</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  
    <!-- Super Admin Modal/Page -->
    <div v-if="showSuperAdmin" class="super-admin-overlay" @click="closeSuperAdmin">
      <div class="super-admin-container" @click.stop>
        <SuperAdminDashboard @close="closeSuperAdmin" />
      </div>
    </div>
  </div>
  </template>
  
  <script>
  import { ref, onMounted } from 'vue'
  
  // Define icon components as simple SVG elements
  const PhoneIcon = {
    template: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path>
    </svg>`
  }
  
  const FolderIcon = {
    template: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path>
    </svg>`
  }
  
  const BarChart3Icon = {
    template: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <path d="M3 3v18h18"></path>
      <path d="m19 9-5 5-4-4-3 3"></path>
    </svg>`
  }
  
  const TrendingUpIcon = {
    template: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <polyline points="23,6 13.5,15.5 8.5,10.5 1,18"></polyline>
      <polyline points="17,6 23,6 23,12"></polyline>
    </svg>`
  }
  
  // Super Admin Dashboard Component
  const SuperAdminDashboard = {
    template: `
      <div class="super-admin-dashboard">
        <div class="super-admin-header">
          <h1>Super Admin Dashboard</h1>
          <button @click="$emit('close')" class="close-btn">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
        <div class="super-admin-content">
          <p>Welcome to the Super Admin Dashboard. Here you can manage system-wide settings, user permissions, and organizational configurations.</p>
          <div class="admin-actions">
            <button class="admin-action-btn">Manage Users</button>
            <button class="admin-action-btn">System Settings</button>
            <button class="admin-action-btn">Organization Management</button>
            <button class="admin-action-btn">Reports & Analytics</button>
          </div>
        </div>
      </div>
    `,
    emits: ['close']
  }
  
  export default {
  name: 'Dashboard',
  components: {
    PhoneIcon,
    FolderIcon,
    BarChart3Icon,
    TrendingUpIcon,
    SuperAdminDashboard
  },
  setup() {
    const isSidebarCollapsed = ref(false)
    const mobileOpen = ref(false)
    const currentTheme = ref(localStorage.getItem('theme') || 'dark')
    const showSuperAdmin = ref(false)
    
    // User data
    const userName = ref('Sarah Johnson')
    const userRole = ref('super-admin') // Change this based on actual user role
    
    // Metrics data
    const metrics = ref([
      {
        label: 'Total Calls Today',
        value: '127',
        trend: 12,
        trendClass: 'positive',
        subtitle: 'vs yesterday',
        icon: 'PhoneIcon',
        iconClass: 'phone'
      },
      {
        label: 'Active Cases',
        value: '34',
        trend: 8,
        trendClass: 'positive',
        subtitle: 'this week',
        icon: 'FolderIcon',
        iconClass: 'folder'
      },
      {
        label: 'Response Time',
        value: '2.3m',
        trend: -15,
        trendClass: 'negative',
        subtitle: 'average',
        icon: 'BarChart3Icon',
        iconClass: 'chart'
      },
      {
        label: 'Resolution Rate',
        value: '94%',
        trend: 5,
        trendClass: 'positive',
        subtitle: 'this month',
        icon: 'TrendingUpIcon',
        iconClass: 'trending'
      }
    ])
    
    // Recent calls data
    const recentCalls = ref([
      {
        id: 1,
        type: 'Emergency Crisis Support',
        time: '2 minutes ago',
        status: 'In Progress',
        statusClass: 'in-progress'
      },
      {
        id: 2,
        type: 'Follow-up Call',
        time: '15 minutes ago',
        status: 'Completed',
        statusClass: 'completed'
      },
      {
        id: 3,
        type: 'Resource Request',
        time: '1 hour ago',
        status: 'Pending',
        statusClass: 'pending'
      }
    ])
    
    // Queue statistics
    const queueStats = ref({
      waiting: 5,
      active: 12,
      agents: 8
    })
    
    const toggleSidebar = () => {
      isSidebarCollapsed.value = !isSidebarCollapsed.value
    }
    
    const toggleMobileMenu = () => {
      mobileOpen.value = !mobileOpen.value
    }
    
    const toggleTheme = () => {
      const newTheme = currentTheme.value === 'dark' ? 'light' : 'dark'
      currentTheme.value = newTheme
      localStorage.setItem('theme', newTheme)
      document.documentElement.setAttribute('data-theme', newTheme)
    }
    
    const navigateToSuperAdmin = () => {
      showSuperAdmin.value = true
    }
    
    const closeSuperAdmin = () => {
      showSuperAdmin.value = false
    }
    
    const logout = () => {
      // Handle logout logic
      console.log('Logging out...')
    }
    
    const startEmergencyCall = () => {
      console.log('Starting emergency call...')
    }
    
    const createNewCase = () => {
      console.log('Creating new case...')
    }
    
    const viewReports = () => {
      console.log('Viewing reports...')
    }
    
    const accessResources = () => {
      console.log('Accessing resources...')
    }
    
    onMounted(() => {
      document.documentElement.setAttribute('data-theme', currentTheme.value)
    })
    
    return {
      isSidebarCollapsed,
      mobileOpen,
      currentTheme,
      showSuperAdmin,
      userName,
      userRole,
      metrics,
      recentCalls,
      queueStats,
      toggleSidebar,
      toggleMobileMenu,
      toggleTheme,
      navigateToSuperAdmin,
      closeSuperAdmin,
      logout,
      startEmergencyCall,
      createNewCase,
      viewReports,
      accessResources
    }
  }
  }
  </script>
  
  <style scoped>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
  
  :root {
  --primary-color: #1e7e34;
  --primary-hover: #166534;
  --secondary-color: #6c757d;
  --accent-color: #ffc107;
  --danger-color: #dc3545;
  --success-color: #28a745;
  --warning-color: #fd7e14;
  --info-color: #17a2b8;
  
  --bg-primary: #ffffff;
  --bg-secondary: #f8f9fa;
  --bg-tertiary: #e9ecef;
  --text-primary: #212529;
  --text-secondary: #6c757d;
  --text-muted: #adb5bd;
  --border-color: #dee2e6;
  --shadow-sm: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
  --shadow-md: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
  --shadow-lg: 0 1rem 3rem rgba(0, 0, 0, 0.175);
  }
  
  [data-theme="dark"] {
  --bg-primary: #1a1a1a;
  --bg-secondary: #2d2d2d;
  --bg-tertiary: #404040;
  --text-primary: #ffffff;
  --text-secondary: #b3b3b3;
  --text-muted: #808080;
  --border-color: #404040;
  --shadow-sm: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.3);
  --shadow-md: 0 0.5rem 1rem rgba(0, 0, 0, 0.4);
  --shadow-lg: 0 1rem 3rem rgba(0, 0, 0, 0.5);
  }
  
  * {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  }
  
  body {
  font-family: 'Inter', sans-serif;
  background-color: var(--bg-primary);
  color: var(--text-primary);
  transition: all 0.3s ease;
  }
  
  .dashboard-layout {
  display: flex;
  min-height: 100vh;
  background-color: var(--bg-primary);
  transition: all 0.3s ease;
  position: relative;
  }
  
  /* Mobile Menu Button */
  .mobile-menu-btn {
  display: none;
  position: fixed;
  top: 1rem;
  left: 1rem;
  z-index: 1001;
  background: var(--primary-color);
  color: white;
  border: none;
  border-radius: 12px;
  width: 48px;
  height: 48px;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: var(--shadow-md);
  transition: all 0.3s ease;
  }
  
  .mobile-menu-btn:hover {
  background: var(--primary-hover);
  transform: translateY(-2px);
  }
  
  /* Sidebar */
  .sidebar {
  width: 280px;
  background: var(--bg-secondary);
  border-right: 1px solid var(--border-color);
  transition: all 0.3s ease;
  position: relative;
  z-index: 1000;
  display: flex;
  flex-direction: column;
  }
  
  .sidebar.collapsed {
  width: 80px;
  }
  
  .sidebar-content {
  flex: 1;
  padding: 2rem 1rem;
  display: flex;
  flex-direction: column;
  gap: 2rem;
  }
  
  .sidebar.collapsed .sidebar-content {
  padding: 2rem 0.5rem;
  }
  
  /* Logo Section */
  .logo-container {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0 1rem;
  }
  
  .sidebar.collapsed .logo-container {
  justify-content: center;
  padding: 0;
  }
  
  .logo {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: var(--primary-color);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  flex-shrink: 0;
  }
  
  .logo img {
  width: 32px;
  height: 32px;
  object-fit: contain;
  }
  
  .brand-text h2 {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--primary-color);
  margin-bottom: 0.25rem;
  }
  
  .brand-text span {
  font-size: 0.75rem;
  color: var(--text-secondary);
  font-weight: 500;
  }
  
  /* Navigation */
  .nav-menu {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  }
  
  .nav-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  border-radius: 12px;
  text-decoration: none;
  color: var(--text-secondary);
  transition: all 0.3s ease;
  position: relative;
  border: none;
  background: none;
  cursor: pointer;
  width: 100%;
  }
  
  .sidebar.collapsed .nav-item {
  justify-content: center;
  padding: 1rem 0.5rem;
  }
  
  .nav-item:hover {
  background: var(--bg-tertiary);
  color: var(--text-primary);
  transform: translateX(4px);
  }
  
  .nav-item.active {
  background: var(--primary-color);
  color: white;
  }
  
  .nav-item.admin-item {
  background: linear-gradient(135deg, #dc3545, #fd7e14);
  color: white;
  margin-top: 1rem;
  }
  
  .nav-item.admin-item:hover {
  transform: translateX(4px) scale(1.02);
  }
  
  .nav-icon {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
  }
  
  .nav-text {
  font-weight: 500;
  font-size: 0.875rem;
  }
  
  .sidebar.collapsed .nav-text {
  display: none;
  }
  
  /* User Section */
  .user-section {
  margin-top: auto;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  }
  
  .user-profile {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: var(--bg-tertiary);
  border-radius: 12px;
  }
  
  .sidebar.collapsed .user-profile {
  justify-content: center;
  padding: 1rem 0.5rem;
  }
  
  .user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: var(--primary-color);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
  }
  
  .user-info {
  display: flex;
  flex-direction: column;
  }
  
  .user-name {
  font-weight: 600;
  font-size: 0.875rem;
  color: var(--text-primary);
  }
  
  .user-role {
  font-size: 0.75rem;
  color: var(--text-secondary);
  text-transform: capitalize;
  }
  
  .status-indicator {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0 1rem;
  font-size: 0.75rem;
  color: var(--text-secondary);
  }
  
  .status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  }
  
  .status-dot.online {
  background: var(--success-color);
  }
  
  .action-buttons {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  padding: 0 1rem;
  }
  
  .sidebar.collapsed .action-buttons {
  padding: 0 0.5rem;
  }
  
  .join-queue-btn,
  .logout-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.75rem;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.3s ease;
  }
  
  .join-queue-btn {
  background: var(--primary-color);
  color: white;
  }
  
  .join-queue-btn:hover {
  background: var(--primary-hover);
  transform: translateY(-2px);
  }
  
  .logout-btn {
  background: var(--danger-color);
  color: white;
  }
  
  .logout-btn:hover {
  background: #c82333;
  transform: translateY(-2px);
  }
  
  .sidebar.collapsed .join-queue-btn,
  .sidebar.collapsed .logout-btn {
  padding: 0.75rem 0.5rem;
  }
  
  /* Sidebar Toggle */
  .sidebar-toggle {
  position: absolute;
  top: 50%;
  right: -12px;
  transform: translateY(-50%);
  width: 24px;
  height: 24px;
  background: var(--primary-color);
  color: white;
  border: none;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: var(--shadow-sm);
  transition: all 0.3s ease;
  }
  
  .sidebar-toggle:hover {
  background: var(--primary-hover);
  transform: translateY(-50%) scale(1.1);
  }
  
  /* Main Content */
  .main-content {
  flex: 1;
  background: var(--bg-primary);
  transition: all 0.3s ease;
  overflow-x: hidden;
  }
  
  .main-content.sidebar-collapsed {
  margin-left: 0;
  }
  
  /* Header */
  .header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 2rem;
  background: var(--bg-secondary);
  border-bottom: 1px solid var(--border-color);
  }
  
  .header-left h1 {
  font-size: 2rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 0.25rem;
  }
  
  .header-subtitle {
  color: var(--text-secondary);
  font-size: 0.875rem;
  }
  
  .header-right {
  display: flex;
  align-items: center;
  gap: 1rem;
  }
  
  .theme-toggle,
  .notification-btn {
  width: 44px;
  height: 44px;
  border: 1px solid var(--border-color);
  background: var(--bg-primary);
  color: var(--text-primary);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  }
  
  .theme-toggle:hover,
  .notification-btn:hover {
  background: var(--bg-tertiary);
  transform: translateY(-2px);
  }
  
  .notification-badge {
  position: absolute;
  top: -4px;
  right: -4px;
  background: var(--danger-color);
  color: white;
  font-size: 0.625rem;
  font-weight: 600;
  padding: 0.125rem 0.375rem;
  border-radius: 10px;
  min-width: 18px;
  text-align: center;
  }
  
  /* Dashboard Content */
  .dashboard-content {
  padding: 2rem;
  display: flex;
  flex-direction: column;
  gap: 2rem;
  }
  
  /* Metrics Grid */
  .metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
  }
  
  .metric-card {
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: 16px;
  padding: 1.5rem;
  transition: all 0.3s ease;
  }
  
  .metric-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
  }
  
  .metric-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  }
  
  .metric-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  }
  
  .metric-icon.phone { background: var(--primary-color); }
  .metric-icon.folder { background: var(--info-color); }
  .metric-icon.chart { background: var(--warning-color); }
  .metric-icon.trending { background: var(--success-color); }
  
  .metric-trend {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.75rem;
  font-weight: 600;
  padding: 0.25rem 0.5rem;
  border-radius: 6px;
  }
  
  .metric-trend.positive {
  background: rgba(40, 167, 69, 0.1);
  color: var(--success-color);
  }
  
  .metric-trend.negative {
  background: rgba(220, 53, 69, 0.1);
  color: var(--danger-color);
  }
  
  .metric-value {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 0.5rem;
  }
  
  .metric-label {
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 0.25rem;
  }
  
  .metric-subtitle {
  font-size: 0.75rem;
  color: var(--text-secondary);
  }
  
  /* Quick Actions */
  .quick-actions {
  margin-bottom: 2rem;
  }
  
  .section-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 1rem;
  }
  
  .actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  }
  
  .action-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
  padding: 1.5rem;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  color: var(--text-primary);
  font-weight: 500;
  }
  
  .action-card:hover {
  background: var(--primary-color);
  color: white;
  transform: translateY(-4px);
  box-shadow: var(--shadow-md);
  }
  
  /* Activity Section */
  .activity-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  }
  
  .view-all {
  color: var(--primary-color);
  text-decoration: none;
  font-weight: 500;
  font-size: 0.875rem;
  }
  
  .view-all:hover {
  text-decoration: underline;
  }
  
  .activity-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 1.5rem;
  }
  
  .activity-card {
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: 16px;
  padding: 1.5rem;
  }
  
  .card-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 1rem;
  }
  
  /* Call List */
  .call-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  }
  
  .call-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: var(--bg-primary);
  border-radius: 12px;
  transition: all 0.3s ease;
  }
  
  .call-item:hover {
  background: var(--bg-tertiary);
  }
  
  .call-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: var(--primary-color);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  }
  
  .call-details {
  flex: 1;
  }
  
  .call-details h4 {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 0.25rem;
  }
  
  .call-details p {
  font-size: 0.75rem;
  color: var(--text-secondary);
  }
  
  .call-status {
  padding: 0.25rem 0.75rem;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 600;
  }
  
  .call-status.in-progress {
  background: rgba(255, 193, 7, 0.1);
  color: var(--warning-color);
  }
  
  .call-status.completed {
  background: rgba(40, 167, 69, 0.1);
  color: var(--success-color);
  }
  
  .call-status.pending {
  background: rgba(23, 162, 184, 0.1);
  color: var(--info-color);
  }
  
  /* Queue Stats */
  .queue-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  }
  
  .queue-item {
  text-align: center;
  padding: 1rem;
  background: var(--bg-primary);
  border-radius: 12px;
  }
  
  .queue-number {
  font-size: 2rem;
  font-weight: 700;
  color: var(--primary-color);
  margin-bottom: 0.25rem;
  }
  
  .queue-label {
  font-size: 0.75rem;
  color: var(--text-secondary);
  font-weight: 500;
  }
  
  /* Super Admin Overlay */
  .super-admin-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  }
  
  .super-admin-container {
  background: var(--bg-primary);
  border-radius: 16px;
  max-width: 90vw;
  max-height: 90vh;
  overflow: auto;
  box-shadow: var(--shadow-lg);
  }
  
  .super-admin-dashboard {
  padding: 2rem;
  min-width: 600px;
  }
  
  .super-admin-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  border-bottom: 1px solid var(--border-color);
  padding-bottom: 1rem;
  }
  
  .super-admin-header h1 {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text-primary);
  }
  
  .close-btn {
  background: none;
  border: none;
  color: var(--text-secondary);
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 8px;
  transition: all 0.3s ease;
  }
  
  .close-btn:hover {
  background: var(--bg-tertiary);
  color: var(--text-primary);
  }
  
  .super-admin-content p {
  color: var(--text-secondary);
  margin-bottom: 2rem;
  line-height: 1.6;
  }
  
  .admin-actions {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  }
  
  .admin-action-btn {
  padding: 1rem;
  background: var(--primary-color);
  color: white;
  border: none;
  border-radius: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  }
  
  .admin-action-btn:hover {
  background: var(--primary-hover);
  transform: translateY(-2px);
  }
  
  /* Responsive Design */
  @media (max-width: 768px) {
  .mobile-menu-btn {
    display: flex;
  }
  
  .sidebar {
    position: fixed;
    top: 0;
    left: 0;
    height: 100vh;
    z-index: 1000;
    transform: translateX(-100%);
  }
  
  .sidebar.mobile-open {
    transform: translateX(0);
  }
  
  .main-content {
    margin-left: 0 !important;
  }
  
  .header {
    padding: 1rem;
  }
  
  .dashboard-content {
    padding: 1rem;
  }
  
  .metrics-grid {
    grid-template-columns: 1fr;
  }
  
  .actions-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .activity-grid {
    grid-template-columns: 1fr;
  }
  
  .super-admin-container {
    margin: 1rem;
    max-width: calc(100vw - 2rem);
  }
  
  .super-admin-dashboard {
    min-width: auto;
    padding: 1rem;
  }
  }
  
  @media (max-width: 480px) {
  .actions-grid {
    grid-template-columns: 1fr;
  }
  
  .queue-stats {
    grid-template-columns: 1fr;
  }
  
  .admin-actions {
    grid-template-columns: 1fr;
  }
  }
  </style>