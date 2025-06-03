<template>
  <div class="case-creation-page">
    <router-link class="back-button" to="/cases">
      <svg fill="none" height="16" viewbox="0 0 24 24" width="16" xmlns="http://www.w3.org/2000/svg">
        <path d="M19 12H5" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" />
        <path d="M12 19L5 12L12 5" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" />
      </svg>
      Back to Cases
    </router-link>

    <button class="theme-toggle" @click="toggleTheme">
      <svg fill="none" height="16" viewbox="0 0 24 24" width="16" xmlns="http://www.w3.org/2000/svg">
        <path d="M12 16C14.2091 16 16 14.2091 16 12C16 9.79086 14.2091 8 12 8C9.79086 8 8 9.79086 8 12C8 14.2091 9.79086 16 12 16Z" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" />
        <path d="M12 2V4M12 20V22M4.93 4.93L6.34 6.34M17.66 17.66L19.07 19.07M2 12H4M20 12H22M4.93 19.07L6.34 17.66M17.66 6.34L19.07 4.93" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" />
      </svg>
      <span>{{ isDarkMode ? 'Toggle Light Mode' : 'Toggle Dark Mode' }}</span>
    </button>

    <div class="case-container">
      <div class="main-form-container">
        <div class="case-header">
          <div>
            <h1>Create New Case</h1>
            <p>{{ stepDescriptions[currentStep - 1] }}</p>
          </div>
          <div class="toggle-container">
            <span class="toggle-label">
              <span class="ai-icon">
                <svg fill="none" height="16" viewbox="0 0 24 24" width="16" xmlns="http://www.w3.org/2000/svg">
                  <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" />
                  <path d="M2 17L12 22L22 17" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" />
                  <path d="M2 12L12 17L22 12" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" />
                </svg>
              </span>
              AI Enabled
            </span>
            <label class="toggle-switch">
              <input v-model="isAIEnabled" type="checkbox" />
              <span class="toggle-slider"></span>
            </label>
          </div>
        </div>

        <div class="progress-container">
          <div class="progress-steps">
            <div 
              v-for="step in totalSteps" 
              :key="step"
              class="progress-step"
              :class="{ active: currentStep >= step }"
            >
              <div class="step-circle">{{ step }}</div>
              <div class="step-label">{{ stepLabels[step - 1] }}</div>
            </div>
          </div>
        </div>

        <!-- Step 1: Basic Information -->
        <div v-if="currentStep === 1" class="step-content">
          <form class="case-form" @submit.prevent="handleStep1Submit">
            <div class="form-section">
              <div class="section-title">Basic Information</div>
              <div class="form-group">
                <label for="case-name">Case Name*</label>
                <input 
                  v-model="formData.caseName"
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
                  v-model="formData.description"
                  class="form-control" 
                  id="case-description" 
                  placeholder="Enter case description" 
                  required
                ></textarea>
              </div>
              <div class="form-row">
                <div class="form-group">
                  <label for="case-priority">Priority*</label>
                  <select 
                    v-model="formData.priority"
                    class="form-control" 
                    id="case-priority" 
                    required
                  >
                    <option value="">Select priority</option>
                    <option v-for="priority in priorities" :key="priority" :value="priority">
                      {{ priority }}
                    </option>
                  </select>
                </div>
                <div class="form-group">
                  <label for="case-status">Status*</label>
                  <select 
                    v-model="formData.status"
                    class="form-control" 
                    id="case-status" 
                    required
                  >
                    <option value="">Select status</option>
                    <option v-for="status in statuses" :key="status" :value="status">
                      {{ status }}
                    </option>
                  </select>
                </div>
              </div>
              <div class="form-row">
                <div class="form-group">
                  <label for="case-type">Type*</label>
                  <select 
                    v-model="formData.type"
                    class="form-control" 
                    id="case-type" 
                    required
                  >
                    <option value="">Select type</option>
                    <option v-for="type in caseTypes" :key="type" :value="type">
                      {{ type }}
                    </option>
                  </select>
                </div>
                <div class="form-group">
                  <label for="case-source">Source*</label>
                  <select 
                    v-model="formData.source"
                    class="form-control" 
                    id="case-source" 
                    required
                  >
                    <option value="">Select source</option>
                    <option v-for="source in sources" :key="source" :value="source">
                      {{ source }}
                    </option>
                  </select>
                </div>
              </div>
            </div>
            <div class="form-actions">
              <button type="submit" class="btn-primary">Next Step</button>
            </div>
          </form>
        </div>

        <!-- Additional steps will be implemented here -->
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// State
const isDarkMode = ref(false)
const isAIEnabled = ref(false)
const currentStep = ref(1)
const totalSteps = 5

