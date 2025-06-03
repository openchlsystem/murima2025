<template>
  <div class="qa-statistics-page">
    <button class="mobile-menu-btn" @click="toggleMobileMenu">
      <svg fill="none" height="24" viewbox="0 0 24 24" width="24" xmlns="http://www.w3.org/2000/svg">
        <path d="M3 12H21M3 6H21M3 18H21" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" />
      </svg>
    </button>

    <div class="sidebar" :class="{ 'collapsed': isSidebarCollapsed }">
      <div class="toggle-btn" @click="toggleSidebar">
        {{ isSidebarCollapsed ? '>' : '<' }}
      </div>
      <div class="sidebar-content">
        <div class="logo-container">
          <div class="logo">
            <img src="/Openchs logo-1.png" alt="Openchs logo-1.png" />
          </div>
        </div>
        
        <router-link v-for="item in navigationItems" 
          :key="item.path"
          :to="item.path"
          class="nav-item"
          :class="{ active: currentRoute === item.path }"
        >
          <div class="nav-icon">
            <component :is="item.icon" v-if="item.icon" />
          </div>
          <div class="nav-text">{{ item.text }}</div>
        </router-link>

        <div class="user-profile">
          <router-link class="user-avatar" to="/edit-profile">
            <svg fill="currentColor" viewbox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 12C14.2091 12 16 10.2091 16 8C16 5.79086 14.2091 4 12 4C9.79086 4 8 5.79086 8 8C8 10.2091 9.79086 12 12 12Z" />
              <path d="M12 14C7.58172 14 4 17.5817 4 22H20C20 17.5817 16.4183 14 12 14Z" />
            </svg>
          </router-link>
        </div>

        <div class="status">
          <div class="status-dot" :class="{ 'online': isOnline }"></div>
          <span>Status: {{ isOnline ? 'Online' : 'Offline' }}</span>
        </div>

        <div class="button-container">
          <button class="join-queue-btn" @click="toggleQueueStatus">
            {{ isInQueue ? 'Leave Queue' : 'Join Queue' }}
          </button>
          <button class="logout-btn" @click="handleLogout">Logout</button>
        </div>
      </div>
    </div>

    <div class="main-content">
      <div class="header">
        <div class="page-title">QA Statistics</div>
        <button class="theme-toggle" @click="toggleTheme">
          <svg fill="none" height="16" viewbox="0 0 24 24" width="16" xmlns="http://www.w3.org/2000/svg">
            <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" />
          </svg>
          <span>{{ isDarkMode ? 'Light Mode' : 'Dark Mode' }}</span>
        </button>
      </div>

      <div class="filter-container">
        <select v-model="timeRange" class="filter-select" @change="handleFilterChange">
          <option value="all-time">All Time</option>
          <option value="today">Today</option>
          <option value="yesterday">Yesterday</option>
          <option value="this-week">This Week</option>
          <option value="this-month">This Month</option>
          <option value="last-month">Last Month</option>
          <option value="custom">Custom Range</option>
        </select>

        <select v-model="selectedCounselorId" class="filter-select" @change="handleFilterChange">
          <option :value="undefined">All Counselors</option>
          <option v-for="counselor in counselors" :key="counselor.id" :value="counselor.id">
            {{ counselor.name }}
          </option>
        </select>

        <select v-model="selectedSupervisorId" class="filter-select" @change="handleFilterChange">
          <option :value="undefined">All Supervisors</option>
          <option v-for="supervisor in supervisors" :key="supervisor.id" :value="supervisor.id">
            {{ supervisor.name }}
          </option>
        </select>
      </div>

      <div class="search-container">
        <span class="search-icon">
          <svg fill="none" height="16" viewbox="0 0 24 24" width="16" xmlns="http://www.w3.org/2000/svg">
            <path d="M21 21L15 15M17 10C17 13.866 13.866 17 10 17C6.13401 17 3 13.866 3 10C3 6.13401 6.13401 3 10 3C13.866 3 17 6.13401 17 10Z" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" />
          </svg>
        </span>
        <input 
          v-model="searchQuery"
          class="search-input" 
          placeholder="Search by counselor, date, or call ID..." 
          type="text"
          @input="handleSearch"
        />
      </div>

      <div class="view-tabs">
        <button 
          v-for="view in viewOptions" 
          :key="view.id"
          class="view-tab"
          :class="{ active: currentView === view.id }"
          @click="handleViewChange(view.id)"
        >
          {{ view.label }}
        </button>
      </div>

      <!-- Card View -->
      <div v-if="currentView === 'card'" class="view-container">
        <div v-if="isLoading" class="loading-state">
          <div class="spinner"></div>
          <p>Loading evaluations...</p>
        </div>
        
        <div v-else-if="error" class="error-state">
          <p>{{ error }}</p>
          <button @click="fetchData">Retry</button>
        </div>

        <div v-else-if="filteredEvaluations.length === 0" class="empty-state">
          <p>No evaluations found</p>
          <button @click="openAddEvaluationModal">Add New Evaluation</button>
        </div>

        <div v-else class="qa-cards-container">
          <div 
            v-for="evaluation in filteredEvaluations" 
            :key="evaluation.id"
            class="qa-card"
          >
            <div class="qa-card-header">
              <div class="qa-card-avatar">
                <img :alt="evaluation.counselorName" :src="getCounselorAvatar(evaluation.counselorId)" />
              </div>
              <div class="qa-card-user-info">
                <div class="qa-card-name">{{ evaluation.counselorName }}</div>
                <div class="qa-card-calls">{{ evaluation.callsEvaluated }} calls evaluated</div>
              </div>
              <div class="qa-card-score" :class="getScoreClass(evaluation.score)">
                {{ evaluation.score }}%
              </div>
            </div>
            <div class="qa-card-details">
              <div class="qa-card-detail">
                <div class="qa-card-detail-label">Talk Time</div>
                <div class="qa-card-detail-value">{{ evaluation.talkTime }}</div>
              </div>
              <div class="qa-card-detail">
                <div class="qa-card-detail-label">Supervisor</div>
                <div class="qa-card-detail-value">{{ evaluation.supervisorName }}</div>
              </div>
            </div>
            <div class="qa-card-actions">
              <button class="qa-card-btn edit" @click="editEvaluation(evaluation)">
                <svg fill="none" height="16" viewbox="0 0 24 24" width="16" xmlns="http://www.w3.org/2000/svg">
                  <path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" />
                  <path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" />
                </svg>
                Edit
              </button>
              <button class="qa-card-btn delete" @click="confirmDeleteEvaluation(evaluation)">
                <svg fill="none" height="16" viewbox="0 0 24 24" width="16" xmlns="http://www.w3.org/2000/svg">
                  <path d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" />
                </svg>
                Delete
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- List View -->
      <div v-else-if="currentView === 'list'" class="view-container">
        <div class="qa-list-container">
          <table class="qa-table">
            <thead>
              <tr>
                <th>Counselor</th>
                <th>Score</th>
                <th>Calls</th>
                <th>Talk Time</th>
                <th>Supervisor</th>
                <th>Date</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="evaluation in filteredEvaluations" :key="evaluation.id">
                <td>
                  <div class="counselor-cell">
                    <img :alt="evaluation.counselorName" :src="getCounselorAvatar(evaluation.counselorId)" />
                    {{ evaluation.counselorName }}
                  </div>
                </td>
                <td>
                  <span :class="getScoreClass(evaluation.score)">{{ evaluation.score }}%</span>
                </td>
                <td>{{ evaluation.callsEvaluated }}</td>
                <td>{{ evaluation.talkTime }}</td>
                <td>{{ evaluation.supervisorName }}</td>
                <td>{{ formatDate(evaluation.date) }}</td>
                <td>
                  <button @click="editEvaluation(evaluation)">Edit</button>
                  <button @click="confirmDeleteEvaluation(evaluation)">Delete</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Reports View -->
      <div v-else-if="currentView === 'reports'" class="view-container">
        <div class="reports-container">
          <div class="report-card">
            <h3>Overall Performance</h3>
            <div class="report-value">{{ averageScore }}%</div>
            <div class="report-chart">
              <!-- Add chart component here -->
            </div>
          </div>
          <div class="report-card">
            <h3>Top Performers</h3>
            <div class="top-performers">
              <div v-for="(counselor, index) in topPerformers" :key="counselor.id" class="performer">
                <span class="rank">{{ index + 1 }}</span>
                <span class="name">{{ counselor.name }}</span>
                <span class="score">{{ counselor.score }}%</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Analytics View -->
      <div v-else-if="currentView === 'analytics'" class="view-container">
        <div class="analytics-container">
          <div class="analytics-card">
            <h3>Score Distribution</h3>
            <div class="analytics-chart">
              <!-- Add chart component here -->
            </div>
          </div>
          <div class="analytics-card">
            <h3>Trend Analysis</h3>
            <div class="analytics-chart">
              <!-- Add chart component here -->
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Add/Edit Evaluation Modal -->
    <div v-if="showModal" class="modal">
      <div class="modal-content">
        <h2>{{ isEditing ? 'Edit Evaluation' : 'Add New Evaluation' }}</h2>
        <form @submit.prevent="handleEvaluationSubmit">
          <div class="form-group">
            <label for="counselor">Counselor</label>
            <select id="counselor" v-model="evaluationForm.counselorId" required>
              <option v-for="counselor in counselors" :key="counselor.id" :value="counselor.id">
                {{ counselor.name }}
              </option>
            </select>
          </div>
          <div class="form-group">
            <label for="supervisor">Supervisor</label>
            <select id="supervisor" v-model="evaluationForm.supervisorId" required>
              <option v-for="supervisor in supervisors" :key="supervisor.id" :value="supervisor.id">
                {{ supervisor.name }}
              </option>
            </select>
          </div>
          <div class="form-group">
            <label for="score">Score (%)</label>
            <input 
              id="score"
              v-model.number="evaluationForm.score"
              type="number"
              min="0"
              max="100"
              required
            />
          </div>
          <div class="form-group">
            <label for="calls">Calls Evaluated</label>
            <input 
              id="calls"
              v-model.number="evaluationForm.callsEvaluated"
              type="number"
              min="1"
              required
            />
          </div>
          <div class="form-group">
            <label for="talkTime">Talk Time</label>
            <input 
              id="talkTime"
              v-model="evaluationForm.talkTime"
              type="text"
              required
            />
          </div>
          <div class="form-group">
            <label for="notes">Notes</label>
            <textarea
              id="notes"
              v-model="evaluationForm.notes"
            ></textarea>
          </div>
          <div class="modal-actions">
            <button type="button" @click="closeModal">Cancel</button>
            <button type="submit">{{ isEditing ? 'Save Changes' : 'Add Evaluation' }}</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteModal" class="modal">
      <div class="modal-content">
        <h2>Confirm Delete</h2>
        <p>Are you sure you want to delete this evaluation? This action cannot be undone.</p>
        <div class="modal-actions">
          <button @click="closeDeleteModal">Cancel</button>
          <button class="delete-btn" @click="handleDeleteEvaluation">Delete</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { format } from 'date-fns'
