<template>
  <div class="app-container">
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
      <!-- Chat Interface -->
      <div class="chat-interface" :class="{ 'chat-selected': selectedContactId }">
        <!-- Left Panel - Chat List -->
        <div class="chat-sidebar" :class="{ 'full-width': !selectedContactId }">
          <!-- Header -->
          <div class="sidebar-header">
            <div class="header-content">
              <h1 class="header-title">Messages</h1>
              <div class="header-actions">
                <button class="header-btn" @click="toggleTheme" title="Toggle Theme">
                  <svg v-if="currentTheme === 'dark'" width="20" height="20" viewBox="0 0 24 24" fill="none">
                    <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" stroke="currentColor" stroke-width="2"/>
                  </svg>
                  <svg v-else width="20" height="20" viewBox="0 0 24 24" fill="none">
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
                </button>
                <button class="header-btn" @click="showNewChatModal" title="New Chat">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                    <path d="M12 5v14M5 12h14" stroke="currentColor" stroke-width="2"/>
                  </svg>
                </button>
              </div>
            </div>
          </div>

          <!-- Platform Tabs -->
          <div class="platform-tabs">
            <button 
              v-for="platform in platforms" 
              :key="platform.id"
              :class="['platform-tab', { active: activePlatform === platform.id }]"
              @click="setActivePlatform(platform.id)"
            >
              <span class="tab-text">{{ platform.name }}</span>
              <span v-if="getPlatformUnreadCount(platform.id) > 0" class="tab-badge">
                {{ getPlatformUnreadCount(platform.id) }}
              </span>
            </button>
          </div>

          <!-- Search -->
          <div class="search-section">
            <div class="search-container">
              <svg class="search-icon" width="16" height="16" viewBox="0 0 24 24" fill="none">
                <circle cx="11" cy="11" r="8" stroke="currentColor" stroke-width="2"/>
                <path d="M21 21l-4.35-4.35" stroke="currentColor" stroke-width="2"/>
              </svg>
              <input 
                v-model="searchQuery"
                type="text" 
                class="search-input" 
                placeholder="Search conversations..."
                @input="handleSearch"
              />
              <button v-if="searchQuery" class="search-clear" @click="clearSearch">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none">
                  <line x1="18" y1="6" x2="6" y2="18" stroke="currentColor" stroke-width="2"/>
                  <line x1="6" y1="6" x2="18" y2="18" stroke="currentColor" stroke-width="2"/>
                </svg>
              </button>
            </div>
          </div>

          <!-- Chat List -->
          <div class="chat-list">
            <div class="list-header">
              <span class="list-title">{{ activePlatform === 'past' ? 'Past Conversations' : 'Active Chats' }}</span>
              <span class="list-count">{{ filteredContacts.length }}</span>
            </div>
            
            <div class="chat-contacts">
              <div
                v-for="contact in filteredContacts"
                :key="contact.id"
                :class="['chat-contact', { 
                  active: selectedContactId === contact.id, 
                  ended: contact.status === 'ended',
                  unread: contact.unreadCount > 0
                }]"
                @click="selectContact(contact.id)"
              >
                <div class="contact-avatar-wrapper">
                  <div class="contact-avatar" :style="{ backgroundColor: getAvatarColor(contact.name) }">
                    {{ contact.initials }}
                  </div>
                  <div v-if="contact.status === 'active'" class="online-dot"></div>
                </div>
                
                <div class="contact-details">
                  <div class="contact-header">
                    <h4 class="contact-name">{{ contact.name }}</h4>
                    <div class="contact-meta">
                      <span class="contact-time">{{ contact.time }}</span>
                      <div v-if="contact.unreadCount > 0" class="unread-count">
                        {{ contact.unreadCount }}
                      </div>
                    </div>
                  </div>
                  <div class="contact-footer">
                    <p class="contact-preview">{{ contact.preview }}</p>
                    <div class="platform-badge" :class="contact.platform">
                      {{ getPlatformShortName(contact.platform) }}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Right Panel - Chat View -->
        <div class="chat-main" v-if="selectedContact">
          <!-- Chat Header -->
          <div class="chat-header">
            <div class="chat-header-left">
              <button class="back-btn" @click="deselectContact" title="Back to chats">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                  <path d="M19 12H5M12 19l-7-7 7-7" stroke="currentColor" stroke-width="2"/>
                </svg>
              </button>
              <div class="contact-avatar-header" :style="{ backgroundColor: getAvatarColor(selectedContact.name) }">
                {{ selectedContact.initials }}
              </div>
              <div class="contact-info">
                <h3 class="contact-name">{{ selectedContact.name }}</h3>
                <p class="contact-status">
                  <span class="status-indicator" :class="{ online: selectedContact.status === 'active' }"></span>
                  {{ getContactStatus(selectedContact) }}
                </p>
              </div>
            </div>
            
            <div class="chat-header-actions">
              <button class="action-btn" @click="initiateCall" title="Call">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
                  <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z" stroke="currentColor" stroke-width="2"/>
                </svg>
              </button>
              <button class="action-btn" @click="toggleContactInfo" title="Contact Info">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
                  <circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="2"/>
                  <path d="M12 1v6M12 17v6M4.22 4.22l4.24 4.24M15.54 15.54l4.24 4.24M1 12h6M17 12h6M4.22 19.78l4.24-4.24M15.54 8.46l4.24-4.24" stroke="currentColor" stroke-width="2"/>
                </svg>
              </button>
              <button v-if="selectedContact.status === 'active'" class="action-btn end-chat-btn" @click="endChat" title="End Chat">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
                  <path d="M18 6L6 18M6 6l12 12" stroke="currentColor" stroke-width="2"/>
                </svg>
              </button>
            </div>
          </div>

          <!-- Messages Area -->
          <div class="messages-area" ref="messagesArea">
            <div class="messages-content">
              <div v-for="(group, index) in groupedMessages" :key="index" class="message-group">
                <div v-if="group.date" class="date-divider">
                  <span class="date-text">{{ group.date }}</span>
                </div>
                
                <div v-for="message in group.messages" :key="message.id" 
                     :class="['message-container', message.sender]">
                  <div class="message-bubble" :class="message.sender">
                    <p class="message-text">{{ message.text }}</p>
                    <div class="message-info">
                      <span class="message-time">{{ message.time }}</span>
                      <div v-if="message.sender === 'received'" class="message-status">
                        <svg width="12" height="12" viewBox="0 0 24 24" fill="none">
                          <polyline points="20,6 9,17 4,12" stroke="currentColor" stroke-width="2"/>
                        </svg>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Message Input -->
          <div class="message-input-area" v-if="activePlatform !== 'past' && selectedContact.status === 'active'">
            <div class="input-container">
              <button class="input-action-btn" @click="showAttachmentMenu" title="Attach">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                  <path d="M21.44 11.05l-9.19 9.19a6 6 0 0 1-8.49-8.49l9.19-9.19a4 4 0 0 1 5.66 5.66L9.64 16.2a2 2 0 0 1-2.83-2.83l8.49-8.49" stroke="currentColor" stroke-width="2"/>
                </svg>
              </button>
              
              <div class="text-input-wrapper">
                <input 
                  v-model="newMessageText"
                  type="text" 
                  class="message-input" 
                  placeholder="Type a message..."
                  @keypress.enter="sendMessage"
                  @input="handleTyping"
                />
              </div>
              
              <button v-if="newMessageText.trim()" class="send-btn" @click="sendMessage" title="Send">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                  <line x1="22" y1="2" x2="11" y2="13" stroke="currentColor" stroke-width="2"/>
                  <polygon points="22,2 15,22 11,13 2,9 22,2" fill="currentColor"/>
                </svg>
              </button>
              <button v-else class="voice-btn" @click="startVoiceMessage" title="Voice Message">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                  <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z" stroke="currentColor" stroke-width="2"/>
                  <path d="M19 10v2a7 7 0 0 1-14 0v-2M12 19v4M8 23h8" stroke="currentColor" stroke-width="2"/>
                </svg>
              </button>
            </div>
          </div>
          
          <!-- Ended Chat Message -->
          <div class="ended-chat-message" v-if="selectedContact.status === 'ended'">
            <div class="ended-chat-content">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <path d="M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 17.5228 6.47715 22 12 22Z" stroke="currentColor" stroke-width="2"/>
                <path d="M9 12L11 14L15 10" stroke="currentColor" stroke-width="2"/>
              </svg>
              <p>This conversation has ended</p>
            </div>
          </div>
        </div>

        <!-- Contact Info Panel -->
        <div class="contact-info-panel" v-if="selectedContact && showContactInfo">
          <div class="info-header">
            <button class="close-info-btn" @click="toggleContactInfo">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                <line x1="18" y1="6" x2="6" y2="18" stroke="currentColor" stroke-width="2"/>
                <line x1="6" y1="6" x2="18" y2="18" stroke="currentColor" stroke-width="2"/>
              </svg>
            </button>
            <div class="info-avatar" :style="{ backgroundColor: getAvatarColor(selectedContact.name) }">
              {{ selectedContact.initials }}
            </div>
            <h3 class="info-name">{{ selectedContact.name }}</h3>
            <p class="info-subtitle">Survivor Information</p>
          </div>

          <div class="info-content">
            <div class="info-section">
              <h4 class="section-title">Contact Details</h4>
              <div class="info-items">
                <div class="info-item">
                  <span class="info-label">Phone</span>
                  <span class="info-value">{{ selectedContact.phone || 'Not provided' }}</span>
                </div>
                <div class="info-item">
                  <span class="info-label">Age</span>
                  <span class="info-value">{{ selectedContact.age || 'Not provided' }}</span>
                </div>
                <div class="info-item">
                  <span class="info-label">Date of Birth</span>
                  <span class="info-value">{{ selectedContact.dateOfBirth || 'Not provided' }}</span>
                </div>
              </div>
            </div>

            <div class="info-section">
              <h4 class="section-title">Case Information</h4>
              <div class="info-items">
                <div class="info-item">
                  <span class="info-label">Risk Level</span>
                  <span class="info-value risk-level" :class="getRiskLevelClass(selectedContact.riskLevel)">
                    {{ selectedContact.riskLevel || 'Not assessed' }}
                  </span>
                </div>
                <div class="info-item">
                  <span class="info-label">Case Manager</span>
                  <span class="info-value">{{ selectedContact.caseManager || 'Unassigned' }}</span>
                </div>
              </div>
            </div>

            <div class="info-actions">
              <button class="info-btn primary" @click="createCaseFromChat">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" stroke="currentColor" stroke-width="2"/>
                  <polyline points="14,2 14,8 20,8" stroke="currentColor" stroke-width="2"/>
                  <line x1="16" y1="13" x2="8" y2="13" stroke="currentColor" stroke-width="2"/>
                  <line x1="16" y1="17" x2="8" y2="17" stroke="currentColor" stroke-width="2"/>
                </svg>
                Create Case
              </button>
              <button class="info-btn" @click="viewFullProfile">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" stroke="currentColor" stroke-width="2"/>
                  <circle cx="12" cy="7" r="4" stroke="currentColor" stroke-width="2"/>
                </svg>
                View Profile
              </button>
              <button v-if="selectedContact.status === 'active'" class="info-btn danger" @click="endChat">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                  <path d="M18 6L6 18M6 6l12 12" stroke="currentColor" stroke-width="2"/>
                </svg>
                End Chat
              </button>
            </div>
          </div>
        </div>

        <!-- Call Modal -->
        <div class="modal-overlay" v-if="showCallModal" @click="cancelCall">
          <div class="call-modal" @click.stop>
            <div class="call-header">
              <div class="call-avatar" :style="{ backgroundColor: getAvatarColor(selectedContact.name) }">
                {{ selectedContact.initials }}
              </div>
              <h3 class="call-name">{{ selectedContact.name }}</h3>
              <p class="call-number">{{ selectedContact.phone }}</p>
              <p class="call-status">{{ callStatus }}</p>
            </div>
            
            <div class="call-actions">
              <button class="call-btn end-call" @click="endCall" title="End Call">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                  <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z" stroke="currentColor" stroke-width="2"/>
                </svg>
              </button>
              <button class="call-btn mute" @click="toggleMute" title="Mute">
                <svg v-if="!isMuted" width="24" height="24" viewBox="0 0 24 24" fill="none">
                  <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z" stroke="currentColor" stroke-width="2"/>
                  <path d="M19 10v2a7 7 0 0 1-14 0v-2" stroke="currentColor" stroke-width="2"/>
                  <line x1="12" y1="19" x2="12" y2="23" stroke="currentColor" stroke-width="2"/>
                  <line x1="8" y1="23" x2="16" y2="23" stroke="currentColor" stroke-width="2"/>
                </svg>
                <svg v-else width="24" height="24" viewBox="0 0 24 24" fill="none">
                  <line x1="1" y1="1" x2="23" y2="23" stroke="currentColor" stroke-width="2"/>
                  <path d="M9 9v3a3 3 0 0 0 5.12 2.12M15 9.34V4a3 3 0 0 0-5.94-.6" stroke="currentColor" stroke-width="2"/>
                  <path d="M17 16.95A7 7 0 0 1 5 12v-2m14 0v2a7 7 0 0 1-.11 1.23" stroke="currentColor" stroke-width="2"/>
                  <line x1="12" y1="19" x2="12" y2="23" stroke="currentColor" stroke-width="2"/>
                  <line x1="8" y1="23" x2="16" y2="23" stroke="currentColor" stroke-width="2"/>
                </svg>
              </button>
            </div>
          </div>
        </div>

        <!-- End Chat Confirmation Modal -->
        <div class="modal-overlay" v-if="showEndChatModal" @click="cancelEndChat">
          <div class="modal-container" @click.stop>
            <div class="modal-header">
              <h3>End Conversation</h3>
            </div>
            <div class="modal-body">
              <p>Are you sure you want to end this conversation? It will be moved to archived conversations.</p>
            </div>
            <div class="modal-footer">
              <button class="modal-btn" @click="cancelEndChat">Cancel</button>
              <button class="modal-btn danger" @click="confirmEndChat">End Conversation</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import SidePanel from '@/components/SidePanel.vue'

