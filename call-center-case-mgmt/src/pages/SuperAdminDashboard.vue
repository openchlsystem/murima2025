<template>
    <div class="app-container">
      <aside class="sidebar">
        <div class="sidebar-header">
          <img src="/Openchs logo-1.png" alt="OpenCHS Logo" class="logo">
          <span class="brand-name">OpenCHS</span>
        </div>
        <nav class="sidebar-nav">
          <ul>
            <li>
              <a href="#" class="router-link-active">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
                  <polyline points="9,22 9,12 15,12 15,22"></polyline>
                </svg>
                Dashboard
              </a>
            </li>
            <li>
              <a href="#">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"></path>
                  <circle cx="9" cy="7" r="4"></circle>
                  <path d="m22 21-2-2"></path>
                </svg>
                User Management
              </a>
            </li>
            <li>
              <a href="#">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M3 21h18"></path>
                  <path d="M5 21V7l8-4v18"></path>
                  <path d="M19 21V11l-6-4"></path>
                </svg>
                Organizations
              </a>
            </li>
            <li>
              <a href="#">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="12" cy="12" r="3"></circle>
                  <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1 1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
                </svg>
                Settings
              </a>
            </li>
          </ul>
        </nav>
        <div class="sidebar-footer">
          <a href="#" @click="$emit('close')">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
              <polyline points="16,17 21,12 16,7"></polyline>
              <line x1="21" y1="12" x2="9" y2="12"></line>
            </svg>
            Back to Dashboard
          </a>
        </div>
      </aside>
      <div class="dashboard-container">
        <!-- Header -->
        <header class="dashboard-header">
          <div class="header-content">
            <!-- Search Bar -->
            <div class="search-container">
              <div class="search-input-wrapper">
                <svg class="search-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="11" cy="11" r="8"></circle>
                  <path d="m21 21-4.35-4.35"></path>
                </svg>
                <input
                  type="text"
                  placeholder="Search organizations, users, or settings..."
                  class="search-input"
                  v-model="searchQuery"
                >
              </div>
            </div>
    
            <!-- Profile Section -->
            <div class="profile-section">
              <button class="notification-btn">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"></path>
                  <path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
                </svg>
                <span class="notification-badge">3</span>
              </button>
              <div class="profile-info">
                <div class="profile-avatar">
                  <span>SA</span>
                </div>
                <div class="profile-details">
                  <span class="profile-name">Super Admin</span>
                  <span class="profile-role">System Administrator</span>
                </div>
              </div>
            </div>
          </div>
        </header>
    
        <!-- Main Content -->
        <main class="dashboard-main">
          <!-- Metrics Grid -->
          <section class="metrics-section">
            <div class="metrics-grid">
              <div
                v-for="metric in metrics"
                :key="metric.id"
                class="card metric-card"
                :class="{ loading: isLoading }"
              >
                <div v-if="isLoading" class="metric-skeleton">
                  <div class="skeleton-icon"></div>
                  <div class="skeleton-content">
                    <div class="skeleton-number"></div>
                    <div class="skeleton-label"></div>
                    <div class="skeleton-trend"></div>
                  </div>
                </div>
                <div v-else class="metric-content">
                  <div class="metric-icon" :style="{ backgroundColor: metric.iconBg }">
                    <svg class="icon" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path :d="metric.iconPath" />
                    </svg>
                  </div>
                  <div class="metric-info">
                    <h3 class="metric-number">{{ metric.value }}</h3>
                    <p class="metric-label">{{ metric.label }}</p>
                    <div class="metric-trend" :class="metric.trendDirection">
                      <svg v-if="metric.trendDirection === 'up'" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <polyline points="23,6 13.5,15.5 8.5,10.5 1,18"></polyline>
                        <polyline points="17,6 23,6 23,12"></polyline>
                      </svg>
                      <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <polyline points="23,18 13.5,8.5 8.5,13.5 1,6"></polyline>
                        <polyline points="17,18 23,18 23,12"></polyline>
                      </svg>
                      <span>{{ metric.trend }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </section>
    
          <!-- Quick Actions -->
          <section class="quick-actions-section">
            <h2 class="section-title">Quick Actions</h2>
            <div class="quick-actions-grid">
              <div
                v-for="action in quickActions"
                :key="action.id"
                class="card action-card"
                @click="handleQuickAction(action.id)"
              >
                <div class="action-icon" :style="{ backgroundColor: action.iconBg }">
                  <svg class="icon" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path :d="action.iconPath" />
                  </svg>
                </div>
                <div class="action-content">
                  <h3 class="action-title">{{ action.title }}</h3>
                  <p class="action-description">{{ action.description }}</p>
                  <button class="action-button">
                    {{ action.buttonText }}
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <polyline points="9,18 15,12 9,6"></polyline>
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </section>
    
          <!-- Management Section -->
          <section class="management-section">
            <div class="management-grid">
              <!-- Recent Organizations -->
              <div class="card management-card">
                <div class="card-header">
                  <h3 class="card-title">Recent Organizations</h3>
                  <button class="view-all-btn">View All</button>
                </div>
                <div class="organizations-list">
                  <div
                    v-for="org in recentOrganizations"
                    :key="org.id"
                    class="organization-item"
                  >
                    <div class="org-avatar">
                      <span>{{ org.name.charAt(0) }}</span>
                    </div>
                    <div class="org-info">
                      <h4 class="org-name">{{ org.name }}</h4>
                      <p class="org-details">{{ org.users }} users • {{ org.status }}</p>
                    </div>
                    <div class="org-actions">
                      <button class="org-action-btn">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                          <polygon points="12,2 15.09,8.26 22,9.27 17,14.14 18.18,21.02 12,17.77 5.82,21.02 7,14.14 2,9.27 8.91,8.26"></polygon>
                        </svg>
                      </button>
                    </div>
                  </div>
                </div>
              </div>
    
              <!-- Usage Analytics -->
              <div class="card management-card">
                <div class="card-header">
                  <h3 class="card-title">Usage Analytics</h3>
                  <select class="time-filter">
                    <option>Last 7 days</option>
                    <option>Last 30 days</option>
                    <option>Last 90 days</option>
                  </select>
                </div>
                <div class="analytics-content">
                  <div class="analytics-chart">
                    <div class="chart-placeholder">
                      <div class="chart-bars">
                        <div class="chart-bar" style="height: 60%"></div>
                        <div class="chart-bar" style="height: 80%"></div>
                        <div class="chart-bar" style="height: 45%"></div>
                        <div class="chart-bar" style="height: 90%"></div>
                        <div class="chart-bar" style="height: 70%"></div>
                        <div class="chart-bar" style="height: 85%"></div>
                        <div class="chart-bar" style="height: 95%"></div>
                      </div>
                    </div>
                  </div>
                  <div class="analytics-stats">
                    <div class="stat-item">
                      <span class="stat-label">Total Sessions</span>
                      <span class="stat-value">12,847</span>
                    </div>
                    <div class="stat-item">
                      <span class="stat-label">Avg. Duration</span>
                      <span class="stat-value">24m 32s</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </section>
    
          <!-- User Management Table -->
          <section class="user-management-section">
            <div class="card table-card">
              <div class="card-header">
                <h3 class="card-title">User Management</h3>
                <div class="table-controls">
                  <button class="filter-btn">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <polygon points="22,3 2,3 10,12.46 10,19 14,21 14,12.46"></polygon>
                    </svg>
                    Filter
                  </button>
                  <button class="export-btn">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                      <polyline points="7,10 12,15 17,10"></polyline>
                      <line x1="12" y1="15" x2="12" y2="3"></line>
                    </svg>
                    Export
                  </button>
                </div>
              </div>
              <div class="table-container">
                <table class="user-table">
                  <thead>
                    <tr>
                      <th>User</th>
                      <th>Organization</th>
                      <th>Role</th>
                      <th>Status</th>
                      <th>Last Active</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr
                      v-for="user in users"
                      :key="user.id"
                      class="user-row"
                    >
                      <td class="user-cell">
                        <div class="user-info">
                          <div class="user-avatar">
                            <span>{{ user.name.split(' ').map(n => n[0]).join('') }}</span>
                          </div>
                          <div class="user-details">
                            <span class="user-name">{{ user.name }}</span>
                            <span class="user-email">{{ user.email }}</span>
                          </div>
                        </div>
                      </td>
                      <td class="org-cell">{{ user.organization }}</td>
                      <td class="role-cell">
                        <span class="role-badge" :class="user.role.toLowerCase()">
                          {{ user.role }}
                        </span>
                      </td>
                      <td class="status-cell">
                        <span class="status-indicator" :class="user.status.toLowerCase()"></span>
                        {{ user.status }}
                      </td>
                      <td class="activity-cell">{{ user.lastActive }}</td>
                      <td class="actions-cell">
                        <div class="action-buttons">
                          <button
                            class="action-btn activate-btn"
                            :disabled="user.status === 'Active'"
                            @click="handleUserAction('activate', user.id)"
                            title="Activate User"
                          >
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                              <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                              <polyline points="22,4 12,14.01 9,11.01"></polyline>
                            </svg>
                            Activate
                          </button>
                          <button
                            class="action-btn deactivate-btn"
                            :disabled="user.status === 'Inactive'"
                            @click="handleUserAction('deactivate', user.id)"
                            title="Deactivate User"
                          >
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                              <circle cx="12" cy="12" r="10"></circle>
                              <line x1="15" y1="9" x2="9" y2="15"></line>
                              <line x1="9" y1="9" x2="15" y2="15"></line>
                            </svg>
                            Deactivate
                          </button>
                          <button
                            class="action-btn delete-btn"
                            @click="handleUserAction('delete', user.id)"
                            title="Delete User"
                          >
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                              <polyline points="3,6 5,6 21,6"></polyline>
                              <path d="m19,6v14a2,2 0 0,1-2,2H7a2,2 0 0,1-2-2V6m3,0V4a2,2 0 0,1,2-2h4a2,2 0 0,1,2,2v2"></path>
                              <line x1="10" y1="11" x2="10" y2="17"></line>
                              <line x1="14" y1="11" x2="14" y2="17"></line>
                            </svg>
                            Delete
                          </button>
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </section>
        </main>
      </div>
    </div>
    </template>
    
    <script>
    import { ref, onMounted } from 'vue'
    
    export default {
      emits: ['close'],
      setup(props, { emit }) {
        const searchQuery = ref('')
        const isLoading = ref(true)
    
        const metrics = ref([
          {
            id: 1,
            label: 'Organizations',
            value: '247',
            trend: '+12.5%',
            trendDirection: 'up',
            iconPath: 'M3 21h18 M5 21V7l8-4v18 M19 21V11l-6-4',
            iconBg: 'rgba(30, 126, 52, 0.1)'
          },
          {
            id: 2,
            label: 'Active Users',
            value: '12,847',
            trend: '+8.2%',
            trendDirection: 'up',
            iconPath: 'M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2 M9 7a4 4 0 1 0 0 0 M22 21l-2-2',
            iconBg: 'rgba(59, 130, 246, 0.1)'
          },
          {
            id: 3,
            label: 'System Health',
            value: '99.9%',
            trend: '+0.1%',
            trendDirection: 'up',
            iconPath: 'M22 12h-4l-3 9L9 3l-3 9H2',
            iconBg: 'rgba(16, 185, 129, 0.1)'
          },
          {
            id: 4,
            label: 'Growth',
            value: '+24.7%',
            trend: '+3.2%',
            trendDirection: 'up',
            iconPath: 'M23 6l-9.5 9.5-5-5L1 18 M17 6h6v6',
            iconBg: 'rgba(245, 158, 11, 0.1)'
          }
        ])
    
        const quickActions = ref([
          {
            id: 1,
            title: 'Create Organization',
            description: 'Add a new organization to the system',
            buttonText: 'Create New',
            iconPath: 'M5 12h14 M12 5v14',
            iconBg: 'rgba(30, 126, 52, 0.1)'
          },
          {
            id: 2,
            title: 'Add Admin',
            description: 'Invite a new administrator',
            buttonText: 'Add Admin',
            iconPath: 'M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2 M9 7a4 4 0 1 0 0 0 M22 11h-6 M19 8v6',
            iconBg: 'rgba(59, 130, 246, 0.1)'
          },
          {
            id: 3,
            title: 'Settings',
            description: 'Configure system settings',
            buttonText: 'Open Settings',
            iconPath: 'M12 20a8 8 0 1 0 0-16 8 8 0 0 0 0 16Z M12 14a2 2 0 1 0 0-4 2 2 0 0 0 0 4Z M12 2v2 M12 20v2 M4.93 4.93l1.41 1.41 M17.66 17.66l1.41 1.41 M2 12h2 M20 12h2 M4.93 19.07l1.41-1.41 M17.66 6.34l1.41-1.41',
            iconBg: 'rgba(107, 114, 128, 0.1)'
          }
        ])
    
        const recentOrganizations = ref([
          {
            id: 1,
            name: 'Children First Kenya',
            users: 45,
            status: 'Active'
          },
          {
            id: 2,
            name: 'Safe Haven Uganda',
            users: 32,
            status: 'Active'
          },
          {
            id: 3,
            name: 'Hope Foundation',
            users: 28,
            status: 'Pending'
          },
          {
            id: 4,
            name: 'Care Network',
            users: 67,
            status: 'Active'
          }
        ])
    
        const users = ref([
          {
            id: 1,
            name: 'John Doe',
            email: 'john.doe@example.com',
            organization: 'Children First Kenya',
            role: 'Admin',
            status: 'Active',
            lastActive: '2 hours ago'
          },
          {
            id: 2,
            name: 'Sarah Wilson',
            email: 'sarah.wilson@example.com',
            organization: 'Safe Haven Uganda',
            role: 'Manager',
            status: 'Active',
            lastActive: '1 day ago'
          },
          {
            id: 3,
            name: 'Michael Brown',
            email: 'michael.brown@example.com',
            organization: 'Hope Foundation',
            role: 'User',
            status: 'Inactive',
            lastActive: '1 week ago'
          },
          {
            id: 4,
            name: 'Emily Davis',
            email: 'emily.davis@example.com',
            organization: 'Care Network',
            role: 'Admin',
            status: 'Active',
            lastActive: '30 minutes ago'
          },
          {
            id: 5,
            name: 'David Johnson',
            email: 'david.johnson@example.com',
            organization: 'Children First Kenya',
            role: 'User',
            status: 'Pending',
            lastActive: '3 days ago'
          }
        ])
    
        const handleQuickAction = (actionId) => {
          console.log('Quick action clicked:', actionId)
          // Handle quick action logic here
        }
    
        const handleUserAction = (action, userId) => {
          console.log(`${action} user:`, userId)
          // Handle user action logic here
        }
    
        onMounted(() => {
          // Simulate loading
          setTimeout(() => {
            isLoading.value = false
          }, 1500)
        })
    
        return {
          searchQuery,
          isLoading,
          metrics,
          quickActions,
          recentOrganizations,
          users,
          handleQuickAction,
          handleUserAction
        }
      }
    }
    </script>
    
    <style scoped>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    /* Color Variables */
    :root {
    --primary-color: #1e7e34;
    --primary-color-light: rgba(30, 126, 52, 0.1);
    --text-primary: #111827;
    --text-secondary: #6b7280;
    --bg-light: #f8f9fa;
    --bg-white: #ffffff;
    --border-color: #e9ecef;
    }
    
    /* General Styles */
    * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    body {
    font-size: 16px;
    color: var(--text-primary);
    background-color: var(--bg-light);
    }
    
    /* App Container */
    .app-container {
    display: flex;
    min-height: 100vh;
    background-color: var(--bg-light);
    animation: fadeIn 0.6s ease-out;
    }
    
    @keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
    }
    
    /* Sidebar Styles */
    .sidebar {
    width: 240px;
    background: var(--bg-white);
    border-right: 1px solid var(--border-color);
    display: flex;
    flex-direction: column;
    transition: width 0.3s ease;
    }
    
    .sidebar-header {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 1rem;
    border-bottom: 1px solid var(--border-color);
    }
    
    .sidebar-header .logo {
    width: 32px;
    height: 32px;
    margin-right: 0.5rem;
    }
    
    .sidebar-header .brand-name {
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--primary-color);
    }
    
    .sidebar-nav {
    flex-grow: 1;
    padding: 1rem 0;
    }
    
    .sidebar-nav ul {
    list-style: none;
    padding: 0;
    margin: 0;
    }
    
    .sidebar-nav li a {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.75rem 1.5rem;
    color: var(--text-secondary);
    text-decoration: none;
    transition: all 0.2s ease;
    }
    
    .sidebar-nav li a:hover,
    .sidebar-nav li a.router-link-active {
    background-color: var(--primary-color-light);
    color: var(--primary-color);
    font-weight: 600;
    }
    
    .sidebar-nav li a svg {
    width: 1rem;
    height: 1rem;
    }
    
    .sidebar-footer {
    padding: 1rem;
    border-top: 1px solid var(--border-color);
    }
    
    .sidebar-footer a {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    color: var(--text-secondary);
    text-decoration: none;
    }
    
    /* Dashboard Container */
    .dashboard-container {
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    }
    
    /* Header Styles */
    .dashboard-header {
    background: var(--bg-white);
    border-bottom: 1px solid var(--border-color);
    padding: 1rem 2rem;
    position: sticky;
    top: 0;
    z-index: 100;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
    }
    
    .header-content {
    display: flex;
    align-items: center;
    justify-content: space-between;
    max-width: 1400px;
    margin: 0 auto;
    }
    
    /* Search Bar */
    .search-container {
    flex: 1;
    max-width: 500px;
    margin: 0 2rem;
    }
    
    .search-input-wrapper {
    position: relative;
    }
    
    .search-icon {
    position: absolute;
    left: 1rem;
    top: 50%;
    transform: translateY(-50%);
    width: 1.25rem;
    height: 1.25rem;
    color: var(--text-secondary);
    }
    
    .search-input {
    width: 100%;
    padding: 0.75rem 1rem 0.75rem 3rem;
    border: 2px solid var(--border-color);
    border-radius: 8px;
    font-size: 0.875rem;
    background: var(--bg-white);
    transition: all 0.2s ease;
    }
    
    .search-input:focus {
    outline: none;
    border-color: var(--primary-color);
    box-shadow: 0 0 0 3px var(--primary-color-light);
    }
    
    /* Profile Section */
    .profile-section {
    display: flex;
    align-items: center;
    gap: 1rem;
    }
    
    .notification-btn {
    position: relative;
    padding: 0.5rem;
    border: none;
    background: none;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.2s ease;
    }
    
    .notification-btn:hover {
    background: #f3f4f6;
    }
    
    .notification-btn svg {
    width: 1.25rem;
    height: 1.25rem;
    color: var(--text-secondary);
    }
    
    .notification-badge {
    position: absolute;
    top: 0;
    right: 0;
    background: #ef4444;
    color: var(--bg-white);
    font-size: 0.625rem;
    font-weight: 600;
    padding: 0.125rem 0.375rem;
    border-radius: 6px;
    min-width: 1.25rem;
    text-align: center;
    }
    
    .profile-info {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    }
    
    .profile-avatar {
    width: 40px;
    height: 40px;
    border-radius: 12px;
    background: var(--primary-color);
    display: flex;
    align-items: center;
    justify-content: center;
    }
    
    .profile-avatar span {
    color: var(--bg-white);
    font-weight: 600;
    font-size: 0.875rem;
    }
    
    .profile-details {
    display: flex;
    flex-direction: column;
    }
    
    .profile-name {
    font-weight: 600;
    color: var(--text-primary);
    font-size: 0.875rem;
    }
    
    .profile-role {
    font-size: 0.75rem;
    color: var(--text-secondary);
    }
    
    /* Main Content */
    .dashboard-main {
    max-width: 1400px;
    margin: 0 auto;
    padding: 2rem;
    display: flex;
    flex-direction: column;
    gap: 2rem;
    }
    
    /* Card Styles */
    .card {
    background: var(--bg-white);
    border-radius: 16px;
    padding: 1.5rem;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
    transition: all 0.3s ease;
    animation: slideUp 0.6s ease-out;
    }
    
    .card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12);
    }
    
    @keyframes slideUp {
    from {
      opacity: 0;
      transform: translateY(20px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
    }
    
    /* Metrics Section */
    .metrics-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 1.5rem;
    }
    
    .metric-content {
    display: flex;
    align-items: flex-start;
    gap: 1rem;
    }
    
    .metric-icon {
    width: 48px;
    height: 48px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    }
    
    .metric-icon svg {
    width: 24px;
    height: 24px;
    color: var(--primary-color);
    }
    
    .metric-info {
    flex: 1;
    }
    
    .metric-number {
    font-size: 2rem;
    font-weight: 800;
    color: var(--text-primary);
    line-height: 1;
    margin-bottom: 0.25rem;
    }
    
    .metric-label {
    font-size: 0.875rem;
    color: var(--text-secondary);
    font-weight: 500;
    margin-bottom: 0.5rem;
    }
    
    .metric-trend {
    display: flex;
    align-items: center;
    gap: 0.25rem;
    font-size: 0.75rem;
    font-weight: 600;
    }
    
    .metric-trend.up {
    color: #10b981;
    }
    
    .metric-trend.down {
    color: #ef4444;
    }
    
    .metric-trend svg {
    width: 1rem;
    height: 1rem;
    }
    
    /* Loading Skeleton */
    .metric-skeleton {
    display: flex;
    gap: 1rem;
    animation: pulse 1.5s ease-in-out infinite;
    }
    
    @keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
    }
    
    .skeleton-icon {
    width: 48px;
    height: 48px;
    background: var(--border-color);
    border-radius: 12px;
    }
    
    .skeleton-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    }
    
    .skeleton-number {
    height: 2rem;
    background: var(--border-color);
    border-radius: 4px;
    width: 60%;
    }
    
    .skeleton-label {
    height: 1rem;
    background: var(--border-color);
    border-radius: 4px;
    width: 40%;
    }
    
    .skeleton-trend {
    height: 0.75rem;
    background: var(--border-color);
    border-radius: 4px;
    width: 30%;
    }
    
    /* Quick Actions */
    .section-title {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 1rem;
    }
    
    .quick-actions-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 1.5rem;
    }
    
    .action-icon {
    width: 48px;
    height: 48px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 1rem;
    }
    
    .action-icon svg {
    width: 24px;
    height: 24px;
    color: var(--primary-color);
    }
    
    .action-title {
    font-size: 1.125rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 0.5rem;
    }
    
    .action-description {
    font-size: 0.875rem;
    color: var(--text-secondary);
    margin-bottom: 1.5rem;
    line-height: 1.5;
    }
    
    .action-button {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.75rem 1.5rem;
    background: var(--primary-color);
    color: var(--bg-white);
    border: none;
    border-radius: 12px;
    font-weight: 600;
    font-size: 0.875rem;
    cursor: pointer;
    transition: all 0.2s ease;
    }
    
    .action-button:hover {
    background: #166534;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(30, 126, 52, 0.3);
    }
    
    .action-button svg {
    width: 1rem;
    height: 1rem;
    }
    
    /* Management Section */
    .management-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
    gap: 1.5rem;
    }
    
    .card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1.5rem;
    }
    
    .card-title {
    font-size: 1.125rem;
    font-weight: 700;
    color: var(--text-primary);
    }
    
    .view-all-btn {
    padding: 0.5rem 1rem;
    background: none;
    border: 1px solid var(--border-color);
    border-radius: 8px;
    font-size: 0.875rem;
    font-weight: 500;
    color: var(--text-secondary);
    cursor: pointer;
    transition: all 0.2s ease;
    }
    
    .view-all-btn:hover {
    border-color: var(--primary-color);
    color: var(--primary-color);
    }
    
    .time-filter {
    padding: 0.5rem 1rem;
    border: 1px solid var(--border-color);
    border-radius: 8px;
    font-size: 0.875rem;
    background: var(--bg-white);
    cursor: pointer;
    }
    
    /* Organizations List */
    .organizations-list {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    }
    
    .organization-item {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1rem;
    border: 1px solid var(--border-color);
    border-radius: 12px;
    transition: all 0.2s ease;
    }
    
    .organization-item:hover {
    border-color: var(--primary-color);
    background: var(--primary-color-light);
    }
    
    .org-avatar {
    width: 40px;
    height: 40px;
    border-radius: 8px;
    background: var(--primary-color);
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--bg-white);
    font-weight: 600;
    font-size: 0.875rem;
    }
    
    .org-info {
    flex: 1;
    }
    
    .org-name {
    font-weight: 600;
    color: var(--text-primary);
    font-size: 0.875rem;
    margin-bottom: 0.25rem;
    }
    
    .org-details {
    font-size: 0.75rem;
    color: var(--text-secondary);
    }
    
    .org-action-btn {
    padding: 0.5rem;
    border: none;
    background: none;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.2s ease;
    }
    
    .org-action-btn:hover {
    background: #f3f4f6;
    }
    
    .org-action-btn svg {
    width: 1rem;
    height: 1rem;
    color: var(--text-secondary);
    }
    
    /* Analytics */
    .analytics-content {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    }
    
    .chart-placeholder {
    height: 200px;
    background: var(--bg-light);
    border-radius: 12px;
    display: flex;
    align-items: end;
    justify-content: center;
    padding: 1rem;
    }
    
    .chart-bars {
    display: flex;
    align-items: end;
    gap: 0.5rem;
    height: 100%;
    }
    
    .chart-bar {
    width: 24px;
    background: linear-gradient(to top, var(--primary-color), #22c55e);
    border-radius: 4px 4px 0 0;
    transition: all 0.3s ease;
    }
    
    .chart-bar:hover {
    transform: scaleY(1.1);
    }
    
    .analytics-stats {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
    }
    
    .stat-item {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
    }
    
    .stat-label {
    font-size: 0.75rem;
    color: var(--text-secondary);
    font-weight: 500;
    }
    
    .stat-value {
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--text-primary);
    }
    
    /* User Management Table */
    .user-management-section {
    animation: slideUp 0.6s ease-out;
    }
    
    .table-card {
    background: var(--bg-white);
    border-radius: 16px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
    overflow: hidden;
    }
    
    .table-controls {
    display: flex;
    gap: 0.75rem;
    }
    
    .filter-btn,
    .export-btn {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    border: 1px solid var(--border-color);
    border-radius: 8px;
    background: var(--bg-white);
    font-size: 0.875rem;
    font-weight: 500;
    color: var(--text-secondary);
    cursor: pointer;
    transition: all 0.2s ease;
    }
    
    .filter-btn:hover,
    .export-btn:hover {
    border-color: var(--primary-color);
    color: var(--primary-color);
    }
    
    .filter-btn svg,
    .export-btn svg {
    width: 1rem;
    height: 1rem;
    }
    
    .table-container {
    overflow-x: auto;
    }
    
    .user-table {
    width: 100%;
    border-collapse: collapse;
    }
    
    .user-table th {
    text-align: left;
    padding: 1rem 1.5rem;
    font-weight: 600;
    font-size: 0.875rem;
    color: var(--text-secondary);
    border-bottom: 1px solid var(--border-color);
    background: var(--bg-light);
    }
    
    .user-table td {
    padding: 1rem 1.5rem;
    border-bottom: 1px solid var(--border-color);
    font-size: 0.875rem;
    }
    
    .user-row {
    transition: all 0.2s ease;
    }
    
    .user-row:hover {
    background: var(--primary-color-light);
    }
    
    .user-info {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    }
    
    .user-avatar {
    width: 36px;
    height: 36px;
    border-radius: 8px;
    background: var(--primary-color);
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--bg-white);
    font-weight: 600;
    font-size: 0.75rem;
    }
    
    .user-details {
    display: flex;
    flex-direction: column;
    }
    
    .user-name {
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 0.125rem;
    }
    
    .user-email {
    font-size: 0.75rem;
    color: var(--text-secondary);
    }
    
    .role-badge {
    padding: 0.25rem 0.75rem;
    border-radius: 6px;
    font-size: 0.75rem;
    font-weight: 600;
    }
    
    .role-badge.admin {
    background: rgba(239, 68, 68, 0.1);
    color: #dc2626;
    }
    
    .role-badge.manager {
    background: rgba(245, 158, 11, 0.1);
    color: #d97706;
    }
    
    .role-badge.user {
    background: rgba(59, 130, 246, 0.1);
    color: #2563eb;
    }
    
    .status-indicator {
    display: inline-block;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    margin-right: 0.5rem;
    }
    
    .status-indicator.active {
    background: #10b981;
    }
    
    .status-indicator.inactive {
    background: #6b7280;
    }
    
    .status-indicator.pending {
    background: #f59e0b;
    }
    
    .action-buttons {
    display: flex;
    gap: 0.5rem;
    }
    
    .action-btn {
    display: flex;
    align-items: center;
    gap: 0.375rem;
    padding: 0.5rem 0.75rem;
    border: none;
    border-radius: 8px;
    font-size: 0.75rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
    white-space: nowrap;
    }
    
    .action-btn:hover {
    transform: translateY(-1px);
    }
    
    .action-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none;
    }
    
    .activate-btn {
    background: rgba(34, 197, 94, 0.1);
    color: #16a34a;
    border: 1px solid rgba(34, 197, 94, 0.2);
    }
    
    .activate-btn:hover:not(:disabled) {
    background: #16a34a;
    color: var(--bg-white);
    box-shadow: 0 4px 12px rgba(34, 197, 94, 0.3);
    }
    
    .deactivate-btn {
    background: rgba(245, 158, 11, 0.1);
    color: #d97706;
    border: 1px solid rgba(245, 158, 11, 0.2);
    }
    
    .deactivate-btn:hover:not(:disabled) {
    background: #d97706;
    color: var(--bg-white);
    box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);
    }
    
    .delete-btn {
    background: rgba(239, 68, 68, 0.1);
    color: #dc2626;
    border: 1px solid rgba(239, 68, 68, 0.2);
    }
    
    .delete-btn:hover:not(:disabled) {
    background: #dc2626;
    color: var(--bg-white);
    box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
    }
    
    .action-btn svg {
    width: 0.875rem;
    height: 0.875rem;
    }
    
    /* Responsive Design */
    @media (max-width: 1024px) {
    .dashboard-main {
      padding: 1.5rem;
    }
    
    .header-content {
      padding: 0 1rem;
    }
    
    .search-container {
      margin: 0 1rem;
    }
    }
    
    @media (max-width: 768px) {
    .app-container {
      flex-direction: column;
    }
    
    .sidebar {
      width: 100%;
      border-right: none;
      border-bottom: 1px solid var(--border-color);
    }
    
    .dashboard-main {
      padding: 1rem;
    }
    
    .header-content {
      flex-direction: column;
      gap: 1rem;
      align-items: stretch;
    }
    
    .search-container {
      margin: 0;
      max-width: none;
    }
    
    .metrics-grid {
      grid-template-columns: 1fr;
    }
    
    .quick-actions-grid {
      grid-template-columns: 1fr;
    }
    
    .management-grid {
      grid-template-columns: 1fr;
    }
    
    .action-buttons {
      flex-direction: column;
    }
    
    .action-btn {
      justify-content: center;
    }
    }
    
    @media (max-width: 480px) {
    .dashboard-header {
      padding: 1rem;
    }
    
    .dashboard-main {
      padding: 0.75rem;
      gap: 1.5rem;
    }
    
    .card,
    .action-card,
    .management-card,
    .table-card {
      padding: 1rem;
    }
    
    .user-table th,
    .user-table td {
      padding: 0.75rem 1rem;
    }
    
    .action-btn {
      padding: 0.375rem 0.5rem;
      font-size: 0.6875rem;
    }
    
    .action-btn svg {
      width: 0.75rem;
      height: 0.75rem;
    }
    }
    </style>