import type { QAEvaluation } from '../types/qa'
import { useQAStore } from '../stores/qa'
import { useAuthStore } from '../stores/auth'
import { useNotificationStore } from '../stores/notification'

// Store instances
const qaStore = useQAStore()
const authStore = useAuthStore()
const notificationStore = useNotificationStore()

// Router and route
const router = useRouter()
const route = useRoute()

// State
const isSidebarCollapsed = ref(false)
const isOnline = ref(true)
const isInQueue = ref(false)
const isDarkMode = ref(false)
const searchQuery = ref('')
const currentView = ref('card')
const timeRange = ref('this-week')
const selectedCounselorId = ref<number | undefined>()
const selectedSupervisorId = ref<number | undefined>()
const showModal = ref(false)
const showDeleteModal = ref(false)
const isEditing = ref(false)
const selectedEvaluation = ref<QAEvaluation | null>(null)

// Form state
const evaluationForm = ref({
  counselorId: 0,
  supervisorId: 0,
  score: 0,
  callsEvaluated: 1,
  talkTime: '',
  notes: '',
  date: new Date()
})

// Navigation items
const navigationItems = [
  { path: '/dashboard', text: 'Dashboard', icon: 'DashboardIcon' },
  { path: '/calls', text: 'Calls', icon: 'CallsIcon' },
  { path: '/cases', text: 'Cases', icon: 'CasesIcon' },
  { path: '/chats', text: 'Chats', icon: 'ChatsIcon' },
  { path: '/qa-statistics', text: 'QA Statistics', icon: 'QAIcon' },
  { path: '/wallboard', text: 'Wallboard', icon: 'WallboardIcon' },
  { path: '/settings', text: 'Settings', icon: 'SettingsIcon' }
]

