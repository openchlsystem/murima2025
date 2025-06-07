<template>
<div>
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
    <div class="cases-container">
      <div class="header">
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

      <div class="cases-container-inner">
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
                <path d="M12 22C12 22 20 18 20 12V5L12 2L4 5V12C4 18 12 22 12 22Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M9 12L11 14L15 10" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <div class="case-details">
              <div class="case-title">{{ caseItem.title }}</div>
              <div class="case-meta">
                <div class="case-priority">
                  <div :class="['priority-dot', caseItem.priority.toLowerCase()]"></div>
                  <span>{{ caseItem.priority }} priority</span>
                </div>
                <div class="case-assigned">
                  <span>{{ caseItem.assignedTo ? `Assigned: ${caseItem.assignedTo}` : 'Unassigned' }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="case-detail" v-if="selectedCaseDetails">
          <div class="case-detail-header">
            <div class="case-detail-title">{{ selectedCaseDetails.caseTitle || selectedCaseDetails.title }}</div>
            <div class="case-detail-id">Case ID: {{ selectedCaseDetails.id }}</div>
          </div>
          
          <div class="case-detail-content">
            <div class="detail-item">
              <div class="detail-label">Case Filer</div>
              <div class="detail-value">{{ selectedCaseDetails.caseFiler || 'N/A' }}</div>
            </div>
            
            <div class="detail-item">
              <div class="detail-label">Caseer</div>
              <div class="detail-value">{{ selectedCaseDetails.caseer || 'N/A' }}</div>
            </div>
            
            <div class="detail-item">
              <div class="detail-label">Case Priority</div>
              <div :class="['detail-value', selectedCaseDetails.priority.toLowerCase()]">{{ selectedCaseDetails.priority }}</div>
            </div>
            
            <div class="detail-item">
              <div class="detail-label">Jurisdiction</div>
              <div class="detail-value">{{ selectedCaseDetails.jurisdiction || 'N/A' }}</div>
            </div>
            
            <div class="detail-item">
              <div class="detail-label">Disposition</div>
              <div :class="['detail-value', { abusive: selectedCaseDetails.disposition === 'Abusive Call' }]">
                {{ selectedCaseDetails.disposition || 'N/A' }}
              </div>
            </div>
            
            <div class="detail-item">
              <div class="detail-label">Date</div>
              <div class="detail-value">{{ selectedCaseDetails.date || 'N/A' }}</div>
            </div>
            
            <div class="detail-item">
              <div class="detail-label">Escalated to</div>
              <div class="detail-value">{{ selectedCaseDetails.escalatedTo || 'N/A' }}</div>
            </div>
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
import SidePanel from '@/components/SidePanel.vue'

const router = useRouter()

// Reactive state
const searchQuery = ref('')
const activeFilter = ref('all')
const selectedCaseId = ref('123456') // Default to first case
const currentTheme = ref(localStorage.getItem('theme') || 'dark')

// SidePanel related state
const userRole = ref('super-admin')
const isInQueue = ref(false)
const isProcessingQueue = ref(false)
const currentCall = ref(null)

// Filter options
const filters = ref([
  { id: 'all', name: 'All' },
  { id: 'open', name: 'Open', status: 'open' },
  { id: 'pending', name: 'Pending', status: 'pending' },
  { id: 'assigned', name: 'Assigned' },
  { id: 'closed', name: 'Closed', status: 'closed' },
  { id: 'today', name: 'Today' },
  { id: 'priority', name: 'Priority' }
])

// Sample cases data
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
    assignedTo: 'Sarah Mitchell',
    caseTitle: 'Assault Case',
    caseFiler: 'Jane Doe',
    caseer: 'John Smith',
    jurisdiction: 'District Court',
    disposition: 'Under Investigation',
    date: '14th Aug 2025',
    escalatedTo: 'Senior Detective'
  },
  {
    id: '345678-1',
    title: 'Case #345678-In-transit medical support',
    priority: 'Low',
    assignedTo: null,
    caseTitle: 'Medical Support',
    caseFiler: 'Medical Team',
    caseer: 'Emergency Services',
    jurisdiction: 'Emergency Response',
    disposition: 'Resolved',
    date: '13th Aug 2025',
    escalatedTo: 'Hospital Administration'
  },
  {
    id: '901234-1',
    title: 'Case #901234-battery coordination',
    priority: 'High',
    assignedTo: 'Michael Lee',
    caseTitle: 'Battery Case',
    caseFiler: 'Police Department',
    caseer: 'Detective Brown',
    jurisdiction: 'Criminal Court',
    disposition: 'Active Investigation',
    date: '16th Aug 2025',
    escalatedTo: 'District Attorney'
  },
  {
    id: '345678-2',
    title: 'Case #345678-In-transit medical support',
    priority: 'High',
    assignedTo: 'Michael Lee',
    caseTitle: 'Medical Emergency',
    caseFiler: 'Paramedic Team',
    caseer: 'Emergency Coordinator',
    jurisdiction: 'Emergency Response',
    disposition: 'In Progress',
    date: '16th Aug 2025',
    escalatedTo: 'Medical Director'
  },
  {
    id: '901234-2',
    title: 'Case #901234-Transport coordination',
    priority: 'High',
    assignedTo: 'Michael Lee',
    caseTitle: 'Transport Coordination',
    caseFiler: 'Transport Authority',
    caseer: 'Logistics Team',
    jurisdiction: 'Transport Commission',
    disposition: 'Pending Review',
    date: '12th Aug 2025',
    escalatedTo: 'Operations Manager'
  },
  {
    id: '901234-3',
    title: 'Case #901234-Transport coordination',
    priority: 'High',
    assignedTo: 'Michael Lee',
    caseTitle: 'Transport Emergency',
    caseFiler: 'Emergency Services',
    caseer: 'Transport Coordinator',
    jurisdiction: 'Emergency Response',
    disposition: 'Active',
    date: '16th Aug 2025',
    escalatedTo: 'Emergency Director'
  }
])

