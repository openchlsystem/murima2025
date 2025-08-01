<template>
  <div class="app-container" :data-theme="currentTheme">
    <SidePanel 
      :userRole="userRole" 
      :isInQueue="isInQueue" 
      :isProcessingQueue="isProcessingQueue" 
      :currentCall="currentCall" 
      @toggle-queue="handleQueueToggle" 
      @logout="handleLogout" 
      @sidebar-toggle="handleSidebarToggle" 
    />
    
    <div class="main-content" :class="{ 'sidebar-collapsed': isSidebarCollapsed }">
      <div class="header">
        <div class="page-title">Counselor Wallboard</div>
        <div class="header-actions">
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

      <div class="wallboard-main-content">
        <!-- Filter Controls -->
      <div class="filter-container">
          <select class="filter-select glass-btn" v-model="selectedTimeRange">
            <option value="today">Today</option>
            <option value="yesterday">Yesterday</option>
            <option value="this-week" selected>This Week</option>
            <option value="this-month">This Month</option>
            <option value="last-month">Last Month</option>
            <option value="custom">Custom Range</option>
        </select>
          <select class="filter-select glass-btn" v-model="selectedTeam">
            <option value="all-teams">All Teams</option>
            <option value="crisis-response">Crisis Response</option>
            <option value="counseling">Counseling Services</option>
            <option value="legal">Legal Services</option>
            <option value="housing">Housing & Resources</option>
        </select>
      </div>

        <!-- Dashboard Cards -->
      <div class="dashboard-grid">
        <div class="dashboard-card glass-card fine-border">
          <div class="card-header">
              <div class="card-title">Total Calls</div>
            <div class="card-icon">
                <svg fill="none" height="24" viewBox="0 0 24 24" width="24">
                  <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"/>
              </svg>
            </div>
          </div>
            <div class="card-value">1,248</div>
            <div class="card-subtitle">+12% from last week</div>
          </div>

        <div class="dashboard-card glass-card fine-border">
          <div class="card-header">
              <div class="card-title">Average Call Duration</div>
            <div class="card-icon">
                <svg fill="none" height="24" viewBox="0 0 24 24" width="24">
                  <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"/>
                  <polyline points="12 6 12 12 16 14" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"/>
              </svg>
            </div>
          </div>
            <div class="card-value">14:32</div>
            <div class="card-subtitle">-2:15 from last week</div>
          </div>

        <div class="dashboard-card glass-card fine-border">
          <div class="card-header">
              <div class="card-title">Average QA Score</div>
            <div class="card-icon">
                <svg fill="none" height="24" viewBox="0 0 24 24" width="24">
                  <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"/>
                  <polyline points="22 4 12 14.01 9 11.01" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"/>
              </svg>
            </div>
          </div>
            <div class="card-value">87%</div>
            <div class="card-subtitle">+5% from last week</div>
          </div>

        <div class="dashboard-card glass-card fine-border">
          <div class="card-header">
              <div class="card-title">Achievements Unlocked</div>
            <div class="card-icon">
                <svg fill="none" height="24" viewBox="0 0 24 24" width="24">
                  <circle cx="12" cy="8" r="7" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"/>
                  <polyline points="8.21 13.89 7 23 12 20 17 23 15.79 13.88" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"/>
              </svg>
            </div>
          </div>
            <div class="card-value">32</div>
            <div class="card-subtitle">+3 new this week</div>
          </div>
          </div>

        <!-- Leaderboard Section -->
        <div class="leaderboard-section glass-card fine-border">
        <div class="section-header">
            <div class="section-title">Counselor Leaderboard</div>
          <div class="leaderboard-tabs">
              <button 
                v-for="tab in leaderboardTabs" 
                :key="tab.id"
                :class="['leaderboard-tab', { active: activeLeaderboardTab === tab.id }]"
                @click="activeLeaderboardTab = tab.id"
              >
                {{ tab.name }}
            </button>
          </div>
        </div>
          
        <div class="leaderboard">
            <div v-for="(counselor, index) in leaderboardData" :key="counselor.id" class="leaderboard-item">
              <div :class="['leaderboard-rank', `rank-${index + 1}`]">{{ index + 1 }}</div>
            <div class="leaderboard-avatar">
                <img :alt="counselor.name" :src="counselor.avatar" @error="counselor.avatar = null" />
            </div>
            <div class="leaderboard-info">
                <div class="leaderboard-name">{{ counselor.name }}</div>
              <div class="leaderboard-stats">
                <div class="leaderboard-stat">
                    <svg fill="none" height="12" viewBox="0 0 24 24" width="12">
                      <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"/>
                  </svg>
                    {{ counselor.calls }} calls
                </div>
                <div class="leaderboard-stat">
                    <svg fill="none" height="12" viewBox="0 0 24 24" width="12">
                      <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"/>
                      <polyline points="12 6 12 12 16 14" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"/>
                  </svg>
                    Avg {{ counselor.avgTime }}
                </div>
              </div>
                <div v-if="counselor.achievement" class="achievement-badge">
                  <svg class="badge-icon" fill="none" viewBox="0 0 24 24">
                    <path d="M12 15C15.866 15 19 11.866 19 8C19 4.13401 15.866 1 12 1C8.13401 1 5 4.13401 5 8C5 11.866 8.13401 15 12 15Z" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"/>
                    <path d="M8.21 13.89L7 23L12 20L17 23L15.79 13.88" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"/>
                </svg>
                  {{ counselor.achievement }}
              </div>
            </div>
              <div class="leaderboard-score">{{ counselor.calls }}</div>
            </div>
          </div>
            </div>

        <!-- Charts Section -->
      <div class="charts-section">
          <div class="chart-container glass-card fine-border">
          <div class="chart-header">
              <div class="chart-title">Call Volume by Day</div>
              <div class="chart-subtitle">Last 7 days</div>
          </div>
          <div class="chart">
              <div v-for="(day, index) in callVolumeData" :key="day.name" class="chart-bar" :style="{ height: day.percentage + '%' }">
                <div class="chart-bar-label">{{ day.name }}</div>
                <div class="chart-bar-value">{{ day.value }}</div>
              </div>
              </div>
            </div>

          <div class="chart-container glass-card fine-border">
          <div class="chart-header">
              <div class="chart-title">Call Categories Distribution</div>
              <div class="chart-subtitle">This week</div>
          </div>
          <div class="pie-chart">
              <svg width="250" height="250" viewBox="0 0 250 250">
                <circle cx="125" cy="125" r="100" fill="none" stroke="#4CAF50" stroke-width="50" stroke-dasharray="157 628" stroke-dashoffset="0"/>
                <circle cx="125" cy="125" r="100" fill="none" stroke="#4CAF50" stroke-width="50" stroke-dasharray="188 628" stroke-dashoffset="-157"/>
                <circle cx="125" cy="125" r="100" fill="none" stroke="#2196F3" stroke-width="50" stroke-dasharray="94 628" stroke-dashoffset="-345"/>
                <circle cx="125" cy="125" r="100" fill="none" stroke="#FFC107" stroke-width="50" stroke-dasharray="94 628" stroke-dashoffset="-439"/>
                <circle cx="125" cy="125" r="100" fill="none" stroke="#9C27B0" stroke-width="50" stroke-dasharray="94 628" stroke-dashoffset="-533"/>
              </svg>
              <div class="pie-chart-center">1,248</div>
          </div>
          <div class="pie-chart-legend">
              <div v-for="category in callCategories" :key="category.name" class="legend-item">
                <div :class="['legend-color', `legend-color-${category.id}`]"></div>
                <span>{{ category.name }} ({{ category.percentage }}%)</span>
              </div>
            </div>
              </div>
            </div>

        <!-- Achievements Section -->
        <div class="achievements-section glass-card fine-border">
        <div class="section-header">
            <div class="section-title">Available Achievements</div>
        </div>
        <div class="achievements-grid">
            <div v-for="achievement in achievements" :key="achievement.id" :class="['achievement-card', { 'achievement-unlocked': achievement.completed }]">
            <div class="achievement-icon">
                <svg fill="none" height="24" viewBox="0 0 24 24" width="24">
                  <path d="M12 15C15.866 15 19 11.866 19 8C19 4.13401 15.866 1 12 1C8.13401 1 5 4.13401 5 8C5 11.866 8.13401 15 12 15Z" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"/>
                  <path d="M8.21 13.89L7 23L12 20L17 23L15.79 13.88" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"/>
              </svg>
            </div>
              <div class="achievement-title">{{ achievement.title }}</div>
              <div class="achievement-description">{{ achievement.description }}</div>
            <div class="achievement-progress">
                <div class="achievement-progress-bar" :style="{ width: achievement.progress + '%' }"></div>
              </div>
              <div class="achievement-progress-text">{{ achievement.progressText }}</div>
            </div>
            </div>
          </div>
            </div>
    </div>
  </div>
