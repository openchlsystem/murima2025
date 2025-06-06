<template>
  <div class="case-creation-page">
    <router-link class="back-button" to="/cases">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M19 12H5" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" />
        <path d="M12 19L5 12L12 5" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" />
      </svg>
      Back to Cases
    </router-link>

    <button class="theme-toggle" @click="toggleTheme">
      <svg v-if="currentTheme === 'dark'" width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M12 16C14.2091 16 16 14.2091 16 12C16 9.79086 14.2091 8 12 8C9.79086 8 8 9.79086 8 12C8 14.2091 9.79086 16 12 16Z" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" />
        <path d="M12 2V4M12 20V22M4.93 4.93L6.34 6.34M17.66 17.66L19.07 19.07M2 12H4M20 12H22M4.93 19.07L6.34 17.66M17.66 6.34L19.07 4.93" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" />
      </svg>
      <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
      <span>{{ currentTheme === 'dark' ? 'Toggle Light Mode' : 'Toggle Dark Mode' }}</span>
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
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" />
                  <path d="M2 17L12 22L22 17" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" />
                  <path d="M2 12L12 17L22 12" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" />
                </svg>
              </span>
              AI Enabled
            </span>
            <label class="toggle-switch">
              <input v-model="isAIEnabled" type="checkbox" @change="handleAIToggle" />
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
              <div class="step-circle" :class="{ active: currentStep >= step, completed: currentStep > step }">
                {{ currentStep > step ? '✓' : step }}
              </div>
              <div class="step-label" :class="{ active: currentStep >= step }">{{ stepLabels[step - 1] }}</div>
            </div>
          </div>
        </div>

        <!-- Step 1: Basic Information -->
        <div v-show="currentStep === 1" class="step-content">
          <form class="case-form" @submit.prevent="validateAndProceed(1)">
            <div class="form-section">
              <div class="section-title">Basic Information</div>
              <div class="form-group">
                <label for="case-name">Case Name*</label>
                <input 
                  v-model="formData.step1.caseName"
                  class="form-control" 
                  id="case-name" 
                  placeholder="Enter case name" 
                  required 
                  type="text"
                  :class="{ 'error': validationErrors.caseName }"
                />
                <div v-if="validationErrors.caseName" class="error-message">{{ validationErrors.caseName }}</div>
              </div>
              <div class="form-group">
                <label for="case-description">Description*</label>
                <textarea 
                  v-model="formData.step1.description"
                  class="form-control" 
                  id="case-description" 
                  placeholder="Enter case description" 
                  required
                  :class="{ 'error': validationErrors.description }"
                ></textarea>
                <div v-if="validationErrors.description" class="error-message">{{ validationErrors.description }}</div>
              </div>
              <div class="form-row">
                <div class="form-group">
                  <label for="case-priority">Priority*</label>
                  <select 
                    v-model="formData.step1.priority"
                    class="form-control" 
                    id="case-priority" 
                    required
                    :class="{ 'error': validationErrors.priority }"
                  >
                    <option value="">Select priority</option>
                    <option v-for="priority in priorities" :key="priority" :value="priority">
                      {{ priority }}
                    </option>
                  </select>
                  <div v-if="validationErrors.priority" class="error-message">{{ validationErrors.priority }}</div>
                </div>
                <div class="form-group">
                  <label for="case-status">Status*</label>
                  <select 
                    v-model="formData.step1.status"
                    class="form-control" 
                    id="case-status" 
                    required
                    :class="{ 'error': validationErrors.status }"
                  >
                    <option value="">Select status</option>
                    <option v-for="status in statuses" :key="status" :value="status">
                      {{ status }}
                    </option>
                  </select>
                  <div v-if="validationErrors.status" class="error-message">{{ validationErrors.status }}</div>
                </div>
              </div>
              <div class="form-row">
                <div class="form-group">
                  <label for="case-type">Type*</label>
                  <select 
                    v-model="formData.step1.type"
                    class="form-control" 
                    id="case-type" 
                    required
                    :class="{ 'error': validationErrors.type }"
                  >
                    <option value="">Select type</option>
                    <option v-for="type in caseTypes" :key="type" :value="type">
                      {{ type }}
                    </option>
                  </select>
                  <div v-if="validationErrors.type" class="error-message">{{ validationErrors.type }}</div>
                </div>
                <div class="form-group">
                  <label for="case-source">Source*</label>
                  <select 
                    v-model="formData.step1.source"
                    class="form-control" 
                    id="case-source" 
                    required
                    :class="{ 'error': validationErrors.source }"
                  >
                    <option value="">Select source</option>
                    <option v-for="source in sources" :key="source" :value="source">
                      {{ source }}
                    </option>
                  </select>
                  <div v-if="validationErrors.source" class="error-message">{{ validationErrors.source }}</div>
                </div>
              </div>
            </div>
            <div class="form-actions">
              <button type="button" class="btn btn-cancel" @click="cancelForm">Cancel</button>
              <div>
                <button type="button" class="btn btn-skip" @click="skipStep(1)">Skip</button>
                <button type="submit" class="btn btn-next">Next</button>
              </div>
            </div>
          </form>
        </div>

        <!-- Step 2: Client Information -->
        <div v-show="currentStep === 2" class="step-content">
          <form class="case-form" @submit.prevent="saveAndProceed(2)">
            <div class="form-section">
              <div class="section-title">Client Information</div>
              <div class="form-row">
                <div class="form-group">
                  <label for="client-name">Client Name</label>
                  <input 
                    v-model="formData.step2.clientName"
                    type="text" 
                    id="client-name" 
                    class="form-control" 
                    placeholder="Enter client name"
                  />
                </div>
                <div class="form-group">
                  <label for="client-id">Client ID (if existing)</label>
                  <input 
                    v-model="formData.step2.clientId"
                    type="text" 
                    id="client-id" 
                    class="form-control" 
                    placeholder="Enter client ID"
                  />
                </div>
              </div>
              <div class="form-row">
                <div class="form-group">
                  <label for="client-phone">Phone Number</label>
                  <input 
                    v-model="formData.step2.phone"
                    type="tel" 
                    id="client-phone" 
                    class="form-control" 
                    placeholder="Enter phone number"
                  />
                </div>
                <div class="form-group">
                  <label for="client-email">Email</label>
                  <input 
                    v-model="formData.step2.email"
                    type="email" 
                    id="client-email" 
                    class="form-control" 
                    placeholder="Enter email"
                  />
                </div>
              </div>
              <div class="form-group">
                <label for="client-address">Address</label>
                <input 
                  v-model="formData.step2.address"
                  type="text" 
                  id="client-address" 
                  class="form-control" 
                  placeholder="Enter address"
                />
              </div>
              <div class="form-row">
                <div class="form-group">
                  <label for="client-dob">Date of Birth</label>
                  <input 
                    v-model="formData.step2.dob"
                    type="date" 
                    id="client-dob" 
                    class="form-control"
                  />
                </div>
                <div class="form-group">
                  <label for="client-gender">Gender</label>
                  <select 
                    v-model="formData.step2.gender"
                    id="client-gender" 
                    class="form-control"
                  >
                    <option value="">Select gender</option>
                    <option value="female">Female</option>
                    <option value="male">Male</option>
                    <option value="non-binary">Non-binary</option>
                    <option value="transgender">Transgender</option>
                    <option value="other">Other</option>
                    <option value="prefer-not-to-say">Prefer not to say</option>
                  </select>
                </div>
              </div>
              <div class="form-group">
                <label for="client-notes">Additional Notes</label>
                <textarea 
                  v-model="formData.step2.notes"
                  id="client-notes" 
                  class="form-control" 
                  placeholder="Enter any additional notes about the client"
                ></textarea>
              </div>
            </div>
            <div class="form-actions">
              <button type="button" class="btn btn-back" @click="goToStep(1)">Back</button>
              <div>
                <button type="button" class="btn btn-skip" @click="skipStep(2)">Skip</button>
                <button type="submit" class="btn btn-next">Next</button>
              </div>
            </div>
          </form>
        </div>

        <!-- Step 3: Incident Details -->
        <div v-show="currentStep === 3" class="step-content">
          <form class="case-form" @submit.prevent="saveAndProceed(3)">
            <div class="form-section">
              <div class="section-title">Incident Details</div>
              <div class="form-row">
                <div class="form-group">
                  <label for="incident-date">Date of Incident</label>
                  <input 
                    v-model="formData.step3.incidentDate"
                    type="date" 
                    id="incident-date" 
                    class="form-control"
                  />
                </div>
                <div class="form-group">
                  <label for="incident-time">Time of Incident</label>
                  <input 
                    v-model="formData.step3.incidentTime"
                    type="time" 
                    id="incident-time" 
                    class="form-control"
                  />
                </div>
              </div>
              <div class="form-group">
                <label for="incident-location">Location</label>
                <input 
                  v-model="formData.step3.location"
                  type="text" 
                  id="incident-location" 
                  class="form-control" 
                  placeholder="Enter incident location"
                />
              </div>
              <div class="form-group">
                <label for="incident-description">Description of Incident</label>
                <textarea 
                  v-model="formData.step3.description"
                  id="incident-description" 
                  class="form-control" 
                  placeholder="Describe what happened"
                ></textarea>
              </div>
              <div class="form-row">
                <div class="form-group">
                  <label for="incident-type">Type of Incident</label>
                  <select 
                    v-model="formData.step3.incidentType"
                    id="incident-type" 
                    class="form-control"
                  >
                    <option value="">Select incident type</option>
                    <option value="physical-abuse">Physical Abuse</option>
                    <option value="emotional-abuse">Emotional/Psychological Abuse</option>
                    <option value="sexual-assault">Sexual Assault</option>
                    <option value="stalking">Stalking</option>
                    <option value="financial-abuse">Financial Abuse</option>
                    <option value="human-trafficking">Human Trafficking</option>
                    <option value="other">Other</option>
                  </select>
                </div>
                <div class="form-group">
                  <label for="incident-severity">Severity</label>
                  <select 
                    v-model="formData.step3.severity"
                    id="incident-severity" 
                    class="form-control"
                  >
                    <option value="">Select severity</option>
                    <option value="critical">Critical</option>
                    <option value="severe">Severe</option>
                    <option value="moderate">Moderate</option>
                    <option value="mild">Mild</option>
                  </select>
                </div>
              </div>
              <div class="form-group">
                <label for="perpetrator-info">Perpetrator Information</label>
                <textarea 
                  v-model="formData.step3.perpetratorInfo"
                  id="perpetrator-info" 
                  class="form-control" 
                  placeholder="Enter information about the perpetrator (if known)"
                ></textarea>
              </div>
              <div class="form-group">
                <label for="safety-concerns">Safety Concerns</label>
                <textarea 
                  v-model="formData.step3.safetyConcerns"
                  id="safety-concerns" 
                  class="form-control" 
                  placeholder="Describe any immediate safety concerns"
                ></textarea>
              </div>
            </div>
            <div class="form-actions">
              <button type="button" class="btn btn-back" @click="goToStep(2)">Back</button>
              <div>
                <button type="button" class="btn btn-skip" @click="skipStep(3)">Skip</button>
                <button type="submit" class="btn btn-next">Next</button>
              </div>
            </div>
          </form>
        </div>

        <!-- Step 4: Case Assignment -->
        <div v-show="currentStep === 4" class="step-content">
          <form class="case-form" @submit.prevent="saveAndProceed(4)">
            <div class="form-section">
              <div class="section-title">Case Assignment</div>
              <div class="form-group">
                <label for="assignment-type">Assignment Type</label>
                <select 
                  v-model="formData.step4.assignmentType"
                  id="assignment-type" 
                  class="form-control"
                  @change="handleAssignmentTypeChange"
                >
                  <option value="">Select assignment type</option>
                  <option value="individual">Individual Staff Member</option>
                  <option value="team">Team</option>
                  <option value="auto">Auto-assign</option>
                  <option value="unassigned">Leave Unassigned</option>
                </select>
              </div>
              
              <div v-if="formData.step4.assignmentType === 'individual'" class="form-group">
                <label>Select Staff Member</label>
                <div class="staff-list">
                  <div 
                    v-for="staff in staffMembers" 
                    :key="staff.id"
                    class="staff-card" 
                    :class="{ selected: formData.step4.selectedStaffId === staff.id }"
                    @click="selectStaff(staff.id)"
                  >
                    <div class="staff-header">
                      <div class="staff-avatar">
                        <img :src="staff.avatar" :alt="staff.name">
                      </div>
                      <div class="staff-info">
                        <div class="staff-name">{{ staff.name }}</div>
                        <div class="staff-role">{{ staff.role }}</div>
                      </div>
                    </div>
                    <div class="staff-meta">
                      <div class="staff-meta-item">
                        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" width="12" height="12">
                          <path d="M12 8v4l3 3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                          <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                        <span>{{ staff.status }}</span>
                      </div>
                      <div class="staff-meta-item">
                        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" width="12" height="12">
                          <path d="M12 21a9 9 0 100-18 9 9 0 000 18z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                          <path d="M12 13a3 3 0 100-6 3 3 0 000 6z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                          <path d="M6.168 18.849A4 4 0 0110 16h4a4 4 0 013.834 2.855" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                        <span>{{ staff.activeCases }} active cases</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              
              <div v-if="formData.step4.assignmentType === 'team'" class="form-group">
                <label for="team-select">Select Team</label>
                <select 
                  v-model="formData.step4.team"
                  id="team-select" 
                  class="form-control"
                >
                  <option value="">Select team</option>
                  <option value="crisis-response">Crisis Response Team</option>
                  <option value="counseling">Counseling Team</option>
                  <option value="legal">Legal Support Team</option>
                  <option value="housing">Housing & Resources Team</option>
                </select>
              </div>
              
              <div class="form-group">
                <label for="assignment-notes">Assignment Notes</label>
                <textarea 
                  v-model="formData.step4.notes"
                  id="assignment-notes" 
                  class="form-control" 
                  placeholder="Enter any notes about this assignment"
                ></textarea>
              </div>
              
              <div class="form-row">
                <div class="form-group">
                  <label for="due-date">Due Date</label>
                  <input 
                    v-model="formData.step4.dueDate"
                    type="date" 
                    id="due-date" 
                    class="form-control"
                  />
                </div>
                <div class="form-group">
                  <label for="follow-up-date">Follow-up Date</label>
                  <input 
                    v-model="formData.step4.followUpDate"
                    type="date" 
                    id="follow-up-date" 
                    class="form-control"
                  />
                </div>
              </div>
            </div>
            <div class="form-actions">
              <button type="button" class="btn btn-back" @click="goToStep(3)">Back</button>
              <div>
                <button type="button" class="btn btn-skip" @click="skipStep(4)">Skip</button>
                <button type="submit" class="btn btn-next">Next</button>
              </div>
            </div>
          </form>
        </div>

        <!-- Step 5: Review and Submit -->
        <div v-show="currentStep === 5" class="step-content">
          <div class="review-sections">
            <div class="review-section">
              <div class="section-header">
                <div class="section-title">Basic Information</div>
                <button class="edit-btn" @click="goToStep(1)">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                  Edit
                </button>
              </div>
              <div class="review-content">
                <div class="review-item">
                  <div class="review-label">Case Name</div>
                  <div class="review-value">{{ formData.step1.caseName || 'N/A' }}</div>
                </div>
                <div class="review-item">
                  <div class="review-label">Description</div>
                  <div class="review-value">{{ formData.step1.description || 'N/A' }}</div>
                </div>
                <div class="review-item">
                  <div class="review-label">Priority</div>
                  <div class="review-value">{{ formData.step1.priority || 'N/A' }}</div>
                </div>
                <div class="review-item">
                  <div class="review-label">Status</div>
                  <div class="review-value">{{ formData.step1.status || 'N/A' }}</div>
                </div>
                <div class="review-item">
                  <div class="review-label">Type</div>
                  <div class="review-value">{{ formData.step1.type || 'N/A' }}</div>
                </div>
                <div class="review-item">
                  <div class="review-label">Source</div>
                  <div class="review-value">{{ formData.step1.source || 'N/A' }}</div>
                </div>
              </div>
            </div>
            
            <div class="review-section">
              <div class="section-header">
                <div class="section-title">Client Information</div>
                <button class="edit-btn" @click="goToStep(2)">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                  Edit
                </button>
              </div>
              <div class="review-content">
                <div class="review-item">
                  <div class="review-label">Client Name</div>
                  <div class="review-value">{{ formData.step2.clientName || 'N/A' }}</div>
                </div>
                <div class="review-item">
                  <div class="review-label">Client ID</div>
                  <div class="review-value">{{ formData.step2.clientId || 'N/A' }}</div>
                </div>
                <div class="review-item">
                  <div class="review-label">Phone Number</div>
                  <div class="review-value">{{ formData.step2.phone || 'N/A' }}</div>
                </div>
                <div class="review-item">
                  <div class="review-label">Email</div>
                  <div class="review-value">{{ formData.step2.email || 'N/A' }}</div>
                </div>
                <div class="review-item">
                  <div class="review-label">Address</div>
                  <div class="review-value">{{ formData.step2.address || 'N/A' }}</div>
                </div>
                <div class="review-item">
                  <div class="review-label">Date of Birth</div>
                  <div class="review-value">{{ formData.step2.dob || 'N/A' }}</div>
                </div>
                <div class="review-item">
                  <div class="review-label">Gender</div>
                  <div class="review-value">{{ formatGender(formData.step2.gender) || 'N/A' }}</div>
                </div>
                <div class="review-item">
                  <div class="review-label">Additional Notes</div>
                  <div class="review-value">{{ formData.step2.notes || 'N/A' }}</div>
                </div>
              </div>
            </div>
            
            <div class="review-section">
              <div class="section-header">
                <div class="section-title">Incident Details</div>
                <button class="edit-btn" @click="goToStep(3)">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                  Edit
                </button>
              </div>
              <div class="review-content">
                <div class="review-item">
                  <div class="review-label">Date of Incident</div>
                  <div class="review-value">{{ formData.step3.incidentDate || 'N/A' }}</div>
                </div>
                <div class="review-item">
                  <div class="review-label">Time of Incident</div>
                  <div class="review-value">{{ formData.step3.incidentTime || 'N/A' }}</div>
                </div>
                <div class="review-item">
                  <div class="review-label">Location</div>
                  <div class="review-value">{{ formData.step3.location || 'N/A' }}</div>
                </div>
                <div class="review-item">
                  <div class="review-label">Description of Incident</div>
                  <div class="review-value">{{ formData.step3.description || 'N/A' }}</div>
                </div>
                <div class="review-item">
                  <div class="review-label">Type of Incident</div>
                  <div class="review-value">{{ formatIncidentType(formData.step3.incidentType) || 'N/A' }}</div>
                </div>
                <div class="review-item">
                  <div class="review-label">Severity</div>
                  <div class="review-value">{{ formatSeverity(formData.step3.severity) || 'N/A' }}</div>
                </div>
                <div class="review-item">
                  <div class="review-label">Perpetrator Information</div>
                  <div class="review-value">{{ formData.step3.perpetratorInfo || 'N/A' }}</div>
                </div>
                <div class="review-item">
                  <div class="review-label">Safety Concerns</div>
                  <div class="review-value">{{ formData.step3.safetyConcerns || 'N/A' }}</div>
                </div>
              </div>
            </div>
            
            <div class="review-section">
              <div class="section-header">
                <div class="section-title">Case Assignment</div>
                <button class="edit-btn" @click="goToStep(4)">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                  Edit
                </button>
              </div>
              <div class="review-content">
                <div class="review-item">
                  <div class="review-label">Assignment Type</div>
                  <div class="review-value">{{ formatAssignmentType(formData.step4.assignmentType) || 'N/A' }}</div>
                </div>
                <div v-if="formData.step4.assignmentType === 'individual'" class="review-item">
                  <div class="review-label">Assigned Staff</div>
                  <div class="review-value">{{ getSelectedStaffName() || 'N/A' }}</div>
                </div>
                <div v-if="formData.step4.assignmentType === 'team'" class="review-item">
                  <div class="review-label">Team</div>
                  <div class="review-value">{{ formatTeam(formData.step4.team) || 'N/A' }}</div>
                </div>
                <div class="review-item">
                  <div class="review-label">Assignment Notes</div>
                  <div class="review-value">{{ formData.step4.notes || 'N/A' }}</div>
                </div>
                <div class="review-item">
                  <div class="review-label">Due Date</div>
                  <div class="review-value">{{ formData.step4.dueDate || 'N/A' }}</div>
                </div>
                <div class="review-item">
                  <div class="review-label">Follow-up Date</div>
                  <div class="review-value">{{ formData.step4.followUpDate || 'N/A' }}</div>
                </div>
              </div>
            </div>
          </div>
          
          <div class="form-actions">
            <button type="button" class="btn btn-back" @click="goToStep(4)">Back</button>
            <button type="button" class="btn btn-submit" @click="submitCase">Submit Case</button>
          </div>
        </div>
      </div>
      
      <!-- AI Preview Panel -->
      <div v-if="isAIEnabled" class="ai-preview-container">
        <div class="ai-preview">
          <div class="ai-preview-header">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M2 17L12 22L22 17" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M2 12L12 17L22 12" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <div class="ai-preview-title">AI Preview <span class="ai-badge">Generated</span></div>
          </div>
          
          <div class="ai-preview-content">
            <!-- Basic Information Preview -->
            <div class="ai-preview-section">
              <div class="ai-preview-section-title">Basic Information</div>
              <div v-if="currentStep >= 1" class="ai-preview-item">
                <div class="ai-preview-label">Case Name</div>
                <div class="ai-preview-value">{{ aiData.step1.caseName }}</div>
              </div>
              <div v-if="currentStep >= 1" class="ai-preview-item">
                <div class="ai-preview-label">Description</div>
                <div class="ai-preview-value">{{ aiData.step1.description }}</div>
              </div>
              <div v-if="currentStep >= 1" class="ai-preview-item">
                <div class="ai-preview-label">Priority</div>
                <div class="ai-preview-value">{{ aiData.step1.priority }}</div>
              </div>
              <div v-if="currentStep >= 1" class="ai-preview-item">
                <div class="ai-preview-label">Status</div>
                <div class="ai-preview-value">{{ aiData.step1.status }}</div>
              </div>
              <div v-if="currentStep >= 1" class="ai-preview-item">
                <div class="ai-preview-label">Type</div>
                <div class="ai-preview-value">{{ aiData.step1.type }}</div>
              </div>
              <div v-if="currentStep >= 1" class="ai-preview-item">
                <div class="ai-preview-label">Source</div>
                <div class="ai-preview-value">{{ aiData.step1.source }}</div>
              </div>
              <div v-if="currentStep < 1" class="ai-preview-item">
                <div class="ai-preview-label">Status</div>
                <div class="ai-preview-value na">N/A - Complete Step 1 to view</div>
              </div>
            </div>
            
            <!-- Client Information Preview -->
            <div class="ai-preview-section">
              <div class="ai-preview-section-title">Client Information</div>
              <div v-if="currentStep >= 2" class="ai-preview-item">
                <div class="ai-preview-label">Client Name</div>
                <div class="ai-preview-value">{{ aiData.step2.clientName }}</div>
              </div>
              <div v-if="currentStep >= 2" class="ai-preview-item">
                <div class="ai-preview-label">Phone Number</div>
                <div class="ai-preview-value">{{ aiData.step2.phone }}</div>
              </div>
              <div v-if="currentStep >= 2" class="ai-preview-item">
                <div class="ai-preview-label">Email</div>
                <div class="ai-preview-value">{{ aiData.step2.email }}</div>
              </div>
              <div v-if="currentStep >= 2" class="ai-preview-item">
                <div class="ai-preview-label">Address</div>
                <div class="ai-preview-value">{{ aiData.step2.address }}</div>
              </div>
              <div v-if="currentStep >= 2" class="ai-preview-item">
                <div class="ai-preview-label">Date of Birth</div>
                <div class="ai-preview-value">{{ aiData.step2.dob }}</div>
              </div>
              <div v-if="currentStep >= 2" class="ai-preview-item">
                <div class="ai-preview-label">Gender</div>
                <div class="ai-preview-value">{{ aiData.step2.gender }}</div>
              </div>
              <div v-if="currentStep >= 2" class="ai-preview-item">
                <div class="ai-preview-label">Additional Notes</div>
                <div class="ai-preview-value">{{ aiData.step2.notes }}</div>
              </div>
              <div v-if="currentStep < 2" class="ai-preview-item">
                <div class="ai-preview-label">Status</div>
                <div class="ai-preview-value na">N/A - Complete Step 2 to view</div>
              </div>
            </div>
            
            <!-- Incident Details Preview -->
            <div class="ai-preview-section">
              <div class="ai-preview-section-title">Incident Details</div>
              <div v-if="currentStep >= 3" class="ai-preview-item">
                <div class="ai-preview-label">Date of Incident</div>
                <div class="ai-preview-value">{{ aiData.step3.incidentDate }}</div>
              </div>
              <div v-if="currentStep >= 3" class="ai-preview-item">
                <div class="ai-preview-label">Time of Incident</div>
                <div class="ai-preview-value">{{ aiData.step3.incidentTime }}</div>
              </div>
              <div v-if="currentStep >= 3" class="ai-preview-item">
                <div class="ai-preview-label">Location</div>
                <div class="ai-preview-value">{{ aiData.step3.location }}</div>
              </div>
              <div v-if="currentStep >= 3" class="ai-preview-item">
                <div class="ai-preview-label">Description of Incident</div>
                <div class="ai-preview-value">{{ aiData.step3.description }}</div>
              </div>
              <div v-if="currentStep >= 3" class="ai-preview-item">
                <div class="ai-preview-label">Type of Incident</div>
                <div class="ai-preview-value">{{ aiData.step3.incidentType }}</div>
              </div>
              <div v-if="currentStep >= 3" class="ai-preview-item">
                <div class="ai-preview-label">Severity</div>
                <div class="ai-preview-value">{{ aiData.step3.severity }}</div>
              </div>
              <div v-if="currentStep >= 3" class="ai-preview-item">
                <div class="ai-preview-label">Perpetrator Information</div>
                <div class="ai-preview-value">{{ aiData.step3.perpetratorInfo }}</div>
              </div>
              <div v-if="currentStep >= 3" class="ai-preview-item">
                <div class="ai-preview-label">Safety Concerns</div>
                <div class="ai-preview-value">{{ aiData.step3.safetyConcerns }}</div>
              </div>
              <div v-if="currentStep < 3" class="ai-preview-item">
                <div class="ai-preview-label">Status</div>
                <div class="ai-preview-value na">N/A - Complete Step 3 to view</div>
              </div>
            </div>
            
            <!-- Case Assignment Preview -->
            <div class="ai-preview-section">
              <div class="ai-preview-section-title">Case Assignment</div>
              <div v-if="currentStep >= 4" class="ai-preview-item">
                <div class="ai-preview-label">Assignment Type</div>
                <div class="ai-preview-value">{{ aiData.step4.assignmentType }}</div>
              </div>
              <div v-if="currentStep >= 4 && aiData.step4.assignmentType === 'Individual Staff Member'" class="ai-preview-item">
                <div class="ai-preview-label">Assigned Staff</div>
                <div class="ai-preview-value">{{ aiData.step4.assignedStaff }}</div>
              </div>
              <div v-if="currentStep >= 4" class="ai-preview-item">
                <div class="ai-preview-label">Assignment Notes</div>
                <div class="ai-preview-value">{{ aiData.step4.notes }}</div>
              </div>
              <div v-if="currentStep >= 4" class="ai-preview-item">
                <div class="ai-preview-label">Due Date</div>
                <div class="ai-preview-value">{{ aiData.step4.dueDate }}</div>
              </div>
              <div v-if="currentStep >= 4" class="ai-preview-item">
                <div class="ai-preview-label">Follow-up Date</div>
                <div class="ai-preview-value">{{ aiData.step4.followUpDate }}</div>
              </div>
              <div v-if="currentStep < 4" class="ai-preview-item">
                <div class="ai-preview-label">Status</div>
                <div class="ai-preview-value na">N/A - Complete Step 4 to view</div>
              </div>
            </div>
            
            <!-- Case Summary Preview (only shown in step 5) -->
            <div v-if="currentStep === 5" class="ai-preview-section">
              <div class="ai-preview-section-title">Case Summary</div>
              <div class="ai-preview-item">
                <div class="ai-preview-label">Case Type</div>
                <div class="ai-preview-value">{{ aiData.step1.type }}</div>
              </div>
              <div class="ai-preview-item">
                <div class="ai-preview-label">Priority</div>
                <div class="ai-preview-value">{{ aiData.step1.priority }}</div>
              </div>
              <div class="ai-preview-item">
                <div class="ai-preview-label">Client</div>
                <div class="ai-preview-value">{{ aiData.step2.clientName }}</div>
              </div>
              <div class="ai-preview-item">
                <div class="ai-preview-label">Assigned To</div>
                <div class="ai-preview-value">{{ aiData.step4.assignedStaff }}</div>
              </div>
              <div class="ai-preview-item">
                <div class="ai-preview-label">Due Date</div>
                <div class="ai-preview-value">{{ aiData.step4.dueDate }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Warning Modal -->
    <div class="modal-overlay" :class="{ active: showWarningModal }">
      <div class="modal-content">
        <div class="modal-header">
          <div class="modal-title">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            Warning
          </div>
        </div>
        <div class="modal-body">
          <p>This will update the information on the form permanently, erasing your current entries. Are you sure you want to continue?</p>
        </div>
        <div class="modal-footer">
          <button class="modal-btn modal-btn-cancel" @click="cancelAIFill">Cancel</button>
          <button class="modal-btn modal-btn-confirm" @click="confirmAIFill">Continue</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// State
const currentStep = ref(1)
const totalSteps = 5
const currentTheme = ref(localStorage.getItem('theme') || 'dark')
const isAIEnabled = ref(false)
const showWarningModal = ref(false)
const validationErrors = reactive({})
const selectedStepForAI = ref(1)

// Staff members data
const staffMembers = [
  {
    id: 1,
    name: 'Sarah Mitchell',
    role: 'Crisis Advocate',
    avatar: '/placeholder.svg?height=40&width=40',
    status: 'Available',
    activeCases: 3
  },
  {
    id: 2,
    name: 'Robert Jackson',
    role: 'Case Manager',
    avatar: '/placeholder.svg?height=40&width=40',
    status: 'Available',
    activeCases: 5
  },
  {
    id: 3,
    name: 'Emily Chan',
    role: 'Trauma Counselor',
    avatar: '/placeholder.svg?height=40&width=40',
    status: 'Available',
    activeCases: 2
  },
  {
    id: 4,
    name: 'Michael Lee',
    role: 'Legal Advocate',
    avatar: '/placeholder.svg?height=40&width=40',
    status: 'Available',
    activeCases: 4
  }
]

// Form data
const formData = reactive({
  step1: {
    caseName: '',
    description: '',
    priority: '',
    status: '',
    type: '',
    source: ''
  },
  step2: {
    clientName: '',
    clientId: '',
    phone: '',
    email: '',
    address: '',
    dob: '',
    gender: '',
    notes: ''
  },
  step3: {
    incidentDate: '',
    incidentTime: '',
    location: '',
    description: '',
    incidentType: '',
    severity: '',
    perpetratorInfo: '',
    safetyConcerns: ''
  },
  step4: {
    assignmentType: '',
    selectedStaffId: null,
    team: '',
    notes: '',
    dueDate: '',
    followUpDate: ''
  }
})

// AI data
const aiData = reactive({
  step1: {
    caseName: 'Domestic Violence Support - Jane Doe',
    description: 'Client seeking support after experiencing domestic violence from spouse. Needs immediate safety planning and potential shelter placement.',
    priority: 'High',
    status: 'New',
    type: 'Domestic Violence',
    source: 'Hotline Call'
  },
  step2: {
    clientName: 'Jane Doe',
    clientId: '',
    phone: '555-123-4567',
    email: 'anonymous@example.com',
    address: '123 Main St, Anytown, USA',
    dob: '1985-06-15',
    gender: 'Female',
    notes: 'Client prefers to be contacted via email. Has two children (ages 8 and 10) who may also need support services.'
  },
  step3: {
    incidentDate: '2025-05-15',
    incidentTime: '22:30',
    location: 'Client\'s residence',
    description: 'Client reported that her spouse became verbally abusive after drinking, escalating to pushing her against the wall. Children were present in the home. Client was able to take children to a neighbor\'s house for the night.',
    incidentType: 'Physical Abuse',
    severity: 'Moderate',
    perpetratorInfo: 'Spouse, John Doe, 38 years old. History of alcohol abuse. No prior police reports filed.',
    safetyConcerns: 'Client is concerned about returning home. Spouse has access to firearms. Client believes spouse may try to prevent her from leaving with the children.'
  },
  step4: {
    assignmentType: 'Individual Staff Member',
    assignedStaff: 'Sarah Mitchell (Crisis Advocate)',
    team: '',
    notes: 'Client needs immediate safety planning and potential shelter placement. Assign to someone with domestic violence experience.',
    dueDate: '2025-05-20',
    followUpDate: '2025-05-22'
  }
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
  currentTheme.value = currentTheme.value === 'dark' ? 'light' : 'dark'
  localStorage.setItem('theme', currentTheme.value)
  applyTheme()
}

const applyTheme = () => {
  const root = document.documentElement
  
  if (currentTheme.value === 'light') {
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

const handleAIToggle = () => {
  if (isAIEnabled.value) {
    selectedStepForAI.value = currentStep.value
    showWarningModal.value = true
  }
}

const cancelAIFill = () => {
  showWarningModal.value = false
  isAIEnabled.value = false
}

const confirmAIFill = () => {
  showWarningModal.value = false
  fillFormWithAIData(selectedStepForAI.value)
}

const fillFormWithAIData = (step) => {
  if (step === 1) {
    formData.step1.caseName = aiData.step1.caseName
    formData.step1.description = aiData.step1.description
    formData.step1.priority = aiData.step1.priority
    formData.step1.status = aiData.step1.status
    formData.step1.type = aiData.step1.type
    formData.step1.source = aiData.step1.source
  } else if (step === 2) {
    formData.step2.clientName = aiData.step2.clientName
    formData.step2.clientId = aiData.step2.clientId
    formData.step2.phone = aiData.step2.phone
    formData.step2.email = aiData.step2.email
    formData.step2.address = aiData.step2.address
    formData.step2.dob = aiData.step2.dob
    formData.step2.gender = aiData.step2.gender
    formData.step2.notes = aiData.step2.notes
  } else if (step === 3) {
    formData.step3.incidentDate = aiData.step3.incidentDate
    formData.step3.incidentTime = aiData.step3.incidentTime
    formData.step3.location = aiData.step3.location
    formData.step3.description = aiData.step3.description
    formData.step3.incidentType = aiData.step3.incidentType
    formData.step3.severity = aiData.step3.severity
    formData.step3.perpetratorInfo = aiData.step3.perpetratorInfo
    formData.step3.safetyConcerns = aiData.step3.safetyConcerns
  } else if (step === 4) {
    formData.step4.assignmentType = 'individual'
    formData.step4.selectedStaffId = 1 // Sarah Mitchell
    formData.step4.notes = aiData.step4.notes
    formData.step4.dueDate = aiData.step4.dueDate
    formData.step4.followUpDate = aiData.step4.followUpDate
  }
}

const goToStep = (step) => {
  currentStep.value = step
}

const validateAndProceed = (step) => {
  // Clear previous validation errors
  Object.keys(validationErrors).forEach(key => delete validationErrors[key])
  
  let isValid = true
  
  // Validate step 1
  if (step === 1) {
    if (!formData.step1.caseName) {
      validationErrors.caseName = 'Case name is required'
      isValid = false
    }
    if (!formData.step1.description) {
      validationErrors.description = 'Description is required'
      isValid = false
    }
    if (!formData.step1.priority) {
      validationErrors.priority = 'Priority is required'
      isValid = false
    }
    if (!formData.step1.status) {
      validationErrors.status = 'Status is required'
      isValid = false
    }
    if (!formData.step1.type) {
      validationErrors.type = 'Type is required'
      isValid = false
    }
    if (!formData.step1.source) {
      validationErrors.source = 'Source is required'
      isValid = false
    }
  }
  
  if (isValid) {
    currentStep.value = step + 1
  }
}

const skipStep = (step) => {
  currentStep.value = step + 1
}

const saveAndProceed = (step) => {
  currentStep.value = step + 1
}

const handleAssignmentTypeChange = () => {
  if (formData.step4.assignmentType !== 'individual') {
    formData.step4.selectedStaffId = null
  }
}

const selectStaff = (staffId) => {
  formData.step4.selectedStaffId = staffId
}

const getSelectedStaffName = () => {
  if (!formData.step4.selectedStaffId) return null
  
  const staff = staffMembers.find(s => s.id === formData.step4.selectedStaffId)
  return staff ? `${staff.name} (${staff.role})` : null
}

const formatGender = (gender) => {
  const genderMap = {
    'female': 'Female',
    'male': 'Male',
    'non-binary': 'Non-binary',
    'transgender': 'Transgender',
    'other': 'Other',
    'prefer-not-to-say': 'Prefer not to say'
  }
  return genderMap[gender] || gender
}

const formatIncidentType = (type) => {
  const typeMap = {
    'physical-abuse': 'Physical Abuse',
    'emotional-abuse': 'Emotional/Psychological Abuse',
    'sexual-assault': 'Sexual Assault',
    'stalking': 'Stalking',
    'financial-abuse': 'Financial Abuse',
    'human-trafficking': 'Human Trafficking',
    'other': 'Other'
  }
  return typeMap[type] || type
}

const formatSeverity = (severity) => {
  const severityMap = {
    'critical': 'Critical',
    'severe': 'Severe',
    'moderate': 'Moderate',
    'mild': 'Mild'
  }
  return severityMap[severity] || severity
}

const formatAssignmentType = (type) => {
  const typeMap = {
    'individual': 'Individual Staff Member',
    'team': 'Team',
    'auto': 'Auto-assign',
    'unassigned': 'Leave Unassigned'
  }
  return typeMap[type] || type
}

const formatTeam = (team) => {
  const teamMap = {
    'crisis-response': 'Crisis Response Team',
    'counseling': 'Counseling Team',
    'legal': 'Legal Support Team',
    'housing': 'Housing & Resources Team'
  }
  return teamMap[team] || team
}

const cancelForm = () => {
  router.push('/cases')
}

const submitCase = () => {
  // Here you would typically submit the form data
  console.log('Submitting case:', formData)
  alert('Case submitted successfully!')
  router.push('/cases')
}

// Lifecycle hooks
onMounted(() => {
  applyTheme()
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
  transition: background-color 0.3s, color 0.3s;
}

.case-creation-page {
  min-height: 100vh;
  background-color: var(--background-color);
  color: var(--text-color);
  padding: 20px;
  position: relative;
}

.back-button {
  position: absolute;
  top: 20px;
  left: 20px;
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--text-color);
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  padding: 8px 16px;
  border-radius: 8px;
  background-color: var(--content-bg);
  border: 1px solid var(--border-color);
  transition: background-color 0.3s, border-color 0.3s;
  z-index: 10;
}

.back-button:hover {
  background-color: var(--border-color);
}

.theme-toggle {
  position: absolute;
  top: 20px;
  right: 20px;
  display: flex;
  align-items: center;
  gap: 8px;
  background-color: var(--content-bg);
  color: var(--text-color);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 8px 16px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.3s, border-color 0.3s;
  z-index: 10;
}

.theme-toggle:hover {
  background-color: var(--border-color);
}

.case-container {
  display: flex;
  gap: 20px;
  max-width: 1400px;
  margin: 80px auto 0;
  min-height: calc(100vh - 120px);
}

.main-form-container {
  flex: 1;
  background-color: var(--content-bg);
  border-radius: 15px;
  padding: 30px;
  border: 1px solid var(--border-color);
  overflow-y: auto;
  max-height: calc(100vh - 120px);
}

.case-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid var(--border-color);
}

.case-header h1 {
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 8px;
}

.case-header p {
  color: var(--text-secondary);
  font-size: 16px;
}

.toggle-container {
  display: flex;
  align-items: center;
  gap: 12px;
}

.toggle-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 500;
  color: var(--text-color);
}

.ai-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 20px;
  height: 20px;
  background-color: var(--accent-color);
  border-radius: 4px;
}

.ai-icon svg {
  stroke: white;
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
  transition: 0.3s;
  border-radius: 24px;
}

.toggle-slider:before {
  position: absolute;
  content: "";
  height: 18px;
  width: 18px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  transition: 0.3s;
  border-radius: 50%;
}

input:checked + .toggle-slider {
  background-color: var(--accent-color);
}

input:checked + .toggle-slider:before {
  transform: translateX(26px);
}

.progress-container {
  margin-bottom: 40px;
}

.progress-steps {
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
  margin-bottom: 20px;
}

.progress-steps::before {
  content: '';
  position: absolute;
  top: 20px;
  left: 20px;
  right: 20px;
  height: 2px;
  background-color: var(--border-color);
  z-index: 1;
}

.progress-step {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  position: relative;
  z-index: 2;
}

.step-circle {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: var(--content-bg);
  border: 2px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 14px;
  transition: all 0.3s;
}

.step-circle.active {
  background-color: var(--accent-color);
  border-color: var(--accent-color);
  color: white;
}

.step-circle.completed {
  background-color: var(--success-color);
  border-color: var(--success-color);
  color: white;
}

.step-label {
  font-size: 12px;
  font-weight: 500;
  color: var(--text-secondary);
  text-align: center;
  transition: color 0.3s;
}

.step-label.active {
  color: var(--text-color);
  font-weight: 600;
}

.step-content {
  animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.case-form {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.form-section {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.section-title {
  font-size: 20px;
  font-weight: 600;
  color: var(--text-color);
  margin-bottom: 10px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.form-group label {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-color);
}

.form-control {
  padding: 12px 16px;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  background-color: var(--input-bg);
  color: var(--text-color);
  font-size: 14px;
  transition: border-color 0.3s, box-shadow 0.3s;
}

.form-control:focus {
  outline: none;
  border-color: var(--accent-color);
  box-shadow: 0 0 0 3px rgba(150, 75, 0, 0.1);
}

.form-control.error {
  border-color: var(--danger-color);
}

.form-control::placeholder {
  color: var(--text-secondary);
}

textarea.form-control {
  min-height: 100px;
  resize: vertical;
}

.error-message {
  color: var(--danger-color);
  font-size: 12px;
  font-weight: 500;
}

.staff-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 15px;
  margin-top: 10px;
}

.staff-card {
  background-color: var(--input-bg);
  border: 2px solid var(--border-color);
  border-radius: 12px;
  padding: 16px;
  cursor: pointer;
  transition: all 0.3s;
}

.staff-card:hover {
  border-color: var(--accent-color);
  transform: translateY(-2px);
}

.staff-card.selected {
  border-color: var(--accent-color);
  background-color: rgba(150, 75, 0, 0.1);
}

.staff-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.staff-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  overflow: hidden;
  flex-shrink: 0;
}

.staff-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.staff-info {
  flex: 1;
}

.staff-name {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-color);
  margin-bottom: 2px;
}

.staff-role {
  font-size: 14px;
  color: var(--text-secondary);
}

.staff-meta {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.staff-meta-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: var(--text-secondary);
}

.staff-meta-item svg {
  stroke: var(--text-secondary);
}

.form-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 20px;
  border-top: 1px solid var(--border-color);
}