const router = useRouter()

// Reactive state
const searchQuery = ref('')
const activePlatform = ref('whatsapp')
const selectedContactId = ref(null)
const newMessageText = ref('')
const currentTheme = ref(localStorage.getItem('theme') || 'dark')
const showContactInfo = ref(false)
const showEndChatModal = ref(false)
const showCallModal = ref(false)
const callStatus = ref('Calling...')
const isMuted = ref(false)

// SidePanel related state
const userRole = ref('super-admin')
const isInQueue = ref(false)
const isProcessingQueue = ref(false)
const currentCall = ref(null)

// Refs
const messagesArea = ref(null)

// Platform definitions
const platforms = ref([
  { id: 'whatsapp', name: 'WhatsApp' },
  { id: 'sms', name: 'SMS' },
  { id: 'messenger', name: 'Messenger' },
  { id: 'telegram', name: 'Telegram' },
  { id: 'past', name: 'Archive' }
])

// Sample contacts data
const contacts = ref([
  {
    id: 'sarah-miller',
    name: 'Sarah Miller',
    initials: 'SM',
    preview: 'I need help with a domestic violence situation...',
    time: '10:30 AM',
    unreadCount: 2,
    platform: 'whatsapp',
    status: 'active',
    dateOfBirth: '1992-06-15',
    age: 31,
    phone: '+1 623-555-0123',
    riskLevel: 'Medium Risk',
    caseManager: 'Emily Rodriguez',
    messages: [
      { id: 1, text: 'Hello Sarah, this is Maria from the Survivor Helpline. How can I assist you today?', sender: 'received', time: '09:00 AM', date: 'Today' },
      { id: 2, text: 'I need help with a domestic violence situation. My partner has been threatening me and I don\'t know what to do.', sender: 'sent', time: '09:05 AM' },
      { id: 3, text: 'I\'m very sorry to hear that you\'re going through this difficult situation. Your safety is our top priority. Are you currently in a safe location?', sender: 'received', time: '09:07 AM' },
      { id: 4, text: 'Yes, I\'m at work right now. My partner doesn\'t know I\'m reaching out for help.', sender: 'sent', time: '09:10 AM' },
      { id: 5, text: 'I\'m glad you\'re in a safe place at the moment. Would you like me to provide you with information about emergency shelters, safety planning, or legal options?', sender: 'received', time: '09:15 AM' },
      { id: 6, text: 'I think I need information about all of those. I\'m not sure if I need to leave immediately or if there are other options.', sender: 'sent', time: '09:20 AM' }
    ]
  },
  {
    id: 'john-doe',
    name: 'John Doe',
    initials: 'JD',
    preview: 'Thank you for helping me find shelter yesterday...',
    time: 'Yesterday',
    platform: 'sms',
    status: 'active',
    age: 28,
    phone: '+1 623-555-0124',
    riskLevel: 'Low Risk',
    caseManager: 'Michael Torres',
    messages: [
      { id: 1, text: 'Thank you for helping me find shelter yesterday.', sender: 'sent', time: '2:30 PM', date: 'Yesterday' },
      { id: 2, text: 'You\'re welcome, John. I\'m glad I could assist you. How are you settling in?', sender: 'received', time: '2:45 PM' }
    ]
  },
  {
    id: 'emily-brown',
    name: 'Emily Brown',
    initials: 'EB',
    preview: 'When is my counseling appointment scheduled?',
    time: 'Yesterday',
    unreadCount: 1,
    platform: 'messenger',
    status: 'active',
    age: 35,
    phone: '+1 623-555-0125',
    riskLevel: 'High Risk',
    caseManager: 'Lisa Chen',
    messages: [
      { id: 1, text: 'When is my counseling appointment scheduled?', sender: 'sent', time: '11:00 AM', date: 'Yesterday' },
      { id: 2, text: 'Let me check the schedule for you, Emily.', sender: 'received', time: '11:05 AM' }
    ]
  },
  {
    id: 'michael-johnson',
    name: 'Michael Johnson',
    initials: 'MJ',
    preview: 'I need to reschedule my safety planning session...',
    time: 'Mon',
    platform: 'telegram',
    status: 'active',
    age: 42,
    phone: '+1 623-555-0126',
    riskLevel: 'High Risk',
    caseManager: 'David Wilson',
    messages: [
      { id: 1, text: 'I need to reschedule my safety planning session.', sender: 'sent', time: '9:00 AM', date: 'Monday' },
      { id: 2, text: 'Of course, Michael. What time would work best for you?', sender: 'received', time: '9:15 AM' }
    ]
  },
  // Past conversations
  {
    id: 'david-clark',
    name: 'David Clark',
    initials: 'DC',
    preview: 'Thank you for all your help. Case resolved.',
    time: 'Last week',
    platform: 'messenger',
    status: 'ended',
    age: 38,
    phone: '+1 623-555-0128',
    riskLevel: 'Low Risk',
    caseManager: 'Robert Jackson',
    messages: [
      { id: 1, text: 'Can you provide more information about emergency housing?', sender: 'sent', time: '11:45 AM', date: 'Last Week' },
      { id: 2, text: 'Thank you for all your help. Case resolved.', sender: 'sent', time: '2:30 PM' }
    ]
  }
])