</template>

<script setup>
import SidePanel from '../components/SidePanel.vue'
import { ref, computed, onMounted } from 'vue'
import { useThemeStore } from '../stores/theme.js'

// Theme store
const themeStore = useThemeStore()

// Reactive state
const currentTheme = computed(() => themeStore.currentTheme)
const selectedTimeRange = ref('this-week')
const selectedTeam = ref('all-teams')
const activeLeaderboardTab = ref('call-volume')

// Sidebar state
const isSidebarCollapsed = ref(false)
const userRole = ref('user')
const isInQueue = ref(false)
const isProcessingQueue = ref(false)
const currentCall = ref(null)

// Leaderboard tabs
const leaderboardTabs = ref([
  { id: 'call-volume', name: 'Call Volume' },
  { id: 'qa-scores', name: 'QA Scores' },
  { id: 'resolution-rate', name: 'Resolution Rate' }
])

// Leaderboard data
const leaderboardData = ref([
  {
    id: 1,
    name: 'Sarah Mitchell',
    avatar: '/placeholder.svg?height=40&width=40',
    calls: 187,
    avgTime: '16:42',
    achievement: 'Call Champion'
  },
  {
    id: 2,
    name: 'Robert Jackson',
    avatar: '/placeholder.svg?height=40&width=40',
    calls: 165,
    avgTime: '15:18',
    achievement: 'Empathy Expert'
  },
  {
    id: 3,
    name: 'Emily Chan',
    avatar: '/placeholder.svg?height=40&width=40',
    calls: 142,
    avgTime: '18:05',
    achievement: 'Resolution Pro'
  },
  {
    id: 4,
    name: 'Michael Lee',
    avatar: '/placeholder.svg?height=40&width=40',
    calls: 128,
    avgTime: '12:47'
  },
  {
    id: 5,
    name: 'Patience Williams',
    avatar: '/placeholder.svg?height=40&width=40',
    calls: 115,
    avgTime: '14:32'
  }
])

