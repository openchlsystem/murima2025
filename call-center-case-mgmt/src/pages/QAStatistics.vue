<template>
<div class="app-container" :data-theme="currentTheme">
  <!-- Sidebar Component -->
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
              <img src="/placeholder.svg?height=30&width=30" alt="OpenCHS Logo">
            </div>
          </div>
        </div>
        
        <div class="nav-section">
          <div class="nav-item">
            <div class="nav-icon">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M3 9L12 2L21 9V20C21 20.5304 20.7893 21.0391 20.4142 21.4142C20.0391 21.7893 19.5304 22 19 22H5C4.46957 22 3.96086 21.7893 3.58579 21.4142C3.21071 21.0391 3 20.5304 3 20V9Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <polyline points="9,22 9,12 15,12 15,22" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <div class="nav-text">Dashboard</div>
          </div>
          
          <div class="nav-item">
            <div class="nav-icon">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M22 16.92V19C22 20.1046 21.1046 21 20 21C10.6112 21 3 13.3888 3 4C3 2.89543 3.89543 2 5 2H7.08C7.55607 2 7.95823 2.33718 8.02513 2.80754L8.7 7.5C8.76694 7.97036 8.53677 8.42989 8.12 8.67L6.5 9.5C7.84 12.16 11.84 16.16 14.5 17.5L15.33 15.88C15.5701 15.4632 16.0296 15.2331 16.5 15.3L21.1925 16.0249C21.6628 16.0918 22 16.4939 22 16.97V16.92Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <div class="nav-text">Calls</div>
          </div>
          
          <div class="nav-item">
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
          </div>
          
          <div class="nav-item">
            <div class="nav-icon">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M21 15C21 15.5304 20.7893 16.0391 20.4142 16.4142C20.0391 16.7893 19.5304 17 19 17H7L3 21V5C3 4.46957 3.21071 3.96086 3.58579 3.58579C3.96086 3.21071 4.46957 3 5 3H19C19.5304 3 20.0391 3.21071 20.4142 3.58579C20.7893 3.96086 21 4.46957 21 5V15Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M8 9H16" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M8 13H14" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <div class="nav-text">Chats</div>
          </div>
          
          <div class="nav-item active">
            <div class="nav-icon">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <line x1="18" y1="20" x2="18" y2="10" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <line x1="12" y1="20" x2="12" y2="4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <line x1="6" y1="20" x2="6" y2="14" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <div class="nav-text">QA Statistics</div>
          </div>
          
          <div class="nav-item">
            <div class="nav-icon">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <rect x="2" y="3" width="20" height="14" rx="2" ry="2" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <line x1="8" y1="21" x2="16" y2="21" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <line x1="12" y1="17" x2="12" y2="21" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <div class="nav-text">Wallboard</div>
          </div>
          
          <div class="nav-item">
            <div class="nav-icon">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M19.4 15C19.2669 15.3016 19.2272 15.6362 19.286 15.9606C19.3448 16.285 19.4995 16.5843 19.73 16.82L19.79 16.88C19.976 17.0657 20.1235 17.2863 20.2241 17.5291C20.3248 17.7719 20.3766 18.0322 20.3766 18.295C20.3766 18.5578 20.3248 18.8181 20.2241 19.0609C20.1235 19.3037 19.976 19.5243 19.71 19.71C19.6043 19.896 19.3837 20.0435 19.1409 20.1441C18.8981 20.2448 18.6378 20.2966 18.375 20.2966C18.1122 20.2966 17.8519 20.2448 17.6091 20.1441C17.3663 20.0435 17.1457 19.896 16.96 19.71L16.9 19.65C16.6643 19.4195 16.365 19.2648 16.0406 19.206C15.7162 19.1472 15.3816 19.1869 15.08 19.32C14.7842 19.4468 14.532 19.6572 14.3543 19.9255C14.1766 20.1938 14.0813 20.5082 14.08 20.83V21C14.08 21.5304 13.8693 22.0391 13.4942 22.4142C13.1191 22.7893 12.6104 23 12.08 23C11.5496 23 11.0409 22.7893 10.6658 22.4142C10.2907 22.0391 10.08 21.5304 10.08 21V20.91C10.0723 20.579 9.96512 20.2573 9.77251 19.9887C9.5799 19.7201 9.31074 19.5176 9 19.41C8.69838 19.2769 8.36381 19.2372 8.03941 19.296C7.71502 19.3548 7.41568 19.5095 7.18 19.74L7.12 19.8C6.93425 19.986 6.71368 20.1335 6.47088 20.2341C6.22808 20.3348 5.96783 20.3866 5.705 20.3866C5.44217 20.3866 5.18192 20.3348 4.93912 20.2341C4.69632 20.1335 4.47575 19.986 4.29 19.8C4.10405 19.6143 3.95653 19.3937 3.85588 19.1509C3.75523 18.9081 3.70343 18.6478 3.70343 18.385C3.70343 18.1222 3.75523 17.8619 3.85588 17.6191C3.95653 17.3763 4.10405 17.1557 4.29 16.97L4.35 16.91C4.58054 16.6743 4.73519 16.375 4.794 16.0506C4.85282 15.7262 4.81312 15.3916 4.68 15.09C4.55324 14.7942 4.34276 14.542 4.07447 14.3643C3.80618 14.1866 3.49179 14.0913 3.17 14.09H3C2.46957 14.09 1.96086 13.8793 1.58579 13.5042C1.21071 13.1291 1 12.6204 1 12.09C1 11.5596 1.21071 11.0509 1.58579 10.6758C1.96086 10.3007 2.46957 10.09 3 10.09H3.09C3.42099 10.0823 3.742 9.97512 4.01062 9.78251C4.27925 9.5899 4.48167 9.32074 4.59 9.01C4.72312 8.70838 4.76282 8.37381 4.704 8.04941C4.64519 7.72502 4.49054 7.42568 4.26 7.19L4.2 7.13C4.01405 6.94425 3.86653 6.72368 3.76588 6.48088C3.66523 6.23808 3.61343 5.97783 3.61343 5.715C3.61343 5.45217 3.66523 5.19192 3.76588 4.94912C3.86653 4.70632 4.01405 4.48575 4.2 4.3C4.38575 4.11405 4.60632 3.96653 4.84912 3.86588C5.09192 3.76523 5.35217 3.71343 5.615 3.71343C5.87783 3.71343 6.13808 3.76523 6.38088 3.86588C6.62368 3.96653 6.84425 4.11405 7.03 4.3L7.09 4.36C7.32568 4.59054 7.62502 4.74519 7.94941 4.804C8.27381 4.86282 8.60838 4.82312 8.91 4.69H9C9.29577 4.56324 9.54802 4.35276 9.72569 4.08447C9.90337 3.81618 9.99872 3.50179 10 3.18V3C10 2.46957 10.2107 1.96086 10.5858 1.58579C10.9609 1.21071 11.4696 1 12 1C12.5304 1 13.0391 1.21071 13.4142 1.58579C13.7893 1.96086 14 2.46957 14 3V3.09C14.0013 3.41179 14.0966 3.72618 14.2743 3.99447C14.452 4.26276 14.7042 4.47324 15 4.6C15.3016 4.73312 15.6362 4.77282 15.9606 4.714C16.285 4.65519 16.5843 4.50054 16.82 4.27L16.88 4.21C17.0657 4.02405 17.2863 3.87653 17.5291 3.77588C17.7719 3.67523 18.0322 3.62343 18.295 3.62343C18.5578 3.62343 18.8181 3.67523 19.0609 3.77588C19.3037 3.87653 19.5243 4.02405 19.71 4.21C19.896 4.39575 20.0435 4.61632 20.1441 4.85912C20.2448 5.10192 20.2966 5.36217 20.2966 5.625C20.2966 5.88783 20.2448 6.14808 20.1441 6.39088C20.0435 6.63368 19.896 6.85425 19.71 7.04L19.65 7.1C19.4195 7.33568 19.2648 7.63502 19.206 7.95941C19.1472 8.28381 19.1869 8.61838 19.32 8.92V9C19.4468 9.29577 19.6572 9.54802 19.9255 9.72569C20.1938 9.90337 20.5082 9.99872 20.83 10H21C21.5304 10 22.0391 10.2107 22.4142 10.5858C22.7893 10.9609 23 11.4696 23 12C23 12.5304 22.7893 13.0391 22.4142 13.4142C22.0391 13.7893 21.5304 14 21 14H20.91C20.5882 14.0013 20.2738 14.0966 20.0055 14.2743C19.7372 14.452 19.5268 14.7042 19.4 15Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <div class="nav-text">Settings</div>
          </div>
        </div>
        
        <div class="sidebar-bottom">
          <div class="user-profile">
            <div class="user-avatar">
              <svg viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 12C14.2091 12 16 10.2091 16 8C16 5.79086 14.2091 4 12 4C9.79086 4 8 5.79086 8 8C8 10.2091 9.79086 12 12 12Z"/>
                <path d="M12 14C7.58172 14 4 17.5817 4 22H20C20 17.5817 16.4183 14 12 14Z"/>
              </svg>
            </div>
          </div>
          
          <div class="status">
            <div class="status-dot" :class="{ 'in-queue': isInQueue }"></div>
            <span>{{ queueStatus }}</span>
          </div>
          
          <div class="button-container">
            <button 
              class="join-queue-btn" 
              :class="{ 'in-queue': isInQueue, 'has-call': currentCall }"
              @click="handleQueueToggle"
              :disabled="isProcessingQueue"
            >
              {{ queueButtonText }}
            </button>
            <button class="logout-btn" @click="handleLogout">Logout</button>
          </div>
        </div>
      </div>
    </div>

    <button class="expand-btn" @click="expandSidebar" id="expand-btn">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M3 12H21M3 6H21M3 18H21" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </button>
  </div>

  <!-- Main Content -->
  <div class="qa-statistics-container" :class="{ 'sidebar-collapsed': isSidebarCollapsed }">
    <!-- Header Section -->
    <div class="header">
      <div class="page-title">QA Management System</div>
      <div class="header-actions">
        <!-- Removed "Evaluate Calls" button as requested -->
        <button class="theme-toggle" @click="toggleTheme">
          <svg v-if="currentTheme === 'dark'" width="16" height="16" viewBox="0 0 24 24" fill="none">
            <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" stroke="currentColor" stroke-width="2"/>
          </svg>
          <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none">
            <circle cx="12" cy="12" r="5" stroke="currentColor" stroke-width="2"/>
            <line x1="12" y1="1" x2="12" y2="3" stroke="currentColor" stroke-width="2"/>
            <line x1="12" y1="21" x2="12" y2="23" stroke="currentColor" stroke-width="2"/>
            <line x1="4.22" y1="4.22" x2="5.64" y2="5.64" stroke="currentColor" stroke-width="2"/>
            <line x1="18.36" y1="18.36" x2="19.78" y2="19.78" stroke="currentColor" stroke-width="2"/>
            <line x1="1" y1="12" x2="3" y2="12" stroke="currentColor" stroke-width="2"/>
            <line x1="21" y1="12" x2="23" y2="12" stroke="currentColor" stroke-width="2"/>
            <line x1="4.22" y1="19.78" x2="5.64" y2="18.36" stroke="currentColor" stroke-width="2"/>
            <line x1="18.36" y1="5.64" x2="19.78" y2="4.22" stroke="currentColor" stroke-width="2"/>
          </svg>
          <span>{{ currentTheme === 'dark' ? 'Light Mode' : 'Dark Mode' }}</span>
        </button>
      </div>
    </div>

    <!-- View Tabs -->
    <div class="view-tabs">
      <button 
        v-for="tab in viewTabs" 
        :key="tab.id"
        :class="['view-tab', { active: activeView === tab.id }]"
        @click="setActiveView(tab.id)"
      >
        {{ tab.name }}
      </button>
    </div>

    <!-- View as Cards (Default/First View) -->
    <div v-if="activeView === 'cards'" class="cards-view">
      <!-- Summary Stats -->
      <div class="summary-stats">
        <div class="stat-card">
          <div class="stat-value">{{ totalEvaluations }}</div>
          <div class="stat-label">TOTAL EVALUATIONS</div>
        </div>
        <div class="stat-card">
          <div class="stat-value">{{ averageScore }}%</div>
          <div class="stat-label">AVERAGE SCORE</div>
        </div>
        <div class="stat-card">
          <div class="stat-value">{{ averageTalkTime }}</div>
          <div class="stat-label">AVG TALK TIME</div>
        </div>
        <div class="stat-card">
          <div class="stat-value">{{ activeCounselors }}</div>
          <div class="stat-label">ACTIVE COUNSELORS</div>
        </div>
      </div>

      <!-- Agent Performance Cards -->
      <div class="qa-cards-container">
        <div 
          v-for="evaluation in agentEvaluations" 
          :key="evaluation.id"
          class="qa-card"
          @click="selectCard(evaluation.id)"
        >
          <!-- Card Header with Avatar and Score -->
          <div class="qa-card-header">
            <div class="qa-card-avatar">
              <img :src="evaluation.agent.avatar" :alt="evaluation.agent.name" />
            </div>
            <div class="qa-card-user-info">
              <div class="qa-card-name">{{ evaluation.agent.name }}</div>
              <div class="qa-card-calls">{{ evaluation.callsEvaluated }} calls evaluated</div>
            </div>
            <div :class="['qa-card-score', getScoreClass(evaluation.averageScore)]">
              {{ evaluation.averageScore }}%
            </div>
          </div>

          <!-- Card Details -->
          <div class="qa-card-details">
            <div class="qa-card-detail">
              <div class="qa-card-detail-label">AVG TALK TIME</div>
              <div class="qa-card-detail-value">{{ evaluation.averageTalkTime }}</div>
            </div>
            <div class="qa-card-detail">
              <div class="qa-card-detail-label">LAST EVALUATION</div>
              <div class="qa-card-detail-value">{{ formatDate(evaluation.lastEvaluationDate) }}</div>
            </div>
            <div class="qa-card-detail">
              <div class="qa-card-detail-label">BEST CATEGORY</div>
              <div class="qa-card-detail-value">{{ evaluation.bestCategory }}</div>
            </div>
            <div class="qa-card-detail">
              <div class="qa-card-detail-label">IMPROVEMENT AREA</div>
              <div class="qa-card-detail-value">{{ evaluation.improvementArea }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Calls Database View -->
    <div v-if="activeView === 'calls'" class="calls-view">
      <!-- Search and Filters -->
      <div class="calls-header">
        <div class="search-container">
          <span class="search-icon">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
              <circle cx="11" cy="11" r="8" stroke="currentColor" stroke-width="2"/>
              <path d="M21 21l-4.35-4.35" stroke="currentColor" stroke-width="2"/>
            </svg>
          </span>
          <input 
            v-model="callSearchQuery"
            type="text" 
            class="search-input" 
            placeholder="Search by call ID, agent, or caller..."
          />
        </div>
        
        <div class="filter-container">
          <select v-model="selectedEvaluationStatus" class="filter-select">
            <option value="all">All Calls</option>
            <option value="evaluated">Evaluated</option>
            <option value="not-evaluated">Not Evaluated</option>
          </select>
          
          <select v-model="selectedAgent" class="filter-select">
            <option value="all">All Agents</option>
            <option value="patience">Patience Williams</option>
            <option value="berna">Berna Johnson</option>
            <option value="julie">Julie Smith</option>
            <option value="viola">Viola Davis</option>
            <option value="charles">Charles Wilson</option>
          </select>
          
          <select v-model="selectedDateRange" class="filter-select">
            <option value="today">Today</option>
            <option value="yesterday">Yesterday</option>
            <option value="this-week">This Week</option>
            <option value="this-month">This Month</option>
          </select>
        </div>
      </div>

      <!-- Calls Table -->
      <div class="calls-table-container">
        <table class="calls-table">
          <thead>
            <tr>
              <th>Call ID</th>
              <th>Agent</th>
              <th>Caller</th>
              <th>Date & Time</th>
              <th>Duration</th>
              <th>Issue Type</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="call in filteredCalls" :key="call.id" class="call-row" @click="viewCallDetails(call)">
              <td class="call-id">#{{ call.id }}</td>
              <td class="agent-info">
                <div class="agent-avatar">
                  <img :src="call.agent.avatar" :alt="call.agent.name" />
                </div>
                <span>{{ call.agent.name }}</span>
              </td>
              <td>{{ call.caller.name }}</td>
              <td>{{ formatDateTime(call.dateTime) }}</td>
              <td>{{ call.duration }}</td>
              <td>{{ call.issueType }}</td>
              <td>
                <span :class="['status-badge', call.isEvaluated ? 'evaluated' : 'not-evaluated']">
                  {{ call.isEvaluated ? 'Evaluated' : 'Not Evaluated' }}
                </span>
              </td>
              <td class="actions">
                <div class="action-buttons">
                  <button 
                    v-if="!call.isEvaluated" 
                    class="action-btn evaluate" 
                    @click.stop="startEvaluation(call)"
                  >
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                      <path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7" stroke="currentColor" stroke-width="2"/>
                      <path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z" stroke="currentColor" stroke-width="2"/>
                    </svg>
                    <span>Evaluate</span>
                  </button>
                  <button 
                    v-else 
                    class="action-btn edit" 
                    @click.stop="editEvaluation(call)"
                  >
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                      <path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7" stroke="currentColor" stroke-width="2"/>
                      <path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z" stroke="currentColor" stroke-width="2"/>
                    </svg>
                    <span>Edit</span>
                  </button>
                  <button class="action-btn delete" @click.stop="deleteCall(call)">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                      <polyline points="3,6 5,6 21,6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                      <path d="M19,6V20C19,21 18,22 17,22H7C6,22 5,21 5,20V6M8,6V4C8,3 9,2 10,2H14C15,2 16,3 16,4V6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                    <span>Delete</span>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Analytics View -->
    <div v-if="activeView === 'analytics'" class="analytics-container">
      <!-- Performance Chart -->
      <div class="analytics-card">
        <div class="analytics-header">
          <div class="analytics-title">Overall Performance Metrics</div>
          <div class="analytics-subtitle">Average scores across all evaluations</div>
        </div>
        <div class="performance-categories">
          <div v-for="category in performanceCategories" :key="category.name" class="category-item">
            <div class="category-name">{{ category.name }}</div>
            <div class="category-bar">
              <div class="category-fill" :style="{ width: category.score + '%' }"></div>
            </div>
            <div class="category-score">{{ category.score }}%</div>
          </div>
        </div>
      </div>

      <!-- Top Performers -->
      <div class="analytics-card">
        <div class="analytics-header">
          <div class="analytics-title">Top Performers</div>
          <div class="analytics-subtitle">Agents with the highest average scores</div>
        </div>
        <div class="performers-list">
          <div class="performers-header">
            <span>Agent</span>
            <span>Average Score</span>
            <span>Performance</span>
          </div>
          <div v-for="performer in topPerformers" :key="performer.id" class="performer-row">
            <span class="performer-name">{{ performer.name }}</span>
            <span class="performer-score">{{ performer.score }}%</span>
            <div class="performance-bar">
              <div class="performance-fill" :style="{ width: performer.score + '%' }"></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Evaluation Modal -->
  <div v-if="showEvaluationModal" class="modal-overlay" @click="closeEvaluationModal">
    <div class="modal-content evaluation-modal" @click.stop>
      <div class="modal-header">
        <div class="modal-title">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
            <path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7" stroke="currentColor" stroke-width="2"/>
            <path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z" stroke="currentColor" stroke-width="2"/>
          </svg>
          Evaluate Call #{{ selectedCall?.id }}
        </div>
        <button class="modal-close" @click="closeEvaluationModal">&times;</button>
      </div>
      
      <div class="modal-body" v-if="selectedCall">
        <!-- Call Information -->
        <div class="evaluation-section">
          <div class="section-title">Call Information</div>
          <div class="call-info-grid">
            <div class="info-item">
              <div class="info-label">Agent</div>
              <div class="info-value">{{ selectedCall.agent.name }}</div>
            </div>
            <div class="info-item">
              <div class="info-label">Caller</div>
              <div class="info-value">{{ selectedCall.caller.name }}</div>
            </div>
            <div class="info-item">
              <div class="info-label">Duration</div>
              <div class="info-value">{{ selectedCall.duration }}</div>
            </div>
            <div class="info-item">
              <div class="info-label">Issue Type</div>
              <div class="info-value">{{ selectedCall.issueType }}</div>
            </div>
          </div>
        </div>

        <!-- Audio Player -->
        <div class="evaluation-section">
          <div class="section-title">Call Recording</div>
          <div class="audio-player">
            <button class="play-btn" @click="togglePlayback">
              <svg v-if="!isPlaying" width="20" height="20" viewBox="0 0 24 24" fill="none">
                <polygon points="5,3 19,12 5,21" fill="currentColor"/>
              </svg>
              <svg v-else width="20" height="20" viewBox="0 0 24 24" fill="none">
                <rect x="6" y="4" width="4" height="16" fill="currentColor"/>
                <rect x="14" y="4" width="4" height="16" fill="currentColor"/>
              </svg>
            </button>
            <div class="audio-progress">
              <div class="progress-bar">
                <div class="progress-fill" :style="{ width: playbackProgress + '%' }"></div>
              </div>
              <div class="time-display">{{ currentTime }} / {{ totalTime }}</div>
            </div>
          </div>
        </div>

        <!-- Evaluation Criteria -->
        <div class="evaluation-section">
          <div class="section-title">Evaluation Criteria</div>
          <div class="criteria-list">
            <div v-for="criterion in evaluationCriteria" :key="criterion.id" class="criterion-item">
              <div class="criterion-header">
                <div class="criterion-name">{{ criterion.name }}</div>
                <div class="criterion-score">
                  <input 
                    type="number" 
                    v-model="criterion.score" 
                    min="0" 
                    max="100" 
                    class="score-input"
                  />
                  <span>%</span>
                </div>
              </div>
              <div class="criterion-description">{{ criterion.description }}</div>
              <div class="score-slider">
                <input 
                  type="range" 
                  v-model="criterion.score" 
                  min="0" 
                  max="100" 
                  class="slider"
                />
                <div class="slider-labels">
                  <span>Poor</span>
                  <span>Average</span>
                  <span>Excellent</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Overall Score -->
        <div class="evaluation-section">
          <div class="section-title">Overall Score</div>
          <div class="overall-score">
            <div class="score-display" :class="getScoreClass(overallScore)">
              {{ overallScore }}%
            </div>
            <div class="score-breakdown">
              <div class="breakdown-item" v-for="criterion in evaluationCriteria" :key="criterion.id">
                <span>{{ criterion.name }}: {{ criterion.score }}%</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Notes -->
        <div class="evaluation-section">
          <div class="section-title">Evaluation Notes</div>
          <textarea 
            v-model="evaluationNotes" 
            class="notes-textarea" 
            placeholder="Add your evaluation notes, feedback, and recommendations..."
            rows="4"
          ></textarea>
        </div>
      </div>
      
      <div class="modal-footer">
        <button class="modal-btn modal-btn-cancel" @click="closeEvaluationModal">Cancel</button>
        <button class="modal-btn modal-btn-submit" @click="submitEvaluation">Submit Evaluation</button>
      </div>
    </div>
  </div>

  <!-- View Evaluation Modal -->
  <div v-if="showViewModal" class="modal-overlay" @click="closeViewModal">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <div class="modal-title">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
            <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" stroke="currentColor" stroke-width="2"/>
            <circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="2"/>
          </svg>
          Evaluation Details - Call #{{ selectedEvaluationCall?.id }}
        </div>
        <button class="modal-close" @click="closeViewModal">&times;</button>
      </div>
      <div class="modal-body" v-if="selectedEvaluationCall">
        <!-- Call Information -->
        <div class="modal-section">
          <div class="modal-section-title">Call Information</div>
          <div class="modal-grid">
            <div class="modal-item">
              <div class="modal-label">Agent</div>
              <div class="modal-value">{{ selectedEvaluationCall.agent.name }}</div>
            </div>
            <div class="modal-item">
              <div class="modal-label">Caller</div>
              <div class="modal-value">{{ selectedEvaluationCall.caller.name }}</div>
            </div>
            <div class="modal-item">
              <div class="modal-label">Duration</div>
              <div class="modal-value">{{ selectedEvaluationCall.duration }}</div>
            </div>
            <div class="modal-item">
              <div class="modal-label">Issue Type</div>
              <div class="modal-value">{{ selectedEvaluationCall.issueType }}</div>
            </div>
          </div>
        </div>

        <!-- Score Breakdown -->
        <div class="modal-section">
          <div class="modal-section-title">Score Breakdown</div>
          <div class="modal-score-grid">
            <div 
              v-for="(score, category) in selectedEvaluationCall.evaluation.scores" 
              :key="category"
              class="modal-score-item"
            >
              <div class="modal-score-label">{{ formatCategory(category) }}</div>
              <div class="modal-score-bar">
                <div 
                  class="modal-score-fill" 
                  :style="{ width: score + '%' }"
                  :class="getScoreClass(score)"
                ></div>
              </div>
              <div class="modal-score-value">{{ score }}%</div>
            </div>
            <div class="modal-score-item overall">
              <div class="modal-score-label">Overall</div>
              <div class="modal-score-bar">
                <div 
                  class="modal-score-fill" 
                  :style="{ width: selectedEvaluationCall.evaluation.overallScore + '%' }"
                  :class="getScoreClass(selectedEvaluationCall.evaluation.overallScore)"
                ></div>
              </div>
              <div class="modal-score-value">{{ selectedEvaluationCall.evaluation.overallScore }}%</div>
            </div>
          </div>
        </div>

        <!-- Evaluation Notes -->
        <div v-if="selectedEvaluationCall.evaluation.notes" class="modal-section">
          <div class="modal-section-title">Evaluation Notes</div>
          <div class="modal-notes">{{ selectedEvaluationCall.evaluation.notes }}</div>
        </div>

        <!-- Evaluator Information -->
        <div class="modal-section">
          <div class="modal-section-title">Evaluation Details</div>
          <div class="modal-grid">
            <div class="modal-item">
              <div class="modal-label">Evaluated By</div>
              <div class="modal-value">{{ selectedEvaluationCall.evaluation.evaluatedBy }}</div>
            </div>
            <div class="modal-item">
              <div class="modal-label">Evaluation Date</div>
              <div class="modal-value">{{ formatDate(selectedEvaluationCall.evaluation.evaluationDate) }}</div>
            </div>
          </div>
        </div>
      </div>
      <div class="modal-footer">
        <button class="modal-btn modal-btn-cancel" @click="closeViewModal">Close</button>
        <button class="modal-btn modal-btn-edit" @click="editEvaluation(selectedEvaluationCall)">Edit Evaluation</button>
      </div>
    </div>
  </div>

  <!-- Call Details Modal -->
  <div v-if="showCallDetailsModal" class="modal-overlay" @click="closeCallDetailsModal">
    <div class="modal-content call-details-modal" @click.stop>
      <div class="modal-header">
        <div class="modal-title">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
            <path d="M22 16.92V19C22 20.1046 21.1046 21 20 21C10.6112 21 3 13.3888 3 4C3 2.89543 3.89543 2 5 2H7.08C7.55607 2 7.95823 2.33718 8.02513 2.80754L8.7 7.5C8.76694 7.97036 8.53677 8.42989 8.12 8.67L6.5 9.5C7.84 12.16 11.84 16.16 14.5 17.5L15.33 15.88C15.5701 15.4632 16.0296 15.2331 16.5 15.3L21.1925 16.0249C21.6628 16.0918 22 16.4939 22 16.97V16.92Z" stroke="currentColor" stroke-width="2"/>
          </svg>
          Call Details #{{ selectedCallDetails?.id }}
        </div>
        <button class="modal-close" @click="closeCallDetailsModal">&times;</button>
      </div>
      
      <div class="modal-body" v-if="selectedCallDetails">
        <!-- Call Information -->
        <div class="modal-section">
          <div class="modal-section-title">Call Information</div>
          <div class="call-details-grid">
            <div class="detail-item">
              <div class="detail-label">Agent</div>
              <div class="detail-value">
                <div class="agent-info">
                  <div class="agent-avatar">
                    <img :src="selectedCallDetails.agent.avatar" :alt="selectedCallDetails.agent.name" />
                  </div>
                  <span>{{ selectedCallDetails.agent.name }}</span>
                </div>
              </div>
            </div>
            <div class="detail-item">
              <div class="detail-label">Caller</div>
              <div class="detail-value">{{ selectedCallDetails.caller.name }}</div>
            </div>
            <div class="detail-item">
              <div class="detail-label">Phone Number</div>
              <div class="detail-value">{{ selectedCallDetails.caller.phone }}</div>
            </div>
            <div class="detail-item">
              <div class="detail-label">Date & Time</div>
              <div class="detail-value">{{ formatDateTime(selectedCallDetails.dateTime) }}</div>
            </div>
            <div class="detail-item">
              <div class="detail-label">Duration</div>
              <div class="detail-value">{{ selectedCallDetails.duration }}</div>
            </div>
            <div class="detail-item">
              <div class="detail-label">Issue Type</div>
              <div class="detail-value">{{ selectedCallDetails.issueType }}</div>
            </div>
            <div class="detail-item">
              <div class="detail-label">Status</div>
              <div class="detail-value">
                <span :class="['status-badge', selectedCallDetails.isEvaluated ? 'evaluated' : 'not-evaluated']">
                  {{ selectedCallDetails.isEvaluated ? 'Evaluated' : 'Not Evaluated' }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- Audio Player -->
        <div class="modal-section">
          <div class="modal-section-title">Call Recording</div>
          <div class="audio-player">
            <button class="play-btn" @click="togglePlayback">
              <svg v-if="!isPlaying" width="20" height="20" viewBox="0 0 24 24" fill="none">
                <polygon points="5,3 19,12 5,21" fill="currentColor"/>
              </svg>
              <svg v-else width="20" height="20" viewBox="0 0 24 24" fill="none">
                <rect x="6" y="4" width="4" height="16" fill="currentColor"/>
                <rect x="14" y="4" width="4" height="16" fill="currentColor"/>
              </svg>
            </button>
            <div class="audio-progress">
              <div class="progress-bar">
                <div class="progress-fill" :style="{ width: playbackProgress + '%' }"></div>
              </div>
              <div class="time-display">{{ currentTime }} / {{ totalTime }}</div>
            </div>
          </div>
        </div>

        <!-- Evaluation Details (if evaluated) -->
        <div v-if="selectedCallDetails.isEvaluated" class="modal-section">
          <div class="modal-section-title">Evaluation Summary</div>
          <div class="evaluation-summary">
            <div class="overall-score-display">
              <div class="score-circle" :class="getScoreClass(selectedCallDetails.evaluation.overallScore)">
                {{ selectedCallDetails.evaluation.overallScore }}%
              </div>
              <div class="score-label">Overall Score</div>
            </div>
            
            <div class="score-breakdown">
              <div class="modal-score-grid">
                <div 
                  v-for="(score, category) in selectedCallDetails.evaluation.scores" 
                  :key="category"
                  class="modal-score-item"
                >
                  <div class="modal-score-label">{{ formatCategory(category) }}</div>
                  <div class="modal-score-bar">
                    <div 
                      class="modal-score-fill" 
                      :style="{ width: score + '%' }"
                      :class="getScoreClass(score)"
                    ></div>
                  </div>
                  <div class="modal-score-value">{{ score }}%</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Evaluation Notes (if evaluated) -->
        <div v-if="selectedCallDetails.isEvaluated && selectedCallDetails.evaluation.notes" class="modal-section">
          <div class="modal-section-title">Evaluation Notes</div>
          <div class="modal-notes">{{ selectedCallDetails.evaluation.notes }}</div>
        </div>

        <!-- Evaluator Information (if evaluated) -->
        <div v-if="selectedCallDetails.isEvaluated" class="modal-section">
          <div class="modal-section-title">Evaluation Details</div>
          <div class="modal-grid">
            <div class="modal-item">
              <div class="modal-label">Evaluated By</div>
              <div class="modal-value">{{ selectedCallDetails.evaluation.evaluatedBy }}</div>
            </div>
            <div class="modal-item">
              <div class="modal-label">Evaluation Date</div>
              <div class="modal-value">{{ formatDate(selectedCallDetails.evaluation.evaluationDate) }}</div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="modal-footer">
        <button class="modal-btn modal-btn-cancel" @click="closeCallDetailsModal">Close</button>
        <button 
          v-if="!selectedCallDetails?.isEvaluated" 
          class="modal-btn modal-btn-submit" 
          @click="startEvaluationFromDetails"
        >
          Evaluate Call
        </button>
        <button 
          v-else 
          class="modal-btn modal-btn-edit" 
          @click="editEvaluationFromDetails"
        >
          Edit Evaluation
        </button>
      </div>
    </div>
  </div>
</div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

// Reactive state
const currentTheme = ref('dark')
const activeView = ref('cards') // Changed default to 'cards'
const selectedCard = ref(null)
const showEvaluationModal = ref(false)
const showViewModal = ref(false)
const showCallDetailsModal = ref(false)
const selectedCall = ref(null)
const selectedEvaluationCall = ref(null)
const selectedCallDetails = ref(null)
const callSearchQuery = ref('')
const selectedEvaluationStatus = ref('all')
const selectedAgent = ref('all')
const selectedDateRange = ref('today')
const evaluationNotes = ref('')
const isPlaying = ref(false)
const playbackProgress = ref(0)
const currentTime = ref('0:00')
const totalTime = ref('5:32')

// Sidebar state
const isSidebarCollapsed = ref(false)
const mobileOpen = ref(false)
const userRole = ref('user')
const isInQueue = ref(false)
const isProcessingQueue = ref(false)
const currentCall = ref(null)

// View tabs configuration - reordered with cards first
const viewTabs = ref([
  { id: 'cards', name: 'View as Cards' },
  { id: 'calls', name: 'Evaluate Calls' },
  { id: 'analytics', name: 'Analytics' }
])

// Evaluation criteria
const evaluationCriteria = ref([
  {
    id: 1,
    name: 'Opening',
    description: 'Professional greeting, introduction, and call setup',
    score: 0
  },
  {
    id: 2,
    name: 'Active Listening',
    description: 'Demonstrates understanding and empathy',
    score: 0
  },
  {
    id: 3,
    name: 'Proactive Questioning',
    description: 'Asks relevant questions to understand the situation',
    score: 0
  },
  {
    id: 4,
    name: 'Problem Resolution',
    description: 'Provides appropriate solutions and resources',
    score: 0
  },
  {
    id: 5,
    name: 'Call Closing',
    description: 'Professional closure with follow-up information',
    score: 0
  }
])

// Performance categories for analytics
const performanceCategories = ref([
  { name: 'Opening', score: 82 },
  { name: 'Listening', score: 79 },
  { name: 'Proactive', score: 70 },
  { name: 'Resolution', score: 78 },
  { name: 'Closing', score: 77 }
])

// Sample calls database - Added more sample data
const callsDatabase = ref([
  {
    id: '12345',
    agent: {
      name: 'Patience Williams',
      avatar: '/placeholder.svg?height=40&width=40'
    },
    caller: {
      name: 'Sarah Johnson',
      phone: '+1-555-0123'
    },
    dateTime: new Date('2024-12-07T09:30:00'),
    duration: '8:32',
    issueType: 'Domestic Violence',
    isEvaluated: false,
    recordingUrl: '/sample-recording.mp3'
  },
  {
    id: '12346',
    agent: {
      name: 'Berna Johnson',
      avatar: '/placeholder.svg?height=40&width=40'
    },
    caller: {
      name: 'Michael Davis',
      phone: '+1-555-0124'
    },
    dateTime: new Date('2024-12-07T10:15:00'),
    duration: '16:45',
    issueType: 'Crisis Support',
    isEvaluated: true,
    recordingUrl: '/sample-recording.mp3',
    evaluation: {
      overallScore: 72,
      scores: {
        opening: 75,
        listening: 78,
        proactive: 65,
        resolution: 75,
        closing: 70
      },
      notes: 'Good rapport building. Could improve on proactive questioning and resource offering.',
      evaluatedBy: 'Isaac Martinez',
      evaluationDate: new Date('2024-12-07T11:00:00')
    }
  },
  {
    id: '12347',
    agent: {
      name: 'Julie Smith',
      avatar: '/placeholder.svg?height=40&width=40'
    },
    caller: {
      name: 'Emily Wilson',
      phone: '+1-555-0125'
    },
    dateTime: new Date('2024-12-07T11:20:00'),
    duration: '7:35',
    issueType: 'Information Request',
    isEvaluated: false,
    recordingUrl: '/sample-recording.mp3'
  },
  {
    id: '12348',
    agent: {
      name: 'Viola Davis',
      avatar: '/placeholder.svg?height=40&width=40'
    },
    caller: {
      name: 'Robert Brown',
      phone: '+1-555-0126'
    },
    dateTime: new Date('2024-12-07T14:30:00'),
    duration: '12:18',
    issueType: 'Emergency Support',
    isEvaluated: true,
    recordingUrl: '/sample-recording.mp3',
    evaluation: {
      overallScore: 92,
      scores: {
        opening: 95,
        listening: 92,
        proactive: 90,
        resolution: 94,
        closing: 89
      },
      notes: 'Outstanding performance across all categories. Excellent crisis management and resource coordination.',
      evaluatedBy: 'Milly Rodriguez',
      evaluationDate: new Date('2024-12-07T15:15:00')
    }
  },
  {
    id: '12349',
    agent: {
      name: 'Charles Wilson',
      avatar: '/placeholder.svg?height=40&width=40'
    },
    caller: {
      name: 'Lisa Anderson',
      phone: '+1-555-0127'
    },
    dateTime: new Date('2024-12-07T16:45:00'),
    duration: '14:22',
    issueType: 'Legal Assistance',
    isEvaluated: false,
    recordingUrl: '/sample-recording.mp3'
  },
  // Added more sample data
  {
    id: '12350',
    agent: {
      name: 'Patience Williams',
      avatar: '/placeholder.svg?height=40&width=40'
    },
    caller: {
      name: 'Thomas Wright',
      phone: '+1-555-0128'
    },
    dateTime: new Date('2024-12-08T08:15:00'),
    duration: '9:47',
    issueType: 'Mental Health Support',
    isEvaluated: true,
    recordingUrl: '/sample-recording.mp3',
    evaluation: {
      overallScore: 85,
      scores: {
        opening: 88,
        listening: 85,
        proactive: 82,
        resolution: 87,
        closing: 83
      },
      notes: 'Excellent empathy and active listening skills. Strong resource coordination.',
      evaluatedBy: 'Sarah Martinez',
      evaluationDate: new Date('2024-12-08T09:00:00')
    }
  },
  {
    id: '12351',
    agent: {
      name: 'Julie Smith',
      avatar: '/placeholder.svg?height=40&width=40'
    },
    caller: {
      name: 'Maria Garcia',
      phone: '+1-555-0129'
    },
    dateTime: new Date('2024-12-08T10:30:00'),
    duration: '13:25',
    issueType: 'Housing Assistance',
    isEvaluated: true,
    recordingUrl: '/sample-recording.mp3',
    evaluation: {
      overallScore: 68,
      scores: {
        opening: 70,
        listening: 72,
        proactive: 60,
        resolution: 68,
        closing: 70
      },
      notes: 'Good basic skills but needs improvement in proactive questioning and resource knowledge.',
      evaluatedBy: 'David Chen',
      evaluationDate: new Date('2024-12-08T11:15:00')
    }
  },
  {
    id: '12352',
    agent: {
      name: 'Charles Wilson',
      avatar: '/placeholder.svg?height=40&width=40'
    },
    caller: {
      name: 'Jennifer Lee',
      phone: '+1-555-0130'
    },
    dateTime: new Date('2024-12-08T13:45:00'),
    duration: '11:18',
    issueType: 'Crisis Intervention',
    isEvaluated: true,
    recordingUrl: '/sample-recording.mp3',
    evaluation: {
      overallScore: 78,
      scores: {
        opening: 80,
        listening: 82,
        proactive: 75,
        resolution: 76,
        closing: 77
      },
      notes: 'Solid performance with good crisis management skills. Could improve on follow-up procedures.',
      evaluatedBy: 'Lisa Rodriguez',
      evaluationDate: new Date('2024-12-08T14:30:00')
    }
  },
  {
    id: '12353',
    agent: {
      name: 'Berna Johnson',
      avatar: '/placeholder.svg?height=40&width=40'
    },
    caller: {
      name: 'Kevin Martinez',
      phone: '+1-555-0131'
    },
    dateTime: new Date('2024-12-08T15:20:00'),
    duration: '6:42',
    issueType: 'Information Request',
    isEvaluated: false,
    recordingUrl: '/sample-recording.mp3'
  },
  {
    id: '12354',
    agent: {
      name: 'Viola Davis',
      avatar: '/placeholder.svg?height=40&width=40'
    },
    caller: {
      name: 'Amanda Thompson',
      phone: '+1-555-0132'
    },
    dateTime: new Date('2024-12-08T16:30:00'),
    duration: '18:45',
    issueType: 'Domestic Violence',
    isEvaluated: true,
    recordingUrl: '/sample-recording.mp3',
    evaluation: {
      overallScore: 94,
      scores: {
        opening: 96,
        listening: 95,
        proactive: 92,
        resolution: 95,
        closing: 92
      },
      notes: 'Exceptional handling of sensitive situation. Perfect protocol adherence and excellent resource coordination.',
      evaluatedBy: 'Michael Johnson',
      evaluationDate: new Date('2024-12-08T17:15:00')
    }
  },
  {
    id: '12355',
    agent: {
      name: 'Patience Williams',
      avatar: '/placeholder.svg?height=40&width=40'
    },
    caller: {
      name: 'Daniel Rodriguez',
      phone: '+1-555-0133'
    },
    dateTime: new Date('2024-12-09T09:15:00'),
    duration: '10:22',
    issueType: 'Legal Assistance',
    isEvaluated: false,
    recordingUrl: '/sample-recording.mp3'
  },
  {
    id: '12356',
    agent: {
      name: 'Julie Smith',
      avatar: '/placeholder.svg?height=40&width=40'
    },
    caller: {
      name: 'Rebecca White',
      phone: '+1-555-0134'
    },
    dateTime: new Date('2024-12-09T11:45:00'),
    duration: '15:30',
    issueType: 'Crisis Support',
    isEvaluated: true,
    recordingUrl: '/sample-recording.mp3',
    evaluation: {
      overallScore: 76,
      scores: {
        opening: 78,
        listening: 80,
        proactive: 72,
        resolution: 75,
        closing: 75
      },
      notes: 'Good crisis management with room for improvement in proactive questioning techniques.',
      evaluatedBy: 'Jennifer Adams',
      evaluationDate: new Date('2024-12-09T12:30:00')
    }
  },
  {
    id: '12357',
    agent: {
      name: 'Charles Wilson',
      avatar: '/placeholder.svg?height=40&width=40'
    },
    caller: {
      name: 'Steven Clark',
      phone: '+1-555-0135'
    },
    dateTime: new Date('2024-12-09T14:20:00'),
    duration: '8:15',
    issueType: 'Information Request',
    isEvaluated: false,
    recordingUrl: '/sample-recording.mp3'
  },
  {
    id: '12358',
    agent: {
      name: 'Berna Johnson',
      avatar: '/placeholder.svg?height=40&width=40'
    },
    caller: {
      name: 'Michelle Taylor',
      phone: '+1-555-0136'
    },
    dateTime: new Date('2024-12-09T16:00:00'),
    duration: '12:55',
    issueType: 'Mental Health Support',
    isEvaluated: true,
    recordingUrl: '/sample-recording.mp3',
    evaluation: {
      overallScore: 81,
      scores: {
        opening: 83,
        listening: 85,
        proactive: 78,
        resolution: 82,
        closing: 77
      },
      notes: 'Strong empathy and listening skills. Good resource knowledge with minor areas for improvement in closing procedures.',
      evaluatedBy: 'Robert Kim',
      evaluationDate: new Date('2024-12-09T16:45:00')
    }
  }
])

const topPerformers = ref([
  { id: 1, name: 'Viola Davis', score: 93 },
  { id: 2, name: 'Patience Williams', score: 85 },
  { id: 3, name: 'Charles Wilson', score: 78 },
  { id: 4, name: 'Berna Johnson', score: 77 },
  { id: 5, name: 'Julie Smith', score: 72 }
])

// Computed properties
const filteredCalls = computed(() => {
  let filtered = callsDatabase.value

  if (selectedEvaluationStatus.value !== 'all') {
    filtered = filtered.filter(call => {
      if (selectedEvaluationStatus.value === 'evaluated') {
        return call.isEvaluated
      } else {
        return !call.isEvaluated
      }
    })
  }

  if (selectedAgent.value !== 'all') {
    filtered = filtered.filter(call => 
      call.agent.name.toLowerCase().includes(selectedAgent.value)
    )
  }

  if (callSearchQuery.value) {
    const query = callSearchQuery.value.toLowerCase()
    filtered = filtered.filter(call =>
      call.id.includes(query) ||
      call.agent.name.toLowerCase().includes(query) ||
      call.caller.name.toLowerCase().includes(query) ||
      call.issueType.toLowerCase().includes(query)
    )
  }

  return filtered
})

const agentEvaluations = computed(() => {
  const agentMap = new Map()
  
  callsDatabase.value.filter(call => call.isEvaluated).forEach(call => {
    const agentName = call.agent.name
    if (!agentMap.has(agentName)) {
      agentMap.set(agentName, {
        id: agentName,
        agent: call.agent,
        evaluations: [],
        callsEvaluated: 0,
        totalScore: 0,
        averageScore: 0,
        averageTalkTime: '0:00',
        lastEvaluationDate: null,
        bestCategory: '',
        improvementArea: ''
      })
    }
    
    const agentData = agentMap.get(agentName)
    agentData.evaluations.push(call.evaluation)
    agentData.callsEvaluated = agentData.evaluations.length
    agentData.totalScore = agentData.evaluations.reduce((sum, evaluation) => sum + evaluation.overallScore, 0)
    agentData.averageScore = Math.round(agentData.totalScore / agentData.evaluations.length)
    agentData.averageTalkTime = '11:26' // Mock data
    agentData.lastEvaluationDate = call.evaluation.evaluationDate

    // Calculate best and worst categories
    const categoryScores = {
      opening: 0,
      listening: 0,
      proactive: 0,
      resolution: 0,
      closing: 0
    }

    agentData.evaluations.forEach(evaluation => {
      Object.keys(categoryScores).forEach(category => {
        categoryScores[category] += evaluation.scores[category] || 0
      })
    })
    
    Object.keys(categoryScores).forEach(category => {
      categoryScores[category] = Math.round(categoryScores[category] / agentData.evaluations.length)
    })
    
    const sortedCategories = Object.entries(categoryScores).sort((a, b) => b[1] - a[1])
    agentData.bestCategory = formatCategory(sortedCategories[0][0])
    agentData.improvementArea = formatCategory(sortedCategories[sortedCategories.length - 1][0])
  })
  
  return Array.from(agentMap.values())
})

const overallScore = computed(() => {
  const total = evaluationCriteria.value.reduce((sum, criterion) => sum + parseInt(criterion.score || 0), 0)
  return Math.round(total / evaluationCriteria.value.length)
})

const totalEvaluations = computed(() => {
  return callsDatabase.value.filter(call => call.isEvaluated).length
})

const averageScore = computed(() => {
  const evaluatedCalls = callsDatabase.value.filter(call => call.isEvaluated)
  if (evaluatedCalls.length === 0) return 0
  const total = evaluatedCalls.reduce((sum, call) => sum + call.evaluation.overallScore, 0)
  return Math.round(total / evaluatedCalls.length)
})

const averageTalkTime = computed(() => {
  return '11:26'
})

const activeCounselors = computed(() => {
  const uniqueAgents = new Set(callsDatabase.value.map(call => call.agent.name))
  return uniqueAgents.size
})

// Sidebar computed properties
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
const toggleTheme = () => {
  currentTheme.value = currentTheme.value === 'dark' ? 'light' : 'dark'
}

const setActiveView = (viewId) => {
  activeView.value = viewId
}

const selectCard = (cardId) => {
  selectedCard.value = cardId
  // Find the evaluation call for this agent
  const agentEval = agentEvaluations.value.find(evaluation => evaluation.id === cardId)
  if (agentEval) {
    // Find the most recent evaluated call for this agent
    const recentCall = callsDatabase.value
      .filter(call => call.agent.name === agentEval.agent.name && call.isEvaluated)
      .sort((a, b) => new Date(b.dateTime) - new Date(a.dateTime))[0]
    
    if (recentCall) {
      selectedEvaluationCall.value = recentCall
      showViewModal.value = true
    }
  }
}

const startEvaluation = (call) => {
  selectedCall.value = call
  // Reset evaluation criteria
  evaluationCriteria.value.forEach(criterion => {
    criterion.score = 0
  })
  evaluationNotes.value = ''
  showEvaluationModal.value = true
}

const viewEvaluation = (call) => {
  selectedEvaluationCall.value = call
  showViewModal.value = true
}

const deleteCall = (call) => {
  if (confirm(`Are you sure you want to delete call #${call.id}?`)) {
    const index = callsDatabase.value.findIndex(c => c.id === call.id)
    if (index !== -1) {
      callsDatabase.value.splice(index, 1)
    }
  }
}

const closeEvaluationModal = () => {
  showEvaluationModal.value = false
  selectedCall.value = null
}

const closeViewModal = () => {
  showViewModal.value = false
  selectedEvaluationCall.value = null
}

const viewCallDetails = (call) => {
  selectedCallDetails.value = call
  showCallDetailsModal.value = true
}

const closeCallDetailsModal = () => {
  showCallDetailsModal.value = false
  selectedCallDetails.value = null
}

const startEvaluationFromDetails = () => {
  if (selectedCallDetails.value) {
    selectedCall.value = selectedCallDetails.value
    evaluationCriteria.value.forEach(criterion => {
      criterion.score = 0
    })
    evaluationNotes.value = ''
    closeCallDetailsModal()
    showEvaluationModal.value = true
  }
}

const editEvaluationFromDetails = () => {
  if (selectedCallDetails.value) {
    editEvaluation(selectedCallDetails.value)
    closeCallDetailsModal()
  }
}

const submitEvaluation = () => {
  if (selectedCall.value) {
    // Create evaluation object
    const evaluation = {
      overallScore: overallScore.value,
      scores: {},
      notes: evaluationNotes.value,
      evaluatedBy: 'Current User', // This would come from auth
      evaluationDate: new Date()
    }
    
    // Map criteria scores
    evaluationCriteria.value.forEach(criterion => {
      let key = criterion.name.toLowerCase().replace(/\s+/g, '').replace('active', '').replace('problem', '')
      if (key === 'listening') key = 'listening'
      if (key === 'questioning') key = 'proactive'
      if (key === 'resolution') key = 'resolution'
      if (key === 'closing') key = 'closing'
      if (key === 'opening') key = 'opening'
      evaluation.scores[key] = parseInt(criterion.score)
    })
    
    // Update the call in database
    const callIndex = callsDatabase.value.findIndex(call => call.id === selectedCall.value.id)
    if (callIndex !== -1) {
      callsDatabase.value[callIndex].isEvaluated = true
      callsDatabase.value[callIndex].evaluation = evaluation
    }
    
    closeEvaluationModal()
    
    // Show success message (you could add a toast notification here)
    console.log('Evaluation submitted successfully!')
  }
}

const playRecording = (call) => {
  console.log('Playing recording for call:', call.id)
  // Implement audio playback logic
}

const togglePlayback = () => {
  isPlaying.value = !isPlaying.value
  // Implement actual audio control
}

const editEvaluation = (call) => {
  // Pre-populate the evaluation form with existing data
  selectedCall.value = call
  
  if (call.evaluation) {
    evaluationCriteria.value.forEach(criterion => {
      let key = criterion.name.toLowerCase().replace(/\s+/g, '').replace('active', '').replace('problem', '')
      if (key === 'listening') key = 'listening'
      if (key === 'questioning') key = 'proactive'
      if (key === 'resolution') key = 'resolution'
      if (key === 'closing') key = 'closing'
      if (key === 'opening') key = 'opening'
      criterion.score = call.evaluation.scores[key] || 0
    })
    evaluationNotes.value = call.evaluation.notes || ''
  }
  
  closeViewModal()
  showEvaluationModal.value = true
}

const getScoreClass = (score) => {
  if (score >= 80) return 'score-high'
  if (score >= 60) return 'score-medium'
  return 'score-low'
}

const formatCategory = (category) => {
  return category.charAt(0).toUpperCase() + category.slice(1)
}

const formatDate = (date) => {
  return date.toLocaleDateString('en-US', { 
    month: 'short', 
    day: 'numeric', 
    year: 'numeric' 
  })
}

const formatDateTime = (date) => {
  return date.toLocaleString('en-US', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// Sidebar methods
const toggleSidebar = () => {
  isSidebarCollapsed.value = !isSidebarCollapsed.value
}

const expandSidebar = () => {
  isSidebarCollapsed.value = false
}

const toggleMobileMenu = () => {
  mobileOpen.value = !mobileOpen.value
}

const handleQueueToggle = () => {
  isInQueue.value = !isInQueue.value
  console.log('Queue toggle:', isInQueue.value)
}

const handleLogout = () => {
  console.log('Logout clicked')
}

// Lifecycle
onMounted(() => {
  // Apply initial theme
})
</script>

<style>
/* CSS Variables */
:root {
  --background-color: #0a0a0a;
  --sidebar-bg: #111111;
  --content-bg: #222222;
  --text-color: #ffffff;
  --text-secondary: #aaaaaa;
  --border-color: #333333;
  --accent-color: #964B00;
  --accent-hover: #b25900;
  --danger-color: #ff3b30;
  --success-color: #4CAF50;
  --pending-color: #FFA500;
  --logo-bg: #333333;
  --unassigned-color: #666666;
}

[data-theme="light"] {
  --background-color: #f5f5f5;
  --sidebar-bg: #ffffff;
  --content-bg: #ffffff;
  --text-color: #333333;
  --text-secondary: #666666;
  --border-color: #dddddd;
  --logo-bg: #f0f0f0;
}

/* Global layout */
.app-container {
  display: flex;
  min-height: 100vh;
  background-color: var(--background-color);
  color: var(--text-color);
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  transition: all 0.3s ease;
}

/* Sidebar styles */
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

/* Main Content */
.qa-statistics-container {
  flex: 1;
  margin-left: 250px;
  padding: 20px;
  overflow-y: auto;
  transition: margin-left 0.3s ease;
}

.qa-statistics-container.sidebar-collapsed {
  margin-left: 20px;
}

/* Header */
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  flex-wrap: wrap;
  gap: 20px;
}

.page-title {
  font-size: 32px;
  font-weight: 700;
  margin: 0;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 15px;
  flex-wrap: wrap;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  background-color: var(--content-bg);
  color: var(--text-color);
  border: 1px solid var(--border-color);
  border-radius: 25px;
  padding: 10px 16px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.action-btn:hover {
  background-color: var(--border-color);
}

.action-btn.active {
  background-color: var(--accent-color);
  border-color: var(--accent-color);
  color: white;
}

.theme-toggle {
  display: flex;
  align-items: center;
  gap: 8px;
  background-color: var(--content-bg);
  color: var(--text-color);
  border: 1px solid var(--border-color);
  border-radius: 25px;
  padding: 10px 16px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
  z-index: 1;
  white-space: nowrap;
  overflow: hidden;
}

.theme-toggle:hover {
  background-color: var(--border-color);
}

/* View Tabs */
.view-tabs {
  display: flex;
  gap: 20px;
  margin-bottom: 30px;
  border-bottom: 1px solid var(--border-color);
  padding-bottom: 15px;
}

.view-tab {
  background: none;
  border: none;
  color: var(--text-secondary);
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  padding: 10px 0;
  position: relative;
  transition: color 0.2s ease;
}

.view-tab.active {
  color: var(--text-color);
}

.view-tab.active::after {
  content: '';
  position: absolute;
  bottom: -16px;
  left: 0;
  width: 100%;
  height: 2px;
  background-color: var(--accent-color);
}

/* Cards View */
.cards-view {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

/* Calls View */
.calls-view {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.calls-header {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.search-container {
  position: relative;
  max-width: 400px;
}

.search-input {
  width: 100%;
  padding: 12px 20px 12px 45px;
  border-radius: 25px;
  border: 1px solid var(--border-color);
  background-color: var(--content-bg);
  color: var(--text-color);
  font-size: 14px;
  transition: all 0.2s ease;
}

.search-input:focus {
  outline: none;
  border-color: var(--accent-color);
  box-shadow: 0 0 0 2px rgba(150, 75, 0, 0.2);
}

.search-input::placeholder {
  color: var(--text-secondary);
}

.search-icon {
  position: absolute;
  left: 15px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-secondary);
}

.filter-container {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 20px;
  width: 100%;
}

.filter-select {
  padding: 12px 20px;
  border-radius: 25px;
  border: 1px solid var(--border-color);
  background-color: var(--content-bg);
  color: var(--text-color);
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
  width: 100%;
}

.filter-select:focus {
  outline: none;
  border-color: var(--accent-color);
  box-shadow: 0 0 0 2px rgba(150, 75, 0, 0.2);
}

.filter-select option {
  background-color: var(--content-bg);
  color: var(--text-color);
  padding: 8px;
}

[data-theme="light"] .filter-select option {
  background-color: #ffffff;
  color: #333333;
}

/* Calls Table */
.calls-table-container {
  background-color: var(--content-bg);
  border-radius: 15px;
  overflow: hidden;
  border: 1px solid var(--border-color);
}

.calls-table {
  width: 100%;
  border-collapse: collapse;
}

.calls-table th {
  background-color: var(--border-color);
  color: var(--text-color);
  padding: 15px;
  text-align: left;
  font-weight: 600;
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.calls-table td {
  padding: 15px;
  border-bottom: 1px solid var(--border-color);
  color: var(--text-color);
}

.call-row:hover {
  background-color: rgba(255, 255, 255, 0.02);
}

.call-id {
  font-weight: 600;
  color: var(--accent-color);
}

.agent-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.agent-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  overflow: hidden;
  flex-shrink: 0;
}

.agent-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.status-badge {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.status-badge.evaluated {
  background-color: rgba(76, 175, 80, 0.2);
  color: #4CAF50;
}

.status-badge.not-evaluated {
  background-color: rgba(255, 165, 0, 0.2);
  color: var(--pending-color);
}

.actions {
  text-align: right;
}

.action-buttons {
  display: flex;
  gap: 6px;
  flex-wrap: nowrap;
  align-items: center;
}

.action-btn.evaluate,
.action-btn.edit,
.action-btn.delete {
  padding: 6px 10px;
  border-radius: 6px;
  font-size: 11px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 4px;
  border: none;
  white-space: nowrap;
  flex-shrink: 0;
  min-width: fit-content;
}

.action-btn span {
  display: inline-block;
}

.action-btn svg {
  flex-shrink: 0;
}

.action-btn.evaluate {
  background-color: var(--accent-color);
  color: white;
}

.action-btn.edit {
  background-color: var(--success-color);
  color: white;
}

.action-btn.delete {
  background-color: var(--danger-color);
  color: white;
}

/* Summary Stats */
.summary-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.stat-card {
  background-color: var(--content-bg);
  border-radius: 15px;
  padding: 30px;
  text-align: center;
  border: 1px solid var(--border-color);
  transition: all 0.3s ease;
}

.stat-value {
  font-size: 36px;
  font-weight: 700;
  color: var(--accent-color);
  margin-bottom: 8px;
  display: block;
}

.stat-label {
  font-size: 12px;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 1px;
  font-weight: 500;
}

/* QA Cards */
.qa-cards-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 25px;
}

.qa-card {
  background-color: var(--content-bg);
  border-radius: 15px;
  padding: 25px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.qa-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  border-color: var(--accent-color);
}

.qa-card-header {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 20px;
}

.qa-card-avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background-color: var(--border-color);
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
  flex-shrink: 0;
}

.qa-card-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.qa-card-user-info {
  flex: 1;
}

.qa-card-name {
  font-size: 18px;
  font-weight: 600;
  margin: 0 0 5px 0;
  color: var(--text-color);
}

.qa-card-calls {
  font-size: 14px;
  color: var(--text-secondary);
  margin: 0;
}

.qa-card-score {
  font-size: 24px;
  font-weight: 700;
  padding: 10px 15px;
  border-radius: 10px;
  text-align: center;
  min-width: 80px;
}

.score-high {
  background-color: rgba(76, 175, 80, 0.2);
  color: #4CAF50;
}

.score-medium {
  background-color: rgba(255, 165, 0, 0.2);
  color: #FFA500;
}

.score-low {
  background-color: rgba(255, 59, 48, 0.2);
  color: #ff3b30;
}

.qa-card-details {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}

.qa-card-detail {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.qa-card-detail-label {
  font-size: 11px;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-weight: 500;
}

.qa-card-detail-value {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-color);
}

/* Analytics */
.analytics-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 25px;
}

.analytics-card {
  background-color: var(--content-bg);
  border-radius: 15px;
  padding: 25px;
  border: 1px solid var(--border-color);
}

.analytics-header {
  margin-bottom: 20px;
}

.analytics-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-color);
  margin-bottom: 5px;
}

.analytics-subtitle {
  font-size: 14px;
  color: var(--text-secondary);
}

.performance-categories {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.category-item {
  display: grid;
  grid-template-columns: 1fr 2fr auto;
  align-items: center;
  gap: 15px;
}

.category-name {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-color);
}

.category-bar {
  height: 8px;
  background-color: var(--border-color);
  border-radius: 4px;
  overflow: hidden;
}

.category-fill {
  height: 100%;
  background-color: var(--accent-color);
  border-radius: 4px;
  transition: width 0.5s ease;
}

.category-score {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-color);
  min-width: 40px;
  text-align: right;
}

.performers-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.performers-header {
  display: grid;
  grid-template-columns: 2fr 1fr 2fr;
  gap: 15px;
  padding: 10px 0;
  font-size: 12px;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  border-bottom: 1px solid var(--border-color);
}

.performer-row {
  display: grid;
  grid-template-columns: 2fr 1fr 2fr;
  gap: 15px;
  align-items: center;
  padding: 10px 0;
}

.performer-name {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-color);
}

