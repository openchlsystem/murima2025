<template>
  <div class="app-container" :data-theme="currentTheme">
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
    <div class="main-content" :class="{ 'sidebar-collapsed': isSidebarCollapsed }">
      <!-- Header -->
      <div class="header">
        <h1 class="page-title">Admin Panel</h1>
        <button class="theme-toggle" @click="toggleTheme" id="theme-toggle">
          <svg v-if="currentTheme === 'dark'" id="moon-icon" width="24" height="24" viewBox="0 0 24 24" fill="none">
            <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
          </svg>
          <svg v-else id="sun-icon" width="24" height="24" viewBox="0 0 24 24" fill="none">
            <circle cx="12" cy="12" r="5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
            <line x1="12" y1="1" x2="12" y2="3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
            <line x1="12" y1="21" x2="12" y2="23" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
            <line x1="4.22" y1="4.22" x2="5.64" y2="5.64" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
            <line x1="18.36" y1="18.36" x2="19.78" y2="19.78" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
            <line x1="1" y1="12" x2="3" y2="12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
            <line x1="21" y1="12" x2="23" y2="12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
            <line x1="4.22" y1="19.78" x2="5.64" y2="18.36" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
            <line x1="18.36" y1="5.64" x2="19.78" y2="4.22" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
          </svg>
          <span id="theme-text">{{ currentTheme === 'dark' ? 'Light Mode' : 'Dark Mode' }}</span>
        </button>
      </div>

      <!-- Main Scroll Content -->
      <div class="main-scroll-content">
        <!-- Admin Dashboard Content -->
        <div class="admin-dashboard">
          <!-- Stats Grid -->
          <div class="stats-grid">
            <div class="stat-card glass-panel">
              <div class="stat-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                  <path d="M14 2H6C5.46957 2 4.96086 2.21071 4.58579 2.58579C4.21071 2.96086 4 3.46957 4 4V20C4 20.5304 4.21071 21.0391 4.58579 21.4142C4.96086 21.7893 5.46957 22 6 22H18C18.5304 22 19.0391 21.7893 19.4142 21.4142C19.7893 21.0391 20 20.5304 20 20V8L14 2Z" stroke="currentColor" stroke-width="2"/>
                </svg>
              </div>
              <div class="stat-content">
                <h3>{{ dashboardStats.totalCases }}</h3>
                <p>Total Cases</p>
              </div>
            </div>

            <div class="stat-card glass-panel">
              <div class="stat-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                  <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" stroke="currentColor" stroke-width="2"/>
                  <circle cx="9" cy="7" r="4" stroke="currentColor" stroke-width="2"/>
                </svg>
              </div>
              <div class="stat-content">
                <h3>{{ dashboardStats.teamMembers }}</h3>
                <p>Team Members</p>
              </div>
            </div>

            <div class="stat-card glass-panel">
              <div class="stat-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                  <path d="M12 2L2 7l10 5 10-5-10-5z" stroke="currentColor" stroke-width="2"/>
                  <path d="M2 17l10 5 10-5" stroke="currentColor" stroke-width="2"/>
                  <path d="M2 12l10 5 10-5" stroke="currentColor" stroke-width="2"/>
                </svg>
              </div>
              <div class="stat-content">
                <h3>{{ dashboardStats.activeUsers }}</h3>
                <p>Active Users</p>
              </div>
            </div>

            <div class="stat-card glass-panel">
              <div class="stat-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                  <path d="M3 3v18h18" stroke="currentColor" stroke-width="2"/>
                  <path d="M18.7 8l-5.1 5.2-2.8-2.7L7 14.3" stroke="currentColor" stroke-width="2"/>
                </svg>
              </div>
              <div class="stat-content">
                <h3>{{ dashboardStats.resolutionRate }}%</h3>
                <p>Resolution Rate</p>
              </div>
            </div>
          </div>

          <!-- Admin Sections -->
          <div class="admin-sections">
            <!-- Recent Cases Section -->
            <div class="section-card glass-panel">
              <h2>Recent Cases</h2>
              <div class="cases-list">
                <div v-for="caseItem in recentCases" :key="caseItem.id" class="case-item" @click="viewCase(caseItem.id)">
                  <div class="case-info">
                    <h4>{{ caseItem.title }}</h4>
                    <p>{{ caseItem.caseNumber }} - {{ caseItem.assignedTo }}</p>
                  </div>
                  <div class="case-status" :class="caseItem.status.toLowerCase().replace(' ', '-')">
                    {{ caseItem.status }}
                  </div>
                </div>
              </div>
            </div>

            <!-- Quick Actions Section -->
            <div class="section-card glass-panel">
              <h2>Quick Actions</h2>
              <div class="quick-actions">
                <button class="action-btn glass-btn" @click="showCreateCaseModal = true">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                    <path d="M12 5v14M5 12h14" stroke="currentColor" stroke-width="2"/>
                  </svg>
                  Create Case
                </button>
                <button class="action-btn glass-btn" @click="showInviteUserModal = true">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                    <path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" stroke="currentColor" stroke-width="2"/>
                    <circle cx="8.5" cy="7" r="4" stroke="currentColor" stroke-width="2"/>
                    <line x1="20" y1="8" x2="20" y2="14" stroke="currentColor" stroke-width="2"/>
                    <line x1="23" y1="11" x2="17" y2="11" stroke="currentColor" stroke-width="2"/>
                  </svg>
                  Invite User
                </button>
                <button class="action-btn glass-btn" @click="generateReport">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                    <path d="M3 3v18h18" stroke="currentColor" stroke-width="2"/>
                    <path d="M18.7 8l-5.1 5.2-2.8-2.7L7 14.3" stroke="currentColor" stroke-width="2"/>
                  </svg>
                  Generate Report
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Create Case Modal -->
    <div v-if="showCreateCaseModal" class="modal" @click="showCreateCaseModal = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>Create New Case</h2>
          <button class="close-btn" @click="showCreateCaseModal = false">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
              <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" stroke-width="2"/>
            </svg>
          </button>
        </div>
        
        <div class="modal-body">
          <div class="form-grid">
            <div class="form-group">
              <label class="form-label">Case Title *</label>
              <input v-model="newCase.title" class="form-input" placeholder="Enter case title" required />
            </div>
            
            <div class="form-group">
              <label class="form-label">Client Name *</label>
              <input v-model="newCase.clientName" class="form-input" placeholder="Enter client name" required />
            </div>
            
            <div class="form-group">
              <label class="form-label">Category *</label>
              <select v-model="newCase.category" class="form-select" required>
                <option value="">Select category</option>
                <option v-for="category in categories" :key="category.id" :value="category.name">
                  {{ category.name }}
                </option>
              </select>
            </div>
            
            <div class="form-group">
              <label class="form-label">Priority</label>
              <select v-model="newCase.priority" class="form-select">
                <option value="Low">Low</option>
                <option value="Medium">Medium</option>
                <option value="High">High</option>
                <option value="Critical">Critical</option>
              </select>
            </div>
            
            <div class="form-group">
              <label class="form-label">Assigned To</label>
              <select v-model="newCase.assignedTo" class="form-select">
                <option value="">Unassigned</option>
                <option v-for="member in teamMembers" :key="member.id" :value="member.name">
                  {{ member.name }}
                </option>
              </select>
            </div>
            
            <div class="form-group full-width">
              <label class="form-label">Description</label>
              <textarea v-model="newCase.description" class="form-textarea" rows="4" placeholder="Enter case description"></textarea>
            </div>
          </div>
        </div>
        
        <div class="modal-footer">
          <button class="cancel-btn" @click="showCreateCaseModal = false">Cancel</button>
          <button class="submit-btn" @click="createCase">Create Case</button>
        </div>
      </div>
    </div>

    <!-- Invite User Modal -->
    <div v-if="showInviteUserModal" class="modal" @click="showInviteUserModal = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>Invite New User</h2>
          <button class="close-btn" @click="showInviteUserModal = false">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
              <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" stroke-width="2"/>
            </svg>
          </button>
        </div>
        
        <div class="modal-body">
          <div class="form-grid">
            <div class="form-group">
              <label class="form-label">Full Name *</label>
              <input v-model="newUser.name" class="form-input" placeholder="Enter full name" required />
            </div>
            
            <div class="form-group">
              <label class="form-label">Email Address *</label>
              <input v-model="newUser.email" type="email" class="form-input" placeholder="Enter email address" required />
            </div>
            
            <div class="form-group">
              <label class="form-label">Role *</label>
              <select v-model="newUser.role" class="form-select" required>
                <option value="">Select role</option>
                <option value="Admin">Admin</option>
                <option value="Manager">Manager</option>
                <option value="Case Worker">Case Worker</option>
                <option value="Supervisor">Supervisor</option>
              </select>
            </div>
            
            <div class="form-group">
              <label class="form-label">Phone Number</label>
              <input v-model="newUser.phone" class="form-input" placeholder="Enter phone number" />
            </div>
            
            <div class="form-group full-width">
              <label class="form-label">Welcome Message</label>
              <textarea v-model="newUser.welcomeMessage" class="form-textarea" rows="3" placeholder="Enter welcome message"></textarea>
            </div>
          </div>
        </div>
        
        <div class="modal-footer">
          <button class="cancel-btn" @click="showInviteUserModal = false">Cancel</button>
          <button class="submit-btn" @click="inviteUser">Send Invitation</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import SidePanel from '../components/SidePanel.vue'
