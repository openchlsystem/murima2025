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
          
          <a href="/calls" class="nav-item active" @click.prevent="navigateTo('/calls')">
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
          <a href="/super-admin-dashboard" class="nav-item" v-if="userRole === 'super-admin'" @click.prevent="navigateTo('/super-admin-dashboard')">
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
            <div class="status-dot" :class="{ 'in-queue': isInQueue }"></div>
            <span>{{ queueStatus }}</span>
          </div>
          
          <div class="button-container">
            <button 
              class="join-queue-btn" 
              :class="{ 'in-queue': isInQueue, 'has-call': currentCall }"
              @click="toggleQueue"
              :disabled="isProcessingQueue"
            >
              {{ queueButtonText }}
            </button>
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
      <div class="calls-container">
        <div class="header">
          <h1 class="page-title">Calls</h1>
          <div class="header-actions">
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
            <button class="new-call-btn" @click="initiateNewCall">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M22 16.92V19C22 20.1046 21.1046 21 20 21C10.6112 21 3 13.3888 3 4C3 2.89543 3.89543 2 5 2H7.08C7.55607 2 7.95823 2.33718 8.02513 2.80754L8.7 7.5C8.76694 7.97036 8.53677 8.42989 8.12 8.67L6.5 9.5C7.84 12.16 11.84 16.16 14.5 17.5L15.33 15.88C15.5701 15.4632 16.0296 15.2331 16.5 15.3L21.1925 16.0249C21.6628 16.0918 22 16.4939 22 16.97V16.92Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              New Call
            </button>
          </div>
        </div>
        
        <div class="view-tabs">
          <div class="view-tab" :class="{ active: activeView === 'timeline' }" @click="activeView = 'timeline'">Timeline</div>
          <div class="view-tab" :class="{ active: activeView === 'table' }" @click="activeView = 'table'">Table View</div>
          <div class="view-tab" :class="{ active: activeView === 'queue' }" @click="activeView = 'queue'">Call Queue</div>
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
        
        <!-- Timeline View -->
        <div class="view-container" v-show="activeView === 'timeline'">
          <div class="time-section" v-for="(group, label) in groupedCalls" :key="label">
            <h2 class="time-section-title">{{ label }}</h2>
            <div class="call-list">
              <div 
                v-for="(call, index) in group" 
                :key="call.id" 
                class="call-item" 
                :class="{ 
                  selected: call.id === selectedCallId,
                  'timeline-connector': index < group.length - 1
                }" 
                @click="selectCall(call.id)"
              >
                <div class="call-icon">
                  <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M22 16.92V19C22 20.1046 21.1046 21 20 21C10.6112 21 3 13.3888 3 4C3 2.89543 3.89543 2 5 2H7.08C7.55607 2 7.95823 2.33718 8.02513 2.80754L8.7 7.5C8.76694 7.97036 8.53677 8.42989 8.12 8.67L6.5 9.5C7.84 12.16 11.84 16.16 14.5 17.5L15.33 15.88C15.5701 15.4632 16.0296 15.2331 16.5 15.3L21.1925 16.0249C21.6628 16.0918 22 16.4939 22 16.97V16.92Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </div>
                <div class="call-details">
                  <div class="call-type">{{ call.title }}</div>
                  <div class="call-time">{{ call.time }}</div>
                  <div class="call-meta">
                    <span class="case-link">Case: #{{ call.caseId }}</span>
                  </div>
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
                  @click="selectCall(call.id)"
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

        <!-- Queue View -->
        <div class="view-container" v-show="activeView === 'queue'">
          <div class="queue-section">
            <h2 class="queue-title">Call Queue Management</h2>
            <div class="queue-stats">
              <div class="queue-stat">
                <div class="stat-value">{{ queueStats.waiting }}</div>
                <div class="stat-label">Waiting</div>
              </div>
              <div class="queue-stat">
                <div class="stat-value">{{ queueStats.active }}</div>
                <div class="stat-label">Active</div>
              </div>
              <div class="queue-stat">
                <div class="stat-value">{{ queueStats.agents }}</div>
                <div class="stat-label">Agents Online</div>
              </div>
            </div>
            
            <div class="queue-calls">
              <h3 class="queue-subtitle">Pending Calls</h3>
              <div class="queue-call-list">
                <div v-for="call in queueCalls" :key="call.id" class="queue-call-item">
                  <div class="queue-call-info">
                    <div class="queue-call-type">{{ call.type }}</div>
                    <div class="queue-call-details">
                      <span>Wait Time: {{ call.waitTime }}</span>
                      <span>Case: #{{ call.caseId }}</span>
                    </div>
                  </div>
                  <div class="queue-call-actions">
                    <button class="queue-action-btn accept" @click="acceptQueueCall(call.id)" v-if="isInQueue">
                      Accept
                    </button>
                  </div>
                </div>
              </div>
            </div>
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
          <div class="detail-label">Call ID</div>
          <div class="detail-value">#{{ selectedCallDetails.id }}</div>
        </div>
        <div class="detail-item">
          <div class="detail-label">Case ID</div>
          <div class="detail-value">
            <a href="#" @click.prevent="viewCase(selectedCallDetails.caseId)" class="case-link">
              #{{ selectedCallDetails.caseId }}
            </a>
          </div>
        </div>
        <div class="detail-item">
          <div class="detail-label">Call Title</div>
          <div class="detail-value">{{ selectedCallDetails.callTitle }}</div>
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
        <div class="detail-item">
          <div class="detail-label">Priority</div>
          <div class="detail-value">
            <span class="priority-badge" :class="selectedCallDetails.priority">{{ selectedCallDetails.priority }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Queue Popup Modal -->
    <div v-if="showQueuePopup" class="modal-overlay" @click="closeQueuePopup">
      <div class="queue-popup" @click.stop>
        <div class="queue-popup-header">
          <h3>Queue Members</h3>
          <button class="modal-close" @click="closeQueuePopup">×</button>
        </div>
        <div class="queue-members">
          <div v-for="member in queueMembers" :key="member.id" class="queue-member-card" @click="confirmJoinQueue">
            <div class="member-avatar">
              <img :src="member.avatar" :alt="member.name" />
              <div class="status-indicator" :class="member.status"></div>
            </div>
            <div class="member-info">
              <div class="member-name">{{ member.name }}</div>
              <div class="member-role">{{ member.role }}</div>
              <div class="member-status">{{ member.statusText }}</div>
            </div>
          </div>
        </div>
        <div class="queue-popup-footer">
          <button class="btn-primary" @click="confirmJoinQueue">Join Queue</button>
        </div>
      </div>
    </div>

    <!-- Ringing Call Interface -->
    <div v-if="showRingingInterface" class="ringing-overlay">
      <div class="ringing-container">
        <div class="ringing-header">
          <div class="call-type-badge" :class="ringingCall.priority">
            {{ ringingCall.type }}
          </div>
        </div>
        
        <div class="caller-info">
          <div class="caller-avatar">
            <svg width="60" height="60" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M20 21V19C20 17.9391 19.5786 16.9217 18.8284 16.1716C18.0783 15.4214 17.0609 15 16 15H8C6.93913 15 5.92172 15.4214 5.17157 16.1716C4.42143 16.9217 4 17.9391 4 19V21" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <circle cx="12" cy="7" r="4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <div class="caller-name">{{ ringingCall.callerName }}</div>
          <div class="caller-number">{{ ringingCall.number || 'Unknown Number' }}</div>
          <div class="call-duration">{{ ringingDuration }}</div>
        </div>

        <div class="ringing-animation">
          <div class="pulse-ring"></div>
          <div class="pulse-ring delay-1"></div>
          <div class="pulse-ring delay-2"></div>
        </div>

        <div class="call-actions">
          <button class="call-btn decline" @click="declineCall">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M22 16.92V19C22 20.1046 21.1046 21 20 21C10.6112 21 3 13.3888 3 4C3 2.89543 3.89543 2 5 2H7.08C7.55607 2 7.95823 2.33718 8.02513 2.80754L8.7 7.5C8.76694 7.97036 8.53677 8.42989 8.12 8.67L6.5 9.5C7.84 12.16 11.84 16.16 14.5 17.5L15.33 15.88C15.5701 15.4632 16.0296 15.2331 16.5 15.3L21.1925 16.0249C21.6628 16.0918 22 16.4939 22 16.97V16.92Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
          <button class="call-btn answer" @click="answerCall">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M22 16.92V19C22 20.1046 21.1046 21 20 21C10.6112 21 3 13.3888 3 4C3 2.89543 3.89543 2 5 2H7.08C7.55607 2 7.95823 2.33718 8.02513 2.80754L8.7 7.5C8.76694 7.97036 8.53677 8.42989 8.12 8.67L6.5 9.5C7.84 12.16 11.84 16.16 14.5 17.5L15.33 15.88C15.5701 15.4632 16.0296 15.2331 16.5 15.3L21.1925 16.0249C21.6628 16.0918 22 16.4939 22 16.97V16.92Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Case Form During Call -->
    <div v-if="showCaseForm" class="case-form-overlay">
      <div class="case-form-container">
        <div class="case-form-header">
          <div class="form-title">
            <h3>Case Information</h3>
            <div class="case-id">Case #{{ currentCaseId }}</div>
          </div>
          <div class="call-timer">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
              <polyline points="12,6 12,12 16,14" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            {{ callDuration }}
          </div>
          <button class="minimize-btn" @click="minimizeCaseForm">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M6 9L12 15L18 9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
        </div>

        <div class="case-form-content">
          <form @submit.prevent="saveCaseForm">
            <div class="form-section">
              <div class="section-title">Basic Information</div>
              <div class="form-group">
                <label for="case-name">Case Name*</label>
                <input 
                  v-model="caseFormData.caseName"
                  class="form-control" 
                  id="case-name" 
                  placeholder="Enter case name" 
                  required 
                  type="text"
                />
              </div>
              <div class="form-group">
                <label for="case-description">Description*</label>
                <textarea 
                  v-model="caseFormData.description"
                  class="form-control" 
                  id="case-description" 
                  placeholder="Enter case description" 
                  required
                  rows="3"
                ></textarea>
              </div>
              <div class="form-row">
                <div class="form-group">
                  <label for="case-priority">Priority*</label>
                  <select 
                    v-model="caseFormData.priority"
                    class="form-control" 
                    id="case-priority" 
                    required
                  >
                    <option value="">Select priority</option>
                    <option value="Critical">Critical</option>
                    <option value="High">High</option>
                    <option value="Medium">Medium</option>
                    <option value="Low">Low</option>
                  </select>
                </div>
                <div class="form-group">
                  <label for="case-type">Type*</label>
                  <select 
                    v-model="caseFormData.type"
                    class="form-control" 
                    id="case-type" 
                    required
                  >
                    <option value="">Select type</option>
                    <option value="Domestic Violence">Domestic Violence</option>
                    <option value="Sexual Assault">Sexual Assault</option>
                    <option value="Human Trafficking">Human Trafficking</option>
                    <option value="Child Abuse">Child Abuse</option>
                    <option value="Elder Abuse">Elder Abuse</option>
                    <option value="Stalking">Stalking</option>
                  </select>
                </div>
              </div>
              <div class="form-group">
                <label for="caller-info">Caller Information</label>
                <textarea 
                  v-model="caseFormData.callerInfo"
                  class="form-control" 
                  id="caller-info" 
                  placeholder="Enter caller information and notes"
                  rows="3"
                ></textarea>
              </div>
              <div class="form-group">
                <label for="incident-details">Incident Details</label>
                <textarea 
                  v-model="caseFormData.incidentDetails"
                  class="form-control" 
                  id="incident-details" 
                  placeholder="Enter incident details"
                  rows="4"
                ></textarea>
              </div>
            </div>
            
            <div class="form-actions">
              <button type="button" class="btn-secondary" @click="saveDraft">Save Draft</button>
              <button type="submit" class="btn-primary">Save Case</button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Minimized Case Form -->
    <div v-if="caseFormMinimized" class="minimized-case-form" @click="restoreCaseForm">
      <div class="minimized-content">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M14 2H6C5.46957 2 4.96086 2.21071 4.58579 2.58579C4.21071 2.96086 4 3.46957 4 4V20C4 20.5304 4.21071 21.0391 4.58579 21.4142C4.96086 21.7893 5.46957 22 6 22H18C18.5304 22 19.0391 21.7893 19.4142 21.4142C19.7893 21.0391 20 20.5304 20 20V8L14 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <span>Case #{{ currentCaseId }}</span>
        <span class="timer">{{ callDuration }}</span>
      </div>
    </div>

    <!-- Call Disposition Modal -->
    <div v-if="showDisposition" class="modal-overlay" @click="closeDisposition">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>Call Disposition</h3>
          <button class="modal-close" @click="closeDisposition">×</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="submitDisposition">
            <div class="form-group">
              <label>Call Outcome</label>
              <select v-model="disposition.outcome" required>
                <option value="">Select Outcome</option>
                <option value="resolved">Resolved</option>
                <option value="escalated">Escalated</option>
                <option value="follow-up">Follow-up Required</option>
                <option value="referred">Referred</option>
                <option value="incomplete">Incomplete</option>
              </select>
            </div>
            <div class="form-group">
              <label>Category</label>
              <select v-model="disposition.category" required>
                <option value="">Select Category</option>
                <option value="domestic-violence">Domestic Violence</option>
                <option value="mental-health">Mental Health</option>
                <option value="substance-abuse">Substance Abuse</option>
                <option value="child-abuse">Child Abuse</option>
                <option value="elder-abuse">Elder Abuse</option>
                <option value="information">Information Request</option>
              </select>
            </div>
            <div class="form-group">
              <label>Priority</label>
              <select v-model="disposition.priority" required>
                <option value="">Select Priority</option>
                <option value="critical">Critical</option>
                <option value="high">High</option>
                <option value="medium">Medium</option>
                <option value="low">Low</option>
              </select>
            </div>
            <div class="form-group">
              <label>Notes</label>
              <textarea v-model="disposition.notes" rows="4" placeholder="Enter call notes..."></textarea>
            </div>
            <div class="form-actions">
              <button type="button" class="btn-secondary" @click="closeDisposition">Cancel</button>
              <button type="submit" class="btn-primary">Save Disposition</button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Case Link Modal -->
    <div v-if="showCaseLink" class="modal-overlay" @click="closeCaseLink">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>Link Call to Different Case</h3>
          <button class="modal-close" @click="closeCaseLink">×</button>
        </div>
        <div class="modal-body">
          <div class="case-link-options">
            <div class="case-option" @click="selectCaseLinkOption('existing')">
              <div class="option-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M10 13C10.4295 13.5741 10.9774 14.0491 11.6066 14.3929C12.2357 14.7367 12.9315 14.9411 13.6467 14.9923C14.3618 15.0435 15.0796 14.9403 15.7513 14.6897C16.4231 14.4392 17.0331 14.047 17.54 13.54L20.54 10.54C21.4508 9.59695 21.9548 8.33394 21.9434 7.02296C21.932 5.71198 21.4061 4.45791 20.4791 3.53087C19.5521 2.60383 18.298 2.07799 16.987 2.0666C15.676 2.0552 14.413 2.55918 13.47 3.47L11.75 5.18" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M14 11C13.5705 10.4259 13.0226 9.95085 12.3934 9.60706C11.7643 9.26327 11.0685 9.05885 10.3533 9.00769C9.63819 8.95653 8.92037 9.05973 8.24864 9.31028C7.5769 9.56084 6.9669 9.95303 6.46 10.46L3.46 13.46C2.54918 14.403 2.04520 15.6661 2.0566 16.9771C2.06799 18.288 2.59383 19.5421 3.52087 20.4691C4.44791 21.3962 5.70198 21.922 7.01296 21.9334C8.32394 21.9448 9.58695 21.4408 10.53 20.53L12.24 18.82" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </div>
              <div class="option-content">
                <div class="option-title">Link to Existing Case</div>
                <div class="option-description">Connect this call to a different existing case</div>
              </div>
            </div>
            <div class="case-option" @click="selectCaseLinkOption('new')">
              <div class="option-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M12 5V19M5 12H19" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </div>
              <div class="option-content">
                <div class="option-title">Create New Case</div>
                <div class="option-description">Create a new case and link this call to it</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

// Reactive state
const isSidebarCollapsed = ref(false)
const mobileOpen = ref(false)
const activeView = ref('timeline')
const selectedCallId = ref('1348456')
const currentTheme = ref('dark')
const selectedTimeRange = ref('all')
const showCallDetails = ref(true)
const userRole = ref('super-admin')

// Queue management state
const isInQueue = ref(false)
const isProcessingQueue = ref(false)
const currentCall = ref(null)
const callStartTime = ref(null)
const callDuration = ref('00:00')

// New modal states
const showQueuePopup = ref(false)
const showRingingInterface = ref(false)
const showCaseForm = ref(false)
const caseFormMinimized = ref(false)

// Modal states
const showDisposition = ref(false)
const showCaseLink = ref(false)
const selectedCallForLink = ref(null)

// Ringing call state
const ringingCall = ref(null)
const ringingDuration = ref('00:00')
const ringingStartTime = ref(null)

// Case form data
const currentCaseId = ref('')
const caseFormData = ref({
  caseName: '',
  description: '',
  priority: '',
  type: '',
  callerInfo: '',
  incidentDetails: ''
})

// Disposition form
const disposition = ref({
  outcome: '',
  category: '',
  priority: '',
  notes: ''
})

// Queue members data
const queueMembers = ref([
  {
    id: 1,
    name: 'Sarah Davis',
    role: 'Senior Crisis Counselor',
    status: 'available',
    statusText: 'Available',
    avatar: '/placeholder.svg?height=40&width=40'
  },
  {
    id: 2,
    name: 'Mark Reynolds',
    role: 'Crisis Counselor',
    status: 'busy',
    statusText: 'On Call',
    avatar: '/placeholder.svg?height=40&width=40'
  },
  {
    id: 3,
    name: 'Emily Chan',
    role: 'Mental Health Specialist',
    status: 'available',
    statusText: 'Available',
    avatar: '/placeholder.svg?height=40&width=40'
  },
  {
    id: 4,
    name: 'David Lee',
    role: 'Legal Advocate',
    status: 'away',
    statusText: 'Break',
    avatar: '/placeholder.svg?height=40&width=40'
  },
  {
    id: 5,
    name: 'Sophia Clark',
    role: 'Housing Specialist',
    status: 'available',
    statusText: 'Available',
    avatar: '/placeholder.svg?height=40&width=40'
  },
  {
    id: 6,
    name: 'Dr. Lisa Chen',
    role: 'Supervisor',
    status: 'busy',
    statusText: 'In Meeting',
    avatar: '/placeholder.svg?height=40&width=40'
  }
])

// Queue stats
const queueStats = ref({
  waiting: 3,
  active: 12,
  agents: 8
})

// Queue calls with auto-generated case IDs
const queueCalls = ref([
  {
    id: 'queue_001',
    type: 'Emergency Crisis: Domestic Violence',
    waitTime: '2m 15s',
    priority: 'critical',
    callerName: 'Anonymous',
    caseId: generateCaseId()
  },
  {
    id: 'queue_002',
    type: 'Mental Health Support',
    waitTime: '5m 30s',
    priority: 'high',
    callerName: 'Sarah M.',
    caseId: generateCaseId()
  },
  {
    id: 'queue_003',
    type: 'Information Request',
    waitTime: '1m 45s',
    priority: 'medium',
    callerName: 'John D.',
    caseId: generateCaseId()
  }
])

// Helper function to generate case IDs
function generateCaseId() {
  const year = new Date().getFullYear()
  const randomNum = Math.floor(Math.random() * 9000) + 1000
  return `CASE-${year}-${randomNum}`
}

// Call data with auto-generated case IDs
const callData = ref({
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
    group: 'Today',
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
    callTitle: 'Follow-up call',
    callerName: 'Maria Johnson',
    duration: '15min 20 sec',
    callStart: '10:30 am',
    callEnd: '10:45 am',
    disposition: 'Completed',
    date: '15th Aug 2025',
    escalatedTo: 'David Lee',
    group: 'Today',
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
    callTitle: 'Therapy Session',
    callerName: 'James Wilson',
    duration: '45min 10 sec',
    callStart: '02:00 pm',
    callEnd: '02:45 pm',
    disposition: 'Completed',
    date: '15th Aug 2025',
    escalatedTo: 'Dr. Lisa Chen',
    group: 'Today',
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
    callTitle: 'Shelter Information',
    callerName: 'Anonymous',
    duration: '8min 30 sec',
    callStart: '04:45 pm',
    callEnd: '04:53 pm',
    disposition: 'Information Provided',
    date: '15th Aug 2025',
    escalatedTo: 'Unassigned',
    group: 'Today',
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
    callTitle: 'Mental Health Support',
    callerName: 'Rebecca Taylor',
    duration: '22min 15 sec',
    callStart: '11:15 am',
    callEnd: '11:37 am',
    disposition: 'Completed',
    date: '14th Aug 2025',
    escalatedTo: 'Dr. Michael Brown',
    group: 'Yesterday',
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
    callTitle: 'Legal Advocacy',
    callerName: 'Thomas Garcia',
    duration: '12min 40 sec',
    callStart: '01:30 pm',
    callEnd: '01:42 pm',
    disposition: 'Appointment Scheduled',
    date: '14th Aug 2025',
    escalatedTo: 'Legal Team',
    group: 'Yesterday',
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
    callTitle: 'Housing Assistance',
    callerName: 'Jennifer Lopez',
    duration: '18min 22 sec',
    callStart: '05:00 pm',
    callEnd: '05:18 pm',
    disposition: 'Completed',
    date: '14th Aug 2025',
    escalatedTo: 'Housing Department',
    group: 'Yesterday',
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
  return callData.value[selectedCallId.value] || null
})

const queueStatus = computed(() => {
  if (currentCall.value) {
    return currentCall.value.status === 'incoming' ? 'Incoming Call' : 'On Call'
  }
  return isInQueue.value ? 'In Queue' : 'Offline'
})

const queueButtonText = computed(() => {
  if (isProcessingQueue.value) return 'Processing...'
  if (currentCall.value) return 'End Call'
  return isInQueue.value ? 'Leave Queue' : 'Join Queue'
})

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
  alert(`Navigation to ${path} - In a real app, this would navigate to the page`)
}