.form-actions > div {
  display: flex;
  gap: 12px;
}

.btn {
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  border: none;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.btn-cancel {
  background-color: transparent;
  color: var(--text-secondary);
  border: 1px solid var(--border-color);
}

.btn-cancel:hover {
  background-color: var(--border-color);
  color: var(--text-color);
}

.btn-back {
  background-color: transparent;
  color: var(--text-color);
  border: 1px solid var(--border-color);
}

.btn-back:hover {
  background-color: var(--border-color);
}

.btn-skip {
  background-color: transparent;
  color: var(--text-secondary);
  border: 1px solid var(--border-color);
}

.btn-skip:hover {
  background-color: var(--border-color);
  color: var(--text-color);
}

.btn-next {
  background-color: var(--accent-color);
  color: white;
}

.btn-next:hover {
  background-color: var(--accent-hover);
}

.btn-submit {
  background-color: var(--success-color);
  color: white;
}

.btn-submit:hover {
  background-color: #45a049;
}

.review-sections {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.review-section {
  background-color: var(--input-bg);
  border-radius: 12px;
  padding: 20px;
  border: 1px solid var(--border-color);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 12px;
  border-bottom: 1px solid var(--border-color);
}

.edit-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  background-color: transparent;
  color: var(--accent-color);
  border: 1px solid var(--accent-color);
  border-radius: 6px;
  padding: 6px 12px;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
}

.edit-btn:hover {
  background-color: var(--accent-color);
  color: white;
}

.review-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 16px;
}