.performer-score {
  font-size: 14px;
  font-weight: 600;
  color: var(--accent-color);
}

.performance-bar {
  height: 6px;
  background-color: var(--border-color);
  border-radius: 3px;
  overflow: hidden;
}

.performance-fill {
  height: 100%;
  background-color: var(--accent-color);
  border-radius: 3px;
  transition: width 0.5s ease;
}

/* Evaluation Modal */
.evaluation-modal {
  max-width: 800px;
  max-height: 90vh;
  overflow-y: auto;
}

.evaluation-section {
  margin-bottom: 25px;
}

.section-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--accent-color);
  margin-bottom: 15px;
}

.call-info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.info-label {
  font-size: 12px;
  color: var(--text-secondary);
  margin-bottom: 5px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.info-value {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-color);
}

/* Audio Player */
.audio-player {
  display: flex;
  align-items: center;
  gap: 15px;
  background-color: var(--border-color);
  padding: 15px;
  border-radius: 10px;
}

.play-btn {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: var(--accent-color);
  border: none;
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.play-btn:hover {
  background-color: var(--accent-hover);
}

.audio-progress {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.progress-bar {
  height: 4px;
  background-color: var(--background-color);
  border-radius: 2px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background-color: var(--accent-color);
  border-radius: 2px;
  transition: width 0.1s ease;
}

.time-display {
  font-size: 12px;
  color: var(--text-secondary);
}

/* Evaluation Criteria */
.criteria-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.criterion-item {
  background-color: var(--border-color);
  padding: 20px;
  border-radius: 10px;
}

.criterion-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.criterion-name {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-color);
}

.criterion-score {
  display: flex;
  align-items: center;
  gap: 5px;
}

.score-input {
  width: 60px;
  padding: 5px 8px;
  border: 1px solid var(--background-color);
  border-radius: 5px;
  background-color: var(--content-bg);
  color: var(--text-color);
  text-align: center;
  font-weight: 600;
}

.criterion-description {
  font-size: 14px;
  color: var(--text-secondary);
  margin-bottom: 15px;
}

.score-slider {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.slider {
  width: 100%;
  height: 6px;
  border-radius: 3px;
  background-color: var(--background-color);
  outline: none;
  cursor: pointer;
}

.slider::-webkit-slider-thumb {
  appearance: none;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background-color: var(--accent-color);
  cursor: pointer;
}

.slider::-moz-range-thumb {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background-color: var(--accent-color);
  cursor: pointer;
  border: none;
}

.slider-labels {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: var(--text-secondary);
}

/* Overall Score */
.overall-score {
  display: flex;
  align-items: center;
  gap: 20px;
  background-color: var(--border-color);
  padding: 20px;
  border-radius: 10px;
}

.score-display {
  font-size: 48px;
  font-weight: 700;
  padding: 20px;
  border-radius: 15px;
  text-align: center;
  min-width: 120px;
}

.score-breakdown {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.breakdown-item {
  font-size: 14px;
  color: var(--text-secondary);
}

/* Notes */
.notes-textarea {
  width: 100%;
  min-height: 100px;
  padding: 15px;
  border: 1px solid var(--border-color);
  border-radius: 10px;
  background-color: var(--content-bg);
  color: var(--text-color);
  font-family: inherit;
  font-size: 14px;
  resize: vertical;
}

.notes-textarea:focus {
  outline: none;
  border-color: var(--accent-color);
  box-shadow: 0 0 0 2px rgba(150, 75, 0, 0.2);
}

.notes-textarea::placeholder {
  color: var(--text-secondary);
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: var(--content-bg);
  border-radius: 15px;
  padding: 30px;
  width: 90%;
  max-width: 700px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid var(--border-color);
}

.modal-title {
  font-size: 20px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 10px;
  color: var(--text-color);
}

.modal-close {
  background: none;
  border: none;
  color: var(--text-secondary);
  cursor: pointer;
  font-size: 24px;
  line-height: 1;
}

.modal-body {
  margin-bottom: 20px;
}

.modal-section {
  margin-bottom: 25px;
}

.modal-section-title {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 15px;
  color: var(--accent-color);
}

.modal-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}

.modal-item {
  margin-bottom: 10px;
}

.modal-label {
  font-size: 12px;
  color: var(--text-secondary);
  margin-bottom: 5px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.modal-value {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-color);
}

.modal-score-grid {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-top: 10px;
}

.modal-score-item {
  display: grid;
  grid-template-columns: 1fr 2fr auto;
  align-items: center;
  gap: 15px;
}

.modal-score-item.overall {
  margin-top: 10px;
  padding-top: 15px;
  border-top: 1px solid var(--border-color);
}

.modal-score-label {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-color);
}

.modal-score-bar {
  height: 8px;
  background-color: var(--border-color);
  border-radius: 4px;
  overflow: hidden;
}

.modal-score-fill {
  height: 100%;
  border-radius: 4px;
  transition: width 0.5s ease;
}

.modal-score-fill.score-high {
  background-color: #4CAF50;
}

.modal-score-fill.score-medium {
  background-color: #FFA500;
}

.modal-score-fill.score-low {
  background-color: #ff3b30;
}

.modal-score-value {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-color);
  min-width: 40px;
  text-align: right;
}