import { useThemeStore } from '../stores/theme.js'

// Theme store
const themeStore = useThemeStore()
const currentTheme = computed(() => themeStore.currentTheme)

// Sidebar state
const isSidebarCollapsed = ref(false)

// User and system state
const userRole = ref('admin')
const isInQueue = ref(false)
const isProcessingQueue = ref(false)
const currentCall = ref(null)

// Modal states
const showCreateCaseModal = ref(false)
const showInviteUserModal = ref(false)
const showCreateCategoryModal = ref(false)
const showCreateWorkflowModal = ref(false)
const showCaseFilters = ref(false)
const showNotifications = ref(false)

// Form states
const editingRole = ref(null)
const newMessage = ref('')

// Organization and user info
const currentOrganization = ref({
  name: 'Children First Kenya',
  location: 'Nairobi, Kenya'
})

const currentUser = ref({
  name: 'Sarah Johnson',
  role: 'Admin',
  initials: 'SJ'
})

// Dashboard statistics
const dashboardStats = ref({
  totalCases: 247,
  newCasesThisMonth: 23,
  activeCases: 89,
  urgentCases: 12,
  teamMembers: 15,
  activeUsers: 8,
  resolutionRate: 87.3
})

const reportStats = ref({
  totalCases: 247,
  resolvedCases: 198,
  avgResolutionTime: '12 days',
  satisfactionRate: 94
})