// Form data
const formData = ref({
  caseName: '',
  description: '',
  priority: '',
  status: '',
  type: '',
  source: ''
})

// Options
const priorities = ['High', 'Medium', 'Low']
const statuses = ['New', 'In Progress', 'Pending', 'Resolved', 'Closed']
const caseTypes = [
  'Domestic Violence',
  'Sexual Assault',
  'Human Trafficking',
  'Child Abuse',
  'Elder Abuse',
  'Stalking'
]
const sources = [
  'Phone Call',
  'Email',
  'Walk-in',
  'Referral',
  'Online Form',
  'Social Media'
]

// Step information
const stepLabels = [
  'Basic Info',
  'Client Info',
  'Incident Details',
  'Case Assignment',
  'Review'
]

const stepDescriptions = [
  'Step 1: Basic Information',
  'Step 2: Client Information',
  'Step 3: Incident Details',
  'Step 4: Case Assignment',
  'Step 5: Review and Submit'
]

// Methods
const toggleTheme = () => {
  isDarkMode.value = !isDarkMode.value
  document.documentElement.setAttribute('data-theme', isDarkMode.value ? 'dark' : 'light')
}

const handleStep1Submit = () => {
  // Validate form data
  if (!formData.value.caseName || !formData.value.description || 
      !formData.value.priority || !formData.value.status || 
      !formData.value.type || !formData.value.source) {
    return
  }
  
  // Move to next step
  currentStep.value++
}

// Additional step handlers will be implemented here
</script>

<style scoped>
.case-creation-page {
  padding: 20px;
  background-color: var(--background-color);
  color: var(--text-color);
  min-height: 100vh;
}

.back-button {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: var(--text-color);
  text-decoration: none;
  margin-bottom: 20px;
}

.theme-toggle {
  position: fixed;
  top: 20px;
  right: 20px;
  display: flex;
  align-items: center;
  gap: 8px;
  background: none;
  border: none;
  color: var(--text-color);
  cursor: pointer;
}

.case-container {
  max-width: 1200px;
  margin: 0 auto;
}

.main-form-container {
  background-color: var(--content-bg);
  border-radius: 12px;
  padding: 30px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.case-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 30px;
}

.toggle-container {
  display: flex;
  align-items: center;
  gap: 10px;
}

.toggle-label {
  display: flex;
  align-items: center;
  gap: 5px;
}

.toggle-switch {
  position: relative;
  display: inline-block;
  width: 50px;
  height: 24px;
}

.toggle-switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.toggle-slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: var(--border-color);
  transition: .4s;
  border-radius: 24px;
}

.toggle-slider:before {
  position: absolute;
  content: "";
  height: 16px;
  width: 16px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  transition: .4s;
  border-radius: 50%;
}

input:checked + .toggle-slider {
  background-color: var(--accent-color);
}

input:checked + .toggle-slider:before {
  transform: translateX(26px);
}

.progress-container {
  margin-bottom: 30px;
}

.progress-steps {
  display: flex;
  justify-content: space-between;
  position: relative;
}

.progress-step {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  z-index: 1;
}

.step-circle {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background-color: var(--border-color);
  color: var(--text-color);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 8px;
}

.step-label {
  font-size: 14px;
  color: var(--text-secondary);
}

.progress-step.active .step-circle {
  background-color: var(--accent-color);
  color: white;
}

.progress-step.active .step-label {
  color: var(--text-color);
}

.form-section {
  margin-bottom: 30px;
}

.section-title {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 20px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
}

.form-control {
  width: 100%;
  padding: 10px;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  background-color: var(--input-bg);
  color: var(--text-color);
}

textarea.form-control {
  min-height: 100px;
  resize: vertical;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 30px;
}

.btn-primary {
  background-color: var(--accent-color);
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
}

.btn-primary:hover {
  background-color: var(--accent-hover);
}

@media (max-width: 768px) {
  .form-row {
    grid-template-columns: 1fr;
  }

  .case-header {
    flex-direction: column;
    gap: 20px;
  }

  .progress-steps {
    overflow-x: auto;
    padding-bottom: 10px;
  }

  .progress-step {
    min-width: 100px;
  }
}
</style>