const toggleQueue = async () => {
  if (currentCall.value) {
    endCall()
    return
  }

  isProcessingQueue.value = true
  
  try {
    if (isInQueue.value) {
      // Leave queue
      isInQueue.value = false
      console.log('Left queue')
    } else {
      // Join queue - show queue popup first
      showQueuePopup.value = true
    }
  } finally {
    isProcessingQueue.value = false
  }
}

const closeQueuePopup = () => {
  showQueuePopup.value = false
}

const confirmJoinQueue = () => {
  isInQueue.value = true
  showQueuePopup.value = false
  console.log('Joined queue')
  
  // Simulate receiving a call after joining queue
  setTimeout(() => {
    if (isInQueue.value) {
      simulateIncomingCall()
    }
  }, 3000)
}

const initiateNewCall = () => {
  // Show ringing interface for outgoing call
  const outgoingCall = {
    id: `CALL-OUT-${Date.now()}`,
    type: 'Outgoing Call',
    callerName: 'Outgoing Call',
    number: '+1 (555) 123-4567',
    status: 'outgoing',
    priority: 'medium',
    caseId: generateCaseId()
  }
  
  ringingCall.value = outgoingCall
  showRingingInterface.value = true
  ringingStartTime.value = new Date()
  startRingingTimer()
}