// Recent cases data
const recentCases = ref([
  {
    id: 1,
    caseNumber: 'CASE-2024-001',
    title: 'Child Protection Assessment',
    assignedTo: 'John Doe',
    status: 'In Progress',
    priority: 'High',
    createdAt: '2024-06-05T10:30:00Z'
  },
  {
    id: 2,
    caseNumber: 'CASE-2024-002',
    title: 'Family Reunification',
    assignedTo: 'Jane Smith',
    status: 'Open',
    priority: 'Medium',
    createdAt: '2024-06-04T14:15:00Z'
  },
  {
    id: 3,
    caseNumber: 'CASE-2024-003',
    title: 'Emergency Shelter Placement',
    assignedTo: 'Mike Wilson',
    status: 'Resolved',
    priority: 'Critical',
    createdAt: '2024-06-03T09:45:00Z'
  }
])

// Cases data
const cases = ref([
  {
    id: 1,
    caseNumber: 'CASE-2024-001',
    title: 'Child Protection Assessment',
    clientName: 'Anonymous Client',
    assignedTo: 'John Doe',
    status: 'In Progress',
    priority: 'High',
    category: 'Child Protection',
    createdAt: '2024-06-05T10:30:00Z'
  },
  {
    id: 2,
    caseNumber: 'CASE-2024-002',
    title: 'Family Reunification',
    clientName: 'Maria Santos',
    assignedTo: 'Jane Smith',
    status: 'Open',
    priority: 'Medium',
    category: 'Family Services',
    createdAt: '2024-06-04T14:15:00Z'
  },
  {
    id: 3,
    caseNumber: 'CASE-2024-003',
    title: 'Emergency Shelter Placement',
    clientName: 'David Johnson',
    assignedTo: 'Mike Wilson',
    status: 'Resolved',
    priority: 'Critical',
    category: 'Emergency Services',
    createdAt: '2024-06-03T09:45:00Z'
  }
])