.review-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.review-label {
  font-size: 12px;
  font-weight: 500;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.review-value {
  font-size: 14px;
  color: var(--text-color);
  word-wrap: break-word;
}

.ai-preview-container {
  width: 400px;
  flex-shrink: 0;
}

.ai-preview {
  background-color: var(--content-bg);
  border-radius: 15px;
  border: 1px solid var(--border-color);
  height: calc(100vh - 120px);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.ai-preview-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 20px;
  border-bottom: 1px solid var(--border-color);
  background-color: var(--input-bg);
}

.ai-preview-header svg {
  stroke: var(--accent-color);
}

.ai-preview-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-color);
  display: flex;
  align-items: center;
  gap: 8px;
}

.ai-badge {
  background-color: var(--accent-color);
  color: white;
  font-size: 10px;
  font-weight: 500;
  padding: 2px 6px;
  border-radius: 4px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.ai-preview-content {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
}

.ai-preview-section {
  margin-bottom: 24px;
}

.ai-preview-section:last-child {
  margin-bottom: 0;
}

.ai-preview-section-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-color);
  margin-bottom: 12px;
  padding-bottom: 6px;
  border-bottom: 1px solid var(--border-color);
}

.ai-preview-item {
  margin-bottom: 12px;
}

.ai-preview-item:last-child {
  margin-bottom: 0;
}