// Call volume data
const callVolumeData = ref([
  { name: 'Mon', value: 156, percentage: 60 },
  { name: 'Tue', value: 195, percentage: 75 },
  { name: 'Wed', value: 221, percentage: 85 },
  { name: 'Thu', value: 182, percentage: 70 },
  { name: 'Fri', value: 234, percentage: 90 },
  { name: 'Sat', value: 130, percentage: 50 },
  { name: 'Sun', value: 117, percentage: 45 }
])

// Call categories data
const callCategories = ref([
  { id: 1, name: 'Domestic Violence', percentage: 25, color: '#4CAF50' },
  { id: 2, name: 'Sexual Assault', percentage: 30, color: '#2196F3' },
  { id: 3, name: 'Human Trafficking', percentage: 15, color: '#FFC107' },
  { id: 4, name: 'Child Abuse', percentage: 15, color: '#9C27B0' },
  { id: 5, name: 'Other', percentage: 15, color: '#FF5722' }
])

// Achievements data
const achievements = ref([
  {
    id: 1,
    title: 'Call Champion',
    description: 'Handle 100+ calls in a week',
    progress: 100,
    progressText: 'Completed!',
    completed: true
  },
  {
    id: 2,
    title: 'Empathy Expert',
    description: 'Maintain 90%+ listening score for 30 days',
    progress: 75,
    progressText: '75% Complete',
    completed: false
  },
  {
    id: 3,
    title: 'Resolution Pro',
    description: 'Resolve 50 cases with 90%+ satisfaction',
    progress: 60,
    progressText: '30/50 Cases',
    completed: false
  },
  {
    id: 4,
    title: 'Five-Star Support',
    description: 'Receive 25 five-star ratings from callers',
    progress: 40,
    progressText: '10/25 Ratings',
    completed: false
  },
  {
    id: 5,
    title: 'First Responder',
    description: 'Answer 20 emergency priority calls',
    progress: 85,
    progressText: '17/20 Calls',
    completed: false
  },
  {
    id: 6,
    title: 'Team Player',
    description: 'Assist 15 colleagues with their cases',
    progress: 100,
    progressText: 'Completed!',
    completed: true
  }
])