.modal-notes {
  font-size: 14px;
  line-height: 1.6;
  color: var(--text-secondary);
  background-color: var(--background-color);
  padding: 15px;
  border-radius: 10px;
  border-left: 4px solid var(--accent-color);
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
  padding-top: 15px;
  border-top: 1px solid var(--border-color);
}

.modal-btn {
  padding: 10px 20px;
  border-radius: 25px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  border: none;
  transition: all 0.2s ease;
}

.modal-btn-cancel {
  background-color: transparent;
  color: var(--text-color);
  border: 1px solid var(--border-color);
}

.modal-btn-cancel:hover {
  background-color: var(--border-color);
}

.modal-btn-submit {
  background-color: var(--accent-color);
  color: white;
}

.modal-btn-submit:hover {
  background-color: var(--accent-hover);
}

.modal-btn-edit {
  background-color: var(--accent-color);
  color: white;
}

.modal-btn-edit:hover {
  background-color: var(--accent-hover);
}

/* Call Details Modal Styles */
.call-details-modal {
  max-width: 900px;
  max-height: 90vh;
  overflow-y: auto;
}

.call-details-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-top: 15px;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.detail-label {
  font-size: 12px;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-weight: 500;
}

.detail-value {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-color);
}

.evaluation-summary {
  display: flex;
  gap: 30px;
  align-items: flex-start;
}