// Computed properties
const filteredContacts = computed(() => {
  let filtered = contacts.value.filter(contact => {
    if (activePlatform.value === 'past') {
      return contact.status === 'ended'
    } else {
      return contact.platform === activePlatform.value && contact.status === 'active'
    }
  })

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(contact =>
      contact.name.toLowerCase().includes(query) ||
      contact.preview.toLowerCase().includes(query)
    )
  }

  return filtered
})

const selectedContact = computed(() => {
  return contacts.value.find(contact => contact.id === selectedContactId.value)
})

const groupedMessages = computed(() => {
  if (!selectedContact.value || !selectedContact.value.messages) return []
  
  const groups = []
  let currentGroup = null
  
  selectedContact.value.messages.forEach(message => {
    if (message.date && (!currentGroup || currentGroup.date !== message.date)) {
      currentGroup = { date: message.date, messages: [] }
      groups.push(currentGroup)
    }
    
    if (currentGroup) {
      currentGroup.messages.push(message)
    }
  })
  
  return groups
})

// Helper functions
const getPlatformUnreadCount = (platformId) => {
  return contacts.value
    .filter(contact => contact.platform === platformId && contact.status === 'active')
    .reduce((total, contact) => total + (contact.unreadCount || 0), 0)
}

const getPlatformShortName = (platform) => {
  const shortNames = {
    whatsapp: 'WA',
    sms: 'SMS',
    messenger: 'MSG',
    telegram: 'TG'
  }
  return shortNames[platform] || platform.toUpperCase()
}

