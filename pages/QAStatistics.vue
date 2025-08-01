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
        <button class="back-btn glass-btn" v-if="selectedCounsellor || selectedCall" @click="handleBack">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
            <path d="M19 12H5M12 19l-7-7 7-7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          Back
        </button>
      <div class="page-title">QA Management System</div>
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

    <div class="qa-main-content">
      <!-- Step 1: Counsellors List -->
      <div v-if="!selectedCounsellor && !selectedCall" class="counsellors-section">
        <h3 class="section-title">All Counsellors</h3>
        <div class="counsellors-list">
            <div v-for="counsellor in counsellors" :key="counsellor.name" class="counsellor-card glass-card fine-border" @click="selectCounsellor(counsellor)">
            <div class="counsellor-header">
              <template v-if="counsellor.avatar">
                <img :src="counsellor.avatar" class="counsellor-avatar" @error="counsellor.avatar = null" />
              </template>
              <template v-else>
                <div class="counsellor-avatar initials-avatar">{{ getInitials(counsellor.name) }}</div>
              </template>
              <div>
                <div class="counsellor-name">{{ counsellor.name }}</div>
                <div class="counsellor-score">Avg. Score: {{ counsellor.avgScore }}%</div>
              </div>
            </div>
            <div class="counsellor-evals">Evaluations: {{ counsellor.evaluations.length }}</div>
          </div>
        </div>
      </div>

      <!-- Step 2: Calls List for Selected Counsellor -->
      <div v-else-if="selectedCounsellor && !selectedCall" class="calls-section">
        <h3 class="section-title">Calls by {{ selectedCounsellor.name }}</h3>
        <div class="calls-list">
            <div v-for="call in counsellorCalls" :key="call.id" class="call-card glass-card fine-border" @click="selectCall(call)">
            <div class="call-header">
                <span class="call-id">Call #{{ call.id }}</span>
              <span class="call-date">{{ formatDateTime(call.dateTime) }}</span>
              </div>
            <div class="call-score">Score: {{ call.evaluation?.overallScore ?? '-' }}%</div>
            <div class="call-issue">Issue: {{ call.issueType }}</div>
                </div>
                </div>
              </div>

      <!-- Step 3: Evaluation Details for Selected Call -->
      <div v-else-if="selectedCall" class="evaluation-section">
        <h3 class="section-title">Evaluation for Call #{{ selectedCall.id }}</h3>
          <div class="evaluation-details glass-card fine-border">
          <form @submit.prevent="saveEvaluation">
            <div v-for="(score, key) in editableScores" :key="key" class="modal-field">
              <label><strong>{{ formatCategory(key) }}:</strong></label>
              <input type="number" v-model.number="editableScores[key]" min="0" max="100" />
              </div>
            <div class="modal-field">
              <label><strong>Notes:</strong></label>
              <textarea v-model="editableNotes" rows="3"></textarea>
            </div>
            <div class="modal-field">
              <label><strong>Evaluated By:</strong></label>
              <input v-model="editableEvaluator" />
          </div>
            <div class="modal-field">
              <label><strong>Date:</strong></label>
              <input type="datetime-local" v-model="editableDate" />
        </div>
            <div class="modal-actions">
                <button type="submit" class="glass-btn filled">Save</button>
                <button type="button" class="glass-btn" @click="handleBack">Back</button>
              </div>
          </form>
            </div>
              </div>
            </div>
  </div>
</div>
</template>

<script setup>
import SidePanel from '../components/SidePanel.vue'
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useThemeStore } from '../stores/theme.js'

// Theme store
const themeStore = useThemeStore()

// Reactive state
const currentTheme = computed(() => themeStore.currentTheme)
const selectedCall = ref(null)
const selectedCounsellor = ref(null)
const editableScores = ref({})
const editableNotes = ref('')
const editableEvaluator = ref('')
const editableDate = ref('')

// Sidebar state
const isSidebarCollapsed = ref(false)
const userRole = ref('user')
const isInQueue = ref(false)
const isProcessingQueue = ref(false)
const currentCall = ref(null)

// Sample calls database
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
  }
])

// Computed properties
const counsellors = computed(() => {
  const map = {};
  callsDatabase.value.forEach(call => {
    const name = call.agent.name;
    if (!map[name]) {
      map[name] = {
        name,
        avatar: call.agent.avatar,
        evaluations: [],
        avgScore: 0
      };
    }
    if (call.evaluation) {
      map[name].evaluations.push(call.evaluation);
    }
  });
  
  Object.values(map).forEach(c => {
    if (c.evaluations.length) {
      c.avgScore = Math.round(c.evaluations.reduce((sum, e) => sum + (e.overallScore || 0), 0) / c.evaluations.length);
    }
  });
  return Object.values(map);
});

const counsellorCalls = computed(() => {
  if (!selectedCounsellor.value) return []
  return callsDatabase.value.filter(call => call.agent.name === selectedCounsellor.value.name)
})

// Watch for selected call changes
watch(selectedCall, (call) => {
  if (call && call.evaluation) {
    editableScores.value = { ...call.evaluation.scores }
    editableNotes.value = call.evaluation.notes
    editableEvaluator.value = call.evaluation.evaluatedBy
    const d = call.evaluation.evaluationDate
    editableDate.value = d ? new Date(d).toISOString().slice(0,16) : ''
  }
})