const simulateIncomingCall = () => {
  const caseId = generateCaseId()
  const incomingCall = {
    id: `CALL-${Date.now()}`,
    type: 'Emergency Crisis: Domestic Violence',
    callerName: 'Anonymous Caller',
    number: '+1 (555) 987-6543',
    status: 'incoming',
    priority: 'critical',
    caseId: caseId
  }
  
  ringingCall.value = incomingCall
  showRingingInterface.value = true
  ringingStartTime.value = new Date()
  startRingingTimer()
}

const startRingingTimer = () => {
  const timer = setInterval(() => {
    if (!ringingStartTime.value || !showRingingInterface.value) {
      clearInterval(timer)
      return
    }
    
    const now = new Date()
    const diff = now - ringingStartTime.value
    const minutes = Math.floor(diff / 60000)
    const seconds = Math.floor((diff % 60000) / 1000)
    ringingDuration.value = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`
  }, 1000)
}

const answerCall = () => {
  if (ringingCall.value) {
    currentCall.value = {
      ...ringingCall.value,
      status: 'active'
    }
    
    callStartTime.value = new Date()
    currentCaseId.value = ringingCall.value.caseId
    
    // Initialize case form data
    caseFormData.value = {
      caseName: ringingCall.value.type,
      description: '',
      priority: ringingCall.value.priority,
      type: '',
      callerInfo: `Caller: ${ringingCall.value.callerName}\nNumber: ${ringingCall.value.number || 'Unknown'}`,
      incidentDetails: ''
    }
    
    showRingingInterface.value = false
    showCaseForm.value = true
    startCallTimer()
    
    // Add call to call data
    const newCallId = currentCall.value.id
    callData.value[newCallId] = {
      id: newCallId,
      title: currentCall.value.type,
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      dateLabel: 'Today',
      status: 'In Progress',
      agent: 'Current User',
      callTitle: currentCall.value.type,
      callerName: currentCall.value.callerName,
      duration: '0min 0 sec',
      callStart: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      callEnd: '',
      disposition: '',
      date: new Date().toLocaleDateString(),
      escalatedTo: '',
      group: 'Today',
      caseId: currentCall.value.caseId,
      priority: currentCall.value.priority
    }
  }
  
  ringingCall.value = null
  ringingStartTime.value = null
  ringingDuration.value = '00:00'
}

const declineCall = () => {
  showRingingInterface.value = false
  ringingCall.value = null
  ringingStartTime.value = null
  ringingDuration.value = '00:00'
}

const endCall = () => {
  if (currentCall.value) {
    const callId = currentCall.value.id
    
    // Update call data
    if (callData.value[callId]) {
      callData.value[callId].status = 'Completed'
      callData.value[callId].callEnd = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      callData.value[callId].duration = callDuration.value
    }
    
    currentCall.value = null
    callStartTime.value = null
    callDuration.value = '00:00'
    showCaseForm.value = false
    caseFormMinimized.value = false
    
    // Open disposition modal
    showDisposition.value = true
  }
}

const startCallTimer = () => {
  const timer = setInterval(() => {
    if (!callStartTime.value || !currentCall.value) {
      clearInterval(timer)
      return
    }
    
    const now = new Date()
    const diff = now - callStartTime.value
    const minutes = Math.floor(diff / 60000)
    const seconds = Math.floor((diff % 60000) / 1000)
    callDuration.value = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`
  }, 1000)
}