// View options
const viewOptions = [
  { id: 'card', label: 'Card View' },
  { id: 'list', label: 'List View' },
  { id: 'reports', label: 'Reports' },
  { id: 'analytics', label: 'Analytics' }
]

// Computed
const currentRoute = computed(() => route.path)
const isLoading = computed(() => qaStore.loading)
const error = computed(() => qaStore.error)
const counselors = computed(() => qaStore.counselors)
const supervisors = computed(() => qaStore.supervisors)
const filteredEvaluations = computed(() => qaStore.filteredEvaluations)
const averageScore = computed(() => qaStore.averageScore)

const topPerformers = computed(() => {
  const counselorScores = new Map<number, { name: string; totalScore: number; count: number }>()
  
  qaStore.evaluations.forEach(evaluation => {
    const current = counselorScores.get(evaluation.counselorId) || { 
      name: evaluation.counselorName, 
      totalScore: 0, 
      count: 0 
    }
    current.totalScore += evaluation.score
    current.count++
    counselorScores.set(evaluation.counselorId, current)
  })

  return Array.from(counselorScores.entries())
    .map(([id, data]) => ({
      id,
      name: data.name,
      score: Math.round(data.totalScore / data.count)
    }))
    .sort((a, b) => b.score - a.score)
    .slice(0, 5)
})

