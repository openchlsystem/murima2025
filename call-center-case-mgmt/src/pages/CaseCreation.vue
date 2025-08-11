<template>
  <div class="case-creation-page">
    <div class="header-controls">
      <router-link class="back-button" to="/cases">
        <ChevronLeft class="w-4 h-4" />
        Back to Cases
      </router-link>

      <button class="theme-toggle" @click="toggleTheme">
        <component :is="theme === 'dark' ? Sun : Moon" class="w-4 h-4" />
        <span>{{ theme === 'dark' ? 'Light Mode' : 'Dark Mode' }}</span>
      </button>
    </div>

    <div class="case-container">
      <div class="main-form-container">
        <div class="case-header">
          <div>
            <h1>Create New Case</h1>
            <p>{{ stepDescriptions[currentStep - 1] }}</p>
          </div>
          <div class="toggle-container">
            <span class="toggle-label">
              <FlaskConical class="w-4 h-4" />
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
              v-for="(label, index) in stepLabels" 
              :key="index + 1"
              class="progress-step"
              :class="{ active: currentStep >= index + 1 }"
              @click="goToStep(index + 1)"
            >
              <div class="step-circle" :class="{ active: currentStep >= index + 1, completed: currentStep > index + 1 }">
                <Check v-if="currentStep > index + 1" class="w-5 h-5" />
                <span v-else>{{ index + 1 }}</span>
              </div>
              <div class="step-label" :class="{ active: currentStep >= index + 1 }">{{ label }}</div>
            </div>
          </div>
        </div>

        <!-- Step 1: Reporter Selection -->
        <div v-show="currentStep === 1" class="step-content">
          <form class="case-form" @submit.prevent="validateAndProceed(1)">
            <div class="form-section">
              <div class="section-title">Select Reporter</div>
              <p class="section-description">Choose an existing contact or create a new reporter for this case.</p>
              
              <div class="search-section">
                <div class="search-box">
                  <Search class="w-4 h-4" />
                  <input 
                    v-model="searchQuery" 
                    type="text" 
                    placeholder="Search existing contacts..." 
                    class="search-input"
                  />
                </div>
              </div>

              <div class="contacts-grid">
                <div 
                  v-for="contact in filteredContacts" 
                  :key="contact.id"
                  class="contact-card"
                  :class="{ selected: selectedReporter?.id === contact.id }"
                  @click="selectExistingReporter(contact)"
                >
                  <div class="contact-avatar">
                    <span>{{ getInitials(contact.name) }}</span>
                  </div>
                  <div class="contact-info">
                    <div class="contact-name">{{ contact.name }}</div>
                    <div class="contact-details">
                      <span class="contact-tag">{{ contact.age }}y</span>
                      <span class="contact-tag">{{ contact.gender }}</span>
                    </div>
                    <div class="contact-meta">
                      <div class="contact-location">📍 {{ contact.location }}</div>
                      <div class="contact-phone">📞 {{ contact.phone }}</div>
                    </div>
                    <div class="contact-timestamp">{{ contact.lastContact }}</div>
                  </div>
                  <div class="contact-select-indicator">
                    <Check v-if="selectedReporter?.id === contact.id" class="w-5 h-5" />
                  </div>
                </div>
              </div>

              <div class="action-buttons">
                <button 
                  v-if="selectedReporter" 
                  type="submit"
                  class="btn btn-primary btn-large" 
                >
                  <Check class="w-4 h-4" />
                  Continue with {{ selectedReporter.name }}
                </button>
                <button type="button" class="btn btn-secondary btn-large" @click="createNewReporter">
                  <Plus class="w-4 h-4" />
                  Create New Reporter
                </button>
              </div>
            </div>
            <div class="form-actions">
              <button type="button" class="btn btn-cancel" @click="cancelForm">Cancel</button>
              <div class="form-actions-right">
                <button type="button" class="btn btn-skip" @click="skipStep(1)">Skip</button>
                <button type="submit" class="btn btn-next" :disabled="!selectedReporter">Next</button>
              </div>
            </div>
          </form>
        </div>

        <!-- Step 2: Reporter Details -->
        <div v-show="currentStep === 2" class="step-content">
          <form class="case-form" @submit.prevent="saveAndProceed(2)">
            <div class="form-section">
              <div class="section-title">
                {{ selectedReporter ? 'Reporter Details' : 'New Reporter Information' }}
              </div>
              <p class="section-description">Enter the reporter's contact information and details.</p>
              
              <div class="form-row">
                <div class="form-group">
                  <label for="reporter-name">Full Name*</label>
                  <input 
                    v-model="formData.step2.name"
                    type="text" 
                    id="reporter-name" 
                    class="form-control" 
                    placeholder="Enter full name"
                    required
                    :readonly="!!selectedReporter"
                  />
                </div>
                <div class="form-group">
                  <label for="reporter-age">Age</label>
                  <input 
                    v-model="formData.step2.age"
                    type="number" 
                    id="reporter-age" 
                    class="form-control" 
                    placeholder="Enter age"
                    min="1"
                    max="120"
                  />
                </div>
              </div>
              
              <div class="form-row">
                <div class="form-group">
                  <label for="reporter-gender">Gender</label>
                  <select v-model="formData.step2.gender" id="reporter-gender" class="form-control">
                    <option value="">Select gender</option>
                    <option value="female">Female</option>
                    <option value="male">Male</option>
                    <option value="non-binary">Non-binary</option>
                    <option value="transgender">Transgender</option>
                    <option value="other">Other</option>
                    <option value="prefer-not-to-say">Prefer not to say</option>
                  </select>
                </div>
                <div class="form-group">
                  <label for="reporter-location">Location</label>
                  <input 
                    v-model="formData.step2.location"
                    type="text" 
                    id="reporter-location" 
                    class="form-control" 
                    placeholder="Enter location"
                  />
                </div>
              </div>
              
              <div class="form-row">
                <div class="form-group">
                  <label for="reporter-phone">Phone Number*</label>
                  <input 
                    v-model="formData.step2.phone"
                    type="tel" 
                    id="reporter-phone" 
                    class="form-control" 
                    placeholder="Enter phone number"
                    required
                  />
                </div>
                <div class="form-group">
                  <label for="reporter-alt-phone">Alternative Phone</label>
                  <input 
                    v-model="formData.step2.altPhone"
                    type="tel" 
                    id="reporter-alt-phone" 
                    class="form-control" 
                    placeholder="Enter alternative phone"
                  />
                </div>
              </div>
              
              <div class="form-group">
                <label for="reporter-email">Email Address</label>
                <input 
                  v-model="formData.step2.email"
                  type="email" 
                  id="reporter-email" 
                  class="form-control" 
                  placeholder="Enter email address"
                />
              </div>
              
              <div class="form-row">
                <div class="form-group">
                  <label for="reporter-id-type">ID Type</label>
                  <select v-model="formData.step2.idType" id="reporter-id-type" class="form-control">
                    <option value="">Select ID type</option>
                    <option value="national-id">National ID</option>
                    <option value="passport">Passport</option>
                    <option value="drivers-license">Driver's License</option>
                    <option value="other">Other</option>
                  </select>
                </div>
                <div class="form-group">
                  <label for="reporter-id-number">ID Number</label>
                  <input 
                    v-model="formData.step2.idNumber"
                    type="text" 
                    id="reporter-id-number" 
                    class="form-control" 
                    placeholder="Enter ID number"
                  />
                </div>
              </div>

              <div class="form-group">
                <label>Is Reporter also a Client?</label>
                <div class="radio-group">
                  <label class="radio-option">
                    <input 
                      v-model="formData.step2.isClient" 
                      type="radio" 
                      :value="true"
                    />
                    <span class="radio-indicator"></span>
                    <span class="radio-label">Yes</span>
                  </label>
                  <label class="radio-option">
                    <input 
                      v-model="formData.step2.isClient" 
                      type="radio" 
                      :value="false"
                    />
                    <span class="radio-indicator"></span>
                    <span class="radio-label">No</span>
                  </label>
                </div>
              </div>

              <!-- Client Management Section -->
              <div v-if="formData.step2.isClient === false" class="client-management-section">
                <div class="section-title">Clients</div>
                <div class="client-list">
                  <div v-for="client in clients" :key="client.id" class="client-item">
                    <div class="client-info">
                      <span class="client-name">{{ client.name }}</span>
                      <span class="client-details">{{ client.age }}y, {{ client.gender }}</span>
                    </div>
                    <button type="button" class="btn btn-tiny btn-outline" @click="removeClient(client.id)">
                      <X class="w-3 h-3" />
                    </button>
                  </div>
                </div>
                <div class="client-actions">
                  <button type="button" class="btn btn-secondary" @click="openAddClientModal">
                    <Plus class="w-4 h-4" />
                    Add a Client
                  </button>
                  <button type="button" class="btn btn-secondary" @click="openAddToContactsModal">
                    <UserPlus class="w-4 h-4" />
                    Add to Clients/Contacts
                  </button>
                </div>
              </div>

              <!-- Perpetrators Section -->
              <div class="perpetrators-section">
                <div class="section-title">Perpetrators</div>
                <div class="perpetrator-list">
                  <div v-for="perpetrator in perpetrators" :key="perpetrator.id" class="perpetrator-item">
                    <div class="perpetrator-info">
                      <span class="perpetrator-name">{{ perpetrator.name }}</span>
                      <span class="perpetrator-details">{{ perpetrator.relationship }}</span>
                    </div>
                    <button type="button" class="btn btn-tiny btn-outline" @click="removePerpetrator(perpetrator.id)">
                      <X class="w-3 h-3" />
                    </button>
                  </div>
                </div>
                <button type="button" class="btn btn-secondary" @click="openAddPerpetratorModal">
                  <Plus class="w-4 h-4" />
                  Add a Perpetrator
                </button>
              </div>

              <!-- Related Files Section -->
              <div class="related-files-section">
                <div class="section-title">Related Files</div>
                <div class="file-list">
                  <div v-for="file in relatedFiles" :key="file.id" class="file-item">
                    <div class="file-info">
                      <FileText class="w-4 h-4" />
                      <span class="file-name">{{ file.name }}</span>
                      <span class="file-size">{{ file.size }}</span>
                    </div>
                    <button type="button" class="btn btn-tiny btn-outline" @click="removeFile(file.id)">
                      <X class="w-3 h-3" />
                    </button>
                  </div>
                </div>
                <button type="button" class="btn btn-secondary" @click="attachFile">
                  <Paperclip class="w-4 h-4" />
                  Attach a File
                </button>
              </div>
            </div>
            <div class="form-actions">
              <button type="button" class="btn btn-back" @click="goToStep(1)">Back</button>
              <div class="form-actions-right">
                <button type="button" class="btn btn-skip" @click="skipStep(2)">Skip</button>
                <button type="submit" class="btn btn-next">Next</button>
              </div>
            </div>
          </form>
        </div>

        <!-- Step 3: Case Details -->
        <div v-show="currentStep === 3" class="step-content">
          <form class="case-form" @submit.prevent="saveAndProceed(3)">
            <div class="form-section">
              <div class="section-title">Case Information</div>
              <p class="section-description">Provide detailed information about the case and incident.</p>
              
              <div class="form-group">
                <label for="case-narrative">Case Narrative*</label>
                <textarea 
                  v-model="formData.step3.narrative"
                  id="case-narrative" 
                  class="form-control" 
                  placeholder="Describe the case details, incident, and circumstances in detail..."
                  required
                  rows="6"
                ></textarea>
              </div>

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
                <label for="incident-location">Location of Incident</label>
                <input 
                  v-model="formData.step3.location"
                  type="text" 
                  id="incident-location" 
                  class="form-control" 
                  placeholder="Enter location where incident occurred"
                />
              </div>

              <div class="form-group">
                <label>Is this Case GBV Related?*</label>
                <div class="radio-group">
                  <label class="radio-option">
                    <input 
                      v-model="formData.step3.isGBVRelated" 
                      type="radio" 
                      :value="true"
                      required
                    />
                    <span class="radio-indicator"></span>
                    <span class="radio-label">Yes</span>
                  </label>
                  <label class="radio-option">
                    <input 
                      v-model="formData.step3.isGBVRelated" 
                      type="radio" 
                      :value="false"
                      required
                    />
                    <span class="radio-indicator"></span>
                    <span class="radio-label">No</span>
                  </label>
                </div>
              </div>

              <div class="form-group">
                <label for="case-plan">Case Plan</label>
                <textarea 
                  v-model="formData.step3.casePlan"
                  id="case-plan" 
                  class="form-control" 
                  placeholder="Outline the planned interventions and support services..."
                  rows="4"
                ></textarea>
              </div>
            </div>
            <div class="form-actions">
              <button type="button" class="btn btn-back" @click="goToStep(2)">Back</button>
              <div class="form-actions-right">
                <button type="button" class="btn btn-skip" @click="skipStep(3)">Skip</button>
                <button type="submit" class="btn btn-next">Next</button>
              </div>
            </div>
          </form>
        </div>

        <!-- Step 4: Case Classification -->
        <div v-show="currentStep === 4" class="step-content">
          <form class="case-form" @submit.prevent="saveAndProceed(4)">
            <div class="form-section">
              <div class="section-title">Case Classification & Assignment</div>
              <p class="section-description">Classify the case and set priority levels for proper handling.</p>
              
              <div class="form-row">
                <div class="form-group">
                  <label>Department*</label>
                  <div class="radio-group">
                    <label class="radio-option">
                      <input 
                        v-model="formData.step4.department" 
                        type="radio" 
                        value="116"
                        required
                      />
                      <span class="radio-indicator"></span>
                      <span class="radio-label">116 (Emergency Helpline)</span>
                    </label>
                    <label class="radio-option">
                      <input 
                        v-model="formData.step4.department" 
                        type="radio" 
                        value="labor"
                        required
                      />
                      <span class="radio-indicator"></span>
                      <span class="radio-label">Labor Department</span>
                    </label>
                  </div>
                </div>
                <div class="form-group">
                  <label for="case-category">Case Category*</label>
                  <div class="relative">
                    <button
                      type="button"
                      class="form-control multi-select-button"
                      @click="toggleCategoryDropdown"
                    >
                      <div class="flex flex-wrap gap-1">
                        <span v-if="formData.step4.category.length === 0" class="text-secondary">Select category</span>
                        <span
                          v-for="value in formData.step4.category"
                          :key="value"
                          class="selected-tag"
                        >
                          {{ caseCategoryOptions.find(opt => opt.value === value)?.label }}
                          <button
                            type="button"
                            class="remove-tag-button"
                            @click.stop="handleCategorySelect(value)"
                          >
                            <X class="w-3 h-3" />
                          </button>
                        </span>
                      </div>
                      <ChevronDown class="ml-2 h-4 w-4 shrink-0 opacity-50" />
                    </button>
                    <div v-if="showCategoryDropdown" class="multi-select-dropdown">
                      <div class="p-1">
                        <input
                          type="text"
                          placeholder="Search options..."
                          class="form-control search-input-dropdown"
                          v-model="categorySearchQuery"
                        />
                        <div class="multi-select-options-container">
                          <div v-if="filteredCategoryOptions.length === 0" class="no-options-found">No options found.</div>
                          <div
                            v-for="option in filteredCategoryOptions"
                            :key="option.value"
                            class="multi-select-option"
                            :class="{ 'selected-option': formData.step4.category.includes(option.value) }"
                            @click="handleCategorySelect(option.value)"
                          >
                            <Check
                              :class="['mr-2 h-4 w-4', formData.step4.category.includes(option.value) ? 'opacity-100' : 'opacity-0']"
                            />
                            {{ option.label }}
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Conditional Modules based on Case Category -->
              <div v-if="showMedicalAndCounselingModules" class="conditional-module-section">
                <h4 class="subsection-title">Additional Case Details</h4>
                <p class="section-description">
                  Provide further details relevant to the selected case categories.
                </p>

                <div class="form-group">
                  <label>Has the client received medical examination?</label>
                  <div class="radio-group">
                    <label class="radio-option">
                      <input type="radio" value="yes" v-model="formData.step4.receivedMedicalExam" />
                      <span class="radio-indicator"></span>
                      <span class="radio-label">Yes</span>
                    </label>
                    <label class="radio-option">
                      <input type="radio" value="no" v-model="formData.step4.receivedMedicalExam" />
                      <span class="radio-indicator"></span>
                      <span class="radio-label">No</span>
                    </label>
                    <label class="radio-option">
                      <input type="radio" value="unknown" v-model="formData.step4.receivedMedicalExam" />
                      <span class="radio-indicator"></span>
                      <span class="radio-label">Unknown</span>
                    </label>
                  </div>
                </div>

                <div class="form-group">
                  <label>Was ECP provided to prevent Un-intended pregnancies?</label>
                  <div class="radio-group">
                    <label class="radio-option">
                      <input type="radio" value="yes" v-model="formData.step4.preventedUnintendedPregnancies" />
                      <span class="radio-indicator"></span>
                      <span class="radio-label">Yes</span>
                    </label>
                    <label class="radio-option">
                      <input type="radio" value="no" v-model="formData.step4.preventedUnintendedPregnancies" />
                      <span class="radio-indicator"></span>
                      <span class="radio-label">No</span>
                    </label>
                    <label class="radio-option">
                      <input type="radio" value="unknown" v-model="formData.step4.preventedUnintendedPregnancies" />
                      <span class="radio-indicator"></span>
                      <span class="radio-label">Unknown</span>
                    </label>
                  </div>
                </div>

                <div class="form-group">
                  <label>Has the Client been tested for HIV?</label>
                  <div class="radio-group">
                    <label class="radio-option">
                      <input type="radio" value="yes" v-model="formData.step4.testedForHIV" />
                      <span class="radio-indicator"></span>
                      <span class="radio-label">Yes</span>
                    </label>
                    <label class="radio-option">
                      <input type="radio" value="no" v-model="formData.step4.testedForHIV" />
                      <span class="radio-indicator"></span>
                      <span class="radio-label">No</span>
                    </label>
                    <label class="radio-option">
                      <input type="radio" value="unknown" v-model="formData.step4.testedForHIV" />
                      <span class="radio-indicator"></span>
                      <span class="radio-label">Unknown</span>
                    </label>
                  </div>
                </div>

                <div class="form-group">
                  <label>
                    Did the client get counselling / referred for Counselling and further psycho-social support?
                  </label>
                  <div class="radio-group">
                    <label class="radio-option">
                      <input type="radio" value="yes" v-model="formData.step4.receivedCounselling" />
                      <span class="radio-indicator"></span>
                      <span class="radio-label">Yes</span>
                    </label>
                    <label class="radio-option">
                      <input type="radio" value="no" v-model="formData.step4.receivedCounselling" />
                      <span class="radio-indicator"></span>
                      <span class="radio-label">No</span>
                    </label>
                    <label class="radio-option">
                      <input type="radio" value="unknown" v-model="formData.step4.receivedCounselling" />
                      <span class="radio-indicator"></span>
                      <span class="radio-label">Unknown</span>
                    </label>
                  </div>
                </div>
              </div>
              
              <div class="form-row">
                <div class="form-group">
                  <label for="priority">Priority*</label>
                  <select 
                    v-model="formData.step4.priority"
                    id="priority" 
                    class="form-control"
                    required
                  >
                    <option value="">Select priority</option>
                    <option value="critical">🔴 Critical</option>
                    <option value="high">🟠 High</option>
                    <option value="medium">🟡 Medium</option>
                    <option value="low">🟢 Low</option>
                  </select>
                </div>
                <div class="form-group">
                  <label for="status">Status*</label>
                  <select 
                    v-model="formData.step4.status"
                    id="status" 
                    class="form-control"
                    required
                  >
                    <option value="">Select status</option>
                    <option value="new">New</option>
                    <option value="in-progress">In Progress</option>
                    <option value="pending">Pending</option>
                    <option value="resolved">Resolved</option>
                  </select>
                </div>
              </div>

              <div class="form-group">
                <label for="escalated-to">Escalated To</label>
                <select 
                  v-model="formData.step4.escalatedTo"
                  id="escalated-to" 
                  class="form-control"
                >
                  <option value="">Select escalation level</option>
                  <option value="supervisor">Supervisor</option>
                  <option value="manager">Manager</option>
                  <option value="director">Director</option>
                  <option value="external-agency">External Agency</option>
                  <option value="law-enforcement">Law Enforcement</option>
                </select>
              </div>

              <div class="form-group">
                <label>Services Offered</label>
                <div class="checkbox-grid">
                  <label class="checkbox-option">
                    <input 
                      type="checkbox" 
                      value="counseling"
                      :checked="formData.step4.servicesOffered.includes('counseling')"
                      @change="e => handleServiceChange('counseling', e.target.checked)"
                    />
                    <span class="checkbox-indicator"></span>
                    <span class="checkbox-label">Counseling</span>
                  </label>
                  <label class="checkbox-option">
                    <input 
                      type="checkbox" 
                      value="legal-aid"
                      :checked="formData.step4.servicesOffered.includes('legal-aid')"
                      @change="e => handleServiceChange('legal-aid', e.target.checked)"
                    />
                    <span class="checkbox-indicator"></span>
                    <span class="checkbox-label">Legal Aid</span>
                  </label>
                  <label class="checkbox-option">
                    <input 
                      type="checkbox" 
                      value="shelter"
                      :checked="formData.step4.servicesOffered.includes('shelter')"
                      @change="e => handleServiceChange('shelter', e.target.checked)"
                    />
                    <span class="checkbox-indicator"></span>
                    <span class="checkbox-label">Shelter</span>
                  </label>
                  <label class="checkbox-option">
                    <input 
                      type="checkbox" 
                      value="medical-assistance"
                      :checked="formData.step4.servicesOffered.includes('medical-assistance')"
                      @change="e => handleServiceChange('medical-assistance', e.target.checked)"
                    />
                    <span class="checkbox-indicator"></span>
                    <span class="checkbox-label">Medical Assistance</span>
                  </label>
                  <label class="checkbox-option">
                    <input 
                      type="checkbox" 
                      value="financial-support"
                      :checked="formData.step4.servicesOffered.includes('financial-support')"
                      @change="e => handleServiceChange('financial-support', e.target.checked)"
                    />
                    <span class="checkbox-indicator"></span>
                    <span class="checkbox-label">Financial Support</span>
                  </label>
                  <label class="checkbox-option">
                    <input 
                      type="checkbox" 
                      value="referral"
                      :checked="formData.step4.servicesOffered.includes('referral')"
                      @change="e => handleServiceChange('referral', e.target.checked)"
                    />
                    <span class="checkbox-indicator"></span>
                    <span class="checkbox-label">Referral Services</span>
                  </label>
                </div>
              </div>
            </div>
            <div class="form-actions">
              <button type="button" class="btn btn-back" @click="goToStep(3)">Back</button>
              <div class="form-actions-right">
                <button type="button" class="btn btn-skip" @click="skipStep(4)">Skip</button>
                <button type="submit" class="btn btn-next">Next</button>
              </div>
            </div>
          </form>
        </div>

        <!-- Step 5: Review -->
        <div v-show="currentStep === 5" class="step-content">
          <div class="review-sections">
            <div class="review-section">
              <div class="section-header">
                <div class="section-title">Reporter Information</div>
                <button class="edit-btn" @click="goToStep(2)">
                  <Edit class="w-4 h-4" />
                  Edit
                </button>
              </div>
              <div class="review-content">
                <div class="review-item">
                  <div class="review-label">Name</div>
                  <div class="review-value">{{ formData.step2.name || 'N/A' }}</div>
                </div>
                <div class="review-item">
                  <div class="review-label">Phone</div>
                  <div class="review-value">{{ formData.step2.phone || 'N/A' }}</div>
                </div>
                <div class="review-item">
                  <div class="review-label">Location</div>
                  <div class="review-value">{{ formData.step2.location || 'N/A' }}</div>
                </div>
                <div class="review-item">
                  <div class="review-label">Is Client</div>
                  <div class="review-value">
                    <span class="status-badge" :class="formData.step2.isClient ? 'status-yes' : 'status-no'">
                      {{ formData.step2.isClient ? 'Yes' : 'No' }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="review-section">
              <div class="section-header">
                <div class="section-title">Case Details</div>
                <button class="edit-btn" @click="goToStep(3)">
                  <Edit class="w-4 h-4" />
                  Edit
                </button>
              </div>
              <div class="review-content">
                <div class="review-item review-item-full">
                  <div class="review-label">Case Narrative</div>
                  <div class="review-value">{{ formData.step3.narrative || 'N/A' }}</div>
                </div>
                <div class="review-item">
                  <div class="review-label">GBV Related</div>
                  <div class="review-value">
                    <span class="status-badge" :class="formData.step3.isGBVRelated ? 'status-warning' : 'status-info'">
                      {{ formData.step3.isGBVRelated ? 'Yes' : 'No' }}
                    </span>
                  </div>
                </div>
                <div class="review-item">
                  <div class="review-label">Incident Date</div>
                  <div class="review-value">{{ formData.step3.incidentDate || 'N/A' }}</div>
                </div>
                <div class="review-item">
                  <div class="review-label">Location</div>
                  <div class="review-value">{{ formData.step3.location || 'N/A' }}</div>
                </div>
              </div>
            </div>
            
            <div class="review-section">
              <div class="section-header">
                <div class="section-title">Classification</div>
                <button class="edit-btn" @click="goToStep(4)">
                  <Edit class="w-4 h-4" />
                  Edit
                </button>
              </div>
              <div class="review-content">
                <div class="review-item">
                  <div class="review-label">Department</div>
                  <div class="review-value">{{ formatDepartment(formData.step4.department) || 'N/A' }}</div>
                </div>
                <div class="review-item">
                  <div class="review-label">Category</div>
                  <div class="review-value">{{ formatCategory(formData.step4.category) || 'N/A' }}</div>
                </div>
                <div class="review-item">
                  <div class="review-label">Priority</div>
                  <div class="review-value">
                    <span v-if="formData.step4.priority" class="priority-badge" :class="`priority-${formData.step4.priority}`">
                      {{ formatPriority(formData.step4.priority) }}
                    </span>
                    <span v-else>N/A</span>
                  </div>
                </div>
                <div class="review-item">
                  <div class="review-label">Status</div>
                  <div class="review-value">
                    <span v-if="formData.step4.status" class="status-badge status-info">
                      {{ formatStatus(formData.step4.status) }}
                    </span>
                    <span v-else>N/A</span>
                  </div>
                </div>
                <div class="review-item review-item-full">
                  <div class="review-label">Services Offered</div>
                  <div class="review-value">
                    <div v-if="formData.step4.servicesOffered.length > 0" class="services-tags">
                      <span 
                        v-for="service in formData.step4.servicesOffered" 
                        :key="service" 
                        class="service-tag"
                      >
                        {{ formatService(service) }}
                      </span>
                    </div>
                    <span v-else>None selected</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <div class="form-actions">
            <button type="button" class="btn btn-back" @click="goToStep(4)">Back</button>
            <button type="button" class="btn btn-primary" @click="submitCase">Create Case</button>
          </div>
        </div>
      </div>
      
      <!-- Enhanced AI Insights Panel -->
      <div v-if="isAIEnabled" class="ai-preview-container">
        <div class="ai-preview">
          <div class="ai-preview-header">
            <FlaskConical class="w-6 h-6" />
            <div class="ai-preview-title">AI Insights <span class="ai-badge">LIVE</span></div>
          </div>
          <div class="ai-preview-content">
            <!-- Audio Transcription Results -->
            <div v-if="transcriptionData" class="ai-preview-section">
              <div class="ai-preview-section-title">Audio Analysis Results</div>
              <!-- Transcription -->
              <div v-if="transcriptionData.transcript" class="transcription-section">
                <h4 class="subsection-title">Transcription</h4>
                <div class="transcription-text">{{ transcriptionData.transcript }}</div>
                <button class="btn btn-tiny btn-outline" @click="useTranscription">Use in Case Narrative</button>
              </div>
              <!-- Summary -->
              <div v-if="transcriptionData.summary" class="summary-section">
                <h4 class="subsection-title">Summary</h4>
                <div class="summary-text">{{ transcriptionData.summary }}</div>
              </div>
              <!-- Named Entities -->
              <div v-if="transcriptionData.summary_entities && transcriptionData.summary_entities.length" class="entities-section">
                <h4 class="subsection-title">Detected Entities</h4>
                <div class="entity-suggestions">
                  <div v-for="entity in transcriptionData.summary_entities" :key="entity.text" class="entity-suggestion">
                    <span class="entity-text">{{ entity.text }}</span>
                    <span class="entity-label">{{ entity.label }}</span>
                    <button class="btn btn-tiny btn-outline" @click="useEntity(entity)">Use</button>
                  </div>
                </div>
              </div>
              <!-- Classification Suggestions -->
              <div v-if="transcriptionData.summary_classification" class="classification-section">
                <h4 class="subsection-title">AI Classification Suggestions</h4>
                <div class="classification-suggestions">
                  <div class="suggestion-item">
                    <span class="suggestion-label">Category:</span>
                    <span class="suggestion-value">{{ transcriptionData.summary_classification.sub_category }}</span>
                    <button class="btn btn-tiny btn-primary" @click="useClassification('category', transcriptionData.summary_classification.sub_category)">Use This Category</button>
                  </div>
                  <div class="suggestion-item">
                    <span class="suggestion-label">Priority:</span>
                    <span class="suggestion-value">{{ getPriorityText(transcriptionData.summary_classification.priority) }}</span>
                    <button class="btn btn-tiny btn-primary" @click="useClassification('priority', getPriorityValue(transcriptionData.summary_classification.priority))">Use This Priority</button>
                  </div>
                  <div class="suggestion-item">
                    <span class="suggestion-label">Intervention:</span>
                    <span class="suggestion-value">{{ transcriptionData.summary_classification.intervention }}</span>
                    <button class="btn btn-tiny btn-primary" @click="useClassification('intervention', transcriptionData.summary_classification.intervention)">Add to Services</button>
                  </div>
                </div>
              </div>
            </div>
            <!-- AI Insights from Audio -->
            <div v-if="aiInsights" class="ai-preview-section">
              <div class="ai-preview-section-title">Detailed AI Insights</div>
              <!-- Case Summary -->
              <div v-if="aiInsights.case_summary" class="insight-section">
                <h4 class="subsection-title">Case Summary</h4>
                <p class="insight-text">{{ aiInsights.case_summary }}</p>
                <button class="btn btn-tiny btn-outline" @click="useCaseSummary">Use in Case Plan</button>
              </div>
              <!-- Named Entities -->
              <div v-if="aiInsights.named_entities" class="insight-section">
                <h4 class="subsection-title">Key Information</h4>
                <div v-if="aiInsights.named_entities.persons && aiInsights.named_entities.persons.length" class="entity-group">
                  <h5 class="entity-type">Persons Involved</h5>
                  <div class="entity-tags">
                    <span v-for="person in aiInsights.named_entities.persons" :key="person" class="entity-tag">{{ person }}<button class="entity-use-btn" @click="usePerson(person)"><Plus class="w-3 h-3" /></button></span>
                  </div>
                </div>
                <div v-if="aiInsights.named_entities.locations && aiInsights.named_entities.locations.length" class="entity-group">
                  <h5 class="entity-type">Locations</h5>
                  <div class="entity-tags">
                    <span v-for="location in aiInsights.named_entities.locations" :key="location" class="entity-tag">{{ location }}<button class="entity-use-btn" @click="useLocation(location)"><Plus class="w-3 h-3" /></button></span>
                  </div>
                </div>
                <div v-if="aiInsights.named_entities.organizations && aiInsights.named_entities.organizations.length" class="entity-group">
                  <h5 class="entity-type">Organizations</h5>
                  <div class="entity-tags">
                    <span v-for="org in aiInsights.named_entities.organizations" :key="org" class="entity-tag">{{ org }}<button class="entity-use-btn" @click="useOrganization(org)"><Plus class="w-3 h-3" /></button></span>
                  </div>
                </div>
              </div>
              <!-- Risk Assessment -->
              <div v-if="aiInsights.risk_assessment" class="insight-section">
                <h4 class="subsection-title">Risk Assessment</h4>
                <div v-if="aiInsights.risk_assessment.red_flags && aiInsights.risk_assessment.red_flags.length" class="risk-group">
                  <h5 class="risk-type"><Flag class="w-3 h-3 text-red-500" /> Red Flags</h5>
                  <ul class="risk-list">
                    <li v-for="flag in aiInsights.risk_assessment.red_flags" :key="flag">{{ flag }}</li>
                  </ul>
                </div>
                <div v-if="aiInsights.risk_assessment.protective_factors && aiInsights.risk_assessment.protective_factors.length" class="risk-group">
                  <h5 class="risk-type"><Shield class="w-3 h-3 text-green-500" /> Protective Factors</h5>
                  <ul class="risk-list">
                    <li v-for="factor in aiInsights.risk_assessment.protective_factors" :key="factor">{{ factor }}</li>
                  </ul>
                </div>
              </div>
              <!-- Recommended Services -->
              <div v-if="aiInsights.case_management && aiInsights.case_management.psychosocial_support" class="insight-section">
                <h4 class="subsection-title">Recommended Services</h4>
                <div v-if="aiInsights.case_management.psychosocial_support.short_term && aiInsights.case_management.psychosocial_support.short_term.length" class="service-group">
                  <h5 class="service-type">Immediate Support</h5>
                  <div class="service-suggestions">
                    <button v-for="service in aiInsights.case_management.psychosocial_support.short_term" :key="service" class="service-suggestion-btn" @click="addRecommendedService(service)">{{ service }}<span class="add-icon"><Plus class="w-3 h-3" /></span></button>
                  </div>
                </div>
                <div v-if="aiInsights.case_management.psychosocial_support.long_term && aiInsights.case_management.psychosocial_support.long_term.length" class="service-group">
                  <h5 class="service-type">Long-term Support</h5>
                  <div class="service-suggestions">
                    <button v-for="service in aiInsights.case_management.psychosocial_support.long_term" :key="service" class="service-suggestion-btn" @click="addRecommendedService(service)">{{ service }}<span class="add-icon"><Plus class="w-3 h-3" /></span></button>
                  </div>
                </div>
              </div>
            </div>
            <!-- Original AI Auto-Fill Section -->
            <div class="ai-preview-section">
              <div class="ai-preview-section-title">AI Auto-Fill</div>
              <div class="ai-autofill-section">
                <p class="ai-autofill-description">Let AI automatically populate form fields with sample data based on common case patterns.</p>
                <button class="btn btn-primary btn-small ai-autofill-btn" @click="openAutoFillModal">
                  <FlaskConical class="w-4 h-4" />
                  Auto-Fill Current Step
                </button>
              </div>
            </div>
            <!-- Smart Suggestions -->
            <div class="ai-preview-section">
              <div class="ai-preview-section-title">Smart Suggestions</div>
              <div class="ai-suggestions">
                <div v-for="suggestion in getActiveSuggestions()" :key="suggestion.id" class="ai-suggestion" :class="`suggestion-${suggestion.type}`">
                  <div class="suggestion-icon">{{ suggestion.icon }}</div>
                  <div class="suggestion-content">
                    <div class="suggestion-text">{{ suggestion.text }}</div>
                    <div v-if="suggestion.action" class="suggestion-action">
                      <button class="btn btn-tiny btn-outline" @click="applySuggestion(suggestion)">Apply</button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <!-- Case Summary -->
            <div class="ai-preview-section">
              <div class="ai-preview-section-title">Case Summary</div>
              <div class="ai-summary">
                <div class="summary-item">
                  <div class="summary-label">Reporter</div>
                  <div class="summary-value">{{ formData.step2.name || 'Not selected' }}</div>
                </div>
                <div class="summary-item">
                  <div class="summary-label">Case Type</div>
                  <div class="summary-value">{{ formatCategory(formData.step4.category) || 'Not classified' }}</div>
                </div>
                <div class="summary-item">
                  <div class="summary-label">Priority</div>
                  <div class="summary-value">
                    <span v-if="formData.step4.priority" class="priority-badge" :class="`priority-${formData.step4.priority}`">{{ formatPriority(formData.step4.priority) }}</span>
                    <span v-else class="text-muted">Not set</span>
                  </div>
                </div>
                <div class="summary-item">
                  <div class="summary-label">GBV Related</div>
                  <div class="summary-value">
                    <span v-if="formData.step3.isGBVRelated !== null" class="status-badge" :class="formData.step3.isGBVRelated ? 'status-warning' : 'status-info'">{{ formData.step3.isGBVRelated ? 'Yes' : 'No' }}</span>
                    <span v-else class="text-muted">Not specified</span>
                  </div>
                </div>
              </div>
            </div>
            <!-- Progress Insights -->
            <div v-if="getCompletedSteps().length > 0" class="ai-preview-section">
              <div class="ai-preview-section-title">Progress Insights</div>
              <div class="progress-insights">
                <div class="insight-item">
                  <BarChart class="w-4 h-4" />
                  <div class="insight-text">{{ getCompletedSteps().length }} of {{ totalSteps }} steps completed</div>
                </div>
                <div v-if="getEstimatedTime()" class="insight-item">
                  <Clock class="w-4 h-4" />
                  <div class="insight-text">Estimated time remaining: {{ getEstimatedTime() }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- AI Auto-Fill Warning Modal -->
    <div v-if="showAutoFillModal" class="modal-overlay active">
      <div class="modal-content">
        <div class="modal-header">
          <div class="modal-title">
            <AlertTriangle class="w-6 h-6" />
            AI Auto-Fill Warning
          </div>
        </div>
        <div class="modal-body">
          <p><strong>⚠️ This action will replace all existing data in the current step.</strong></p>
          <p>AI will automatically populate the form fields with sample data. Any information you've already entered will be overwritten.</p>
          <p>Are you sure you want to continue?</p>
        </div>
        <div class="modal-footer">
          <button class="modal-btn modal-btn-cancel" @click="closeAutoFillModal">Cancel</button>
          <button class="modal-btn modal-btn-confirm" @click="confirmAutoFill">
            <FlaskConical class="w-4 h-4" />
            Yes, Auto-Fill Data
          </button>
        </div>
      </div>
    </div>

    <!-- Add Client Modal -->
    <div v-if="showAddClientModal" class="modal-overlay active">
      <div class="modal-content">
        <div class="modal-header">
          <div class="modal-title">
            <Plus class="w-6 h-6" />
            Add Client
          </div>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label for="client-name">Full Name*</label>
            <input 
              v-model="newClient.name"
              type="text" 
              id="client-name" 
              class="form-control" 
              placeholder="Enter client name"
              required
            />
          </div>
          <div class="form-row">
            <div class="form-group">
              <label for="client-age">Age</label>
              <input 
                v-model="newClient.age"
                type="number" 
                id="client-age" 
                class="form-control" 
                placeholder="Age"
                min="1"
                max="120"
              />
            </div>
            <div class="form-group">
              <label for="client-gender">Gender</label>
              <select v-model="newClient.gender" id="client-gender" class="form-control">
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
            <label for="client-relationship">Relationship to Reporter</label>
            <input 
              v-model="newClient.relationship"
              type="text" 
              id="client-relationship" 
              class="form-control" 
              placeholder="e.g., Child, Spouse, Self"
            />
          </div>
        </div>
        <div class="modal-footer">
          <button class="modal-btn modal-btn-cancel" @click="closeAddClientModal">Cancel</button>
          <button class="modal-btn modal-btn-confirm" @click="addClient">
            <Plus class="w-4 h-4" />
            Add Client
          </button>
        </div>
      </div>
    </div>

    <!-- Add to Contacts Modal -->
    <div v-if="showAddToContactsModal" class="modal-overlay active">
      <div class="modal-content">
        <div class="modal-header">
          <div class="modal-title">
            <UserPlus class="w-6 h-6" />
            Add to Clients/Contacts
          </div>
        </div>
        <div class="modal-body">
          <div class="search-section">
            <div class="search-box">
              <Search class="w-4 h-4" />
              <input 
                v-model="contactSearchQuery" 
                type="text" 
                placeholder="Search existing contacts..." 
                class="search-input"
              />
            </div>
          </div>
          <div class="contacts-list">
            <div 
              v-for="contact in filteredContactsForModal" 
              :key="contact.id"
              class="contact-item"
              @click="selectContactForClient(contact)"
            >
              <div class="contact-avatar">
                <span>{{ getInitials(contact.name) }}</span>
              </div>
              <div class="contact-info">
                <div class="contact-name">{{ contact.name }}</div>
                <div class="contact-details">{{ contact.age }}y, {{ contact.gender }}</div>
              </div>
              <Check class="w-4 h-4" />
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button class="modal-btn modal-btn-cancel" @click="closeAddToContactsModal">Cancel</button>
        </div>
      </div>
    </div>

    <!-- Add Perpetrator Modal -->
    <div v-if="showAddPerpetratorModal" class="modal-overlay active">
      <div class="modal-content">
        <div class="modal-header">
          <div class="modal-title">
            <Plus class="w-6 h-6" />
            Add Perpetrator
          </div>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label for="perpetrator-name">Full Name*</label>
            <input 
              v-model="newPerpetrator.name"
              type="text" 
              id="perpetrator-name" 
              class="form-control" 
              placeholder="Enter perpetrator name"
              required
            />
          </div>
          <div class="form-row">
            <div class="form-group">
              <label for="perpetrator-age">Age</label>
              <input 
                v-model="newPerpetrator.age"
                type="number" 
                id="perpetrator-age" 
                class="form-control" 
                placeholder="Age"
                min="1"
                max="120"
              />
            </div>
            <div class="form-group">
              <label for="perpetrator-gender">Gender</label>
              <select v-model="newPerpetrator.gender" id="perpetrator-gender" class="form-control">
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
            <label for="perpetrator-relationship">Relationship to Client</label>
            <input 
              v-model="newPerpetrator.relationship"
              type="text" 
              id="perpetrator-relationship" 
              class="form-control" 
              placeholder="e.g., Spouse, Parent, Stranger, Known person"
            />
          </div>
        </div>
        <div class="modal-footer">
          <button class="modal-btn modal-btn-cancel" @click="closeAddPerpetratorModal">Cancel</button>
          <button class="modal-btn modal-btn-confirm" @click="addPerpetrator">
            <Plus class="w-4 h-4" />
            Add Perpetrator
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import {
  ChevronLeft,
  Sun,
  Moon,
  Search,
  Check,
  Plus,
  Edit,
  AlertTriangle,
  BarChart,
  Clock,
  Shield,
  Flag,
  FlaskConical,
  ChevronDown,
  X,
  UserPlus,
  FileText,
  Paperclip,
} from 'lucide-vue-next'

const router = useRouter()

// State
const currentStep = ref(1)
const totalSteps = 5
const theme = ref(localStorage.getItem('theme') || 'dark')
const isAIEnabled = ref(true)
const showAutoFillModal = ref(false)
const searchQuery = ref('')
const selectedReporter = ref(null)
const showCategoryDropdown = ref(false)
const categorySearchQuery = ref("")

// New modal states - now properly managed
const showAddClientModal = ref(false)
const showAddToContactsModal = ref(false)
const showAddPerpetratorModal = ref(false)
const contactSearchQuery = ref('')

// AI Data from audio transcription
const transcriptionData = ref(null)
const aiInsights = ref(null)

// New data structures
const clients = reactive([])
const perpetrators = reactive([])
const relatedFiles = reactive([])

const newClient = reactive({
  name: '',
  age: '',
  gender: '',
  relationship: ''
})

const newPerpetrator = reactive({
  name: '',
  age: '',
  gender: '',
  relationship: ''
})

// Mock contacts data - updated with sample data
const contacts = reactive([
  {
    id: 1,
    name: 'Ivan Somondi',
    age: 16,
    gender: 'Male',
    location: 'Narok County',
    phone: '254700112233',
    lastContact: '23 May 2025 3:30 PM'
  },
  {
    id: 2,
    name: 'Susan Kirigwa',
    age: 45,
    gender: 'Female',
    location: 'Narok',
    phone: '254700445566',
    lastContact: '20 May 2025 1:42 PM'
  },
  {
    id: 3,
    name: 'Amira',
    age: 28,
    gender: 'Female',
    location: 'Nairobi',
    phone: '254700778899',
    lastContact: '1 Jun 2025 9:34 AM'
  }
])

// AI Suggestions data
const aiSuggestions = reactive({
  1: [
    {
      id: 'duplicate-check',
      type: 'info',
      icon: '💡',
      text: 'Consider checking for duplicate contacts before creating new reporters',
      action: null
    }
  ],
  2: [
    {
      id: 'contact-validation',
      type: 'warning',
      icon: '⚠️',
      text: 'Ensure phone number is valid and reachable for follow-ups',
      action: null
    }
  ],
  3: [
    {
      id: 'narrative-analysis',
      type: 'success',
      icon: '🎯',
      text: 'Case narrative indicates potential high priority - consider urgent classification',
      action: { type: 'set-priority', value: 'high' }
    },
    {
      id: 'gbv-detection',
      type: 'warning',
      icon: '🚨',
      text: 'Keywords suggest this may be GBV-related. Ensure proper protocols are followed',
      action: null
    }
  ],
  4: [
    {
      id: 'priority-recommendation',
      type: 'success',
      icon: '🎯',
      text: 'Based on case details, recommended priority: Medium',
      action: { type: 'set-priority', value: 'medium' }
    },
    {
      id: 'service-suggestion',
      type: 'info',
      icon: '💼',
      text: 'Consider adding counseling and legal aid services for this case type',
      action: { type: 'add-services', value: ['counseling', 'legal-aid'] }
    }
  ],
  5: [
    {
      id: 'completeness-check',
      type: 'success',
      icon: '✅',
      text: 'All required fields completed. Case is ready for submission',
      action: null
    }
  ]
})

// Form data
const formData = reactive({
  step2: {
    name: '',
    age: '',
    gender: '',
    location: '',
    phone: '',
    altPhone: '',
    email: '',
    idType: '',
    idNumber: '',
    isClient: null
  },
  step3: {
    narrative: '',
    incidentDate: '',
    incidentTime: '',
    location: '',
    isGBVRelated: null,
    casePlan: ''
  },
  step4: {
    department: '',
    category: [], // Changed to array for multi-select
    priority: '',
    status: '',
    escalatedTo: '',
    servicesOffered: [],
    // New fields for conditional modules
    receivedMedicalExam: null,
    preventedUnintendedPregnancies: null,
    testedForHIV: null,
    receivedCounselling: null,
  }
})

// Step information
const stepLabels = [
  'Select Reporter',
  'Reporter Details',
  'Case Information',
  'Classification',
  'Review'
]

const stepDescriptions = [
  'Step 1: Select an existing contact or create a new reporter',
  'Step 2: Enter reporter details and contact information',
  'Step 3: Provide case narrative and incident details',
  'Step 4: Classify case and assign priority',
  'Step 5: Review all information before creating the case'
]

// Computed
const filteredContacts = computed(() => {
  if (!searchQuery.value) return contacts
  return contacts.filter(contact =>
    contact.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    contact.phone.includes(searchQuery.value)
  )
})

const filteredContactsForModal = computed(() => {
  if (!contactSearchQuery.value) return contacts
  return contacts.filter(contact =>
    contact.name.toLowerCase().includes(contactSearchQuery.value.toLowerCase()) ||
    contact.phone.includes(contactSearchQuery.value)
  )
})

const caseCategoryOptions = computed(() => [
  { value: "domestic-violence", label: "Domestic Violence" },
  { value: "sexual-assault", label: "Sexual Assault" },
  { value: "child-abuse", label: "Child Abuse" },
  { value: "human-trafficking", label: "Human Trafficking" },
  { value: "labor-exploitation", label: "Labor Exploitation" },
  { value: "elder-abuse", label: "Elder Abuse" },
  { value: "stalking", label: "Stalking" },
  { value: "substance-abuse", label: "Substance Abuse" },
  { value: "other", label: "Other" },
])

const filteredCategoryOptions = computed(() => {
  if (!categorySearchQuery.value) return caseCategoryOptions.value
  return caseCategoryOptions.value.filter(option =>
    option.label.toLowerCase().includes(categorySearchQuery.value.toLowerCase())
  )
})

const showMedicalAndCounselingModules = computed(() => {
  return formData.step4.category.some((cat) =>
    ["sexual-assault", "domestic-violence", "child-abuse"].includes(cat),
  )
})

// Methods
const toggleTheme = () => {
  theme.value = theme.value === 'dark' ? 'light' : 'dark'
  localStorage.setItem('theme', theme.value)
  applyTheme()
}

const applyTheme = () => {
  const root = document.documentElement
  
  if (theme.value === 'light') {
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

const getInitials = (name) => {
  return name.split(' ').map(n => n[0]).join('').toUpperCase()
}

const selectExistingReporter = (contact) => {
  selectedReporter.value = contact
}

const createNewReporter = () => {
  selectedReporter.value = null
  // Clear reporter data
  Object.keys(formData.step2).forEach(key => {
    formData.step2[key] = key === 'isClient' ? null : ''
  })
  currentStep.value = 2
}

const goToStep = (step) => {
  currentStep.value = step
}

const validateAndProceed = (step) => {
  if (step === 1 && selectedReporter.value) {
    // Pre-fill reporter data with selected contact
    formData.step2.name = selectedReporter.value.name
    formData.step2.age = selectedReporter.value.age
    formData.step2.gender = selectedReporter.value.gender.toLowerCase()
    formData.step2.location = selectedReporter.value.location
    formData.step2.phone = selectedReporter.value.phone
    currentStep.value = 2
  }
}

const skipStep = (step) => {
  currentStep.value = step + 1
}

const saveAndProceed = (step) => {
  currentStep.value = step + 1
}

// Modal management methods - Fixed to prevent overlapping
const closeAllModals = () => {
  showAutoFillModal.value = false
  showAddClientModal.value = false
  showAddToContactsModal.value = false
  showAddPerpetratorModal.value = false
}

const openAutoFillModal = () => {
  closeAllModals()
  showAutoFillModal.value = true
}

const openAddClientModal = () => {
  closeAllModals()
  showAddClientModal.value = true
}

const openAddToContactsModal = () => {
  closeAllModals()
  showAddToContactsModal.value = true
}

const openAddPerpetratorModal = () => {
  closeAllModals()
  showAddPerpetratorModal.value = true
}

const closeAutoFillModal = () => {
  showAutoFillModal.value = false
}

const closeAddClientModal = () => {
  resetNewClient()
  showAddClientModal.value = false
}

const closeAddToContactsModal = () => {
  showAddToContactsModal.value = false
  contactSearchQuery.value = ''
}

const closeAddPerpetratorModal = () => {
  resetNewPerpetrator()
  showAddPerpetratorModal.value = false
}

// Client management methods
const addClient = () => {
  if (newClient.name) {
    clients.push({
      id: Date.now(),
      name: newClient.name,
      age: newClient.age,
      gender: newClient.gender,
      relationship: newClient.relationship
    })
    closeAddClientModal()
  }
}

const removeClient = (clientId) => {
  const index = clients.findIndex(c => c.id === clientId)
  if (index > -1) {
    clients.splice(index, 1)
  }
}

const resetNewClient = () => {
  newClient.name = ''
  newClient.age = ''
  newClient.gender = ''
  newClient.relationship = ''
}

const selectContactForClient = (contact) => {
  clients.push({
    id: Date.now(),
    name: contact.name,
    age: contact.age,
    gender: contact.gender,
    relationship: 'Client'
  })
  closeAddToContactsModal()
}

// Perpetrator management methods
const addPerpetrator = () => {
  if (newPerpetrator.name) {
    perpetrators.push({
      id: Date.now(),
      name: newPerpetrator.name,
      age: newPerpetrator.age,
      gender: newPerpetrator.gender,
      relationship: newPerpetrator.relationship
    })
    closeAddPerpetratorModal()
  }
}

const removePerpetrator = (perpetratorId) => {
  const index = perpetrators.findIndex(p => p.id === perpetratorId)
  if (index > -1) {
    perpetrators.splice(index, 1)
  }
}

const resetNewPerpetrator = () => {
  newPerpetrator.name = ''
  newPerpetrator.age = ''
  newPerpetrator.gender = ''
  newPerpetrator.relationship = ''
}

// File management methods
const attachFile = () => {
  // Simulate file attachment
  const input = document.createElement('input')
  input.type = 'file'
  input.multiple = true
  input.onchange = (e) => {
    Array.from(e.target.files).forEach(file => {
      relatedFiles.push({
        id: Date.now() + Math.random(),
        name: file.name,
        size: `${(file.size / 1024).toFixed(1)} KB`,
        file: file
      })
    })
  }
  input.click()
}

const removeFile = (fileId) => {
  const index = relatedFiles.findIndex(f => f.id === fileId)
  if (index > -1) {
    relatedFiles.splice(index, 1)
  }
}

// AI methods
const confirmAutoFill = () => {
  closeAutoFillModal()
  applyAISuggestions()
}

const applyAISuggestions = () => {
  // Auto-fill based on current step
  switch (currentStep.value) {
    case 2:
      if (!selectedReporter.value) {
        formData.step2.name = 'John Doe'
        formData.step2.age = '35'
        formData.step2.gender = 'male'
        formData.step2.location = 'Downtown'
        formData.step2.phone = '+1234567890'
        formData.step2.email = 'john.doe@example.com'
        formData.step2.idType = 'national-id'
        formData.step2.idNumber = 'ID123456789'
        formData.step2.isClient = false
      }
      break
          
    case 3:
      formData.step3.narrative = 'Incident reported involving domestic dispute. Caller requested immediate assistance and support services. Situation appears to require urgent intervention and follow-up care.'
      formData.step3.incidentDate = new Date().toISOString().split('T')[0]
      formData.step3.incidentTime = '14:30'
      formData.step3.location = 'Residential area, Main Street'
      formData.step3.isGBVRelated = true
      formData.step3.casePlan = 'Provide immediate safety assessment, connect with counseling services, and follow up within 24 hours. Coordinate with local support agencies for ongoing assistance.'
      break
          
    case 4:
      formData.step4.department = '116'
      formData.step4.category = ['domestic-violence', 'sexual-assault'] // Example multi-select
      formData.step4.priority = 'high'
      formData.step4.status = 'new'
      formData.step4.escalatedTo = 'supervisor'
      formData.step4.servicesOffered = ['counseling', 'legal-aid', 'shelter']
      formData.step4.receivedMedicalExam = 'yes'
      formData.step4.preventedUnintendedPregnancies = 'yes'
      formData.step4.testedForHIV = 'no'
      formData.step4.receivedCounselling = 'yes'
      break
  }
}

const getActiveSuggestions = () => {
  const currentSuggestions = aiSuggestions[currentStep.value] || []
  const previousSteps = Array.from({length: currentStep.value - 1}, (_, i) => i + 1)

  let allSuggestions = [...currentSuggestions]

  // Add suggestions from completed steps
  previousSteps.forEach(step => {
    const stepSuggestions = aiSuggestions[step] || []
    allSuggestions = [...allSuggestions, ...stepSuggestions]
  })

  return allSuggestions
}

const applySuggestion = (suggestion) => {
  if (!suggestion.action) return

  switch (suggestion.action.type) {
    case 'set-priority':
      formData.step4.priority = suggestion.action.value
      break
    case 'add-services':
      formData.step4.servicesOffered = [...new Set([...formData.step4.servicesOffered, ...suggestion.action.value])]
      break
  }
}

const getCompletedSteps = () => {
  return Array.from({length: currentStep.value - 1}, (_, i) => i + 1)
}

const getEstimatedTime = () => {
  const remaining = totalSteps - currentStep.value
  if (remaining <= 0) return null
  return `${remaining * 2} minutes`
}

// Load sample transcription data
const loadSampleTranscriptionData = () => {
  // Sample data based on the provided transcription
  transcriptionData.value = {
    transcript: "Hello. Hello. Good evening. Good evening. You are speaking to Amira from Child Health Line. How may I assist? I was asking, like this Child Health Line, like in Asahidia, what to do? Thank you so much for the question. Who am I speaking to? You are speaking to Eva and Sumu. Are you speaking to Ivan Somondi? You're calling us from which county, Ivan Somondi? Um, in, um, Narok. Which ward in Narok County? I don't know exactly, but I'm in Narok County...",
    summary: "Child Health Counseling Line deals with all child protection cases. Case involves a 16-year-old named Ivan Somondi from Narok County seeking help for substance abuse (alcohol and cannabis). The caller admits to daily substance use and wants to quit.",
    summary_entities: [
      { text: "Ivan Somondi", label: "PERSON" },
      { text: "Narok County", label: "LOCATION" },
      { text: "Child Health Line", label: "ORG" },
      { text: "Susan Kirigwa", label: "PERSON" },
      { text: "Nyarach Secondary School", label: "ORG" }
    ],
    summary_classification: {
      main_category: "Child Protection",
      sub_category: "Substance Abuse",
      intervention: "Professional counseling",
      priority: 2
    }
  }

  aiInsights.value = {
    case_summary: "Case involving a 16-year-old minor from Narok County seeking help for substance abuse. The child reports daily use of alcohol and cannabis, started with peer influence, and expresses desire to change. Parents are unaware of the substance use.",
    named_entities: {
      persons: ["Ivan Somondi", "Susan Kirigwa", "Amira"],
      organizations: ["Child Health Line", "Nyarach Secondary School"],
      locations: ["Narok County", "Nairobi"],
      contact_information: ["Child Health Line"]
    },
    classification: {
      category: ["Child Protection", "Substance Abuse"],
      interventions_needed: ["Professional counseling", "Rehabilitation services"],
      priority_level: "High"
    },
    case_management: {
      psychosocial_support: {
        short_term: ["Professional counseling", "Peer support groups", "Family counseling"],
        long_term: ["Rehabilitation program", "Educational support", "Life skills training"]
      },
      safety_planning: {
        immediate_actions: ["Assess immediate safety", "Contact parents/guardians"],
        long_term_measures: ["Regular follow-up", "School coordination"]
      }
    },
    risk_assessment: {
      red_flags: ["Daily substance use", "Hiding behavior from parents", "Peer influence"],
      protective_factors: ["Expressed desire to change", "Access to education", "Family support available"],
      potential_barriers: ["Peer pressure", "Lack of parental awareness", "Geographic distance from services"]
    }
  }
}

// AI Suggestion Usage Methods
const useTranscription = () => {
  if (transcriptionData.value?.transcript) {
    formData.step3.narrative = transcriptionData.value.transcript
    goToStep(3)
  }
}

const useEntity = (entity) => {
  if (entity.label === 'PERSON') {
    formData.step2.name = entity.text
    goToStep(2)
  } else if (entity.label === 'LOCATION') {
    formData.step3.location = entity.text
    goToStep(3)
  }
}

const useClassification = (type, value) => {
  if (type === 'category') {
    const categoryMap = {
      'Child Abuse': 'child-abuse',
      'Substance Abuse': 'substance-abuse',
      'Domestic Violence': 'domestic-violence',
      // Add other mappings if needed
    }
    const mappedValue = categoryMap[value] || value.toLowerCase().replace(" ", "-")
    if (!formData.step4.category.includes(mappedValue)) {
      formData.step4.category.push(mappedValue)
    }
  } else if (type === 'priority') {
    formData.step4.priority = value
  } else if (type === 'intervention') {
    const serviceMap = {
      'Professional counseling': 'counseling',
      'Legal assistance': 'legal-aid',
      'Medical assistance': 'medical-assistance',
      // Add other mappings if needed
    }
    const service = serviceMap[value] || value.toLowerCase().replace(' ', '-')
    if (!formData.step4.servicesOffered.includes(service)) {
      formData.step4.servicesOffered.push(service)
    }
  }
  goToStep(4)
}

const useCaseSummary = () => {
  if (aiInsights.value?.case_summary) {
    formData.step3.casePlan = aiInsights.value.case_summary
    goToStep(3)
  }
}

const usePerson = (person) => {
  formData.step2.name = person
  goToStep(2)
}

const useLocation = (location) => {
  formData.step3.location = location
  goToStep(3)
}

const useOrganization = (org) => {
  // Could be used in case narrative or other relevant fields
  const currentNarrative = formData.step3.narrative || ''
  formData.step3.narrative = currentNarrative + (currentNarrative ? '\n\n' : '') + `Organization involved: ${org}`
  goToStep(3)
}

const addRecommendedService = (service) => {
  const serviceMap = {
    'Professional counseling': 'counseling',
    'Peer support groups': 'counseling',
    'Family counseling': 'counseling',
    'Rehabilitation program': 'medical-assistance',
    'Educational support': 'referral',
    'Life skills training': 'counseling'
  }
  const mappedService = serviceMap[service] || 'counseling'
  if (!formData.step4.servicesOffered.includes(mappedService)) {
    formData.step4.servicesOffered.push(mappedService)
  }
  goToStep(4)
}

const getPriorityText = (priority) => {
  const priorityMap = { 1: 'Critical', 2: 'High', 3: 'Medium', 4: 'Low' }
  return priorityMap[priority] || 'Medium'
}

const getPriorityValue = (priority) => {
  const priorityMap = { 1: 'critical', 2: 'high', 3: 'medium', 4: 'low' }
  return priorityMap[priority] || 'medium'
}

// Formatting methods
const formatDepartment = (dept) => {
  const deptMap = {
    '116': '116 (Emergency Helpline)',
    'labor': 'Labor Department'
  }
  return deptMap[dept] || dept
}

const formatCategory = (categories) => {
  const categoryMap = {
    'domestic-violence': 'Domestic Violence',
    'sexual-assault': 'Sexual Assault',
    'child-abuse': 'Child Abuse',
    'human-trafficking': 'Human Trafficking',
    'labor-exploitation': 'Labor Exploitation',
    'elder-abuse': 'Elder Abuse',
    'stalking': 'Stalking',
    'substance-abuse': 'Substance Abuse',
    'other': 'Other'
  }
  return categories.map(cat => categoryMap[cat] || cat).join(', ')
}

const formatPriority = (priority) => {
  const priorityMap = {
    'critical': 'Critical',
    'high': 'High',
    'medium': 'Medium',
    'low': 'Low'
  }
  return priorityMap[priority] || priority
}

const formatStatus = (status) => {
  const statusMap = {
    'new': 'New',
    'in-progress': 'In Progress',
    'pending': 'Pending',
    'resolved': 'Resolved'
  }
  return statusMap[status] || status
}

const formatService = (service) => {
  const serviceMap = {
    'counseling': 'Counseling',
    'legal-aid': 'Legal Aid',
    'shelter': 'Shelter',
    'medical-assistance': 'Medical Assistance',
    'financial-support': 'Financial Support',
    'referral': 'Referral Services'
  }
  return serviceMap[service] || service
}

const cancelForm = () => {
  router.push('/cases')
}

const submitCase = () => {
  const casePayload = {
    reporter: formData.step2,
    caseDetails: formData.step3,
    classification: formData.step4,
    clients: clients,
    perpetrators: perpetrators,
    relatedFiles: relatedFiles,
    aiInsights: aiInsights.value,
    transcriptionData: transcriptionData.value,
    createdAt: new Date().toISOString()
  }

  console.log('Creating case:', casePayload)
  alert('Case created successfully!')
  router.push('/cases')
}

const toggleCategoryDropdown = () => {
  showCategoryDropdown.value = !showCategoryDropdown.value
}

const handleCategorySelect = (value) => {
  const index = formData.step4.category.indexOf(value)
  if (index > -1) {
    formData.step4.category.splice(index, 1)
  } else {
    formData.step4.category.push(value)
  }
}

const handleServiceChange = (serviceValue, isChecked) => {
  if (isChecked) {
    if (!formData.step4.servicesOffered.includes(serviceValue)) {
      formData.step4.servicesOffered.push(serviceValue)
    }
  } else {
    formData.step4.servicesOffered = formData.step4.servicesOffered.filter(s => s !== serviceValue)
  }
}

// Lifecycle hooks
onMounted(() => {
  applyTheme()
  // Load sample data for demonstration
  setTimeout(() => {
    loadSampleTranscriptionData()
  }, 2000)
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

.header-controls {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  background-color: var(--background-color);
  border-bottom: 1px solid var(--border-color);
  z-index: 50;
}

.back-button {
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
}

.back-button:hover {
  background-color: var(--border-color);
}

.theme-toggle {
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
}

.theme-toggle:hover {
  background-color: var(--border-color);
}

.case-container {
  display: flex;
  gap: 20px;
  max-width: 1400px;
  margin: 100px auto 0;
  min-height: calc(100vh - 140px);
}

.main-form-container {
  flex: 1;
  background-color: var(--content-bg);
  border-radius: 15px;
  padding: 30px;
  border: 1px solid var(--border-color);
  overflow-y: auto;
  max-height: calc(100vh - 140px);
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
  cursor: pointer;
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

.section-description {
  color: var(--text-secondary);
  font-size: 14px;
  margin-bottom: 20px;
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

.form-control::placeholder {
  color: var(--text-secondary);
}

.form-control:read-only {
  background-color: var(--border-color);
  cursor: not-allowed;
}

textarea.form-control {
  min-height: 100px;
  resize: vertical;
}

.search-section {
  margin-bottom: 20px;
}

.search-box {
  position: relative;
  max-width: 400px;
}

.search-box svg {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  stroke: var(--text-secondary);
}

.search-input {
  width: 100%;
  padding: 12px 16px 12px 40px;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  background-color: var(--input-bg);
  color: var(--text-color);
  font-size: 14px;
  transition: border-color 0.3s;
}

.search-input:focus {
  outline: none;
  border-color: var(--accent-color);
}

.contacts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 16px;
  margin-bottom: 20px;
}

.contact-card {
  background-color: var(--input-bg);
  border: 2px solid var(--border-color);
  border-radius: 12px;
  padding: 16px;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  gap: 12px;
  position: relative;
}

.contact-card:hover {
  border-color: var(--accent-color);
  transform: translateY(-2px);
}

.contact-card.selected {
  border-color: var(--accent-color);
  background-color: rgba(150, 75, 0, 0.1);
}

.contact-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: var(--accent-color);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 14px;
  flex-shrink: 0;
}

.contact-info {
  flex: 1;
}

.contact-name {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-color);
  margin-bottom: 4px;
}

.contact-details {
  display: flex;
  gap: 8px;
  margin-bottom: 8px;
}

.contact-tag {
  font-size: 12px;
  background-color: var(--border-color);
  color: var(--text-secondary);
  padding: 2px 6px;
  border-radius: 4px;
}

.contact-meta {
  display: flex;
  flex-direction: column;
  gap: 4px;
  font-size: 12px;
  color: var(--text-secondary);
}

.contact-timestamp {
  font-size: 11px;
  color: var(--text-secondary);
  margin-top: 8px;
}

.contact-select-indicator {
  position: absolute;
  top: 50%;
  right: 16px;
  transform: translateY(-50%);
  color: var(--accent-color);
  opacity: 0;
  transition: opacity 0.3s;
}

.contact-card.selected .contact-select-indicator {
  opacity: 1;
}

.action-buttons {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.radio-group {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.radio-option {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  position: relative;
  padding-left: 28px;
}

.radio-option input[type="radio"] {
  opacity: 0;
  position: absolute;
  width: 0;
  height: 0;
}

.radio-indicator {
  position: absolute;
  left: 0;
  top: 2px;
  height: 20px;
  width: 20px;
  background-color: var(--input-bg);
  border: 2px solid var(--border-color);
  border-radius: 50%;
  transition: all 0.3s;
}

.radio-option:hover .radio-indicator {
  border-color: var(--accent-color);
}

.radio-option input[type="radio"]:checked ~ .radio-indicator {
  background-color: var(--accent-color);
  border-color: var(--accent-color);
}

.radio-indicator::after {
  content: "";
  position: absolute;
  display: none;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: white;
}

.radio-option input[type="radio"]:checked ~ .radio-indicator::after {
  display: block;
}

.radio-label {
  font-size: 14px;
  color: var(--text-color);
}

.checkbox-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 12px;
}

.checkbox-option {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  position: relative;
  padding-left: 28px;
}

.checkbox-option input[type="checkbox"] {
  opacity: 0;
  position: absolute;
  width: 0;
  height: 0;
}

.checkbox-indicator {
  position: absolute;
  left: 0;
  top: 2px;
  height: 20px;
  width: 20px;
  background-color: var(--input-bg);
  border: 2px solid var(--border-color);
  border-radius: 4px;
  transition: all 0.3s;
}

.checkbox-option:hover .checkbox-indicator {
  border-color: var(--accent-color);
}

.checkbox-option input[type="checkbox"]:checked ~ .checkbox-indicator {
  background-color: var(--accent-color);
  border-color: var(--accent-color);
}

.checkbox-indicator::after {
  content: "";
  position: absolute;
  display: none;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%) rotate(45deg);
  width: 6px;
  height: 10px;
  border: solid white;
  border-width: 0 2px 2px 0;
}

.checkbox-option input[type="checkbox"]:checked ~ .checkbox-indicator::after {
  display: block;
}

.checkbox-label {
  font-size: 14px;
  color: var(--text-color);
}

/* New styles for client/perpetrator management */
.client-management-section,
.perpetrators-section,
.related-files-section {
  background-color: var(--input-bg);
  border-radius: 12px;
  padding: 20px;
  border: 1px solid var(--border-color);
  margin-top: 20px;
}

.client-list,
.perpetrator-list,
.file-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 16px;
}

.client-item,
.perpetrator-item,
.file-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px;
  background-color: var(--content-bg);
  border-radius: 8px;
  border: 1px solid var(--border-color);
}

.client-info,
.perpetrator-info,
.file-info {
  display: flex;
  align-items: center;
  gap: 12px;
  flex: 1;
}

.client-name,
.perpetrator-name,
.file-name {
  font-weight: 500;
  color: var(--text-color);
}

.client-details,
.perpetrator-details,
.file-size {
  font-size: 12px;
  color: var(--text-secondary);
}

.client-actions {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.contacts-list {
  max-height: 300px;
  overflow-y: auto;
  margin-bottom: 16px;
}

.contact-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background-color: var(--input-bg);
  border-radius: 8px;
  border: 1px solid var(--border-color);
  cursor: pointer;
  transition: all 0.3s;
  margin-bottom: 8px;
}

.contact-item:hover {
  border-color: var(--accent-color);
  background-color: rgba(150, 75, 0, 0.1);
}

.form-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 20px;
  border-top: 1px solid var(--border-color);
}

.form-actions-right {
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

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
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

.btn-next:hover:not(:disabled) {
  background-color: var(--accent-hover);
}

.btn-primary {
  background-color: var(--accent-color);
  color: white;
}

.btn-primary:hover {
  background-color: var(--accent-hover);
}

.btn-secondary {
  background-color: transparent;
  color: var(--text-color);
  border: 1px solid var(--border-color);
}

.btn-secondary:hover {
  background-color: var(--border-color);
}

.btn-submit {
  background-color: var(--success-color);
  color: white;
}

.btn-submit:hover {
  background-color: #45a049;
}

.btn-large {
  padding: 16px 24px;
  font-size: 16px;
}

.btn-small {
  padding: 8px 12px;
  font-size: 12px;
}

.btn-tiny {
  padding: 6px 10px;
  font-size: 11px;
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

.review-item-full {
  grid-column: 1 / -1;
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

.status-badge {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
  color: white;
}

.status-yes {
  background-color: var(--success-color);
}

.status-no {
  background-color: var(--danger-color);
}

.status-info {
  background-color: #3b82f6;
}

.status-warning {
  background-color: var(--pending-color);
}

.priority-badge {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
  color: white;
}

.priority-critical {
  background-color: var(--danger-color);
}

.priority-high {
  background-color: var(--pending-color);
}

.priority-medium {
  background-color: #ffc857;
  color: #333;
}

.priority-low {
  background-color: var(--success-color);
}

.services-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.service-tag {
  font-size: 12px;
  background-color: var(--border-color);
  color: var(--text-color);
  padding: 4px 8px;
  border-radius: 4px;
}

.ai-preview-container {
  width: 400px;
  flex-shrink: 0;
}

.ai-preview {
  background-color: var(--content-bg);
  border-radius: 15px;
  border: 1px solid var(--border-color);
  height: calc(100vh - 140px);
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

.ai-autofill-section {
  background-color: var(--input-bg);
  border-radius: 8px;
  padding: 16px;
  border: 1px solid var(--border-color);
}

.ai-autofill-description {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.4;
  margin-bottom: 12px;
}

.ai-autofill-btn {
  width: 100%;
  justify-content: center;
}

.ai-suggestions {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.ai-suggestion {
  display: flex;
  gap: 12px;
  padding: 12px;
  background-color: var(--input-bg);
  border-radius: 8px;
  border-left: 3px solid var(--border-color);
}

.suggestion-info {
  border-left-color: #3b82f6;
}

.suggestion-warning {
  border-left-color: var(--pending-color);
}

.suggestion-success {
  border-left-color: var(--success-color);
}

.suggestion-icon {
  font-size: 16px;
  line-height: 1;
  flex-shrink: 0;
}

.suggestion-content {
  flex: 1;
}

.suggestion-text {
  font-size: 13px;
  color: var(--text-color);
  line-height: 1.4;
  margin-bottom: 8px;
}

.suggestion-action {
  display: flex;
  justify-content: flex-end;
}

.btn-outline {
  background-color: transparent;
  color: var(--accent-color);
  border: 1px solid var(--accent-color);
}

.btn-outline:hover {
  background-color: var(--accent-color);
  color: white;
}

.ai-summary {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.summary-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 13px;
}

.summary-label {
  font-weight: 500;
  color: var(--text-secondary);
}

.summary-value {
  text-align: right;
  color: var(--text-color);
}

.text-muted {
  color: var(--text-secondary);
}

.progress-insights {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.insight-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: var(--text-color);
}

/* Fixed Modal Overlay System */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(4px);
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
  max-height: 80vh;
  border: 1px solid var(--border-color);
  animation: modalSlideIn 0.3s ease-out;
  overflow-y: auto;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

@keyframes modalSlideIn {
  from {
    transform: translateY(-20px) scale(0.95);
    opacity: 0;
  }
  to {
    transform: translateY(0) scale(1);
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
  stroke: var(--accent-color);
}

.modal-body {
  padding: 20px;
}

.modal-body p {
  color: var(--text-color);
  line-height: 1.5;
  margin: 0 0 12px 0;
}

.modal-body p:last-child {
  margin-bottom: 0;
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
  display: inline-flex;
  align-items: center;
  gap: 8px;
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
  background-color: var(--accent-color);
  color: white;
}

.modal-btn-confirm:hover {
  background-color: var(--accent-hover);
}

/* New AI Insights Specific Styles */
.transcription-section,
.summary-section,
.entities-section,
.classification-section {
  margin-bottom: 1.5rem;
  padding: 1rem;
  background-color: var(--input-bg);
  border-radius: 8px;
  border: 1px solid var(--border-color);
}

.transcription-text,
.summary-text {
  font-size: 0.875rem;
  line-height: 1.5;
  color: var(--text-color);
  margin-bottom: 0.75rem;
  max-height: 150px;
  overflow-y: auto;
  background-color: var(--content-bg);
  padding: 0.75rem;
  border-radius: 6px;
  border: 1px solid var(--border-color);
}

.entity-suggestions {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.entity-suggestion {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.5rem;
  background-color: var(--content-bg);
  border-radius: 6px;
  border: 1px solid var(--border-color);
}

.entity-text {
  font-weight: 500;
  color: var(--text-color);
}

.entity-label {
  font-size: 0.75rem;
  background-color: var(--accent-color);
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  text-transform: uppercase;
}

.classification-suggestions {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.suggestion-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.75rem;
  background-color: var(--content-bg);
  border-radius: 6px;
  border: 1px solid var(--border-color);
  flex-wrap: wrap;
  gap: 0.5rem;
}

.suggestion-label {
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--text-secondary);
}

.suggestion-value {
  font-size: 0.875rem;
  color: var(--text-color);
  font-weight: 500;
}

.insight-section {
  margin-bottom: 1.5rem;
  padding: 1rem;
  background-color: var(--input-bg);
  border-radius: 8px;
  border: 1px solid var(--border-color);
}

.insight-text {
  font-size: 0.875rem;
  line-height: 1.5;
  color: var(--text-color);
  margin-bottom: 0.75rem;
}

.entity-group,
.risk-group,
.service-group {
  margin-bottom: 1rem;
}

.entity-type,
.risk-type,
.service-type {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-color);
  margin-bottom: 0.5rem;
}

.entity-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.entity-tag {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.25rem 0.75rem;
  background-color: var(--accent-color);
  color: white;
  border-radius: 1rem;
  font-size: 0.875rem;
  font-weight: 500;
}

.entity-use-btn {
  background-color: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  font-size: 0.75rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.2s;
}

.entity-use-btn:hover {
  background-color: rgba(255, 255, 255, 0.3);
}

.risk-list {
  list-style-type: disc;
  padding-left: 1.5rem;
  color: var(--text-color);
  font-size: 0.875rem;
}

.service-suggestions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.service-suggestion-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0.75rem;
  background-color: var(--content-bg);
  border: 1px solid var(--border-color);
  border-radius: 6px;
  color: var(--text-color);
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s;
}

.service-suggestion-btn:hover {
  background-color: var(--accent-color);
  color: white;
  border-color: var(--accent-color);
}

.add-icon {
  background-color: var(--accent-color);
  color: white;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  font-size: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.service-suggestion-btn:hover .add-icon {
  background-color: white;
  color: var(--accent-color);
}

.subsection-title {
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--text-color);
  margin-bottom: 0.5rem;
  margin-top: 0.75rem;
}

/* Multi-select specific styles */
.multi-select-button {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  min-height: 40px;
  padding: 8px 16px;
  cursor: pointer;
  position: relative;
  text-align: left;
}

.multi-select-dropdown {
  position: absolute;
  z-index: 30;
  width: 100%;
  background-color: var(--content-bg);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  margin-top: 4px;
  max-height: 250px;
  overflow-y: auto;
}

.search-input-dropdown {
  width: calc(100% - 16px);
  margin: 8px;
  padding: 8px 12px;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  background-color: var(--input-bg);
  color: var(--text-color);
  font-size: 14px;
}

.multi-select-options-container {
  max-height: 180px;
  overflow-y: auto;
}

.multi-select-option {
  display: flex;
  align-items: center;
  padding: 8px 12px;
  font-size: 14px;
  color: var(--text-color);
  cursor: pointer;
  transition: background-color 0.2s;
}

.multi-select-option:hover {
  background-color: var(--border-color);
}

.multi-select-option.selected-option {
  background-color: rgba(150, 75, 0, 0.1);
  color: var(--accent-color);
}

.multi-select-option svg {
  margin-right: 8px;
  color: var(--accent-color);
}

.selected-tag {
  display: inline-flex;
  align-items: center;
  background-color: var(--border-color);
  color: var(--text-color);
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
  gap: 4px;
}

.remove-tag-button {
  background: none;
  border: none;
  color: var(--text-secondary);
  cursor: pointer;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: color 0.2s;
}

.remove-tag-button:hover {
  color: var(--text-color);
}

.no-options-found {
  padding: 16px;
  text-align: center;
  color: var(--text-secondary);
  font-size: 14px;
}

.conditional-module-section {
  padding: 20px;
  border: 1px solid var(--border-color);
  border-radius: 12px;
  background-color: var(--input-bg);
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* Utility classes */
.flex {
  display: flex;
}

.flex-wrap {
  flex-wrap: wrap;
}

.gap-1 {
  gap: 0.25rem;
}

.text-secondary {
  color: var(--text-secondary);
}

.ml-2 {
  margin-left: 0.5rem;
}

.h-4 {
  height: 1rem;
}

.w-4 {
  width: 1rem;
}

.w-3 {
  width: 0.75rem;
}

.h-3 {
  height: 0.75rem;
}

.w-5 {
  width: 1.25rem;
}

.h-5 {
  height: 1.25rem;
}

.w-6 {
  width: 1.5rem;
}

.h-6 {
  height: 1.5rem;
}

.shrink-0 {
  flex-shrink: 0;
}

.opacity-50 {
  opacity: 0.5;
}

.opacity-100 {
  opacity: 1;
}

.opacity-0 {
  opacity: 0;
}

.mr-2 {
  margin-right: 0.5rem;
}

.p-1 {
  padding: 0.25rem;
}

.relative {
  position: relative;
}

.text-red-500 {
  color: #ef4444;
}

.text-green-500 {
  color: #10b981;
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
  
  .entity-tags {
    flex-direction: column;
  }
  
  .service-suggestions {
    flex-direction: column;
  }
  
  .classification-suggestions {
    gap: 0.5rem;
  }
  
  .suggestion-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
}

@media (max-width: 768px) {
  .case-creation-page {
    padding: 10px;
  }
  
  .header-controls {
    flex-direction: column;
    gap: 10px;
    padding: 15px;
  }
  
  .back-button,
  .theme-toggle {
    width: 100%;
    justify-content: center;
  }
  
  .case-container {
    margin-top: 120px;
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
  
  .contacts-grid {
    grid-template-columns: 1fr;
  }
  
  .review-content {
    grid-template-columns: 1fr;
  }
  
  .form-actions {
    flex-direction: column;
    gap: 15px;
  }
  
  .form-actions-right {
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
  
  .checkbox-grid {
    grid-template-columns: 1fr;
  }
  
  .transcription-text,
  .summary-text {
    max-height: 100px;
  }
  
  .entity-suggestion {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
  
  .client-actions {
    flex-direction: column;
  }
}

@media (max-width: 480px) {
  .case-container {
    margin-top: 140px;
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
  
  .contacts-grid {
    padding: 0;
  }
  
  .contact-card {
    flex-direction: column;
    text-align: center;
  }
  
  .contact-select-indicator {
    position: static;
    transform: none;
    align-self: center;
    margin-top: 10px;
  }
  
  .modal-content {
    width: 95%;
    margin: 10px;
  }
  
  .modal-header,
  .modal-body,
  .modal-footer {
    padding: 15px;
  }
  
  .ai-preview {
    height: 300px;
  }
  
  .ai-preview-content {
    padding: 15px;
  }
}
</style>