// Methods
const toggleTheme = () => {
  themeStore.toggleTheme()
}

const handleQueueToggle = () => {
  isInQueue.value = !isInQueue.value
}

const handleLogout = () => {
  // Handle logout logic
}

const handleSidebarToggle = (collapsed) => {
  isSidebarCollapsed.value = collapsed
}

// Lifecycle
onMounted(() => {
  // Theme is already initialized in main.js
})
</script>

<style scoped>
.app-container {
  min-height: 100vh;
  background: var(--background-color);
  color: var(--text-color);
}

.main-content {
  margin-left: 250px;
  width: calc(100% - 250px);
  min-height: 100vh;
  background: var(--background-color);
  transition: margin-left 0.3s, width 0.3s;
}

.main-content.sidebar-collapsed {
  margin-left: 20px;
  width: calc(100% - 20px);
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 2rem 2.5rem 1.5rem 2.5rem;
  background: transparent;
  border-bottom: 1px solid var(--border-color);
  position: sticky;
  top: 0;
  z-index: 10;
}

.page-title {
  font-size: 2rem;
  font-weight: 800;
  color: var(--accent-color);
  letter-spacing: 1px;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.theme-toggle {
  background: var(--content-bg);
  border: 1px solid var(--border-color);
  border-radius: 24px;
  padding: 0.5rem 1rem;
  font-weight: 700;
  color: var(--text-color);
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  transition: background 0.2s, border 0.2s;
}

.theme-toggle:hover {
  background: var(--card-bg);
  border-color: var(--accent-color);
}

.wallboard-main-content {
  padding: 2rem 2.5rem;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.filter-container {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}

.filter-select {
  padding: 0.5rem 1rem;
  border-radius: 12px;
  border: 1px solid var(--border-color);
  background: var(--content-bg);
  color: var(--text-color);
  font-size: 0.9rem;
  cursor: pointer;
  outline: none;
  transition: border-color 0.2s;
}

.filter-select:focus {
  border-color: var(--accent-color);
}

.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.dashboard-card {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-title {
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-color);
}

.card-icon {
  width: 40px;
  height: 40px;
  background: rgba(150, 75, 0, 0.1);
  border-radius: 10px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.card-icon svg {
  width: 24px;
  height: 24px;
  stroke: var(--accent-color);
}

.card-value {
  font-size: 2rem;
  font-weight: 700;
  color: var(--accent-color);
}

.card-subtitle {
  font-size: 0.9rem;
  color: var(--text-secondary);
}

.leaderboard-section {
  padding: 2rem;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--accent-color);
}

.leaderboard-tabs {
  display: flex;
  gap: 0.5rem;
}

.leaderboard-tab {
  padding: 0.5rem 1rem;
  border-radius: 12px;
  background: transparent;
  color: var(--text-secondary);
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
}

.leaderboard-tab.active {
  color: var(--accent-color);
  background: rgba(150, 75, 0, 0.1);
}

.leaderboard {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.leaderboard-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  border-radius: 12px;
  background: var(--content-bg);
  transition: background 0.2s;
}

.leaderboard-item:hover {
  background: var(--card-bg);
}

.leaderboard-rank {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.9rem;
}

.rank-1 {
  background: #FFD700;
  color: #000;
}

.rank-2 {
  background: #C0C0C0;
  color: #000;
}

.rank-3 {
  background: #CD7F32;
  color: #fff;
}

.rank-4, .rank-5 {
  background: var(--border-color);
  color: var(--text-color);
}

.leaderboard-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  overflow: hidden;
}

.leaderboard-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.leaderboard-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.leaderboard-name {
  font-weight: 700;
  color: var(--accent-color);
}

.leaderboard-stats {
  display: flex;
  gap: 1rem;
  font-size: 0.9rem;
  color: var(--text-secondary);
}

.leaderboard-stat {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.achievement-badge {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.8rem;
  color: var(--accent-color);
  font-weight: 600;
}

.badge-icon {
  width: 16px;
  height: 16px;
}

.leaderboard-score {
  font-weight: 700;
  color: var(--accent-color);
  font-size: 1.2rem;
}

.charts-section {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  margin-bottom: 2rem;
}

.chart-container {
  padding: 2rem;
}

.chart-header {
  margin-bottom: 1.5rem;
}

.chart-title {
  font-size: 1.2rem;
  font-weight: 700;
  margin-bottom: 0.25rem;
}

.chart-subtitle {
  font-size: 0.9rem;
  color: var(--text-secondary);
}

.chart {
  height: 300px;
  display: flex;
  align-items: flex-end;
  gap: 0.5rem;
  padding-top: 2rem;
}

.chart-bar {
  flex: 1;
  background: var(--accent-color);
  border-radius: 4px 4px 0 0;
  position: relative;
  min-width: 30px;
  transition: height 0.5s ease;
}

.chart-bar-label {
  position: absolute;
  top: -1.5rem;
  left: 0;
  right: 0;
  text-align: center;
  font-size: 0.8rem;
  font-weight: 500;
}

.chart-bar-value {
  position: absolute;
  bottom: 0.25rem;
  left: 0;
  right: 0;
  text-align: center;
  font-size: 0.8rem;
  font-weight: 700;
  color: white;
}

.pie-chart {
  position: relative;
  width: 250px;
  height: 250px;
  margin: 0 auto;
}

.pie-chart svg {
  position: absolute;
  top: 0;
  left: 0;
}

.pie-chart-center {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 100px;
  height: 100px;
  background: var(--content-bg);
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 1.2rem;
  font-weight: 700;
}

.pie-chart-legend {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-top: 1.5rem;
  justify-content: center;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
}

.legend-color {
  width: 12px;
  height: 12px;
  border-radius: 2px;
}

.legend-color-1 { background: #4CAF50; }
.legend-color-2 { background: #2196F3; }
.legend-color-3 { background: #FFC107; }
.legend-color-4 { background: #9C27B0; }
.legend-color-5 { background: #FF5722; }

.achievements-section {
  padding: 2rem;
}

.achievements-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-top: 1.5rem;
}

.achievement-card {
  padding: 1.5rem;
  border-radius: 12px;
  background: var(--content-bg);
  transition: background 0.2s;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.achievement-card:hover {
  background: var(--card-bg);
}

.achievement-card.achievement-unlocked {
  border: 2px solid var(--accent-color);
}

.achievement-icon {
  width: 48px;
  height: 48px;
  background: rgba(150, 75, 0, 0.1);
  border-radius: 12px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.achievement-icon svg {
  width: 24px;
  height: 24px;
  stroke: var(--accent-color);
}

.achievement-title {
  font-weight: 700;
  color: var(--text-color);
}

.achievement-description {
  font-size: 0.9rem;
  color: var(--text-secondary);
}

.achievement-progress {
  height: 8px;
  background: var(--border-color);
  border-radius: 4px;
  overflow: hidden;
}

.achievement-progress-bar {
  height: 100%;
  background: var(--accent-color);
  border-radius: 4px;
  transition: width 0.3s ease;
}

.achievement-progress-text {
  font-size: 0.8rem;
  color: var(--accent-color);
  font-weight: 600;
}

@media (max-width: 1200px) {
  .charts-section {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 900px) {
  .main-content {
    margin-left: 0;
    width: 100%;
  }
  
  .wallboard-main-content {
    padding: 1rem;
    gap: 1.5rem;
  }
  
  .header {
    padding: 1.2rem 1rem 1rem 1rem;
  }
  
  .dashboard-grid {
    grid-template-columns: 1fr;
  }
  
  .achievements-grid {
    grid-template-columns: 1fr;
  }
  
  .leaderboard-tabs {
    flex-wrap: wrap;
  }
  
  .leaderboard-stats {
    flex-direction: column;
    gap: 0.25rem;
  }
}
</style>