// Methods
const toggleTheme = () => {
  themeStore.toggleTheme()
}

const selectCounsellor = (counsellor) => {
  selectedCounsellor.value = counsellor
  selectedCall.value = null
}

const selectCall = (call) => {
  selectedCall.value = call
  if (call.evaluation) {
    editableScores.value = { ...call.evaluation.scores }
    editableNotes.value = call.evaluation.notes
    editableEvaluator.value = call.evaluation.evaluatedBy
    const d = call.evaluation.evaluationDate
    editableDate.value = d ? new Date(d).toISOString().slice(0,16) : ''
  } else {
    editableScores.value = {}
    editableNotes.value = ''
    editableEvaluator.value = ''
    editableDate.value = ''
  }
}

const handleBack = () => {
  if (selectedCall.value) {
  selectedCall.value = null
  } else if (selectedCounsellor.value) {
    selectedCounsellor.value = null
  }
}

const saveEvaluation = () => {
  if (selectedCall.value && selectedCall.value.evaluation) {
    selectedCall.value.evaluation.scores = { ...editableScores.value }
    selectedCall.value.evaluation.notes = editableNotes.value
    selectedCall.value.evaluation.evaluatedBy = editableEvaluator.value
    selectedCall.value.evaluation.evaluationDate = new Date(editableDate.value)
    handleBack()
  }
}

const getInitials = (name) => {
  if (!name) return ''
  const parts = name.trim().split(' ')
  if (parts.length === 1) return parts[0].slice(0, 2).toUpperCase()
  return (parts[0][0] + parts[1][0]).toUpperCase()
}

const formatCategory = (category) => {
  return category.charAt(0).toUpperCase() + category.slice(1)
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
  color: var(--text-color);
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

.back-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: var(--content-bg);
  border: 1.5px solid var(--accent-color);
  border-radius: 18px;
  color: var(--accent-color);
  font-weight: 700;
  padding: 0.5rem 1.2rem;
  box-shadow: 0 2px 8px 0 rgba(30,126,52,0.08);
  transition: background 0.2s, border 0.2s;
}

.back-btn:hover {
  background: var(--card-bg);
  border-color: var(--accent-hover);
}

  .qa-main-content {
  padding: 2rem 2.5rem;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text-color);
  margin-bottom: 1.5rem;
}

.counsellors-section {
  margin-top: 2rem;
}

.counsellors-list {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
  overflow-x: auto;
  padding-bottom: 1rem;
}

.counsellor-card {
  min-width: 220px;
  max-width: 300px;
  flex: 1 1 220px;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  cursor: pointer;
  transition: box-shadow 0.2s, border 0.2s;
}

.counsellor-card:hover {
  box-shadow: 0 4px 16px rgba(0,0,0,0.10);
  border-color: var(--accent-hover);
}

.counsellor-header {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.counsellor-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  object-fit: cover;
  background: var(--card-bg);
  border: 2px solid var(--accent-color);
}

.counsellor-avatar.initials-avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--accent-color);
  color: #fff;
  font-weight: 700;
  font-size: 1.2rem;
  text-transform: uppercase;
}

.counsellor-name {
  font-weight: 700;
  color: var(--text-color);
}

.counsellor-score {
  font-size: 0.95rem;
  color: var(--accent-color);
}

.counsellor-evals {
  font-size: 0.95rem;
  color: var(--text-secondary);
}

.calls-list {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
  margin-top: 1.5rem;
}

.call-card {
  min-width: 220px;
  max-width: 320px;
  flex: 1 1 220px;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  cursor: pointer;
  transition: box-shadow 0.2s, border 0.2s;
}

.call-card:hover {
  box-shadow: 0 4px 16px rgba(0,0,0,0.10);
  border-color: var(--accent-hover);
}

.call-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
  color: var(--text-color);
}

.call-score {
  color: var(--accent-color);
  font-weight: 700;
}

.call-issue {
  color: var(--text-secondary);
  font-size: 0.95rem;
}

.evaluation-details {
  max-width: 480px;
  margin: 2rem auto;
  padding: 2rem 2.5rem;
}

.modal-field {
  margin-bottom: 1.2rem;
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

.modal-field label {
  font-weight: 600;
  color: var(--text-color);
}

.modal-field input,
.modal-field textarea {
  background: var(--background-color);
  color: var(--text-color);
  border: 1px solid var(--border-color);
  border-radius: 6px;
  padding: 0.5rem;
  font-size: 1rem;
  width: 100%;
}

.modal-field input:focus,
.modal-field textarea:focus {
  outline: none;
  border-color: var(--accent-color);
}

.modal-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
}

@media (max-width: 900px) {
  .main-content {
    margin-left: 0;
    width: 100%;
  }
  
  .qa-main-content {
    padding: 1rem;
    gap: 1.2rem;
  }
  
  .header {
    padding: 1.2rem 1rem 1rem 1rem;
  }
  
  .counsellors-list {
    flex-wrap: nowrap;
    overflow-x: auto;
    gap: 1rem;
  }
  
  .counsellor-card {
    min-width: 220px;
    max-width: 80vw;
    flex: 0 0 220px;
}

.calls-list {
    flex-wrap: nowrap;
    overflow-x: auto;
    gap: 1rem;
  }
  
.call-card {
  min-width: 220px;
    max-width: 80vw;
    flex: 0 0 220px;
  }
}
</style>