.overall-score-display {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.score-circle {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  font-weight: 700;
  border: 4px solid;
}

.score-circle.score-high {
  background-color: rgba(76, 175, 80, 0.2);
  color: #4CAF50;
  border-color: #4CAF50;
}

.score-circle.score-medium {
  background-color: rgba(255, 165, 0, 0.2);
  color: #FFA500;
  border-color: #FFA500;
}

.score-circle.score-low {
  background-color: rgba(255, 59, 48, 0.2);
  color: #ff3b30;
  border-color: #ff3b30;
}

.score-label {
  font-size: 14px;
  color: var(--text-secondary);
  text-align: center;
}

.score-breakdown {
  flex: 1;
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
  
  .expand-btn {
    display: none !important;
  }
  
  .qa-statistics-container {
    margin-left: 0;
  }
  
  .analytics-container {
    grid-template-columns: 1fr;
  }

  .modal-grid {
    grid-template-columns: 1fr;
  }

  .call-info-grid {
    grid-template-columns: 1fr;
  }

  .filter-container {
    grid-template-columns: 1fr;
    gap: 15px;
  }
}

@media (max-width: 768px) {
  .qa-statistics-container {
    padding: 15px;
  }
  
  .page-title {
    font-size: 24px;
  }
  
  .header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .filter-container {
    grid-template-columns: 1fr;
  }
  
  .qa-cards-container {
    grid-template-columns: 1fr;
  }
  
  .summary-stats {
    grid-template-columns: 1fr 1fr;
  }
  
  .qa-card-details {
    grid-template-columns: 1fr;
  }

  .calls-table-container {
    overflow-x: auto;
  }

  .calls-table {
    min-width: 800px;
  }

  .overall-score {
    flex-direction: column;
    text-align: center;
  }

  .call-details-grid {
    grid-template-columns: 1fr;
  }

  .evaluation-summary {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }

  .action-buttons {
    flex-direction: column;
    gap: 4px;
  }

  .action-btn {
    width: 100%;
    justify-content: center;
  }
}

@media (max-width: 480px) {
  .summary-stats {
    grid-template-columns: 1fr;
  }
  
  .view-tabs {
    flex-wrap: wrap;
    gap: 10px;
  }
  
  .modal-score-item {
    grid-template-columns: 1fr;
    gap: 5px;
  }
  
  .modal-score-value {
    text-align: left;
  }

  .action-btn span {
    display: none;
  }

  .action-btn {
    padding: 8px;
    min-width: 36px;
    justify-content: center;
  }
}

@media (max-width: 768px) {
  .header-actions {
    width: 100%;
    justify-content: flex-start;
  }
  
  .theme-toggle span {
    display: none;
  }
}

.calls-table td.actions {
  min-width: 180px;
  white-space: nowrap;
}
</style>