const getAvatarColor = (name) => {
  const colors = [
    '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7',
    '#DDA0DD', '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E9'
  ]
  const index = name.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0)
  return colors[index % colors.length]
}

const getRiskLevelClass = (riskLevel) => {
  if (!riskLevel) return ''
  if (riskLevel.toLowerCase().includes('high')) return 'high-risk'
  if (riskLevel.toLowerCase().includes('medium')) return 'medium-risk'
  if (riskLevel.toLowerCase().includes('low')) return 'low-risk'
  return ''
}

const getContactStatus = (contact) => {
  if (!contact) return ''
  if (contact.status === 'ended') return 'Conversation ended'
  return `Active • Last seen ${contact.time}`
}

// SidePanel event handlers
const handleQueueToggle = () => {
  isInQueue.value = !isInQueue.value
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
    root.style.setProperty('--bg-primary', '#ffffff')
    root.style.setProperty('--bg-secondary', '#f8f9fa')
    root.style.setProperty('--bg-tertiary', '#f1f3f4')
    root.style.setProperty('--text-primary', '#1a1a1a')
    root.style.setProperty('--text-secondary', '#5f6368')
    root.style.setProperty('--text-tertiary', '#80868b')
    root.style.setProperty('--border-color', '#e8eaed')
    root.style.setProperty('--accent-color', '#FF8C00')
    root.style.setProperty('--accent-light', '#FFF4E6')
    root.style.setProperty('--success-color', '#34C759')
    root.style.setProperty('--warning-color', '#FF9500')
    root.style.setProperty('--error-color', '#FF3B30')
    root.style.setProperty('--danger-color', '#FF3B30')
    root.style.setProperty('--message-sent', '#FF8C00')
    root.style.setProperty('--message-received', '#E5E5EA')
    root.style.setProperty('--shadow-light', '0 1px 3px rgba(0, 0, 0, 0.1)')
    root.style.setProperty('--shadow-medium', '0 4px 6px rgba(0, 0, 0, 0.1)')
  } else {
    root.style.setProperty('--bg-primary', '#000000')
    root.style.setProperty('--bg-secondary', '#1C1C1E')
    root.style.setProperty('--bg-tertiary', '#2C2C2E')
    root.style.setProperty('--text-primary', '#FFFFFF')
    root.style.setProperty('--text-secondary', '#AEAEB2')
    root.style.setProperty('--text-tertiary', '#8E8E93')
    root.style.setProperty('--border-color', '#38383A')
    root.style.setProperty('--accent-color', '#FF8C00')
    root.style.setProperty('--accent-light', '#2D1B0A')
    root.style.setProperty('--success-color', '#30D158')
    root.style.setProperty('--warning-color', '#FF9F0A')
    root.style.setProperty('--error-color', '#FF453A')
    root.style.setProperty('--danger-color', '#FF453A')
    root.style.setProperty('--message-sent', '#FF8C00')
    root.style.setProperty('--message-received', '#3A3A3C')
    root.style.setProperty('--shadow-light', '0 1px 3px rgba(0, 0, 0, 0.3)')
    root.style.setProperty('--shadow-medium', '0 4px 6px rgba(0, 0, 0, 0.3)')
  }
}