// Methods
const toggleMobileMenu = () => {
  isSidebarCollapsed.value = !isSidebarCollapsed.value
}

const toggleSidebar = () => {
  isSidebarCollapsed.value = !isSidebarCollapsed.value
}

const toggleQueueStatus = () => {
  isInQueue.value = !isInQueue.value
}

const toggleTheme = () => {
  isDarkMode.value = !isDarkMode.value
  // TODO: Implement theme switching logic
}

const handleLogout = async () => {
  try {
    await authStore.logout()
    router.push('/login')
  } catch (error) {
    notificationStore.error('Failed to logout. Please try again.')
  }
}

const fetchData = async () => {
  try {
    await Promise.all([
      qaStore.fetchEvaluations(),
      qaStore.fetchCounselors(),
      qaStore.fetchSupervisors()
    ])
  } catch (error) {
    notificationStore.error('Failed to load data. Please try again.')
  }
}

const handleFilterChange = () => {
  qaStore.setFilter({
    timeRange: timeRange.value,
    counselorId: selectedCounselorId.value,
    supervisorId: selectedSupervisorId.value
  })
}

const handleSearch = () => {
  // TODO: Implement search functionality
}

const handleViewChange = (viewId: string) => {
  currentView.value = viewId
}

const getCounselorAvatar = (counselorId: number) => {
  const counselor = counselors.value.find(c => c.id === counselorId)
  return counselor?.avatar || '/placeholder.svg?height=50&width=50'
}

const getScoreClass = (score: number) => {
  if (score >= 80) return 'score-high'
  if (score >= 60) return 'score-medium'
  return 'score-low'
}

const formatDate = (date: string | Date) => {
  return format(new Date(date), 'MMM d, yyyy')
}

const openAddEvaluationModal = () => {
  isEditing.value = false
  evaluationForm.value = {
    counselorId: 0,
    supervisorId: 0,
    score: 0,
    callsEvaluated: 1,
    talkTime: '',
    notes: '',
    date: new Date()
  }
  showModal.value = true
}