const minimizeCaseForm = () => {
  showCaseForm.value = false
  caseFormMinimized.value = true
}

const restoreCaseForm = () => {
  caseFormMinimized.value = false
  showCaseForm.value = true
}

const saveCaseForm = () => {
  console.log('Saving case form:', caseFormData.value)
  alert('Case saved successfully!')
}

const saveDraft = () => {
  console.log('Saving draft:', caseFormData.value)
  alert('Draft saved successfully!')
}

const acceptQueueCall = (callId) => {
  const queueCall = queueCalls.value.find(call => call.id === callId)
  if (queueCall && isInQueue.value) {
    ringingCall.value = {
      id: `CALL-${Date.now()}`,
      type: queueCall.type,
      callerName: queueCall.callerName,
      number: '+1 (555) 123-4567',
      status: 'incoming',
      priority: queueCall.priority,
      caseId: queueCall.caseId
    }
    
    showRingingInterface.value = true
    ringingStartTime.value = new Date()
    startRingingTimer()
    
    // Remove from queue
    queueCalls.value = queueCalls.value.filter(call => call.id !== callId)
    queueStats.value.waiting--
  }
}

const openDisposition = () => {
  showDisposition.value = true
}

const closeDisposition = () => {
  showDisposition.value = false
  disposition.value = {
    outcome: '',
    category: '',
    priority: '',
    notes: ''
  }
}

