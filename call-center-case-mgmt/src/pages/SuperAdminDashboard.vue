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
          <div class="sidebar-header">
            <div class="logo-container">
              <div class="logo">
                <img src="/Openchs logo-1.png" alt="OpenCHS Logo">
              </div>
            </div>
          </div>
          
          <div class="nav-section">
            <a href="/dashboard" class="nav-item" @click.prevent="navigateTo('/dashboard')">
              <div class="nav-icon">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M3 9L12 2L21 9V20C21 20.5304 20.7893 21.0391 20.4142 21.4142C20.0391 21.7893 19.5304 22 19 22H5C4.46957 22 3.96086 21.7893 3.58579 21.4142C3.21071 21.0391 3 20.5304 3 20V9Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <polyline points="9,22 9,12 15,12 15,22" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </div>
              <div class="nav-text">Dashboard</div>
            </a>
            
            <a href="/calls" class="nav-item" @click.prevent="navigateTo('/calls')">
              <div class="nav-icon">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M22 16.92V19C22 20.1046 21.1046 21 20 21C10.6112 21 3 13.3888 3 4C3 2.89543 3.89543 2 5 2H7.08C7.55607 2 7.95823 2.33718 8.02513 2.80754L8.7 7.5C8.76694 7.97036 8.53677 8.42989 8.12 8.67L6.5 9.5C7.84 12.16 11.84 16.16 14.5 17.5L15.33 15.88C15.5701 15.4632 16.0296 15.2331 16.5 15.3L21.1925 16.0249C21.6628 16.0918 22 16.4939 22 16.97V16.92Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </div>
              <div class="nav-text">Calls</div>
            </a>
            
            <a href="/cases" class="nav-item" @click.prevent="navigateTo('/cases')">
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
            </a>
            
            <a href="/chats" class="nav-item" @click.prevent="navigateTo('/chats')">
              <div class="nav-icon">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M21 15C21 15.5304 20.7893 16.0391 20.4142 16.4142C20.0391 16.7893 19.5304 17 19 17H7L3 21V5C3 4.46957 3.21071 3.96086 3.58579 3.58579C3.96086 3.21071 4.46957 3 5 3H19C19.5304 3 20.0391 3.21071 20.4142 3.58579C20.7893 3.96086 21 4.46957 21 5V15Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M8 9H16" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M8 13H14" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </div>
              <div class="nav-text">Chats</div>
            </a>
            
            <a href="/qa-statistics" class="nav-item" @click.prevent="navigateTo('/qa-statistics')">
              <div class="nav-icon">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <line x1="18" y1="20" x2="18" y2="10" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <line x1="12" y1="20" x2="12" y2="4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <line x1="6" y1="20" x2="6" y2="14" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </div>
              <div class="nav-text">QA Statistics</div>
            </a>
            
            <a href="/wallboard" class="nav-item" @click.prevent="navigateTo('/wallboard')">
              <div class="nav-icon">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <rect x="2" y="3" width="20" height="14" rx="2" ry="2" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <line x1="8" y1="21" x2="16" y2="21" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <line x1="12" y1="17" x2="12" y2="21" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </div>
              <div class="nav-text">Wallboard</div>
            </a>
            
            <a href="/settings" class="nav-item" @click.prevent="navigateTo('/settings')">
              <div class="nav-icon">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M19.4 15C19.2669 15.3016 19.2272 15.6362 19.286 15.9606C19.3448 16.285 19.4995 16.5843 19.73 16.82L19.79 16.88C19.976 17.0657 20.1235 17.2863 20.2241 17.5291C20.3248 17.7719 20.3766 18.0322 20.3766 18.295C20.3766 18.5578 20.3248 18.8181 20.2241 19.0609C20.1235 19.3037 19.976 19.5243 19.79 19.71C19.6043 19.896 19.3837 20.0435 19.1409 20.1441C18.8981 20.2448 18.6378 20.2966 18.375 20.2966C18.1122 20.2966 17.8519 20.2448 17.6091 20.1441C17.3663 20.0435 17.1457 19.896 16.96 19.71L16.9 19.65C16.6643 19.4195 16.365 19.2648 16.0406 19.206C15.7162 19.1472 15.3816 19.1869 15.08 19.32C14.7842 19.4468 14.532 19.6572 14.3543 19.9255C14.1766 20.1938 14.0813 20.5082 14.08 20.83V21C14.08 21.5304 13.8693 22.0391 13.4942 22.4142C13.1191 22.7893 12.6104 23 12.08 23C11.5496 23 11.0409 22.7893 10.6658 22.4142C10.2907 22.0391 10.08 21.5304 10.08 21V20.91C10.0723 20.579 9.96512 20.2573 9.77251 19.9887C9.5799 19.7201 9.31074 19.5176 9 19.41C8.69838 19.2769 8.36381 19.2372 8.03941 19.296C7.71502 19.3548 7.41568 19.5095 7.18 19.74L7.12 19.8C6.93425 19.986 6.71368 20.1335 6.47088 20.2341C6.22808 20.3348 5.96783 20.3866 5.705 20.3866C5.44217 20.3866 5.18192 20.3348 4.93912 20.2341C4.69632 20.1335 4.47575 19.986 4.29 19.8C4.10405 19.6143 3.95653 19.3937 3.85588 19.1509C3.75523 18.9081 3.70343 18.6478 3.70343 18.385C3.70343 18.1222 3.75523 17.8619 3.85588 17.6191C3.95653 17.3763 4.10405 17.1557 4.29 16.97L4.35 16.91C4.58054 16.6743 4.73519 16.375 4.794 16.0506C4.85282 15.7262 4.81312 15.3916 4.68 15.09C4.55324 14.7942 4.34276 14.542 4.07447 14.3643C3.80618 14.1866 3.49179 14.0913 3.17 14.09H3C2.46957 14.09 1.96086 13.8793 1.58579 13.5042C1.21071 13.1291 1 12.6204 1 12.09C1 11.5596 1.21071 11.0509 1.58579 10.6758C1.96086 10.3007 2.46957 10.09 3 10.09H3.09C3.42099 10.0823 3.742 9.97512 4.01062 9.78251C4.27925 9.5899 4.48167 9.32074 4.59 9.01C4.72312 8.70838 4.76282 8.37381 4.704 8.04941C4.64519 7.72502 4.49054 7.42568 4.26 7.19L4.2 7.13C4.01405 6.94425 3.86653 6.72368 3.76588 6.48088C3.66523 6.23808 3.61343 5.97783 3.61343 5.715C3.61343 5.45217 3.66523 5.19192 3.76588 4.94912C3.86653 4.70632 4.01405 4.48575 4.2 4.3C4.38575 4.11405 4.60632 3.96653 4.84912 3.86588C5.09192 3.76523 5.35217 3.71343 5.615 3.71343C5.87783 3.71343 6.13808 3.76523 6.38088 3.86588C6.62368 3.96653 6.84425 4.11405 7.03 4.3L7.09 4.36C7.32568 4.59054 7.62502 4.74519 7.94941 4.804C8.27381 4.86282 8.60838 4.82312 8.91 4.69H9C9.29577 4.56324 9.54802 4.35276 9.72569 4.08447C9.90337 3.81618 9.99872 3.50179 10 3.18V3C10 2.46957 10.2107 1.96086 10.5858 1.58579C10.9609 1.21071 11.4696 1 12 1C12.5304 1 13.0391 1.21071 13.4142 1.58579C13.7893 1.96086 14 2.46957 14 3V3.09C14.0013 3.41179 14.0966 3.72618 14.2743 3.99447C14.452 4.26276 14.7042 4.47324 15 4.6C15.3016 4.73312 15.6362 4.77282 15.9606 4.714C16.285 4.65519 16.5843 4.50054 16.82 4.27L16.88 4.21C17.0657 4.02405 17.2863 3.87653 17.5291 3.77588C17.7719 3.67523 18.0322 3.62343 18.295 3.62343C18.5578 3.62343 18.8181 3.67523 19.0609 3.77588C19.3037 3.87653 19.5243 4.02405 19.71 4.21C19.896 4.39575 20.0435 4.61632 20.1441 4.85912C20.2448 5.10192 20.2966 5.36217 20.2966 5.625C20.2966 5.88783 20.2448 6.14808 20.1441 6.39088C20.0435 6.63368 19.896 6.85425 19.71 7.04L19.65 7.1C19.4195 7.33568 19.2648 7.63502 19.206 7.95941C19.1472 8.28381 19.1869 8.61838 19.32 8.92V9C19.4468 9.29577 19.6572 9.54802 19.9255 9.72569C20.1938 9.90337 20.5082 9.99872 20.83 10H21C21.5304 10 22.0391 10.2107 22.4142 10.5858C22.7893 10.9609 23 11.4696 23 12C23 12.5304 22.7893 13.0391 22.4142 13.4142C22.0391 13.7893 21.5304 14 21 14H20.91C20.5882 14.0013 20.2738 14.0966 20.0055 14.2743C19.7372 14.452 19.5268 14.7042 19.4 15Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </div>
              <div class="nav-text">Settings</div>
            </a>
  
            <!-- Super Admin Dashboard Button -->
            <a href="/super-admin-dashboard" class="nav-item active" @click.prevent="navigateTo('/super-admin-dashboard')">
              <div class="nav-icon">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M12 22S8 18 8 12V5L12 2L16 5V12C16 18 12 22 12 22Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M9 12L11 14L15 10" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </div>
              <div class="nav-text">Super Admin</div>
            </a>
          </div>
          
          <div class="sidebar-bottom">
            <div class="user-profile">
              <a href="/edit-profile" class="user-avatar" @click.prevent="navigateTo('/edit-profile')">
                <svg viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                  <path d="M12 12C14.2091 12 16 10.2091 16 8C16 5.79086 14.2091 4 12 4C9.79086 4 8 5.79086 8 8C8 10.2091 9.79086 12 12 12Z"/>
                  <path d="M12 14C7.58172 14 4 17.5817 4 22H20C20 17.5817 16.4183 14 12 14Z"/>
                </svg>
              </a>
            </div>
            
            <div class="status">
              <div class="status-dot"></div>
              <span>Online</span>
            </div>
            
            <div class="button-container">
              <button class="logout-btn" @click="logout">Logout</button>
            </div>
          </div>
        </div>
      </div>
  
      <button class="expand-btn" @click="expandSidebar" id="expand-btn">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M3 12H21M3 6H21M3 18H21" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </button>
  
      <!-- Main Content -->
      <div class="main-content">
        <div class="header">
          <h1 class="page-title">Super Admin Dashboard</h1>
          <button class="theme-toggle" @click="toggleTheme" id="theme-toggle">
            <svg v-if="currentTheme === 'dark'" id="moon-icon" width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <svg v-else id="sun-icon" width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
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
            <span id="theme-text">{{ currentTheme === 'dark' ? 'Light Mode' : 'Dark Mode' }}</span>
          </button>
        </div>
  
        <div class="main-scroll-content">
          <!-- Dashboard Grid -->
          <div class="dashboard-grid">
            <div class="dashboard-card">
              <div class="card-header">
                <div class="card-title">Organizations</div>
                <div class="card-icon">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M3 21h18M5 21V7l8-4v18M19 21V11l-6-4" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </div>
              </div>
              <div class="card-value">247</div>
              <div class="card-subtitle">+12.5% from last month</div>
            </div>
            
            <div class="dashboard-card">
              <div class="card-header">
                <div class="card-title">Active Users</div>
                <div class="card-icon">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <circle cx="9" cy="7" r="4" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M23 21v-2a4 4 0 0 0-3-3.87" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M16 3.13a4 4 0 0 1 0 7.75" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </div>
              </div>
              <div class="card-value">12,847</div>
              <div class="card-subtitle">+8.2% from last month</div>
            </div>
            
            <div class="dashboard-card">
              <div class="card-header">
                <div class="card-title">System Health</div>
                <div class="card-icon">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M22 12h-4l-3 9L9 3l-3 9H2" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </div>
              </div>
              <div class="card-value">99.9%</div>
              <div class="card-subtitle">+0.1% from last week</div>
            </div>
            
            <div class="dashboard-card">
              <div class="card-header">
                <div class="card-title">Growth</div>
                <div class="card-icon">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M23 6l-9.5 9.5-5-5L1 18" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M17 6h6v6" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </div>
              </div>
              <div class="card-value">+24.7%</div>
              <div class="card-subtitle">+3.2% from last month</div>
            </div>
          </div>
  
          <!-- Quick Actions -->
          <div class="quick-actions-section">
            <div class="section-header">
              <div class="section-title">Quick Actions</div>
            </div>
            
            <div class="quick-actions-grid">
              <div class="action-card" @click="handleQuickAction('create-org')">
                <div class="action-icon">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 5v14M5 12h14" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </div>
                <div class="action-content">
                  <h3 class="action-title">Create Organization</h3>
                  <p class="action-description">Add a new organization to the system</p>
                  <button class="action-button">
                    Create New
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <polyline points="9 18 15 12 9 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                  </button>
                </div>
              </div>
              
              <div class="action-card" @click="handleQuickAction('add-admin')">
                <div class="action-icon">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <circle cx="9" cy="7" r="4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M19 8v6M16 11h6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </div>
                <div class="action-content">
                  <h3 class="action-title">Add Admin</h3>
                  <p class="action-description">Invite a new administrator</p>
                  <button class="action-button">
                    Add Admin
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <polyline points="9 18 15 12 9 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                  </button>
                </div>
              </div>
              
              <div class="action-card" @click="handleQuickAction('settings')">
                <div class="action-icon">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </div>
                <div class="action-content">
                  <h3 class="action-title">Settings</h3>
                  <p class="action-description">Configure system settings</p>
                  <button class="action-button">
                    Open Settings
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <polyline points="9 18 15 12 9 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </div>
  
          <!-- Management Section -->
          <div class="management-grid">
            <!-- Recent Organizations -->
            <div class="management-card">
              <div class="card-header">
                <div class="section-title">Recent Organizations</div>
                <button class="view-all-btn" @click="viewAllOrganizations">View All</button>
              </div>
              <div class="organizations-list">
                <div v-for="org in recentOrganizations" :key="org.id" class="organization-item">
                  <div class="org-avatar">
                    <span>{{ org.name.charAt(0) }}</span>
                  </div>
                  <div class="org-info">
                    <h4 class="org-name">{{ org.name }}</h4>
                    <p class="org-details">{{ org.users }} users • {{ org.status }}</p>
                  </div>
                  <div class="org-actions">
                    <button class="org-action-btn" @click="toggleFavorite(org.id)">
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <polygon points="12,2 15.09,8.26 22,9.27 17,14.14 18.18,21.02 12,17.77 5.82,21.02 7,14.14 2,9.27 8.91,8.26" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                      </svg>
                    </button>
                  </div>
                </div>
              </div>
            </div>
  
            <!-- Usage Analytics -->
            <div class="management-card">
              <div class="card-header">
                <div class="section-title">Usage Analytics</div>
                <select class="time-filter" v-model="selectedTimeframe">
                  <option value="7days">Last 7 days</option>
                  <option value="30days">Last 30 days</option>
                  <option value="90days">Last 90 days</option>
                </select>
              </div>
              <div class="analytics-content">
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
  
          <!-- User Management Table -->
          <div class="user-management-section">
            <div class="table-card">
              <div class="card-header">
                <div class="section-title">User Management</div>
                <div class="table-controls">
                  <button class="filter-btn" @click="toggleFilters">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <polygon points="22,3 2,3 10,12.46 10,19 14,21 14,12.46" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                    Filter
                  </button>
                  <button class="export-btn" @click="exportUserData">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                      <polyline points="7,10 12,15 17,10" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                      <line x1="12" y1="15" x2="12" y2="3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
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
                    <tr v-for="user in users" :key="user.id" class="user-row">
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
                      <td>{{ user.organization }}</td>
                      <td>
                        <span class="role-badge" :class="user.role.toLowerCase()">{{ user.role }}</span>
                      </td>
                      <td>
                        <div class="status-indicator-container">
                          <span class="status-indicator" :class="user.status.toLowerCase()"></span>
                          <span>{{ user.status }}</span>
                        </div>
                      </td>
                      <td>{{ user.lastActive }}</td>
                      <td>
                        <div class="action-buttons">
                          <button 
                            class="action-btn activate-btn" 
                            :disabled="user.status === 'Active'"
                            @click="handleUserAction('activate', user.id)"
                          >
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                              <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                              <polyline points="22,4 12,14.01 9,11.01" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                            </svg>
                            Activate
                          </button>
                          <button 
                            class="action-btn deactivate-btn" 
                            :disabled="user.status === 'Inactive'"
                            @click="handleUserAction('deactivate', user.id)"
                          >
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                              <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                              <line x1="15" y1="9" x2="9" y2="15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                              <line x1="9" y1="9" x2="15" y2="15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                            </svg>
                            Deactivate
                          </button>
                          <button 
                            class="action-btn delete-btn"
                            @click="handleUserAction('delete', user.id)"
                          >
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                              <polyline points="3,6 5,6 21,6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                              <path d="m19,6v14a2,2 0 0,1-2,2H7a2,2 0 0,1-2-2V6m3,0V4a2,2 0 0,1,2-2h4a2,2 0 0,1,2,2v2" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                              <line x1="10" y1="11" x2="10" y2="17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                              <line x1="14" y1="11" x2="14" y2="17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
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
          </div>
  
          <!-- Create Organization Modal -->
          <div class="modal" v-if="showCreateOrgModal">
            <div class="modal-content">
              <div class="modal-header">
                <h2>Create New Organization</h2>
                <button class="close-btn" @click="showCreateOrgModal = false">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <line x1="18" y1="6" x2="6" y2="18" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <line x1="6" y1="6" x2="18" y2="18" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </button>
              </div>
              <div class="modal-body">
                <div class="form-group">
                  <label for="org-name">Organization Name</label>
                  <input type="text" id="org-name" v-model="newOrg.name" placeholder="Enter organization name">
                </div>
                <div class="form-group">
                  <label for="org-location">Location</label>
                  <input type="text" id="org-location" v-model="newOrg.location" placeholder="Enter location">
                </div>
                <div class="form-group">
                  <label for="org-admin">Admin Email</label>
                  <input type="email" id="org-admin" v-model="newOrg.adminEmail" placeholder="Enter admin email">
                </div>
                <div class="form-group">
                  <label for="org-type">Organization Type</label>
                  <select id="org-type" v-model="newOrg.type">
                    <option value="ngo">NGO</option>
                    <option value="government">Government</option>
                    <option value="private">Private</option>
                    <option value="other">Other</option>
                  </select>
                </div>
              </div>
              <div class="modal-footer">
                <button class="cancel-btn" @click="showCreateOrgModal = false">Cancel</button>
                <button class="submit-btn" @click="createOrganization">Create Organization</button>
              </div>
            </div>
          </div>
  
          <!-- Add Admin Modal -->
          <div class="modal" v-if="showAddAdminModal">
            <div class="modal-content">
              <div class="modal-header">
                <h2>Add New Admin</h2>
                <button class="close-btn" @click="showAddAdminModal = false">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <line x1="18" y1="6" x2="6" y2="18" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <line x1="6" y1="6" x2="18" y2="18" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </button>
              </div>
              <div class="modal-body">
                <div class="form-group">
                  <label for="admin-name">Full Name</label>
                  <input type="text" id="admin-name" v-model="newAdmin.name" placeholder="Enter full name">
                </div>
                <div class="form-group">
                  <label for="admin-email">Email</label>
                  <input type="email" id="admin-email" v-model="newAdmin.email" placeholder="Enter email">
                </div>
                <div class="form-group">
                  <label for="admin-org">Organization</label>
                  <select id="admin-org" v-model="newAdmin.organization">
                    <option v-for="org in recentOrganizations" :key="org.id" :value="org.name">
                      {{ org.name }}
                    </option>
                  </select>
                </div>
                <div class="form-group">
                  <label for="admin-role">Role</label>
                  <select id="admin-role" v-model="newAdmin.role">
                    <option value="Admin">Admin</option>
                    <option value="Manager">Manager</option>
                    <option value="User">User</option>
                  </select>
                </div>
              </div>
              <div class="modal-footer">
                <button class="cancel-btn" @click="showAddAdminModal = false">Cancel</button>
                <button class="submit-btn" @click="addAdmin">Add Admin</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  
  // Reactive state
  const isSidebarCollapsed = ref(false)
  const mobileOpen = ref(false)
  const currentTheme = ref('dark')
  const selectedTimeframe = ref('7days')
  const showCreateOrgModal = ref(false)
  const showAddAdminModal = ref(false)
  
  // Form data
  const newOrg = ref({
    name: '',
    location: '',
    adminEmail: '',
    type: 'ngo'
  })
  
  const newAdmin = ref({
    name: '',
    email: '',
    organization: '',
    role: 'Admin'
  })
  
  // Data
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
  
  // Methods
  const toggleSidebar = () => {
    isSidebarCollapsed.value = !isSidebarCollapsed.value
  }
  
  const expandSidebar = () => {
    isSidebarCollapsed.value = false
  }
  
  const toggleMobileMenu = () => {
    mobileOpen.value = !mobileOpen.value
  }
  
  const navigateTo = (path) => {
    console.log(`Navigating to: ${path}`)
    // In a real app, you would use router.push(path) or window.location.href = path
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
      root.style.setProperty('--logo-bg', '#ffffff')
      root.style.setProperty('--logo-color', '#333')
      root.setAttribute('data-theme', 'light')
    } else {
      root.style.setProperty('--background-color', '#0a0a0a')
      root.style.setProperty('--sidebar-bg', '#111')
      root.style.setProperty('--content-bg', '#222')
      root.style.setProperty('--text-color', '#fff')
      root.style.setProperty('--text-secondary', '#aaa')
      root.style.setProperty('--border-color', '#333')
      root.style.setProperty('--card-bg', '#222')
      root.style.setProperty('--logo-bg', '#fff')
      root.style.setProperty('--logo-color', '#0a0a0a')
      root.setAttribute('data-theme', 'dark')
    }
    
    // Set common variables
    root.style.setProperty('--accent-color', '#964B00')
    root.style.setProperty('--accent-hover', '#b25900')
    root.style.setProperty('--danger-color', '#ff3b30')
    root.style.setProperty('--success-color', '#4CAF50')
    root.style.setProperty('--pending-color', '#FFA500')
    root.style.setProperty('--unassigned-color', '#808080')
    root.style.setProperty('--highlight-color', '#ff3b30')
  }
  
  const toggleTheme = () => {
    currentTheme.value = currentTheme.value === 'dark' ? 'light' : 'dark'
    localStorage.setItem('theme', currentTheme.value)
    applyTheme(currentTheme.value)
  }
  
  const logout = () => {
    console.log('Logging out...')
    alert('Logged out successfully!')
  }
  
  const handleQuickAction = (action) => {
    console.log('Quick action:', action)
    
    if (action === 'create-org') {
      showCreateOrgModal.value = true
    } else if (action === 'add-admin') {
      showAddAdminModal.value = true
    } else if (action === 'settings') {
      navigateTo('/settings')
    }
  }
  
  const handleUserAction = (action, userId) => {
    console.log(`${action} user:`, userId)
    
    const userIndex = users.value.findIndex(user => user.id === userId)
    if (userIndex !== -1) {
      if (action === 'activate') {
        users.value[userIndex].status = 'Active'
        alert(`User ${users.value[userIndex].name} has been activated.`)
      } else if (action === 'deactivate') {
        users.value[userIndex].status = 'Inactive'
        alert(`User ${users.value[userIndex].name} has been deactivated.`)
      } else if (action === 'delete') {
        if (confirm(`Are you sure you want to delete ${users.value[userIndex].name}?`)) {
          users.value = users.value.filter(user => user.id !== userId)
          alert('User has been deleted.')
        }
      }
    }
  }
  
  const viewAllOrganizations = () => {
    navigateTo('/organizations')
  }
  
  const toggleFavorite = (orgId) => {
    console.log('Toggle favorite for org:', orgId)
    alert(`Organization ${orgId} has been added to favorites.`)
  }
  
  const toggleFilters = () => {
    console.log('Toggle filters')
    alert('Filters functionality would be implemented here.')
  }
  
  const exportUserData = () => {
    console.log('Export user data')
    alert('User data would be exported here.')
  }
  
  const createOrganization = () => {
    console.log('Creating organization:', newOrg.value)
    
    // Validate form
    if (!newOrg.value.name || !newOrg.value.location || !newOrg.value.adminEmail) {
      alert('Please fill in all required fields.')
      return
    }
    
    // Add new organization to the list
    const newId = recentOrganizations.value.length + 1
    recentOrganizations.value.unshift({
      id: newId,
      name: newOrg.value.name,
      users: 1,
      status: 'Active'
    })
    
    // Reset form and close modal
    newOrg.value = {
      name: '',
      location: '',
      adminEmail: '',
      type: 'ngo'
    }
    
    showCreateOrgModal.value = false
    alert('Organization created successfully!')
  }
  
  const addAdmin = () => {
    console.log('Adding admin:', newAdmin.value)
    
    // Validate form
    if (!newAdmin.value.name || !newAdmin.value.email || !newAdmin.value.organization) {
      alert('Please fill in all required fields.')
      return
    }
    
    // Add new admin to the list
    const newId = users.value.length + 1
    users.value.unshift({
      id: newId,
      name: newAdmin.value.name,
      email: newAdmin.value.email,
      organization: newAdmin.value.organization,
      role: newAdmin.value.role,
      status: 'Active',
      lastActive: 'Just now'
    })
    
    // Reset form and close modal
    newAdmin.value = {
      name: '',
      email: '',
      organization: '',
      role: 'Admin'
    }
    
    showAddAdminModal.value = false
    alert('Admin added successfully!')
  }
  
  // Lifecycle
  onMounted(() => {
    // Load saved theme
    const savedTheme = localStorage.getItem('theme')
    if (savedTheme) {
      currentTheme.value = savedTheme
    }
    
    // Apply theme immediately
    applyTheme(currentTheme.value)
  
    // Handle window resize
    const handleResize = () => {
      if (window.innerWidth > 1024) {
        mobileOpen.value = false
      }
    }
    window.addEventListener('resize', handleResize)
  
    // Handle click outside sidebar on mobile/tablet
    const handleClickOutside = (event) => {
      const isMobileOrTablet = window.innerWidth <= 1024
      const sidebar = document.getElementById('sidebar')
      const mobileMenuBtn = document.getElementById('mobile-menu-btn')
      
      if (isMobileOrTablet && sidebar && !sidebar.contains(event.target) && event.target !== mobileMenuBtn) {
        mobileOpen.value = false
      }
    }
    document.addEventListener('click', handleClickOutside)
  })
  </script>
  
  <style>
  /* Global styles - not scoped */
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
  
  .sidebar {
    width: 250px;
    background-color: var(--sidebar-bg);
    color: var(--text-color);
    height: 100vh;
    position: fixed;
    transition: width 0.3s ease, transform 0.3s ease, background-color 0.3s;
    overflow: hidden;
    border-radius: 0 30px 30px 0;
    z-index: 100;
    display: flex;
    flex-direction: column;
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
    display: none;
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
  
  .sidebar.collapsed ~ .expand-btn {
    display: flex;
  }
  
  .sidebar-content {
    width: 250px;
    height: 100%;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }
  
  .sidebar.collapsed .sidebar-content {
    opacity: 0;
    pointer-events: none;
  }
  
  .sidebar-header {
    flex-shrink: 0;
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
    border-radius: 50%;
    background-color: var(--logo-bg);
    display: flex;
    justify-content: center;
    align-items: center;
    overflow: hidden;
  }
  
  .logo img {
    width: 30px;
    height: 30px;
    object-fit: contain;
  }
  
  .nav-section {
    flex: 1;
    overflow-y: auto;
    overflow-x: hidden;
    padding: 0 15px;
    margin-bottom: 15px;
    /* Completely invisible scrollbar */
    scrollbar-width: none; /* Firefox */
    -ms-overflow-style: none; /* Internet Explorer 10+ */
  }
  
  .nav-section::-webkit-scrollbar {
    display: none; /* WebKit browsers */
  }
  
  .nav-item {
    display: flex;
    align-items: center;
    padding: 10px 12px;
    cursor: pointer;
    margin-bottom: 4px;
    border-radius: 12px;
    text-decoration: none;
    color: var(--text-color);
    transition: all 0.3s ease;
    min-height: 44px;
  }
  
  .nav-item:hover {
    background-color: rgba(255, 255, 255, 0.05);
    transform: translateX(3px);
  }
  
  .nav-item.active {
    background-color: rgba(255, 255, 255, 0.1);
  }
  
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
    flex-shrink: 0;
  }
  
  .nav-item:hover .nav-icon {
    background-color: rgba(255, 255, 255, 0.2);
    transform: scale(1.05);
  }
  
  .nav-icon svg {
    color: var(--text-color);
    stroke: var(--text-color);
    width: 18px;
    height: 18px;
  }
  
  .nav-text {
    font-size: 14px;
    font-weight: 600;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  
  .sidebar-bottom {
    padding: 0 15px 20px 15px;
    flex-shrink: 0;
  }
  
  .user-profile {
    display: flex;
    justify-content: center;
    margin-bottom: 12px;
  }
  
  .user-avatar {
    width: 44px;
    height: 44px;
    border-radius: 50%;
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
    transform: scale(1.05);
  }
  
  .user-avatar svg {
    width: 24px;
    height: 24px;
    fill: var(--background-color);
  }
  
  .status {
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    font-weight: 600;
    margin-bottom: 12px;
    color: var(--text-secondary);
  }
  
  .status-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background-color: var(--success-color);
    margin-right: 6px;
  }
  
  .button-container {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }
  
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
    background-color: #e60000;
    transform: translateY(-1px);
  }
  
  .main-content {
    flex: 1;
    margin-left: 250px;
    height: 100vh;
    background-color: var(--background-color);
    transition: margin-left 0.3s ease, width 0.3s ease, background-color 0.3s;
    width: calc(100% - 250px);
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }
  
  .sidebar.collapsed ~ .main-content {
    margin-left: 20px;
    width: calc(100% - 20px);
  }
  
  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px 20px 0 20px;
    flex-shrink: 0;
  }
  
  .page-title {
    font-size: 28px;
    font-weight: 700;
  }
  
  .theme-toggle {
    background-color: var(--content-bg);
    color: var(--text-color);
    border: 1px solid var(--border-color);
    border-radius: 30px;
    padding: 8px 15px;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 8px;
    transition: all 0.3s ease;
  }
  
  .theme-toggle:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
  }
  
  .theme-toggle svg {
    width: 16px;
    height: 16px;
  }
  
  .main-scroll-content {
    flex: 1;
    padding: 20px;
    overflow-y: auto;
    overflow-x: hidden;
    /* Completely invisible scrollbar */
    scrollbar-width: none; /* Firefox */
    -ms-overflow-style: none; /* Internet Explorer 10+ */
  }
  
  .main-scroll-content::-webkit-scrollbar {
    display: none; /* WebKit browsers */
  }
  
  .dashboard-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 20px;
    margin-bottom: 30px;
  }
  
  .dashboard-card {
    background-color: var(--card-bg);
    border-radius: 30px;
    padding: 20px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transition: transform 0.2s, box-shadow 0.2s, background-color 0.3s;
  }
  
  .dashboard-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
  }
  
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 15px;
  }
  
  .card-title {
    font-size: 16px;
    font-weight: 700;
  }
  
  .card-icon {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background-color: var(--accent-color);
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  .card-icon svg {
    stroke: white;
  }
  
  .card-value {
    font-size: 32px;
    font-weight: 800;
    margin-bottom: 5px;
  }
  
  .card-subtitle {
    font-size: 13px;
    font-weight: 600;
    color: var(--text-secondary);
  }
  
  .quick-actions-section {
    margin-bottom: 30px;
  }
  
  .section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
  }
  
  .section-title {
    font-size: 20px;
    font-weight: 700;
  }
  
  .quick-actions-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 20px;
  }
  
  .action-card {
    background-color: var(--card-bg);
    border-radius: 30px;
    padding: 20px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transition: transform 0.2s, box-shadow 0.2s, background-color 0.3s;
    cursor: pointer;
  }
  
  .action-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
  }
  
  .action-icon {
    width: 48px;
    height: 48px;
    border-radius: 12px;
    background-color: rgba(150, 75, 0, 0.1);
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 15px;
  }
  
  .action-icon svg {
    width: 24px;
    height: 24px;
    color: var(--accent-color);
  }
  
  .action-title {
    font-size: 18px;
    font-weight: 700;
    margin-bottom: 8px;
  }
  
  .action-description {
    font-size: 14px;
    color: var(--text-secondary);
    margin-bottom: 15px;
    line-height: 1.5;
  }
  
  .action-button {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 10px 20px;
    background-color: var(--accent-color);
    color: white;
    border: none;
    border-radius: 25px;
    font-weight: 600;
    font-size: 14px;
    cursor: pointer;
    transition: all 0.3s ease;
    width: 100%;
    justify-content: center;
  }
  
  .action-button:hover {
    background-color: var(--accent-hover);
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(150, 75, 0, 0.3);
  }
  
  .action-button svg {
    width: 16px;
    height: 16px;
  }
  
  .management-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
    gap: 20px;
    margin-bottom: 30px;
  }
  
  .management-card {
    background-color: var(--card-bg);
    border-radius: 30px;
    padding: 20px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transition: background-color 0.3s;
  }
  
  .view-all-btn {
    padding: 8px 16px;
    background: none;
    border: 1px solid var(--border-color);
    border-radius: 20px;
    font-size: 14px;
    font-weight: 600;
    color: var(--text-secondary);
    cursor: pointer;
    transition: all 0.3s ease;
    background: var(--background-color);
  }
  
  .view-all-btn:hover {
    border-color: var(--accent-color);
    color: var(--accent-color);
  }
  
  .organizations-list {
    display: flex;
    flex-direction: column;
    gap: 15px;
  }
  
  .organization-item {
    display: flex;
    align-items: center;
    gap: 15px;
    padding: 15px;
    border: 1px solid var(--border-color);
    border-radius: 20px;
    transition: all 0.3s ease;
  }
  
  .organization-item:hover {
    border-color: var(--accent-color);
    background-color: rgba(150, 75, 0, 0.05);
  }
  
  .org-avatar {
    width: 40px;
    height: 40px;
    border-radius: 10px;
    background-color: var(--accent-color);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-weight: 600;
    font-size: 14px;
  }
  
  .org-info {
    flex: 1;
  }
  
  .org-name {
    font-weight: 600;
    margin-bottom: 4px;
  }
  
  .org-details {
    font-size: 12px;
    color: var(--text-secondary);
  }
  
  .org-actions {
    display: flex;
    gap: 8px;
  }
  
  .org-action-btn {
    padding: 8px;
    border: none;
    background: none;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.3s ease;
    color: var(--text-secondary);
  }
  
  .org-action-btn:hover {
    background-color: var(--background-color);
    color: var(--text-color);
  }
  
  .org-action-btn svg {
    width: 16px;
    height: 16px;
  }
  
  .time-filter {
    padding: 8px 12px;
    background: var(--background-color);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    font-size: 14px;
    font-weight: 500;
    color: var(--text-color);
    cursor: pointer;
    transition: all 0.3s ease;
  }
  
  .analytics-content {
    display: flex;
    flex-direction: column;
    gap: 20px;
  }
  
  .chart-placeholder {
    height: 200px;
    background-color: var(--background-color);
    border-radius: 15px;
    display: flex;
    align-items: end;
    justify-content: center;
    padding: 20px;
  }
  
  .chart-bars {
    display: flex;
    align-items: end;
    gap: 8px;
    height: 100%;
  }
  
  .chart-bar {
    width: 20px;
    background: linear-gradient(to top, var(--accent-color), #b25900);
    border-radius: 4px 4px 0 0;
    transition: all 0.3s ease;
  }
  
  .chart-bar:hover {
    transform: scaleY(1.1);
  }
  
  .analytics-stats {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 20px;
  }
  
  .stat-item {
    display: flex;
    flex-direction: column;
    gap: 4px;
  }
  
  .stat-label {
    font-size: 12px;
    color: var(--text-secondary);
    font-weight: 500;
  }
  
  .stat-value {
    font-size: 20px;
    font-weight: 700;
  }
  
  .user-management-section {
    margin-bottom: 30px;
  }
  
  .table-card {
    background-color: var(--card-bg);
    border-radius: 30px;
    padding: 20px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transition: background-color 0.3s;
  }
  
  .table-controls {
    display: flex;
    gap: 10px;
  }
  
  .filter-btn,
  .export-btn {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 16px;
    border: 1px solid var(--border-color);
    border-radius: 20px;
    background: var(--background-color);
    font-size: 14px;
    font-weight: 500;
    color: var(--text-secondary);
    cursor: pointer;
    transition: all 0.3s ease;
  }
  
  .filter-btn:hover,
  .export-btn:hover {
    border-color: var(--accent-color);
    color: var(--accent-color);
  }
  
  .filter-btn svg,
  .export-btn svg {
    width: 16px;
    height: 16px;
  }
  
  .table-container {
    overflow-x: auto;
    margin-top: 20px;
  }
  
  .user-table {
    width: 100%;
    border-collapse: collapse;
  }
  
  .user-table th {
    text-align: left;
    padding: 15px 20px;
    font-weight: 600;
    font-size: 14px;
    color: var(--text-secondary);
    border-bottom: 1px solid var(--border-color);
    background: var(--background-color);
  }
  
  .user-table td {
    padding: 15px 20px;
    border-bottom: 1px solid var(--border-color);
    font-size: 14px;
  }
  
  .user-row {
    transition: all 0.3s ease;
  }
  
  .user-row:hover {
    background-color: rgba(150, 75, 0, 0.05);
  }
  
  .user-info {
    display: flex;
    align-items: center;
    gap: 12px;
  }
  
  .user-avatar {
    width: 36px;
    height: 36px;
    border-radius: 8px;
    background-color: var(--accent-color);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-weight: 600;
    font-size: 12px;
  }
  
  .user-details {
    display: flex;
    flex-direction: column;
  }
  
  .user-name {
    font-weight: 600;
    margin-bottom: 2px;
  }
  
  .user-email {
    font-size: 12px;
    color: var(--text-secondary);
  }
  
  .role-badge {
    padding: 4px 12px;
    border-radius: 12px;
    font-size: 12px;
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
  
  .status-indicator-container {
    display: flex;
    align-items: center;
    gap: 8px;
  }
  
  .status-indicator {
    width: 8px;
    height: 8px;
    border-radius: 50%;
  }
  
  .status-indicator.active {
    background: var(--success-color);
  }
  
  .status-indicator.inactive {
    background: #6b7280;
  }
  
  .status-indicator.pending {
    background: var(--pending-color);
  }
  
  .action-buttons {
    display: flex;
    gap: 8px;
  }
  
  .action-btn {
    display: flex;
    align-items: center;
    gap: 4px;
    padding: 6px 12px;
    border: none;
    border-radius: 15px;
    font-size: 12px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
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
    color: white;
    box-shadow: 0 4px 12px rgba(34, 197, 94, 0.3);
  }
  
  .deactivate-btn {
    background: rgba(245, 158, 11, 0.1);
    color: #d97706;
    border: 1px solid rgba(245, 158, 11, 0.2);
  }
  
  .deactivate-btn:hover:not(:disabled) {
    background: #d97706;
    color: white;
    box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);
  }
  
  .delete-btn {
    background: rgba(239, 68, 68, 0.1);
    color: #dc2626;
    border: 1px solid rgba(239, 68, 68, 0.2);
  }
  
  .delete-btn:hover:not(:disabled) {
    background: #dc2626;
    color: white;
    box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
  }
  
  .action-btn svg {
    width: 14px;
    height: 14px;
  }
  
  /* Modal Styles */
  .modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
  }
  
  .modal-content {
    background-color: var(--card-bg);
    border-radius: 20px;
    width: 90%;
    max-width: 500px;
    max-height: 90vh;
    overflow-y: auto;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
  }
  
  .modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px 20px 0 20px;
    margin-bottom: 20px;
  }
  
  .modal-header h2 {
    font-size: 20px;
    font-weight: 700;
    margin: 0;
  }
  
  .close-btn {
    background: none;
    border: none;
    cursor: pointer;
    padding: 8px;
    border-radius: 8px;
    color: var(--text-secondary);
    transition: all 0.3s ease;
  }
  
  .close-btn:hover {
    background-color: var(--background-color);
    color: var(--text-color);
  }
  
  .modal-body {
    padding: 0 20px;
  }
  
  .form-group {
    margin-bottom: 20px;
  }
  
  .form-group label {
    display: block;
    margin-bottom: 8px;
    font-weight: 600;
    font-size: 14px;
  }
  
  .form-group input,
  .form-group select {
    width: 100%;
    padding: 12px 16px;
    border: 1px solid var(--border-color);
    border-radius: 12px;
    font-size: 14px;
    background-color: var(--background-color);
    color: var(--text-color);
    transition: all 0.3s ease;
  }
  
  .form-group input:focus,
  .form-group select:focus {
    outline: none;
    border-color: var(--accent-color);
    box-shadow: 0 0 0 3px rgba(150, 75, 0, 0.1);
  }
  
  .modal-footer {
    display: flex;
    gap: 12px;
    padding: 20px;
    justify-content: flex-end;
  }
  
  .cancel-btn {
    padding: 10px 20px;
    border: 1px solid var(--border-color);
    border-radius: 12px;
    background: var(--background-color);
    color: var(--text-color);
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
  }
  
  .cancel-btn:hover {
    border-color: var(--accent-color);
    color: var(--accent-color);
  }
  
  .submit-btn {
    padding: 10px 20px;
    border: none;
    border-radius: 12px;
    background: var(--accent-color);
    color: white;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
  }
  
  .submit-btn:hover {
    background: var(--accent-hover);
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(150, 75, 0, 0.3);
  }
  
  .mobile-menu-btn {
    display: none;
    position: fixed;
    top: 20px;
    left: 20px;
    z-index: 101;
    background-color: #ffffff;
    color: #333333;
    border: none;
    border-radius: 50%;
    width: 44px;
    height: 44px;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
  }
  
  .mobile-menu-btn:hover {
    transform: scale(1.1);
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
  }
  
  /* Responsive styles */
  @media (max-width: 1024px) {
    .mobile-menu-btn {
      display: flex;
    }
    
    .sidebar {
      transform: translateX(-250px);
      z-index: 1000;
    }
    
    .sidebar.mobile-open {
      transform: translateX(0);
    }
    
    .main-content {
      margin-left: 0;
      width: 100%;
    }
    
    .dashboard-grid {
      grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
      gap: 15px;
    }
    
    .expand-btn {
      display: none !important;
    }
    
    .management-grid {
      grid-template-columns: 1fr;
    }
    
    .quick-actions-grid {
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    }
  }
  
  @media (max-width: 768px) {
    body {
      overflow: auto;
    }
    
    .header {
      padding: 15px;
    }
    
    .main-scroll-content {
      padding: 15px;
    }
    
    .dashboard-grid {
      grid-template-columns: 1fr;
    }
    
    .quick-actions-grid {
      grid-template-columns: 1fr;
    }
    
    .page-title {
      font-size: 24px;
    }
    
    .action-buttons {
      flex-direction: column;
    }
    
    .action-btn {
      justify-content: center;
    }
    
    .modal-content {
      width: 95%;
      margin: 20px;
    }
  }
  
  @media (min-width: 1025px) {
    .mobile-menu-btn {
      display: none;
    }
  }
  
  /* Enhanced tablet and mobile sidebar scrolling */
  @media (max-width: 1024px) {
    .sidebar-content {
      overflow-y: auto;
      overflow-x: hidden;
      /* Completely invisible scrollbar */
      scrollbar-width: none; /* Firefox */
      -ms-overflow-style: none; /* Internet Explorer 10+ */
    }
    
    .sidebar-content::-webkit-scrollbar {
      display: none; /* WebKit browsers */
    }
    
    .nav-section {
      margin-bottom: 10px;
    }
    
    .nav-item {
      padding: 8px 10px;
      margin-bottom: 3px;
      min-height: 40px;
    }
    
    .nav-icon {
      width: 30px;
      height: 30px;
      margin-right: 10px;
    }
    
    .nav-icon svg {
      width: 16px;
      height: 16px;
    }
    
    .nav-text {
      font-size: 13px;
    }
    
    .sidebar-bottom {
      padding: 0 15px 15px 15px;
    }
    
    .user-avatar {
      width: 40px;
      height: 40px;
    }
    
    .user-avatar svg {
      width: 22px;
      height: 22px;
    }
    
    .status {
      font-size: 11px;
      margin-bottom: 10px;
    }
    
    .button-container {
      gap: 8px;
    }
    
    .logout-btn {
      padding: 8px 12px;
      font-size: 12px;
    }
  }
  
  /* Compact mode for smaller heights on tablets */
  @media (max-width: 1024px) and (max-height: 700px) {
    .sidebar-header {
      padding: 15px;
    }
    
    .logo {
      width: 45px;
      height: 45px;
    }
    
    .logo img {
      width: 28px;
      height: 28px;
    }
    
    .nav-item {
      padding: 6px 8px;
      margin-bottom: 2px;
      min-height: 36px;
    }
    
    .nav-icon {
      width: 28px;
      height: 28px;
      margin-right: 8px;
    }
    
    .nav-icon svg {
      width: 15px;
      height: 15px;
    }
    
    .nav-text {
      font-size: 12px;
    }
    
    .user-avatar {
      width: 36px;
      height: 36px;
    }
    
    .user-avatar svg {
      width: 20px;
      height: 20px;
    }
    
    .status {
      font-size: 10px;
      margin-bottom: 8px;
    }
    
    .button-container {
      gap: 6px;
    }
    
    .logout-btn {
      padding: 6px 10px;
      font-size: 11px;
    }
  }
  
  /* Extra compact mode for very small heights on mobile */
  @media (max-width: 768px) and (max-height: 600px) {
    .sidebar-header {
      padding: 12px;
    }
    
    .logo {
      width: 40px;
      height: 40px;
    }
    
    .logo img {
      width: 25px;
      height: 25px;
    }
    
    .nav-item {
      padding: 5px 6px;
      margin-bottom: 1px;
      min-height: 32px;
    }
    
    .nav-icon {
      width: 24px;
      height: 24px;
      margin-right: 6px;
    }
    
    .nav-icon svg {
      width: 13px;
      height: 13px;
    }
    
    .nav-text {
      font-size: 11px;
    }
    
    .sidebar-bottom {
      padding: 0 12px 12px 12px;
    }
    
    .user-avatar {
      width: 32px;
      height: 32px;
    }
    
    .user-avatar svg {
      width: 18px;
      height: 18px;
    }
    
    .status {
      font-size: 9px;
      margin-bottom: 6px;
    }
    
    .status-dot {
      width: 4px;
      height: 4px;
      margin-right: 3px;
    }
    
    .button-container {
      gap: 5px;
    }
    
    .logout-btn {
      padding: 5px 8px;
      font-size: 10px;
    }
  }
  </style>