const editEvaluation = (evaluation: QAEvaluation) => {
  isEditing.value = true
  selectedEvaluation.value = evaluation
  evaluationForm.value = {
    counselorId: evaluation.counselorId,
    supervisorId: evaluation.supervisorId,
    score: evaluation.score,
    callsEvaluated: evaluation.callsEvaluated,
    talkTime: evaluation.talkTime,
    notes: evaluation.notes || '',
    date: new Date(evaluation.date)
  }
  showModal.value = true
}

const confirmDeleteEvaluation = (evaluation: QAEvaluation) => {
  selectedEvaluation.value = evaluation
  showDeleteModal.value = true
}

const closeModal = () => {
  showModal.value = false
  evaluationForm.value = {
    counselorId: 0,
    supervisorId: 0,
    score: 0,
    callsEvaluated: 1,
    talkTime: '',
    notes: '',
    date: new Date()
  }
  selectedEvaluation.value = null
}

const closeDeleteModal = () => {
  showDeleteModal.value = false
  selectedEvaluation.value = null
}

const handleEvaluationSubmit = async () => {
  try {
    if (isEditing.value && selectedEvaluation.value) {
      await qaStore.updateEvaluation(selectedEvaluation.value.id, evaluationForm.value)
      notificationStore.success('Evaluation updated successfully')
    } else {
      const newEvaluation = {
        id: Date.now(),
        date: new Date(evaluationForm.value.date),
        counselorName: counselors.value.find(c => c.id === evaluationForm.value.counselorId)?.name,
        supervisorName: supervisors.value.find(s => s.id === evaluationForm.value.supervisorId)?.name,
        counselorId: evaluationForm.value.counselorId,
        supervisorId: evaluationForm.value.supervisorId,
        score: evaluationForm.value.score,
        callsEvaluated: evaluationForm.value.callsEvaluated,
        talkTime: evaluationForm.value.talkTime,
        notes: evaluationForm.value.notes
      }
      await qaStore.addEvaluation(newEvaluation)
      notificationStore.success('Evaluation created successfully')
    }
    closeModal()
  } catch (error) {
    notificationStore.error('Failed to save evaluation. Please try again.')
  }
}

const handleDeleteEvaluation = async () => {
  if (!selectedEvaluation.value) return
  
  try {
    await qaStore.deleteEvaluation(selectedEvaluation.value.id)
    notificationStore.success('Evaluation deleted successfully')
    closeDeleteModal()
  } catch (error) {
    notificationStore.error('Failed to delete evaluation. Please try again.')
  }
}

// Lifecycle hooks
onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.qa-statistics-page {
  display: flex;
  min-height: 100vh;
  background-color: var(--background-color);
  color: var(--text-color);
}

.sidebar {
  width: 250px;
  background-color: var(--sidebar-bg);
  transition: width 0.3s ease;
}

.sidebar.collapsed {
  width: 60px;
}

.main-content {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-title {
  font-size: 24px;
  font-weight: 600;
}

.theme-toggle {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: none;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  color: var(--text-color);
  cursor: pointer;
}

.filter-container {
  display: flex;
  gap: 16px;
  margin-bottom: 20px;
}

.filter-select {
  padding: 8px 12px;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  background-color: var(--input-bg);
  color: var(--text-color);
  min-width: 150px;
}

.search-container {
  position: relative;
  margin-bottom: 20px;
}

.search-icon {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-secondary);
}

.search-input {
  width: 100%;
  padding: 8px 12px 8px 36px;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  background-color: var(--input-bg);
  color: var(--text-color);
}

.view-tabs {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.view-tab {
  padding: 8px 16px;
  border-radius: 8px;
  cursor: pointer;
  background-color: var(--content-bg);
  border: none;
  color: var(--text-color);
}

.view-tab.active {
  background-color: var(--accent-color);
  color: white;
}

/* Card View */
.qa-cards-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.qa-card {
  background-color: var(--content-bg);
  border-radius: 12px;
  padding: 20px;
  transition: transform 0.2s ease;
}

.qa-card:hover {
  transform: translateY(-2px);
}

.qa-card-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.qa-card-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  overflow: hidden;
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
  font-weight: 600;
  font-size: 16px;
}