const submitDisposition = () => {
  console.log('Submitting disposition:', disposition.value)
  
  // Update the call's case with disposition information
  if (currentCall.value && callData.value[currentCall.value.id]) {
    callData.value[currentCall.value.id].disposition = disposition.value.outcome
    callData.value[currentCall.value.id].priority = disposition.value.priority
  }
  
  closeDisposition()
  alert('Call disposition saved successfully!')
}

const viewCallDetails = (callId) => {
  selectedCallId.value = callId
  showCallDetails.value = true
}

const linkToCase = (callId) => {
  selectedCallForLink.value = callId
  showCaseLink.value = true
}

const closeCaseLink = () => {
  showCaseLink.value = false
  selectedCallForLink.value = null
}

const selectCaseLinkOption = (option) => {
  if (option === 'existing') {
    // In a real app, this would open a case search modal
    const caseId = prompt('Enter existing case ID:')
    if (caseId && selectedCallForLink.value) {
      callData.value[selectedCallForLink.value].caseId = caseId
      alert(`Call linked to case ${caseId}`)
    }
  } else if (option === 'new') {
    // Create new case
    const caseTitle = prompt('Enter case title:')
    if (caseTitle && selectedCallForLink.value) {
      const caseId = generateCaseId()
      callData.value[selectedCallForLink.value].caseId = caseId
      alert(`New case ${caseId} created and linked to call`)
    }
  }
  closeCaseLink()
}