// Team members data
const teamMembers = ref([
  {
    id: 1,
    name: 'John Doe',
    email: 'john.doe@cfk.org',
    role: 'Case Worker',
    status: 'Active',
    casesAssigned: 12,
    lastActive: '2 hours ago'
  },
  {
    id: 2,
    name: 'Jane Smith',
    email: 'jane.smith@cfk.org',
    role: 'Manager',
    status: 'Active',
    casesAssigned: 8,
    lastActive: '1 hour ago'
  },
  {
    id: 3,
    name: 'Mike Wilson',
    email: 'mike.wilson@cfk.org',
    role: 'Supervisor',
    status: 'Active',
    casesAssigned: 15,
    lastActive: '30 minutes ago'
  }
])

// Categories data
const categories = ref([
  {
    id: 1,
    name: 'Child Protection',
    description: 'Cases involving child safety and welfare',
    color: '#FF6B6B',
    caseCount: 45,
    isActive: true
  },
  {
    id: 2,
    name: 'Family Services',
    description: 'Family support and reunification services',
    color: '#4ECDC4',
    caseCount: 32,
    isActive: true
  },
  {
    id: 3,
    name: 'Emergency Services',
    description: 'Urgent intervention and emergency placement',
    color: '#45B7D1',
    caseCount: 18,
    isActive: true
  },
  {
    id: 4,
    name: 'Community Outreach',
    description: 'Community education and prevention programs',
    color: '#96CEB4',
    caseCount: 12,
    isActive: true
  }
])

// Workflows data
const workflows = ref([
  {
    id: 1,
    name: 'Child Protection Assessment',
    description: 'Standard workflow for child protection cases',
    status: 'Active',
    steps: [
      { name: 'Initial Assessment', assignee: 'Case Worker' },
      { name: 'Safety Planning', assignee: 'Supervisor' },
      { name: 'Service Planning', assignee: 'Manager' },
      { name: 'Case Review', assignee: 'Supervisor' }
    ]
  },
  {
    id: 2,
    name: 'Emergency Response',
    description: 'Rapid response workflow for emergency cases',
    status: 'Active',
    steps: [
      { name: 'Emergency Assessment', assignee: 'On-call Worker' },
      { name: 'Safety Intervention', assignee: 'Supervisor' },
      { name: 'Placement Decision', assignee: 'Manager' }
    ]
  }
])

// Form data
const newCase = ref({
  title: '',
  clientName: '',
  category: '',
  priority: 'Medium',
  assignedTo: '',
  dueDate: '',
  description: ''
})

const newUser = ref({
  name: '',
  email: '',
  role: '',
  phone: '',
  welcomeMessage: ''
})

const newCategory = ref({
  name: '',
  description: '',
  color: '#FF6B6B'
})

const newWorkflow = ref({
  name: '',
  description: '',
  steps: [
    { name: '', assignee: '' }
  ]
})

// Filter states
const caseFilters = ref({
  status: '',
  priority: '',
  assignedTo: '',
  search: ''
})

const userFilters = ref({
  role: '',
  status: '',
  search: ''
})

// Settings
const settings = ref({
  organizationName: 'Children First Kenya',
  location: 'Nairobi, Kenya',
  contactEmail: 'admin@cfk.org',
  phoneNumber: '+254 700 123 456',
  casePrefix: 'CASE',
  autoAssign: true,
  defaultPriority: 'Medium',
  emailNotifications: true,
  assignmentAlerts: true,
  deadlineReminders: true,
  twoFactorAuth: false,
  sessionTimeout: 60,
  passwordStrength: 'medium'
})

// Computed properties
const filteredCases = computed(() => {
  return cases.value.filter(case_ => {
    if (caseFilters.value.status && case_.status !== caseFilters.value.status) return false
    if (caseFilters.value.priority && case_.priority !== caseFilters.value.priority) return false
    if (caseFilters.value.assignedTo && case_.assignedTo !== caseFilters.value.assignedTo) return false
    if (caseFilters.value.search) {
      const search = caseFilters.value.search.toLowerCase()
      if (!case_.title.toLowerCase().includes(search) &&
          !case_.caseNumber.toLowerCase().includes(search) &&
          !case_.clientName.toLowerCase().includes(search)) return false
    }
    return true
  })
})

