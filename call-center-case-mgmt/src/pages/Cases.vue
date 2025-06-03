<template>
  <div class="dashboard-layout">
    <button class="mobile-menu-btn" id="mobile-menu-btn" @click="toggleMobileMenu">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M3 12H21M3 6H21M3 18H21" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </button>

    <div class="sidebar" id="sidebar" :class="{ 'collapsed': isSidebarCollapsed, 'mobile-open': mobileOpen }">
      <div class="sidebar-content">
        <div class="logo-container">
          <div class="logo">
            <img src="/Openchs logo-1.png" alt="OpenCHS Logo">
          </div>
        </div>
        
        <router-link to="/dashboard" class="nav-item">
          <div class="nav-icon"></div>
          <div class="nav-text">Dashboard</div>
        </router-link>
        
        <router-link to="/calls" class="nav-item">
          <div class="nav-icon"></div>
          <div class="nav-text">Calls</div>
        </router-link>
        
        <router-link to="/cases" class="nav-item active">
          <div class="nav-icon"></div>
          <div class="nav-text">Cases</div>
        </router-link>
        
        <router-link to="/chats" class="nav-item">
          <div class="nav-icon"></div>
          <div class="nav-text">Chats</div>
        </router-link>
        
        <router-link to="/qa-statistics" class="nav-item">
          <div class="nav-icon"></div>
          <div class="nav-text">QA Statistics</div>
        </router-link>
        
        <router-link to="/wallboard" class="nav-item">
          <div class="nav-icon"></div>
          <div class="nav-text">Wallboard</div>
        </router-link>
        
        <router-link to="/settings" class="nav-item">
          <div class="nav-icon"></div>
          <div class="nav-text">Settings</div>
        </router-link>
        
        <div class="user-profile">
          <router-link to="/edit-profile" class="user-avatar">
            <svg viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 12C14.2091 12 16 10.2091 16 8C16 5.79086 14.2091 4 12 4C9.79086 4 8 5.79086 8 8C8 10.2091 9.79086 12 12 12Z"/>
              <path d="M12 14C7.58172 14 4 17.5817 4 22H20C20 17.5817 16.4183 14 12 14Z"/>
            </svg>
          </router-link>
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

    <div class="main-content" :style="{ marginLeft: mainContentMarginLeft }">
      <div class="header">
        <button class="sidebar-toggle" @click="toggleSidebar">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M4 6H20M4 12H20M4 18H20" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
        <div class="header-left">
          <h1>Cases</h1>
          <router-link to="/case-creation" class="add-case-btn">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 5V19M5 12H19" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            Add New Case
          </router-link>
        </div>
        <button class="theme-toggle" @click="toggleTheme">
          <svg fill="none" height="24" id="moon-icon" viewbox="0 0 24 24" width="24" xmlns="http://www.w3.org/2000/svg" v-show="currentTheme === 'dark'">
            <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <svg fill="none" height="24" id="sun-icon" viewbox="0 0 24 24" width="24" xmlns="http://www.w3.org/2000/svg" v-show="currentTheme === 'light'">
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

      <div class="search-container">
        <input 
          v-model="searchQuery"
          class="search-input" 
          placeholder="Search cases..." 
          type="text"
          @input="handleSearch"
        />
      </div>

      <div class="filter-tabs">
        <button 
          v-for="filter in filters" 
          :key="filter.id"
          :class="['filter-tab', { active: activeFilter === filter.id }]"
          @click="setActiveFilter(filter.id)"
        >
          {{ filter.name }}
        </button>
      </div>

      <div class="cases-container">
        <div class="cases-list">
          <h2 class="cases-title">Cases</h2>
          
          <div 
            v-for="caseItem in filteredCases" 
            :key="caseItem.id"
            :class="['case-item', { selected: selectedCaseId === caseItem.id }]"
            @click="selectCase(caseItem.id)"
          >
            <div class="case-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M20 7H4C2.89543 7 2 7.89543 2 9V19C2 20.1046 2.89543 21 4 21H20C21.1046 21 22 20.1046 22 19V9C22 7.89543 21.1046 7 20 7Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M16 21V5C16 4.46957 15.7893 3.96086 15.4142 3.58579C15.0391 3.21071 14.5304 3 14 3H10C9.46957 3 8.96086 3.21071 8.58579 3.58579C8.21071 3.96086 8 4.46957 8 5V21" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <div class="case-details">
              <div class="case-title">{{ caseItem.title }}</div>
              <div class="case-meta">
                <div class="case-priority">
                  <div :class="['priority-dot', caseItem.priority.toLowerCase()]"></div>
                  {{ caseItem.priority }} priority
                </div>
                <div class="case-assigned">
                  {{ caseItem.assignedTo ? `Assigned: ${caseItem.assignedTo}` : 'Unassigned' }}
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="case-detail" v-if="selectedCaseDetails">
          <div class="case-detail-header">
            <div class="case-detail-title">{{ selectedCaseDetails.caseTitle }}</div>
            <div class="case-detail-id">Case ID: {{ selectedCaseDetails.id }}</div>
          </div>
          
          <div class="case-detail-content">
            <div class="detail-item">
              <div class="detail-label">Case Filer</div>
              <div class="detail-value">{{ selectedCaseDetails.caseFiler }}</div>
            </div>
            
            <div class="detail-item">
              <div class="detail-label">Caseer</div>
              <div class="detail-value">{{ selectedCaseDetails.caseer }}</div>
            </div>
            
            <div class="detail-item">
              <div class="detail-label">Case Priority</div>
              <div :class="['detail-value', selectedCaseDetails.priority.toLowerCase()]">{{ selectedCaseDetails.priority }}</div>
            </div>
            
            <div class="detail-item">
              <div class="detail-label">Jurisdiction</div>
              <div class="detail-value">{{ selectedCaseDetails.jurisdiction }}</div>
            </div>
            
            <div class="detail-item">
              <div class="detail-label">Disposition</div>
              <div :class="['detail-value', { abusive: selectedCaseDetails.disposition === 'Abusive Call' }]">{{ selectedCaseDetails.disposition }}</div>
            </div>
            
            <div class="detail-item">
              <div class="detail-label">Date</div>
              <div class="detail-value">{{ selectedCaseDetails.date }}</div>
            </div>
            
            <div class="detail-item">
              <div class="detail-label">Escalated to</div>
              <div class="detail-value">{{ selectedCaseDetails.escalatedTo }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const searchQuery = ref('')
const activeFilter = ref('all')
const selectedCaseId = ref(null)
const currentTheme = ref(localStorage.getItem('theme') || 'dark')

const isSidebarCollapsed = ref(false)
const mobileOpen = ref(false)

const mainContentMarginLeft = computed(() => {
  if (window.innerWidth <= 768) {
    return '0px'
  } else if (isSidebarCollapsed.value) {
    return '80px'
  } else {
    return '250px'
  }
})

const filters = [
  { id: 'all', name: 'All' },
  { id: 'open', name: 'Open', status: 'open' },
  { id: 'pending', name: 'Pending', status: 'pending' },
  { id: 'assigned', name: 'Assigned' },
  { id: 'closed', name: 'Closed', status: 'closed' },
  { id: 'today', name: 'Today' },
  { id: 'priority', name: 'Priority' }
]

const cases = ref([
  {
    id: '123456',
    title: 'Case #123456-GBV request',
    priority: 'High',
    assignedTo: 'Robert Jackson',
    caseTitle: 'Emergency call',
    caseFiler: 'Nelson Adega',
    caseer: 'Mitch Ngugi',
    jurisdiction: 'Judge- in Court',
    disposition: 'Abusive Call',
    date: '15th Aug 2025',
    escalatedTo: 'Ntaate Kimani'
  },
  {
    id: '789012',
    title: 'Case #789012 - Assault',
    priority: 'Medium',
    assignedTo: 'Sarah Mitchell'
  },
  {
    id: '345678-1',
    title: 'Case #345678-In-transit medical support',
    priority: 'Low',
    assignedTo: null
  },
  {
    id: '901234-1',
    title: 'Case #901234-battery coordination',
    priority: 'High',
    assignedTo: 'Michael Lee'
  },
  {
    id: '345678-2',
    title: 'Case #345678-In-transit medical support',
    priority: 'High',
    assignedTo: 'Michael Lee'
  },
  {
    id: '901234-2',
    title: 'Case #901234-Transport coordination',
    priority: 'High',
    assignedTo: 'Michael Lee'
  },
  {
    id: '901234-3',
    title: 'Case #901234-Transport coordination',
    priority: 'High',
    assignedTo: 'Michael Lee'
  }
])

const filteredCases = computed(() => {
  let filtered = cases.value

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(c => 
      c.title.toLowerCase().includes(query) ||
      (c.assignedTo && c.assignedTo.toLowerCase().includes(query))
    )
  }

  if (activeFilter.value !== 'all') {
    const filterStatus = filters.find(f => f.id === activeFilter.value)?.status
    if (filterStatus) {
      filtered = filtered.filter(c => c.status === filterStatus)
    }
  }

  return filtered
})