.ai-preview-label {
  font-size: 11px;
  font-weight: 500;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 4px;
}

.ai-preview-value {
  font-size: 13px;
  color: var(--text-color);
  line-height: 1.4;
  word-wrap: break-word;
}

.ai-preview-value.na {
  color: var(--text-secondary);
  font-style: italic;
}

.modal-overlay {
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
  opacity: 0;
  visibility: hidden;
  transition: all 0.3s;
}

.modal-overlay.active {
  opacity: 1;
  visibility: visible;
}

.modal-content {
  background-color: var(--content-bg);
  border-radius: 12px;
  padding: 0;
  max-width: 500px;
  width: 90%;
  border: 1px solid var(--border-color);
  animation: modalSlideIn 0.3s ease-out;
}

@keyframes modalSlideIn {
  from {
    transform: translateY(-20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.modal-header {
  padding: 20px;
  border-bottom: 1px solid var(--border-color);
}

.modal-title {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 18px;
  font-weight: 600;
  color: var(--text-color);
}

.modal-title svg {
  stroke: var(--danger-color);
}

.modal-body {
  padding: 20px;
}

.modal-body p {
  color: var(--text-color);
  line-height: 1.5;
  margin: 0;
}

.modal-footer {
  padding: 20px;
  border-top: 1px solid var(--border-color);
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.modal-btn {
  padding: 10px 20px;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
  border: none;
}

.modal-btn-cancel {
  background-color: transparent;
  color: var(--text-secondary);
  border: 1px solid var(--border-color);
}

.modal-btn-cancel:hover {
  background-color: var(--border-color);
  color: var(--text-color);
}

.modal-btn-confirm {
  background-color: var(--danger-color);
  color: white;
}

.modal-btn-confirm:hover {
  background-color: #e6342a;
}

/* Responsive styles */
@media (max-width: 1200px) {
  .case-container {
    flex-direction: column;
  }
  
  .ai-preview-container {
    width: 100%;
  }
  
  .ai-preview {
    height: 400px;
  }
}

@media (max-width: 768px) {
  .case-creation-page {
    padding: 10px;
  }
  
  .case-container {
    margin-top: 60px;
  }
  
  .main-form-container {
    padding: 20px;
  }
  
  .case-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 15px;
  }
  
  .case-header h1 {
    font-size: 24px;
  }
  
  .form-row {
    grid-template-columns: 1fr;
  }
  
  .staff-list {
    grid-template-columns: 1fr;
  }
  
  .review-content {
    grid-template-columns: 1fr;
  }
  
  .form-actions {
    flex-direction: column;
    gap: 15px;
  }
  
  .form-actions > div {
    width: 100%;
    justify-content: center;
  }
  
  .progress-steps {
    flex-wrap: wrap;
    gap: 10px;
  }
  
  .step-circle {
    width: 35px;
    height: 35px;
    font-size: 12px;
  }
  
  .step-label {
    font-size: 11px;
  }
}

@media (max-width: 480px) {
  .back-button,
  .theme-toggle {
    position: relative;
    top: 0;
    left: 0;
    right: 0;
    margin-bottom: 10px;
  }
  
  .case-container {
    margin-top: 20px;
  }
  
  .main-form-container {
    padding: 15px;
  }
  
  .case-header h1 {
    font-size: 20px;
  }
  
  .btn {
    padding: 10px 16px;
    font-size: 13px;
  }
}
</style>