// Computed properties
const filteredCases = computed(() => {
  let filtered = cases.value

  // Search filter
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(c => 
      c.title.toLowerCase().includes(query) ||
      (c.assignedTo && c.assignedTo.toLowerCase().includes(query)) ||
      (c.caseFiler && c.caseFiler.toLowerCase().includes(query))
    )
  }

  // Status filter
  if (activeFilter.value !== 'all') {
    const filterStatus = filters.value.find(f => f.id === activeFilter.value)?.status
    if (filterStatus) {
      filtered = filtered.filter(c => c.status === filterStatus)
    } else if (activeFilter.value === 'assigned') {
      filtered = filtered.filter(c => c.assignedTo)
    } else if (activeFilter.value === 'priority') {
      filtered = filtered.filter(c => c.priority === 'High')
    } else if (activeFilter.value === 'today') {
      // Filter for today's cases (simplified for demo)
      filtered = filtered.filter(c => c.date && c.date.includes('16th Aug 2025'))
    }
  }

  return filtered
})

const selectedCaseDetails = computed(() => {
  return cases.value.find(caseItem => caseItem.id === selectedCaseId.value)
})

// SidePanel event handlers
const handleQueueToggle = () => {
  isInQueue.value = !isInQueue.value
  console.log('Queue toggled:', isInQueue.value)
}

const handleLogout = () => {
  router.push('/')
}

const handleSidebarToggle = (collapsed) => {
  console.log('Sidebar toggled:', collapsed)
}