const filteredUsers = computed(() => {
  return teamMembers.value.filter(user => {
    if (userFilters.value.role && user.role !== userFilters.value.role) return false
    if (userFilters.value.status && user.status !== userFilters.value.status) return false
    if (userFilters.value.search) {
      const search = userFilters.value.search.toLowerCase()
      if (!user.name.toLowerCase().includes(search) &&
          !user.email.toLowerCase().includes(search)) return false
    }
    return true
  })
})

// Methods
const handleQueueToggle = () => {
  isInQueue.value = !isInQueue.value
}

const handleLogout = () => {
  console.log('Logging out...')
  alert('Logged out successfully!')
}

const handleSidebarToggle = (collapsed) => {
  isSidebarCollapsed.value = collapsed
}

const toggleTheme = () => {
  themeStore.toggleTheme()
}

const createCase = () => {
  if (!newCase.value.title || !newCase.value.clientName || !newCase.value.category) {
    alert('Please fill in all required fields.')
    return
  }

  const caseNumber = `CASE-${new Date().getFullYear()}-${String(cases.value.length + 1).padStart(3, '0')}`
  const newCaseObj = {
    id: cases.value.length + 1,
    caseNumber,
    title: newCase.value.title,
    clientName: newCase.value.clientName,
    assignedTo: newCase.value.assignedTo || 'Unassigned',
    status: 'Open',
    priority: newCase.value.priority,
    category: newCase.value.category,
    createdAt: new Date().toISOString()
  }

  cases.value.unshift(newCaseObj)
  recentCases.value.unshift(newCaseObj)

  // Reset form
  newCase.value = {
    title: '',
    clientName: '',
    category: '',
    priority: 'Medium',
    assignedTo: '',
    dueDate: '',
    description: ''
  }

  showCreateCaseModal.value = false
  alert('Case created successfully!')
}

const inviteUser = () => {
  if (!newUser.value.name || !newUser.value.email || !newUser.value.role) {
    alert('Please fill in all required fields.')
    return
  }

  const newUserObj = {
    id: teamMembers.value.length + 1,
    name: newUser.value.name,
    email: newUser.value.email,
    role: newUser.value.role,
    status: 'Pending',
    casesAssigned: 0,
    lastActive: 'Never'
  }

  teamMembers.value.unshift(newUserObj)

  // Reset form
  newUser.value = {
    name: '',
    email: '',
    role: '',
    phone: '',
    welcomeMessage: ''
  }

  showInviteUserModal.value = false
  alert('Invitation sent successfully!')
}

const generateReport = () => {
  alert('Generating report...')
}

const viewCase = (caseId) => {
  console.log('View case:', caseId)
  alert(`View case ${caseId} functionality would be implemented here.`)
}

const editCase = (caseId) => {
  console.log('Edit case:', caseId)
  alert(`Edit case ${caseId} functionality would be implemented here.`)
}

const editUser = (userId) => {
  console.log('Edit user:', userId)
  alert(`Edit user ${userId} functionality would be implemented here.`)
}

const toggleUserStatus = (userId) => {
  const userIndex = teamMembers.value.findIndex(user => user.id === userId)
  if (userIndex !== -1) {
    const user = teamMembers.value[userIndex]
    user.status = user.status === 'Active' ? 'Inactive' : 'Active'
    alert(`User ${user.name} has been ${user.status.toLowerCase()}.`)
  }
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString()
}