.qa-card-calls {
  font-size: 14px;
  color: var(--text-secondary);
}

.qa-card-score {
  font-weight: 600;
  font-size: 18px;
  padding: 4px 8px;
  border-radius: 12px;
}

.score-high {
  background-color: var(--success-color);
  color: white;
}

.score-medium {
  background-color: var(--warning-color);
  color: white;
}

.score-low {
  background-color: var(--error-color);
  color: white;
}

.qa-card-details {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-bottom: 16px;
}

.qa-card-detail-label {
  font-size: 12px;
  color: var(--text-secondary);
}

.qa-card-detail-value {
  font-weight: 500;
}

.qa-card-actions {
  display: flex;
  gap: 8px;
}

.qa-card-btn {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 6px 12px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
}

.qa-card-btn.edit {
  background-color: var(--accent-color);
  color: white;
}

.qa-card-btn.delete {
  background-color: var(--error-color);
  color: white;
}

/* List View */
.qa-list-container {
  background-color: var(--content-bg);
  border-radius: 12px;
  overflow: hidden;
}

.qa-table {
  width: 100%;
  border-collapse: collapse;
}

.qa-table th,
.qa-table td {
  padding: 12px 16px;
  text-align: left;
  border-bottom: 1px solid var(--border-color);
}

.qa-table th {
  background-color: var(--sidebar-bg);
  font-weight: 600;
}

.qa-table tr:last-child td {
  border-bottom: none;
}

.counselor-cell {
  display: flex;
  align-items: center;
  gap: 8px;
}

.counselor-cell img {
  width: 32px;
  height: 32px;
  border-radius: 50%;
}

/* Reports View */
.reports-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.report-card {
  background-color: var(--content-bg);
  border-radius: 12px;
  padding: 20px;
}

.report-value {
  font-size: 36px;
  font-weight: 600;
  margin: 16px 0;
}

.top-performers {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.performer {
  display: flex;
  align-items: center;
  gap: 12px;
}

.rank {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--accent-color);
  color: white;
  border-radius: 50%;
  font-weight: 600;
}

/* Analytics View */
.analytics-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 20px;
}

.analytics-card {
  background-color: var(--content-bg);
  border-radius: 12px;
  padding: 20px;
}

.analytics-chart {
  height: 300px;
  margin-top: 16px;
}

/* Loading state */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
}

.spinner {
  border: 4px solid var(--border-color);
  border-top: 4px solid var(--accent-color);
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Error state */
.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  padding: 40px;
  text-align: center;
}

/* Empty state */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  padding: 40px;
  text-align: center;
}

/* Modal styles */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background-color: var(--content-bg);
  padding: 24px;
  border-radius: 12px;
  width: 100%;
  max-width: 500px;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  background-color: var(--input-bg);
  color: var(--text-color);
}

.form-group textarea {
  min-height: 100px;
  resize: vertical;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 24px;
}

.modal-actions button {
  padding: 8px 16px;
  border-radius: 8px;
  cursor: pointer;
}

.modal-actions button:last-child {
  background-color: var(--accent-color);
  color: white;
  border: none;
}

.delete-btn {
  background-color: var(--error-color) !important;
}

/* Mobile menu button */
.mobile-menu-btn {
  display: none;
  background: none;
  border: none;
  color: var(--text-color);
  cursor: pointer;
  padding: 8px;
}

@media (max-width: 768px) {
  .mobile-menu-btn {
    display: block;
  }

  .sidebar {
    position: fixed;
    left: -250px;
    height: 100vh;
    z-index: 1000;
  }

  .sidebar.active {
    left: 0;
  }

  .filter-container {
    flex-direction: column;
  }

  .filter-select {
    width: 100%;
  }

  .qa-cards-container {
    grid-template-columns: 1fr;
  }

  .analytics-container {
    grid-template-columns: 1fr;
  }
}
</style>