// Methods
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
    root.style.setProperty('--header-bg', '#f0f0f0')
    root.style.setProperty('--input-bg', '#f0f0f0')
    root.setAttribute('data-theme', 'light')
  } else {
    root.style.setProperty('--background-color', '#0a0a0a')
    root.style.setProperty('--sidebar-bg', '#111')
    root.style.setProperty('--content-bg', '#222')
    root.style.setProperty('--text-color', '#fff')
    root.style.setProperty('--text-secondary', '#aaa')
    root.style.setProperty('--border-color', '#333')
    root.style.setProperty('--card-bg', '#222')
    root.style.setProperty('--header-bg', '#333')
    root.style.setProperty('--input-bg', '#1a1a1a')
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
  root.style.setProperty('--high-priority', '#ff3b30')
  root.style.setProperty('--medium-priority', '#FFA500')
  root.style.setProperty('--low-priority', '#4CAF50')
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

// Lifecycle hooks
onMounted(() => {
  // Load saved theme
  const savedTheme = localStorage.getItem('theme')
  if (savedTheme) {
    currentTheme.value = savedTheme
  }

  // Apply theme immediately
  applyTheme(currentTheme.value)
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

.main-content {
  flex: 1;
  margin-left: var(--sidebar-width, 250px);
  height: 100vh;
  background-color: var(--background-color);
  transition: margin-left 0.3s ease, background-color 0.3s;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.cases-container {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  overflow-x: hidden;
  scrollbar-width: thin;
  scrollbar-color: rgba(255, 255, 255, 0.3) transparent;
}

.cases-container::-webkit-scrollbar {
  width: 8px;
}

.cases-container::-webkit-scrollbar-track {
  background: transparent;
}

.cases-container::-webkit-scrollbar-thumb {
  background-color: rgba(255, 255, 255, 0.3);
  border-radius: 4px;
}

.cases-container::-webkit-scrollbar-thumb:hover {
  background-color: rgba(255, 255, 255, 0.5);
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  flex-shrink: 0;
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
  flex-shrink: 0;
}

.search-input {
  width: 100%;
  padding: 12px 20px;
  border-radius: 30px;
  border: none;
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
  box-shadow: 0 0 0 2px var(--accent-color);
}

.filter-tabs {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  overflow-x: auto;
  padding-bottom: 5px;
  flex-shrink: 0;
}

.filter-tab {
  background-color: var(--content-bg);
  color: var(--text-color);
  border: none;
  border-radius: 30px;
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
}

.filter-tab:hover:not(.active) {
  background-color: rgba(150, 75, 0, 0.1);
}

.cases-container-inner {
  display: flex;
  gap: 20px;
  flex: 1;
  overflow: hidden;
}

.cases-list {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  scrollbar-width: thin;
  scrollbar-color: rgba(255, 255, 255, 0.3) transparent;
}

.cases-list::-webkit-scrollbar {
  width: 8px;
}

.cases-list::-webkit-scrollbar-track {
  background: transparent;
}

.cases-list::-webkit-scrollbar-thumb {
  background-color: rgba(255, 255, 255, 0.3);
  border-radius: 4px;
}

.cases-list::-webkit-scrollbar-thumb:hover {
  background-color: rgba(255, 255, 255, 0.5);
}

.cases-title {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 15px;
}

.case-item {
  background-color: var(--content-bg);
  border-radius: 15px;
  padding: 15px;
  margin-bottom: 15px;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s, background-color 0.3s;
  display: flex;
  align-items: flex-start;
  gap: 15px;
  min-height: 80px;
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
  flex-shrink: 0;
  margin-top: 2px;
}

.case-icon svg {
  width: 20px;
  height: 20px;
  stroke: var(--text-color);
}

.case-details {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.case-title {
  font-size: 16px;
  font-weight: 600;
  line-height: 1.3;
  word-wrap: break-word;
  overflow-wrap: break-word;
}

.case-meta {
  display: flex;
  flex-direction: column;
  gap: 4px;
  font-size: 12px;
  color: var(--text-secondary);
}

.case-priority {
  display: flex;
  align-items: center;
  gap: 6px;
}

.case-priority span {
  white-space: nowrap;
}

.case-assigned {
  display: flex;
  align-items: center;
}

.case-assigned span {
  word-wrap: break-word;
  overflow-wrap: break-word;
}

.priority-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
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

.case-detail {
  background-color: var(--content-bg);
  border-radius: 15px;
  padding: 20px;
  width: 400px;
  flex-shrink: 0;
  overflow-y: auto;
  overflow-x: hidden;
  scrollbar-width: thin;
  scrollbar-color: rgba(255, 255, 255, 0.3) transparent;
}

.case-detail::-webkit-scrollbar {
  width: 8px;
}

.case-detail::-webkit-scrollbar-track {
  background: transparent;
}

.case-detail::-webkit-scrollbar-thumb {
  background-color: rgba(255, 255, 255, 0.3);
  border-radius: 4px;
}

.case-detail::-webkit-scrollbar-thumb:hover {
  background-color: rgba(255, 255, 255, 0.5);
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

.detail-value.high {
  color: var(--high-priority);
  font-weight: 600;
}

.detail-value.medium {
  color: var(--medium-priority);
  font-weight: 600;
}

.detail-value.low {
  color: var(--low-priority);
  font-weight: 600;
}

.detail-value.abusive {
  color: var(--high-priority);
}

/* Responsive styles */
@media (max-width: 1024px) {
  .cases-container-inner {
    flex-direction: column;
  }
  
  .case-detail {
    width: 100%;
  }
}

@media (max-width: 768px) {
  .main-content {
    margin-left: 0;
    padding: 15px;
  }
  
  .header {
    flex-direction: column;
    align-items: flex-start;
    gap: 15px;
  }
  
  .header-left {
    width: 100%;
    justify-content: space-between;
  }

  .header h1 {
    font-size: 20px;
  }

  .cases-container {
    padding: 10px;
  }

  .case-meta {
    font-size: 11px;
  }
}
</style>