const formatTime = (date) => {
  return new Date(date).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

const getInitials = (name) => {
  return name.split(' ').map(n => n[0]).join('')
}

const startEditingRole = async (userId) => {
  editingRole.value = userId
  await nextTick()
}

const saveUserRole = (userId, newRole) => {
  const userIndex = teamMembers.value.findIndex(user => user.id === userId)
  if (userIndex !== -1) {
    const oldRole = teamMembers.value[userIndex].role
    teamMembers.value[userIndex].role = newRole
    alert(`User role updated from ${oldRole} to ${newRole}`)
  }
  editingRole.value = null
}

const saveSettings = () => {
  console.log('Saving settings:', settings.value)
  alert('Settings saved successfully!')
}

// Lifecycle
onMounted(() => {
  const handleResize = () => {
    if (window.innerWidth > 1024) {
      // Handle responsive behavior
    }
  }

  window.addEventListener('resize', handleResize)

  const handleClickOutside = (event) => {
    const isMobileOrTablet = window.innerWidth <= 1024
    
    // Close notifications when clicking outside
    if (showNotifications.value && !event.target.closest('.notification-panel') && !event.target.closest('.notification-btn')) {
      showNotifications.value = false
    }

    // Close role editing when clicking outside
    if (!event.target.closest('.role-cell')) {
      editingRole.value = null
    }
  }

  document.addEventListener('click', handleClickOutside)
})
</script>

<style>
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

.app-container {
  display: flex;
  width: 100%;
  min-height: 100vh;
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

.main-content.sidebar-collapsed {
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
  scrollbar-width: none;
  -ms-overflow-style: none;
}

.main-scroll-content::-webkit-scrollbar {
  display: none;
}

.admin-dashboard {
  width: 100%;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  background-color: var(--card-bg);
  border-radius: 30px;
  padding: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s, box-shadow 0.2s, background-color 0.3s;
  display: flex;
  align-items: center;
  gap: 15px;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.stat-icon {
  width: 50px;
  height: 50px;
  border-radius: 12px;
  background-color: var(--accent-color);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}

.stat-content {
  flex: 1;
}

.stat-content h3 {
  font-size: 32px;
  font-weight: 800;
  margin-bottom: 5px;
}

.stat-content p {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-secondary);
}

.admin-sections {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 20px;
}

.section-card {
  background-color: var(--card-bg);
  border-radius: 30px;
  padding: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: background-color 0.3s;
}

.section-card h2 {
  font-size: 20px;
  font-weight: 700;
  margin-bottom: 20px;
}

.cases-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.case-item {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 15px;
  border: 1px solid var(--border-color);
  border-radius: 20px;
  transition: all 0.3s ease;
  cursor: pointer;
}

.case-item:hover {
  border-color: var(--accent-color);
  background-color: rgba(255, 140, 0, 0.05);
}

.case-info {
  flex: 1;
}

.case-info h4 {
  font-weight: 600;
  margin-bottom: 4px;
}

.case-info p {
  font-size: 12px;
  color: var(--text-secondary);
  margin-bottom: 2px;
}

.case-status {
  display: flex;
  align-items: center;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
}

.case-status.open {
  background: rgba(59, 130, 246, 0.1);
  color: #2563eb;
}

.case-status.in-progress {
  background: rgba(245, 158, 11, 0.1);
  color: #d97706;
}

.case-status.resolved {
  background: rgba(34, 197, 94, 0.1);
  color: #16a34a;
}

.case-status.closed {
  background: rgba(107, 114, 128, 0.1);
  color: #6b7280;
}

.quick-actions {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  background: var(--background-color);
  border: 1px solid var(--border-color);
  border-radius: 15px;
  font-size: 14px;
  font-weight: 600;
  color: var(--text-color);
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: left;
  width: 100%;
}

.action-btn:hover {
  border-color: var(--accent-color);
  background-color: rgba(255, 140, 0, 0.05);
}

.glass-panel {
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.glass-btn {
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
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
  max-width: 600px;
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

.modal-footer {
  display: flex;
  gap: 12px;
  padding: 20px;
  justify-content: flex-end;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.form-grid .form-group.full-width {
  grid-column: 1 / -1;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-label {
  font-weight: 600;
  font-size: 14px;
}

.form-input,
.form-select,
.form-textarea {
  padding: 12px 16px;
  border: 1px solid var(--border-color);
  border-radius: 12px;
  background: var(--background-color);
  color: var(--text-color);
  font-size: 14px;
  transition: all 0.3s ease;
}

.form-input:focus,
.form-select:focus,
.form-textarea:focus {
  outline: none;
  border-color: var(--accent-color);
  box-shadow: 0 0 0 3px rgba(255, 140, 0, 0.1);
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
  box-shadow: 0 4px 12px rgba(255, 140, 0, 0.3);
}

/* Responsive Design */
@media (max-width: 1024px) {
  .main-content {
    margin-left: 0;
    width: 100%;
  }

  .stats-grid {
    grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
    gap: 15px;
  }

  .admin-sections {
    grid-template-columns: 1fr;
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

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .page-title {
    font-size: 24px;
  }

  .modal-content {
    width: 95%;
    margin: 20px;
  }

  .form-grid {
    grid-template-columns: 1fr;
  }
}

@media (min-width: 1025px) {
  .mobile-menu-btn {
    display: none;
  }
}
</style>
ß