const selectedCaseDetails = computed(() => {
  return cases.value.find(caseItem => caseItem.id === selectedCaseId.value)
})

const toggleSidebar = () => {
  isSidebarCollapsed.value = !isSidebarCollapsed.value
}

const toggleMobileMenu = () => {
  mobileOpen.value = !mobileOpen.value
}

const applyTheme = (theme) => {
  if (theme === 'light') {
    document.documentElement.setAttribute('data-theme', 'light')
  } else {
    document.documentElement.setAttribute('data-theme', 'dark')
  }
}

const toggleTheme = () => {
  const newTheme = currentTheme.value === 'dark' ? 'light' : 'dark'
  localStorage.setItem('theme', newTheme)
  currentTheme.value = newTheme
  applyTheme(newTheme)
}

const setActiveFilter = (filterId) => {
  activeFilter.value = filterId
}

const selectCase = (caseId) => {
  selectedCaseId.value = caseId
}

const handleSearch = () => {
  // The filtering is handled by the computed property 'filteredCases'
}

const logout = () => {
  router.push('/')
}

onMounted(() => {
  applyTheme(currentTheme.value)
  if (cases.value.length > 0) {
    selectedCaseId.value = cases.value[0].id
  }

  // Add click outside listener for mobile menu
  document.addEventListener('click', (event) => {
    const sidebar = document.getElementById('sidebar')
    const mobileMenuBtn = document.getElementById('mobile-menu-btn')
    if (window.innerWidth <= 768 && !sidebar.contains(event.target) && event.target !== mobileMenuBtn) {
      mobileOpen.value = false
    }
  })

  // Add window resize listener
  window.addEventListener('resize', () => {
    if (window.innerWidth > 768) {
      mobileOpen.value = false
    }
  })
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
  --input-bg: #1a1a1a;
  --high-priority: #ff3b30;
  --medium-priority: #FFA500;
  --low-priority: #4CAF50;
  --card-bg: var(--content-bg);
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
  --input-bg: #f0f0f0;
  --high-priority: #ff3b30;
  --medium-priority: #FFA500;
  --low-priority: #4CAF50;
  --card-bg: var(--content-bg);
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Inter', sans-serif;
}

body {
  margin: 0;
  min-width: 320px;
  min-height: 100vh;
  transition: background-color 0.3s, color 0.3s;
  overflow-x: hidden;
}

h1, h2, h3, h4, h5, h6, strong {
    font-weight: 700;
}

.nav-text, .card-title, .section-title, th {
    font-weight: 600;
}

.dashboard-layout {
  display: flex;
  width: 100%;
  min-height: 100vh;
  background-color: var(--background-color);
  color: var(--text-color);
  transition: background-color 0.3s, color 0.3s;
}

.sidebar {
  width: 250px;
  flex-shrink: 0;
  position: fixed;
  height: 100vh;
  background-color: var(--sidebar-bg);
  color: var(--text-color);
  transition: width 0.3s ease, transform 0.3s ease, background-color 0.3s;
  overflow-x: hidden;
  border-radius: 0 30px 30px 0;
  z-index: 100;
}

.sidebar.collapsed {
  width: 80px;
  transform: translateX(0);
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
  align-items: center;
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
  transition: background-color 0.3s;
}

.nav-item:hover {
    background-color: rgba(255, 255, 255, 0.05);
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
  transition: background-color 0.3s;
}

.join-queue-btn:hover {
    background-color: var(--accent-hover);
}

.logout-btn {
    background-color: #800000; /* Maroon background */
    color: white;
    border: 1px solid #800000; /* Maroon border */
    border-radius: 30px;
    padding: 10px;
    width: 100%;
    font-weight: 600;
    cursor: pointer;
    transition: background-color 0.3s, border-color 0.3s; /* Add border-color transition */
}

.logout-btn:hover {
    background-color: var(--danger-color); /* Red background on hover */
    border-color: var(--danger-color); /* Red border on hover */
}

.main-content {
  flex: 1;
  padding: 20px;
  min-height: 100vh;
  background-color: var(--background-color);
  transition: margin-left 0.3s ease, background-color 0.3s;
}

.sidebar.collapsed ~ .main-content {
  margin-left: 80px;
  width: auto;
}

.mobile-menu-btn {
  display: none;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 20px;
}

.header h1 {
  font-size: 24px;
  font-weight: 600;
}

.add-case-btn {
  background-color: var(--accent-color);
  color: white;
  border: none;
  border-radius: 30px;
  padding: 10px 20px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  text-decoration: none;
  transition: background-color 0.3s;
}

.add-case-btn:hover {
    background-color: var(--accent-hover);
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
  transition: background-color 0.3s, color 0.3s, border-color 0.3s;
}

.theme-toggle:hover {
    background-color: var(--border-color);
}

.theme-toggle svg {
  width: 16px;
  height: 16px;
}

.search-container {
  margin-bottom: 20px;
}

.search-input {
  width: 100%;
  padding: 12px 20px;
  border-radius: 30px;
  border: 1px solid var(--border-color);
  background-color: var(--content-bg);
  color: var(--text-color);
  font-size: 14px;
  transition: border-color 0.3s, box-shadow 0.3s;
}

.search-input::placeholder {
  color: var(--text-secondary);
}

.search-input:focus {
  outline: none;
  border-color: var(--accent-color);
  box-shadow: 0 0 0 0.1rem rgba(150, 75, 0, 0.25);
}

.filter-tabs {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 20px;
  overflow-x: auto;
  padding-bottom: 5px;
}

.filter-tab {
  background-color: var(--content-bg);
  color: var(--text-color);
  border: 1px solid var(--border-color);
  border-radius: 20px;
  padding: 8px 15px;
  font-size: 14px;
  cursor: pointer;
  white-space: nowrap;
  transition: background-color 0.3s;
  font-weight: 500;
}

.filter-tab.active {
  background-color: var(--accent-color);
  color: white;
  border-color: var(--accent-color);
}

.filter-tab:hover:not(.active) {
    background-color: rgba(150, 75, 0, 0.1);
}

.cases-container {
  display: flex;
  gap: 20px;
}

.cases-list {
  flex: 1;
}

.cases-title {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 15px;
}

.case-item {
  background-color: var(--content-bg);
  border-radius: 20px;
  padding: 15px;
  margin-bottom: 10px;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s, background-color 0.3s;
  display: flex;
  align-items: center;
  gap: 15px;
}

.case-item:hover {
  transform: translateY(-3px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.case-item.selected {
  border: 2px solid var(--accent-color);
}

.case-icon {
  width: 40px;
  height: 40px;
  background-color: var(--background-color);
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.case-icon svg {
  width: 20px;
  height: 20px;
  stroke: var(--text-color);
}

.case-details {
  flex: 1;
}

.case-title {
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 5px;
}

.case-meta {
  font-size: 12px;
  color: var(--text-secondary);
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.case-priority {
  display: inline-flex;
  align-items: center;
  gap: 5px;
}

.priority-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.priority-dot.high {
  background-color: var(--high-priority);
}

.priority-dot.medium {
  background-color: var(--medium-priority);
}

.priority-dot.low {
  background-color: var(--low-priority);
}

.case-assigned {
  /* Styles for assigned info */
}

.case-detail {
  background-color: var(--content-bg);
  border-radius: 15px;
  padding: 20px;
  width: 400px;
  flex-shrink: 0;
  overflow-y: auto;
}

.case-detail-header {
  margin-bottom: 20px;
}

.case-detail-title {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 5px;
}

.case-detail-id {
  font-size: 14px;
  color: var(--text-secondary);
}

.case-detail-content {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.detail-label {
  font-size: 12px;
  color: var(--text-secondary);
}

.detail-value {
  font-size: 14px;
  font-weight: 500;
}

.detail-value.high, .detail-value.medium, .detail-value.low {
    font-weight: 600;
}

.detail-value.abusive {
  color: var(--high-priority);
}

@media (max-width: 1024px) {
  .cases-container {
    flex-direction: column;
  }
  
  .case-detail {
    width: 100%;
  }
}

@media (max-width: 768px) {
  .dashboard-layout {
    flex-direction: column;
  }

  .mobile-menu-btn {
    display: block;
  }

  .sidebar {
    position: fixed;
    top: 0;
    left: -250px;
    height: 100vh;
    z-index: 1000;
    transition: transform 0.3s ease;
  }

  .sidebar.collapsed {
    transform: translateX(0);
    left: -250px;
  }

  .sidebar.mobile-open {
    transform: translateX(250px);
    left: 0;
  }

  .main-content {
    flex: 1;
    padding: 10px;
    overflow-y: auto;
  }

  .header {
    gap: 10px;
  }

  .header h1 {
    font-size: 20px;
  }

  .sidebar-toggle {
    display: flex;
  }
}

@media (min-width: 769px) {
  .mobile-menu-btn {
    display: none;
  }

  .sidebar {
    width: 250px;
    transition: width 0.3s ease;
    transform: translateX(0);
    left: 0;
  }

  .sidebar.collapsed {
    width: 80px;
  }

  .sidebar.mobile-open {
    transform: translateX(0);
    left: 0;
  }

  .main-content {
    flex: 1;
    padding: 20px;
    overflow-y: auto;
  }

  .sidebar-toggle {
    display: flex;
  }
}

.sidebar-toggle {
  background-color: var(--content-bg);
  color: var(--text-color);
  border: 1px solid var(--border-color);
  border-radius: 30px;
  padding: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.3s;
}

.sidebar-toggle:hover {
  background-color: var(--background-color);
}

.sidebar-toggle svg {
  width: 20px;
  height: 20px;
}

.header-actions {
  display: flex;
  align-items: center;
}

.status-overview {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.status-card {
  background-color: #f9f9f9;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.status-card h2 {
  margin-top: 0;
  font-size: 1.1em;
  color: #555;
}

.status-card p {
  font-size: 1.8em;
  font-weight: bold;
  margin-bottom: 0;
  color: #333;
}

.cases-list h2 {
  margin-top: 0;
  margin-bottom: 15px;
  font-size: 1.5em;
}

.cases-list table {
  width: 100%;
  border-collapse: collapse;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.cases-list th,
.cases-list td {
  padding: 12px;
  border: 1px solid #ddd;
  text-align: left;
}

.cases-list th {
  background-color: #f2f2f2;
  font-weight: bold;
}

.cases-list tr:nth-child(even) {
  background-color: #f9f9f9;
}

.cases-list tr:hover {
  background-color: #e9e9e9;
}

.btn-primary,
.btn-secondary,
.btn-danger {
  padding: 8px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9em;
}

.btn-primary {
  background-color: #007bff;
  color: white;
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
  margin-right: 5px;
}

.btn-danger {
  background-color: #dc3545;
  color: white;
}

.btn-primary:hover {
  background-color: #0056b3;
}

.btn-secondary:hover {
  background-color: #545b62;
}

.btn-danger:hover {
  background-color: #c82333;
}
</style>