const toggleTheme = () => {
  const newTheme = currentTheme.value === 'dark' ? 'light' : 'dark'
  localStorage.setItem('theme', newTheme)
  currentTheme.value = newTheme
  applyTheme(newTheme)
}

const setActivePlatform = (platformId) => {
  activePlatform.value = platformId
  selectedContactId.value = null
  searchQuery.value = ''
}

const selectContact = (contactId) => {
  selectedContactId.value = contactId
  
  // Clear unread count
  const contact = contacts.value.find(c => c.id === contactId)
  if (contact) {
    contact.unreadCount = 0
  }
  
  // Scroll to bottom
  nextTick(() => {
    scrollToBottom()
  })
}

const deselectContact = () => {
  selectedContactId.value = null
  showContactInfo.value = false
}

const toggleContactInfo = () => {
  showContactInfo.value = !showContactInfo.value
}

const endChat = () => {
  showEndChatModal.value = true
}

const cancelEndChat = () => {
  showEndChatModal.value = false
}

const confirmEndChat = () => {
  if (selectedContact.value) {
    // Add end message
    const contact = contacts.value.find(c => c.id === selectedContactId.value)
    if (contact) {
      contact.status = 'ended'
      contact.messages.push({
        id: contact.messages.length + 1,
        text: 'This conversation has been ended by the agent.',
        sender: 'received',
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        date: 'Today'
      })
      
      // Close modal
      showEndChatModal.value = false
      
      // If we're not already in the past conversations tab, switch to it
      if (activePlatform.value !== 'past') {
        activePlatform.value = 'past'
      }
    }
  }
}

const initiateCall = () => {
  if (selectedContact.value && selectedContact.value.phone) {
    showCallModal.value = true
    callStatus.value = 'Calling...'
    
    // Simulate call connection
    setTimeout(() => {
      callStatus.value = 'Connected'
    }, 2000)
  }
}

const endCall = () => {
  showCallModal.value = false
  callStatus.value = 'Calling...'
  isMuted.value = false
}

const cancelCall = () => {
  showCallModal.value = false
  callStatus.value = 'Calling...'
  isMuted.value = false
}

const toggleMute = () => {
  isMuted.value = !isMuted.value
}

const sendMessage = () => {
  if (newMessageText.value.trim() !== '' && selectedContactId.value !== null) {
    const contact = contacts.value.find(c => c.id === selectedContactId.value)
    if (contact && contact.messages && contact.status === 'active') {
      const newMessage = {
        id: contact.messages.length + 1,
        text: newMessageText.value,
        sender: 'received',
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      }
      contact.messages.push(newMessage)
      newMessageText.value = ''
      
      nextTick(() => {
        scrollToBottom()
      })
    }
  }
}

const scrollToBottom = () => {
  if (messagesArea.value) {
    messagesArea.value.scrollTop = messagesArea.value.scrollHeight
  }
}

const clearSearch = () => {
  searchQuery.value = ''
}

const handleSearch = () => {
  // Filtering handled by computed property
}

const handleTyping = () => {
  // Handle typing indicator
}

const createCaseFromChat = () => {
  if (!selectedContact.value) return
  
  const chatSummary = selectedContact.value.messages
    ?.map(msg => `${msg.sender === 'sent' ? 'Survivor' : 'Agent'}: ${msg.text}`)
    .join('\n') || ''
  
  router.push({
    path: '/case-creation',
    query: {
      survivorName: selectedContact.value.name,
      survivorPhone: selectedContact.value.phone,
      riskLevel: selectedContact.value.riskLevel,
      chatSummary: chatSummary,
      platform: activePlatform.value,
      fromChat: 'true'
    }
  })
}

// Placeholder methods
const showNewChatModal = () => console.log('Show new chat modal')
const showAttachmentMenu = () => console.log('Show attachment menu')
const startVoiceMessage = () => console.log('Start voice message')
const viewFullProfile = () => console.log('View full profile')

// Lifecycle
onMounted(() => {
  const savedTheme = localStorage.getItem('theme')
  if (savedTheme) {
    currentTheme.value = savedTheme
  }
  applyTheme(currentTheme.value)
})
</script>

<style>
/* Global Styles */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI', Roboto, sans-serif;
  background-color: var(--bg-primary);
  color: var(--text-primary);
  overflow: hidden;
}

.app-container {
  display: flex;
  height: 100vh;
  background-color: var(--bg-primary);
}

.main-content {
  flex: 1;
  margin-left: var(--sidebar-width, 250px);
  display: flex;
  flex-direction: column;
  background-color: var(--bg-primary);
  transition: margin-left 0.3s ease;
}

/* Chat Interface */
.chat-interface {
  display: flex;
  flex: 1;
  overflow: hidden;
}

/* Chat Sidebar */
.chat-sidebar {
  width: 380px;
  background-color: var(--bg-secondary);
  border-right: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  transition: width 0.3s ease;
}

.chat-sidebar.full-width {
  width: 100%;
}