const viewCase = (caseId) => {
  console.log('Viewing case:', caseId)
  alert(`Opening case ${caseId} - In a real app, this would navigate to the case details page`)
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
    root.style.setProperty('--header-bg', '#f0f0f0')
    root.style.setProperty('--input-bg', '#ffffff')
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
    root.style.setProperty('--header-bg', '#333')
    root.style.setProperty('--input-bg', '#333')
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

const selectCall = (callId) => {
  selectedCallId.value = callId
  showCallDetails.value = true
}

const closeCallDetails = () => {
  showCallDetails.value = false
}

const getStatusClass = (status) => {
  return status.toLowerCase().replace(/\s+/g, '-')
}

const logout = () => {
  console.log('Logging out...')
  alert('Logged out successfully!')
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

onUnmounted(() => {
  // Clean up any timers
  if (callStartTime.value) {
    callStartTime.value = null
  }
  if (ringingStartTime.value) {
    ringingStartTime.value = null
  }
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

.sidebar-content {
  width: 250px;
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.sidebar-header {
  flex-shrink: 0;
  padding: 20px;
  text-align: center;
}

.nav-section {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  padding: 0 15px;
  margin-bottom: 0;
  min-height: 0;
  scrollbar-width: none;
  -ms-overflow-style: none;
}

.nav-section::-webkit-scrollbar {
  display: none;
}

.sidebar-bottom {
  padding: 15px;
  flex-shrink: 0;
  background-color: var(--sidebar-bg);
  border-top: 1px solid rgba(255, 255, 255, 0.1);
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

.sidebar.collapsed {
  width: 20px;
  transform: translateX(-230px);
}

.sidebar.collapsed .sidebar-content {
  opacity: 0;
  pointer-events: none;
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
  background-color: var(--unassigned-color);
  margin-right: 6px;
  transition: all 0.3s ease;
}

.status-dot.in-queue {
  background-color: var(--success-color);
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% { opacity: 1; }
  50% { opacity: 0.5; }
  100% { opacity: 1; }
}

.button-container {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.join-queue-btn {
  background-color: var(--accent-color);
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

.join-queue-btn:hover {
  background-color: var(--accent-hover);
  transform: translateY(-1px);
}

.join-queue-btn.in-queue {
  background-color: var(--success-color);
}

.join-queue-btn.has-call {
  background-color: var(--danger-color);
}

.join-queue-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
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
  transition: margin-left 0.3s ease, background-color 0.3s;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.sidebar.collapsed ~ .main-content {
  margin-left: 20px;
}

.calls-container {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  overflow-x: hidden;
  scrollbar-width: none;
  -ms-overflow-style: none;
}

.calls-container::-webkit-scrollbar {
  display: none;
}

.header {
  margin-bottom: 25px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-shrink: 0;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 15px;
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

.new-call-btn {
  background-color: var(--success-color);
  color: white;
  border: none;
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

.new-call-btn:hover {
  background-color: #45a049;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.new-call-btn svg {
  width: 16px;
  height: 16px;
}

.view-tabs {
  display: flex;
  border-bottom: 1px solid var(--border-color);
  margin-bottom: 25px;
  overflow-x: auto;
  white-space: nowrap;
  flex-shrink: 0;
}

.view-tab {
  padding: 12px 24px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  color: var(--text-secondary);
  position: relative;
  transition: all 0.3s ease;
}

.view-tab:hover {
  color: var(--text-color);
}

.view-tab.active {
  color: var(--text-color);
  font-weight: 700;
}

.view-tab.active::after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 0;
  width: 100%;
  height: 2px;
  background-color: var(--accent-color);
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
  scrollbar-width: none;
  -ms-overflow-style: none;
}

.view-container::-webkit-scrollbar {
  display: none;
}

.time-section {
  margin-bottom: 35px;
}

.time-section-title {
  font-size: 18px;
  font-weight: 700;
  margin-bottom: 20px;
  color: var(--text-color);
}

.call-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.call-item {
  display: flex;
  align-items: flex-start;
  cursor: pointer;
  padding: 15px;
  border-radius: 15px;
  transition: all 0.3s ease;
  position: relative;
}

.call-item:hover {
  background-color: rgba(255, 255, 255, 0.05);
  transform: translateX(5px);
}

.call-item.selected {
  background-color: rgba(255, 59, 48, 0.1);
  border: 1px solid var(--highlight-color);
}

.call-item.selected .call-type {
  color: var(--highlight-color);
  font-weight: 700;
}

.timeline-connector::after {
  content: '';
  position: absolute;
  top: 45px;
  left: 30px;
  width: 1px;
  height: calc(100% + 12px);
  background-color: var(--border-color);
  z-index: 1;
}

.call-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: var(--content-bg);
  display: flex;
  justify-content: center;
  align-items: center;
  margin-right: 15px;
  margin-top: 2px;
  flex-shrink: 0;
  position: relative;
  z-index: 2;
  border: 2px solid var(--background-color);
}

.call-icon svg {
  width: 18px;
  height: 18px;
  stroke: var(--text-color);
}

.call-details {
  flex: 1;
}

.call-type {
  font-size: 15px;
  font-weight: 600;
  margin-bottom: 6px;
  line-height: 1.4;
}

.call-time {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-secondary);
  margin-bottom: 4px;
}

.call-meta {
  display: flex;
  gap: 12px;
  align-items: center;
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

.call-id {
  font-size: 14px;
  font-weight: 700;
  color: var(--text-color);
}

.priority-badge {
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  padding: 4px 8px;
  border-radius: 8px;
  color: white;
}

.priority-badge.critical {
  background-color: var(--critical-color);
}

.priority-badge.high {
  background-color: var(--high-color);
}

.priority-badge.medium {
  background-color: var(--medium-color);
}

.priority-badge.low {
  background-color: var(--low-color);
}

/* Queue Section */
.queue-section {
  padding: 20px;
  background-color: var(--card-bg);
  border-radius: 20px;
  margin-bottom: 20px;
}

.queue-title {
  font-size: 20px;
  font-weight: 700;
  margin-bottom: 20px;
}

.queue-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 15px;
  margin-bottom: 30px;
}

.queue-stat {
  text-align: center;
  padding: 15px;
  background-color: var(--background-color);
  border-radius: 12px;
}

.stat-value {
  font-size: 24px;
  font-weight: 800;
  color: var(--accent-color);
  margin-bottom: 5px;
}

.stat-label {
  font-size: 12px;
  font-weight: 600;
  color: var(--text-secondary);
  text-transform: uppercase;
}

.queue-subtitle {
  font-size: 16px;
  font-weight: 700;
  margin-bottom: 15px;
}

.queue-call-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.queue-call-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  background-color: var(--background-color);
  border-radius: 12px;
  transition: all 0.3s ease;
}

.queue-call-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.queue-call-info {
  flex: 1;
}

.queue-call-type {
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 5px;
}

.queue-call-details {
  display: flex;
  gap: 15px;
  font-size: 12px;
  font-weight: 600;
  color: var(--text-secondary);
}

.queue-call-actions {
  display: flex;
  gap: 8px;
}

.queue-action-btn {
  background-color: var(--success-color);
  color: white;
  border: none;
  border-radius: 8px;
  padding: 6px 12px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.queue-action-btn:hover {
  background-color: #45a049;
  transform: translateY(-1px);
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
  background-color: var(--header-bg);
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
  background-color: rgba(255, 255, 255, 0.05);
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
  overflow-x: hidden;
  display: flex;
  flex-direction: column;
  scrollbar-width: none;
  -ms-overflow-style: none;
}

.call-details-panel::-webkit-scrollbar {
  display: none;
}

.call-details-panel.active {
  transform: translateX(0);
}

.call-details-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 25px;
  border-bottom: 1px solid var(--border-color);
  background-color: var(--content-bg);
  flex-shrink: 0;
}

.call-details-title {
  font-size: 18px;
  font-weight: 700;
  color: var(--highlight-color);
  line-height: 1.4;
}

.close-details {
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

.close-details:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.call-details-content {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  padding: 25px;
  display: flex;
  flex-direction: column;
  gap: 18px;
  scrollbar-width: none;
  -ms-overflow-style: none;
}

.call-details-content::-webkit-scrollbar {
  display: none;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
  background-color: var(--background-color);
  padding: 18px;
  border-radius: 15px;
  transition: all 0.3s ease;
}

.detail-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.detail-label {
  font-size: 12px;
  font-weight: 700;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.detail-value {
  font-size: 15px;
  font-weight: 600;
  color: var(--text-color);
  line-height: 1.4;
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

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  background-color: var(--input-bg);
  color: var(--text-color);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 12px 16px;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: var(--accent-color);
}

.form-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  margin-top: 25px;
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

/* Queue Popup Modal */
.queue-popup {
  background-color: var(--content-bg);
  border-radius: 20px;
  width: 90%;
  max-width: 600px;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  animation: slideUp 0.3s ease-out;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.queue-popup-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 25px;
  border-bottom: 1px solid var(--border-color);
}

.queue-popup-header h3 {
  font-size: 18px;
  font-weight: 700;
  color: var(--text-color);
}

.queue-members {
  padding: 25px;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 15px;
}

.queue-member-card {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 15px;
  background-color: var(--background-color);
  border-radius: 15px;
  transition: all 0.3s ease;
  cursor: pointer;
}

.queue-member-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.member-avatar {
  position: relative;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  overflow: hidden;
  flex-shrink: 0;
}

.member-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.status-indicator {
  position: absolute;
  bottom: 2px;
  right: 2px;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  border: 2px solid var(--content-bg);
}

.status-indicator.available {
  background-color: var(--success-color);
}

.status-indicator.busy {
  background-color: var(--danger-color);
}

.status-indicator.away {
  background-color: var(--pending-color);
}

.member-info {
  flex: 1;
}

.member-name {
  font-size: 14px;
  font-weight: 700;
  color: var(--text-color);
  margin-bottom: 2px;
}

.member-role {
  font-size: 12px;
  font-weight: 600;
  color: var(--text-secondary);
  margin-bottom: 2px;
}

.member-status {
  font-size: 11px;
  font-weight: 600;
  color: var(--accent-color);
}

.queue-popup-footer {
  padding: 20px 25px;
  border-top: 1px solid var(--border-color);
  display: flex;
  justify-content: center;
}

/* Ringing Interface - iOS Style */
.ringing-overlay {
  position: fixed;
  top: 50%;
  right: 2%;
  transform: translateY(-50%);
  width: 25%;
  height: auto;
  padding: 2rem 1rem;
  background: linear-gradient(135deg, #ff8c00, #000000); /* dark orange to black */
  border-radius: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 3000;
  animation: fadeIn 0.3s ease-out;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
  color: white;
}


@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.ringing-container {
  text-align: center;
  color: white;
  max-width: 400px;
  padding: 40px 20px;
}

.ringing-header {
  margin-bottom: 30px;
}

.call-type-badge {
  display: inline-block;
  padding: 8px 16px;
  background-color: rgba(255, 255, 255, 0.2);
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  backdrop-filter: blur(10px);
}

.call-type-badge.critical {
  background-color: rgba(255, 59, 48, 0.3);
}

.call-type-badge.high {
  background-color: rgba(255, 149, 0, 0.3);
}

.call-type-badge.medium {
  background-color: rgba(0, 122, 255, 0.3);
}

.caller-info {
  margin-bottom: 40px;
}

.caller-avatar {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
  backdrop-filter: blur(10px);
  border: 3px solid rgba(255, 255, 255, 0.3);
}

.caller-avatar svg {
  width: 60px;
  height: 60px;
  stroke: white;
}

.caller-name {
  font-size: 24px;
  font-weight: 700;
  margin-bottom: 8px;
}

.caller-number {
  font-size: 16px;
  font-weight: 500;
  opacity: 0.8;
  margin-bottom: 12px;
}

.call-duration {
  font-size: 18px;
  font-weight: 600;
  font-family: 'SF Mono', 'Monaco', 'Inconsolata', 'Roboto Mono', monospace;
}

.ringing-animation {
  position: relative;
  margin-bottom: 50px;
  height: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.pulse-ring {
  position: absolute;
  width: 80px;
  height: 80px;
  border: 2px solid rgba(255, 255, 255, 0.4);
  border-radius: 50%;
  animation: pulsate 2s ease-out infinite;
}

.pulse-ring.delay-1 {
  animation-delay: 0.5s;
}

.pulse-ring.delay-2 {
  animation-delay: 1s;
}

@keyframes pulsate {
  0% {
    transform: scale(0.8);
    opacity: 1;
  }
  100% {
    transform: scale(2);
    opacity: 0;
  }
}

.call-actions {
  display: flex;
  justify-content: center;
  gap: 60px;
}

.call-btn {
  width: 70px;
  height: 70px;
  border-radius: 50%;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.call-btn.decline {
  background-color: rgba(255, 59, 48, 0.9);
}

.call-btn.answer {
  background-color: rgba(52, 199, 89, 0.9);
}

.call-btn:hover {
  transform: scale(1.1);
}

.call-btn:active {
  transform: scale(0.95);
}

.call-btn svg {
  width: 24px;
  height: 24px;
  stroke: white;
}

/* Case Form During Call */
.case-form-overlay {
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
  padding: 20px;
}

.case-form-container {
  background-color: var(--content-bg);
  border-radius: 20px;
  width: 100%;
  max-width: 800px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  animation: slideUp 0.3s ease-out;
}

.case-form-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 25px;
  border-bottom: 1px solid var(--border-color);
  background-color: var(--content-bg);
  border-radius: 20px 20px 0 0;
}

.form-title {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.form-title h3 {
  font-size: 18px;
  font-weight: 700;
  color: var(--text-color);
  margin: 0;
}

.case-id {
  font-size: 12px;
  font-weight: 600;
  color: var(--accent-color);
  background-color: rgba(150, 75, 0, 0.1);
  padding: 2px 8px;
  border-radius: 8px;
  display: inline-block;
}

.call-timer {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 600;
  color: var(--success-color);
  background-color: rgba(76, 175, 80, 0.1);
  padding: 8px 12px;
  border-radius: 12px;
}

.call-timer svg {
  width: 16px;
  height: 16px;
  stroke: var(--success-color);
}

.minimize-btn {
  background: none;
  border: none;
  color: var(--text-color);
  cursor: pointer;
  font-size: 16px;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.minimize-btn:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.case-form-content {
  padding: 25px;
  overflow-y: auto;
  max-height: calc(90vh - 100px);
}

.form-section {
  margin-bottom: 25px;
}

.section-title {
  font-size: 16px;
  font-weight: 700;
  color: var(--text-color);
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid var(--border-color);
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.form-control {
  width: 100%;
  background-color: var(--input-bg);
  color: var(--text-color);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 12px 16px;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.3s ease;
  resize: vertical;
}

.form-control:focus {
  outline: none;
  border-color: var(--accent-color);
  box-shadow: 0 0 0 3px rgba(150, 75, 0, 0.1);
}

/* Minimized Case Form */
.minimized-case-form {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background-color: var(--content-bg);
  border: 1px solid var(--border-color);
  border-radius: 15px;
  padding: 15px 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  z-index: 1500;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.minimized-case-form:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
}

.minimized-content {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 14px;
  font-weight: 600;
  color: var(--text-color);
}

.minimized-content svg {
  width: 16px;
  height: 16px;
  stroke: var(--accent-color);
}

.timer {
  color: var(--success-color);
  font-family: 'SF Mono', 'Monaco', 'Inconsolata', 'Roboto Mono', monospace;
}

/* Case Link Options */
.case-link-options {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.case-option {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 20px;
  background-color: var(--background-color);
  border-radius: 15px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.case-option:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border-color: var(--accent-color);
}

.option-icon {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background-color: var(--accent-color);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.option-icon svg {
  width: 24px;
  height: 24px;
  stroke: white;
}

.option-content {
  flex: 1;
}

.option-title {
  font-size: 16px;
  font-weight: 700;
  color: var(--text-color);
  margin-bottom: 5px;
}

.option-description {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-secondary);
  line-height: 1.4;
}

/* Mobile Responsiveness */
.mobile-menu-btn {
  display: none;
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
  z-index: 102;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.mobile-menu-btn:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

/* Responsive Design */
@media (max-width: 1024px) {
  .mobile-menu-btn {
    display: flex;
  }
  
  .sidebar {
    transform: translateX(-100%);
    z-index: 200;
  }
  
  .sidebar.mobile-open {
    transform: translateX(0);
  }
  
  .main-content {
    margin-left: 0;
  }
  
  .sidebar.collapsed ~ .main-content {
    margin-left: 0;
  }
  
  .expand-btn {
    display: none !important;
  }
  
  .call-details-panel {
    width: 100%;
    border-radius: 0;
  }
  
  .case-form-container {
    width: 95%;
    max-width: none;
  }
  
  .form-row {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .header {
    flex-direction: column;
    gap: 15px;
    align-items: flex-start;
  }
  
  .header-actions {
    width: 100%;
    justify-content: space-between;
  }
  
  .status-cards {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .queue-stats {
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
  }
  
  .queue-members {
    grid-template-columns: 1fr;
  }
  
  .calls-table-container {
    border-radius: 15px;
  }
  
  .calls-table th:first-child,
  .calls-table th:last-child {
    border-radius: 0;
  }
  
  .calls-table tr:last-child td:first-child,
  .calls-table tr:last-child td:last-child {
    border-radius: 0;
  }
  
  .ringing-container {
    padding: 20px 15px;
  }
  
  .caller-avatar {
    width: 100px;
    height: 100px;
  }
  
  .caller-avatar svg {
    width: 50px;
    height: 50px;
  }
  
  .call-actions {
    gap: 40px;
  }
  
  .call-btn {
    width: 60px;
    height: 60px;
  }
  
  .call-btn svg {
    width: 20px;
    height: 20px;
  }
}

@media (max-width: 480px) {
  .status-cards {
    grid-template-columns: 1fr;
  }
  
  .queue-stats {
    grid-template-columns: 1fr;
  }
  
  .view-tabs {
    font-size: 12px;
  }
  
  .view-tab {
    padding: 10px 16px;
  }
  
  .minimized-case-form {
    bottom: 10px;
    right: 10px;
    padding: 10px 15px;
  }
  
  .minimized-content {
    font-size: 12px;
    gap: 8px;
  }
}
</style>