.sidebar-header {
  padding: 20px 20px 16px 20px;
  border-bottom: 1px solid var(--border-color);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-title {
  font-size: 32px;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: -0.5px;
}

.header-actions {
  display: flex;
  gap: 8px;
}

.header-btn {
  width: 36px;
  height: 36px;
  border-radius: 18px;
  background-color: var(--bg-tertiary);
  border: none;
  color: var(--text-secondary);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.header-btn:hover {
  background-color: var(--border-color);
  color: var(--text-primary);
}

/* Platform Tabs */
.platform-tabs {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 8px;
  padding: 16px 20px;
  border-bottom: 1px solid var(--border-color);
}

.platform-tab {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 8px 12px;
  border-radius: 16px;
  background-color: transparent;
  border: 1px solid var(--border-color);
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
  font-size: 13px;
  font-weight: 500;
  min-height: 36px;
}

.platform-tab:hover {
  background-color: var(--bg-tertiary);
  color: var(--text-primary);
}

.platform-tab.active {
  background-color: var(--accent-color);
  color: white;
  border-color: var(--accent-color);
}

.tab-text {
  font-size: 13px;
  font-weight: 500;
}

.tab-badge {
  background-color: rgba(255, 255, 255, 0.3);
  color: white;
  font-size: 11px;
  font-weight: 600;
  padding: 2px 6px;
  border-radius: 10px;
  min-width: 16px;
  text-align: center;
}

.platform-tab:not(.active) .tab-badge {
  background-color: var(--accent-color);
  color: white;
}

/* Search Section */
.search-section {
  padding: 16px 20px;
  border-bottom: 1px solid var(--border-color);
}

.search-container {
  position: relative;
  display: flex;
  align-items: center;
}

.search-icon {
  position: absolute;
  left: 12px;
  color: var(--text-tertiary);
  z-index: 1;
}

.search-input {
  width: 100%;
  padding: 10px 12px 10px 36px;
  border-radius: 20px;
  border: none;
  background-color: var(--bg-tertiary);
  color: var(--text-primary);
  font-size: 14px;
  transition: all 0.2s ease;
}

.search-input:focus {
  outline: none;
  background-color: var(--bg-primary);
  box-shadow: 0 0 0 2px var(--accent-color);
}

.search-input::placeholder {
  color: var(--text-tertiary);
}

.search-clear {
  position: absolute;
  right: 8px;
  width: 20px;
  height: 20px;
  border-radius: 10px;
  background-color: var(--text-tertiary);
  border: none;
  color: var(--bg-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.search-clear:hover {
  background-color: var(--text-secondary);
}

/* Chat List */
.chat-list {
  flex: 1;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px 12px 20px;
}

.list-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
}

.list-count {
  font-size: 12px;
  color: var(--text-tertiary);
  background-color: var(--bg-tertiary);
  padding: 2px 8px;
  border-radius: 10px;
}

.chat-contacts {
  flex: 1;
  overflow-y: auto;
  padding: 0 8px 20px 8px;
}

.chat-contact {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border-radius: 16px;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-bottom: 4px;
  position: relative;
}

.chat-contact:hover {
  background-color: var(--bg-tertiary);
}

.chat-contact.active {
  background-color: var(--accent-light);
}

.chat-contact.unread {
  background-color: var(--bg-tertiary);
}

.chat-contact.ended {
  opacity: 0.6;
}

.contact-avatar-wrapper {
  position: relative;
}

.contact-avatar {
  width: 50px;
  height: 50px;
  border-radius: 25px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 600;
  font-size: 18px;
}

.online-dot {
  position: absolute;
  bottom: 2px;
  right: 2px;
  width: 12px;
  height: 12px;
  background-color: var(--success-color);
  border: 2px solid var(--bg-secondary);
  border-radius: 6px;
}

.contact-details {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.contact-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.contact-name {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.contact-meta {
  display: flex;
  align-items: center;
  gap: 8px;
}

.contact-time {
  font-size: 12px;
  color: var(--text-tertiary);
  white-space: nowrap;
}

.unread-count {
  background-color: var(--accent-color);
  color: white;
  font-size: 11px;
  font-weight: 600;
  padding: 2px 6px;
  border-radius: 10px;
  min-width: 18px;
  text-align: center;
}

.contact-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.contact-preview {
  font-size: 14px;
  color: var(--text-secondary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  flex: 1;
  margin-right: 8px;
}

.platform-badge {
  font-size: 10px;
  font-weight: 600;
  padding: 2px 6px;
  border-radius: 8px;
  background-color: var(--bg-tertiary);
  color: var(--text-tertiary);
}

.platform-badge.whatsapp { background-color: #25D366; color: white; }
.platform-badge.sms { background-color: var(--accent-color); color: white; }
.platform-badge.messenger { background-color: #0084FF; color: white; }
.platform-badge.telegram { background-color: #0088cc; color: white; }

/* Chat Main */
.chat-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  background-color: var(--bg-primary);
  overflow: hidden;
  position: relative;
}

.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid var(--border-color);
  background-color: var(--bg-primary);
}

.chat-header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.back-btn {
  width: 32px;
  height: 32px;
  border-radius: 16px;
  background-color: var(--bg-secondary);
  border: none;
  color: var(--text-secondary);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.back-btn:hover {
  background-color: var(--bg-tertiary);
  color: var(--text-primary);
}

.contact-avatar-header {
  width: 40px;
  height: 40px;
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 600;
  font-size: 16px;
}

.contact-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.contact-info .contact-name {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
}

.contact-status {
  font-size: 13px;
  color: var(--text-secondary);
  display: flex;
  align-items: center;
  gap: 6px;
}

.status-indicator {
  width: 6px;
  height: 6px;
  border-radius: 3px;
  background-color: var(--text-tertiary);
}

.status-indicator.online {
  background-color: var(--success-color);
}

.chat-header-actions {
  display: flex;
  gap: 8px;
}

.action-btn {
  width: 36px;
  height: 36px;
  border-radius: 18px;
  background-color: var(--bg-secondary);
  border: none;
  color: var(--text-secondary);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.action-btn:hover {
  background-color: var(--bg-tertiary);
  color: var(--text-primary);
}

.end-chat-btn {
  color: var(--danger-color);
}

.end-chat-btn:hover {
  background-color: var(--danger-color);
  color: white;
}

/* Messages Area */
.messages-area {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  scroll-behavior: smooth;
}

.messages-content {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.message-group {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.date-divider {
  display: flex;
  justify-content: center;
  margin: 16px 0;
}

.date-text {
  background-color: var(--bg-tertiary);
  color: var(--text-tertiary);
  padding: 6px 12px;
  border-radius: 16px;
  font-size: 12px;
  font-weight: 500;
}

.message-container {
  display: flex;
  margin-bottom: 2px;
}

.message-container.sent {
  justify-content: flex-end;
}

.message-container.received {
  justify-content: flex-start;
}

.message-bubble {
  max-width: 75%;
  padding: 12px 16px;
  border-radius: 20px;
  position: relative;
  word-wrap: break-word;
  box-shadow: var(--shadow-light);
}

.message-bubble.sent {
  background-color: var(--message-sent);
  color: white;
  border-bottom-right-radius: 6px;
}

.message-bubble.received {
  background-color: var(--message-received);
  color: var(--text-primary);
  border-bottom-left-radius: 6px;
}

.message-text {
  font-size: 15px;
  line-height: 1.4;
  margin-bottom: 4px;
}

.message-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 8px;
}

.message-time {
  font-size: 11px;
  opacity: 0.7;
}

.message-status {
  display: flex;
  align-items: center;
}

/* Message Input */
.message-input-area {
  padding: 16px 20px;
  border-top: 1px solid var(--border-color);
  background-color: var(--bg-primary);
}

.input-container {
  display: flex;
  align-items: flex-end;
  gap: 8px;
  background-color: var(--bg-secondary);
  border-radius: 24px;
  padding: 8px;
  border: 1px solid var(--border-color);
}

.input-action-btn {
  width: 32px;
  height: 32px;
  border-radius: 16px;
  background-color: transparent;
  border: none;
  color: var(--text-secondary);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.input-action-btn:hover {
  background-color: var(--bg-tertiary);
  color: var(--text-primary);
}

.text-input-wrapper {
  flex: 1;
  display: flex;
  align-items: center;
}

.message-input {
  flex: 1;
  border: none;
  background: transparent;
  color: var(--text-primary);
  font-size: 15px;
  padding: 8px 0;
  outline: none;
  resize: none;
}

.message-input::placeholder {
  color: var(--text-tertiary);
}

.send-btn, .voice-btn {
  width: 32px;
  height: 32px;
  border-radius: 16px;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.send-btn {
  background-color: var(--accent-color);
  color: white;
}

.send-btn:hover {
  opacity: 0.9;
}

.voice-btn {
  background-color: transparent;
  color: var(--text-secondary);
}

.voice-btn:hover {
  background-color: var(--bg-tertiary);
  color: var(--text-primary);
}

/* Ended Chat Message */
.ended-chat-message {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
  background-color: var(--bg-secondary);
  border-top: 1px solid var(--border-color);
}

.ended-chat-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  color: var(--text-secondary);
}

.ended-chat-content svg {
  color: var(--success-color);
}

.ended-chat-content p {
  font-size: 16px;
  font-weight: 500;
}

/* Contact Info Panel */
.contact-info-panel {
  width: 320px;
  background-color: var(--bg-secondary);
  border-left: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.info-header {
  padding: 20px;
  text-align: center;
  border-bottom: 1px solid var(--border-color);
  position: relative;
}

.close-info-btn {
  position: absolute;
  top: 16px;
  right: 16px;
  width: 28px;
  height: 28px;
  border-radius: 14px;
  background-color: var(--bg-tertiary);
  border: none;
  color: var(--text-secondary);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.close-info-btn:hover {
  background-color: var(--border-color);
  color: var(--text-primary);
}

.info-avatar {
  width: 80px;
  height: 80px;
  border-radius: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 600;
  font-size: 32px;
  margin: 0 auto 16px auto;
}

.info-name {
  font-size: 22px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 4px;
}

.info-subtitle {
  font-size: 14px;
  color: var(--text-secondary);
}

.info-content {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
}

.info-section {
  margin-bottom: 28px;
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 12px;
}

.info-items {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.info-label {
  font-size: 12px;
  color: var(--text-tertiary);
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.info-value {
  font-size: 14px;
  color: var(--text-primary);
  font-weight: 500;
}

.risk-level.high-risk {
  color: var(--error-color);
}

.risk-level.medium-risk {
  color: var(--warning-color);
}

.risk-level.low-risk {
  color: var(--success-color);
}

.info-actions {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 20px;
}

.info-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 16px;
  border-radius: 12px;
  border: 1px solid var(--border-color);
  background-color: var(--bg-tertiary);
  color: var(--text-primary);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.info-btn:hover {
  background-color: var(--bg-primary);
  box-shadow: var(--shadow-medium);
}

.info-btn.primary {
  background-color: var(--accent-color);
  color: white;
  border-color: var(--accent-color);
}

.info-btn.primary:hover {
  opacity: 0.9;
}

.info-btn.danger {
  background-color: var(--danger-color);
  color: white;
  border-color: var(--danger-color);
}

.info-btn.danger:hover {
  opacity: 0.9;
}

/* Call Modal */
.call-modal {
  background-color: var(--bg-secondary);
  border-radius: 20px;
  padding: 40px 30px;
  text-align: center;
  box-shadow: var(--shadow-medium);
  width: 320px;
  max-width: 90%;
}

.call-header {
  margin-bottom: 30px;
}

.call-avatar {
  width: 100px;
  height: 100px;
  border-radius: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 600;
  font-size: 36px;
  margin: 0 auto 20px auto;
}

.call-name {
  font-size: 24px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.call-number {
  font-size: 16px;
  color: var(--text-secondary);
  margin-bottom: 12px;
}

.call-status {
  font-size: 14px;
  color: var(--accent-color);
  font-weight: 500;
}

.call-actions {
  display: flex;
  justify-content: center;
  gap: 20px;
}

.call-btn {
  width: 60px;
  height: 60px;
  border-radius: 30px;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.call-btn.end-call {
  background-color: var(--danger-color);
  color: white;
}

.call-btn.end-call:hover {
  opacity: 0.9;
  transform: scale(1.05);
}

.call-btn.mute {
  background-color: var(--bg-tertiary);
  color: var(--text-secondary);
}

.call-btn.mute:hover {
  background-color: var(--border-color);
  color: var(--text-primary);
}

/* Modal */
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
}

.modal-container {
  width: 400px;
  background-color: var(--bg-secondary);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: var(--shadow-medium);
}

.modal-header {
  padding: 16px 20px;
  border-bottom: 1px solid var(--border-color);
}

.modal-header h3 {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
}

.modal-body {
  padding: 20px;
}

.modal-body p {
  font-size: 15px;
  line-height: 1.5;
  color: var(--text-secondary);
}

.modal-footer {
  padding: 16px 20px;
  border-top: 1px solid var(--border-color);
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.modal-btn {
  padding: 10px 16px;
  border-radius: 8px;
  border: 1px solid var(--border-color);
  background-color: var(--bg-tertiary);
  color: var(--text-primary);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.modal-btn:hover {
  background-color: var(--bg-primary);
  box-shadow: var(--shadow-light);
}

.modal-btn.danger {
  background-color: var(--danger-color);
  color: white;
  border-color: var(--danger-color);
}

.modal-btn.danger:hover {
  opacity: 0.9;
}

/* Responsive Design */
@media (max-width: 1200px) {
  .contact-info-panel {
    display: none;
  }
  
  .chat-sidebar {
    width: 320px;
  }
}

@media (max-width: 768px) {
  .main-content {
    margin-left: 0;
  }
  
  .chat-interface {
    flex-direction: column;
  }
  
  .chat-sidebar {
    width: 100%;
    height: 50%;
    border-right: none;
    border-bottom: 1px solid var(--border-color);
  }
  
  .chat-main {
    height: 50%;
  }
  
  .platform-tabs {
    grid-template-columns: repeat(3, 1fr);
    gap: 6px;
  }
  
  .back-btn {
    display: flex;
  }
  
  .header-title {
    font-size: 28px;
  }
  
  .contact-avatar {
    width: 44px;
    height: 44px;
    font-size: 16px;
  }
  
  .contact-name {
    font-size: 15px;
  }
  
  .contact-preview {
    font-size: 13px;
  }
}

@media (max-width: 480px) {
  .sidebar-header {
    padding: 16px;
  }
  
  .header-title {
    font-size: 24px;
  }
  
  .platform-tabs {
    padding: 12px 16px;
    grid-template-columns: repeat(2, 1fr);
  }
  
  .search-section {
    padding: 12px 16px;
  }
  
  .list-header {
    padding: 12px 16px 8px 16px;
  }
  
  .chat-contacts {
    padding: 0 8px 16px 8px;
  }
  
  .contact-avatar {
    width: 40px;
    height: 40px;
    font-size: 14px;
  }
  
  .contact-name {
    font-size: 14px;
  }
  
  .contact-preview {
    font-size: 12px;
  }
  
  .message-bubble {
    max-width: 85%;
    padding: 10px 14px;
  }
  
  .message-text {
    font-size: 14px;
  }
  
  .messages-area {
    padding: 16px;
  }
  
  .message-input-area {
    padding: 12px 16px;
  }
  
  .chat-header {
    padding: 12px 16px;
  }
  
  .contact-info .contact-name {
    font-size: 16px;
  }
}

/* Animations */
@keyframes slideInFromRight {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

@keyframes slideInFromLeft {
  from {
    transform: translateX(-100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
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

.message-container {
  animation: fadeIn 0.3s ease;
}

.chat-contact {
  animation: fadeIn 0.2s ease;
}

/* Focus States for Accessibility */
.platform-tab:focus,
.header-btn:focus,
.action-btn:focus,
.info-btn:focus,
.input-action-btn:focus,
.send-btn:focus,
.voice-btn:focus,
.back-btn:focus,
.close-info-btn:focus {
  outline: 2px solid var(--accent-color);
  outline-offset: 2px;
}

.search-input:focus,
.message-input:focus {
  outline: none;
}

/* High Contrast Mode */
@media (prefers-contrast: high) {
  .chat-contact.active {
    border: 2px solid var(--accent-color);
  }
  
  .message-bubble.sent {
    border: 1px solid var(--accent-color);
  }
  
  .message-bubble.received {
    border: 1px solid var(--border-color);
  }
}

/* Reduced Motion */
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}

/* Loading States */
.loading {
  opacity: 0.6;
  pointer-events: none;
}

.loading::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 20px;
  height: 20px;
  margin: -10px 0 0 -10px;
  border: 2px solid var(--border-color);
  border-top: 2px solid var(--accent-color);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Hover Effects */
.chat-contact:hover .contact-avatar {
  transform: scale(1.05);
}

.message-bubble:hover {
  transform: translateY(-1px);
}

.platform-tab:hover {
  transform: translateY(-1px);
}

/* Selection States */
::selection {
  background-color: var(--accent-light);
  color: var(--accent-color);
}

::-moz-selection {
  background-color: var(--accent-light);
  color: var(--accent-color);
}

/* Custom Properties for Dynamic Theming */
:root {
  --sidebar-width: 250px;
  --transition-timing: ease;
  --border-radius-sm: 8px;
  --border-radius-md: 12px;
  --border-radius-lg: 16px;
  --border-radius-xl: 20px;
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 12px;
  --spacing-lg: 16px;
  --spacing-xl: 20px;
  --spacing-2xl: 24px;
}

/* Dark mode specific adjustments */
@media (prefers-color-scheme: dark) {
  .message-bubble.sent {
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
  }
  
  .message-bubble.received {
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
  }
  
  .chat-contact:hover {
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  }
}

/* Smooth scrolling */
html {
  scroll-behavior: smooth;
}

/* Custom scrollbar for webkit browsers */
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background-color: var(--border-color);
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background-color: var(--text-tertiary);
}

/* Print styles */
@media print {
  .chat-sidebar,
  .contact-info-panel,
  .message-input-area {
    display: none;
  }
  
  .chat-main {
    width: 100%;
  }
  
  .message-bubble {
    box-shadow: none;
    border: 1px solid var(--border-color);
  }
}
</style>