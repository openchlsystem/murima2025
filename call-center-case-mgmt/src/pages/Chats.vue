<template>
  <div class="dashboard-layout">
    <div class="sidebar" id="sidebar" :class="{ 'collapsed': isSidebarCollapsed }">
      <div class="sidebar-content">
        <div class="logo-container">
          <div class="logo">
            <img src="../assets/Openchs logo-1.png" alt="OpenCHS Logo">
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

        <router-link to="/cases" class="nav-item">
          <div class="nav-icon"></div>
          <div class="nav-text">Cases</div>
        </router-link>

        <router-link to="/chats" class="nav-item active">
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
            <svg fill="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 12C14.2091 12 16 10.2091 16 8C16 5.79086 14.2091 4 12 4C9.79086 4 8 5.79086 8 8C8 10.2091 9.79086 12 12 12Z"></path>
              <path d="M12 14C7.58172 14 4 17.5817 4 22H20C20 17.5817 16.4183 14 12 14Z"></path>
            </svg>
          </router-link>
        </div>
      </div>
    </div>

    <div class="main-content">
      <div class="chats-page">
        <div class="chat-container">
          <div class="header">
            <button class="sidebar-toggle" @click="toggleSidebar">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M4 6H20M4 12H20M4 18H20" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </button>
            <h1>Survivor Support Chats</h1>
            <button class="theme-toggle" @click="toggleTheme">
              <svg fill="none" height="24" id="moon-icon" viewbox="0 0 24 24" width="24" xmlns="http://www.w3.org/2000/svg">
                <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2">
                </path>
              </svg>
              <svg fill="none" height="24" id="sun-icon" style="display: none;" viewbox="0 0 24 24" width="24" xmlns="http://www.w3.org/2000/svg">
                <circle cx="12" cy="12" r="5" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2">
                </circle>
                <line stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" x1="12" x2="12" y1="1" y2="3">
                </line>
                <line stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" x1="12" x2="12" y1="21" y2="23">
                </line>
                <line stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" x1="4.22" x2="5.64" y1="4.22" y2="5.64">
                </line>
                <line stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" x1="18.36" x2="19.78" y1="18.36" y2="19.78">
                </line>
                <line stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" x1="1" x2="3" y1="12" y2="12">
                </line>
                <line stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" x1="21" x2="23" y1="12" y2="12">
                </line>
                <line stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" x1="4.22" x2="5.64" y1="19.78" y2="18.36">
                </line>
                <line stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" x1="18.36" x2="19.78" y1="5.64" y2="4.22">
                </line>
              </svg>
              <span id="theme-text">{{ themeText }}</span>
            </button>
          </div>

          <div class="chat-content-area">
            <div class="chat-list-panel">
              <div class="chat-tabs">
                <div
                  v-for="platform in platforms"
                  :key="platform.id"
                  :class="['chat-tab', platform.id, { active: activePlatform === platform.id }]"
                  @click="setActivePlatform(platform.id)"
                >
                  {{ platform.name }}
                </div>
              </div>

              <div class="chat-search">
                <input
                  v-model="searchQuery"
                  class="search-input"
                  placeholder="Search chats..."
                  type="text"
                  @input="handleSearch"
                />
              </div>

              <div class="chat-contacts">
                <div
                  v-for="contact in filteredContacts"
                  :key="contact.id"
                  :class="['chat-contact', { active: selectedContactId === contact.id, ended: contact.status === 'ended' }]"
                  @click="selectContact(contact.id)"
                >
                  <div class="contact-avatar">
                    {{ contact.initials }}
                  </div>
                  <div class="contact-info">
                    <div class="contact-name">{{ contact.name }}</div>
                    <div class="contact-preview">{{ contact.preview }}</div>
                  </div>
                  <div class="contact-meta">
                    <div v-if="contact.status === 'active'" class="contact-time">{{ contact.time }}</div>
                    <div v-if="contact.unreadCount && contact.status === 'active'" class="contact-badge">
                      {{ contact.unreadCount }}
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div class="chat-panel" :class="{ active: chatPanelActive }">
              <div class="chat-panel-header">
                <button class="back-to-list" @click="closeChatPanel">←</button>
                <div class="contact-info">
                  <div class="contact-name">{{ selectedContact ? selectedContact.name : '' }}</div>
                  <div class="contact-status">Online</div>
                </div>
                 <div class="contact-avatar">
                  {{ selectedContact ? selectedContact.initials : '' }}
                </div>
                <button class="end-conversation" @click="endConversation">End Conversation</button>
                <button class="close-panel" @click="closeChatPanel">X</button>
              </div>
              <div class="chat-messages">
                <div
                  v-for="message in selectedChatMessages"
                  :key="message.id"
                  :class="['chat-message', message.sender]"
                >
                  <div class="message-bubble">{{ message.text }}</div>
                  <div class="message-time">{{ message.time }}</div>
                </div>
              </div>
              <div class="chat-input-area">
                <input
                  v-model="newMessageText"
                  @keypress.enter="sendMessage"
                  placeholder="Type a message..."
                  type="text"
                  :disabled="activePlatform === 'past'"
                />
                <button
                  @click="sendMessage"
                  :disabled="activePlatform === 'past'"
                >Send</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <button class="mobile-menu-btn" id="mobile-menu-btn" @click="toggleMobileMenu">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M3 12H21M3 6H21M3 18H21" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </button>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router';
import logo from '../assets/Openchs logo-1.png';

const route = useRoute();

const searchQuery = ref('')
const activePlatform = ref('whatsapp')
const selectedContactId = ref(null)
const chatPanelActive = ref(false)
const selectedChatMessages = ref([])
const newMessageText = ref('')

const currentTheme = ref(localStorage.getItem('theme') || 'dark')

const themeText = computed(() => {
  return currentTheme.value === 'dark' ? 'Light Mode' : 'Dark Mode'
})

const platforms = [
  { id: 'whatsapp', name: 'WhatsApp' },
  { id: 'messenger', name: 'Messenger' },
  { id: 'telegram', name: 'Telegram' },
  { id: 'past', name: 'Past Conversations' }
]

const contacts = [
  {
    id: 'sarah-miller',
    name: 'Sarah Miller',
    initials: 'SM',
    preview: 'I need help with a domestic violence situation...',
    time: '10:30 AM',
    unreadCount: 2,
    platform: 'whatsapp',
    status: 'active',
    messages: [
      { id: 1, text: 'Hi, I need some help.', sender: 'user', time: '10:30 AM' },
      { id: 2, text: "Hello Sarah, I'm here to help. Can you tell me more about your situation?", sender: 'agent', time: '10:35 AM' }
    ]
  },
  {
    id: 'john-doe',
    name: 'John Doe',
    initials: 'JD',
    preview: 'Thank you for helping me find shelter yesterday...',
    time: 'Yesterday',
    platform: 'whatsapp',
    status: 'active',
    messages: [
      { id: 1, text: 'Thank you for your help yesterday.', sender: 'user', time: 'Yesterday' },
      { id: 2, text: "You're welcome, John. I'm glad I could assist you.", sender: 'agent', time: 'Yesterday' }
    ]
  },
  {
    id: 'emily-brown',
    name: 'Emily Brown',
    initials: 'EB',
    preview: 'When is my counseling appointment scheduled?',
    time: 'Yesterday',
    platform: 'whatsapp',
    status: 'active',
    messages: [
      { id: 1, text: "When is my counseling appointment?", sender: 'user', time: 'Yesterday' },
      { id: 2, text: "Let me check the schedule for you, Emily.", sender: 'agent', time: 'Yesterday' }
    ]
  },
  {
    id: 'michael-johnson',
    name: 'Michael Johnson',
    initials: 'MJ',
    preview: 'I need to reschedule my safety planning session...',
    time: 'Mon',
    platform: 'whatsapp',
    status: 'active',
    messages: [
      { id: 1, text: 'Hi, I need to reschedule my session.', sender: 'user', time: 'Mon' },
      { id: 2, text: "Okay, Michael. What time would work best for you?", sender: 'agent', time: 'Mon' }
    ]
  },
  {
    id: 'lisa-wilson',
    name: 'Lisa Wilson',
    initials: 'LW',
    preview: 'Is there any update on my restraining order?',
    time: 'Sun',
    unreadCount: 1,
    platform: 'whatsapp',
    status: 'active',
    messages: [
      { id: 1, text: "Any updates on the restraining order?", sender: 'user', time: 'Sun' },
      { id: 2, text: "I will check the status for you, Lisa.", sender: 'agent', time: 'Sun' }
    ]
  }
]

const pastConversations = ref([])

const filteredContacts = computed(() => {
  let filtered = contacts.filter(contact => {
    if (activePlatform.value === 'past') {
      return contact.status === 'ended';
    } else {
      return contact.platform === activePlatform.value && contact.status === 'active';
    }
  });

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
  return contacts.find(contact => contact.id === selectedContactId.value)
})

const setActivePlatform = (platformId) => {
  activePlatform.value = platformId
  selectedContactId.value = null
  chatPanelActive.value = false
  searchQuery.value = ''
}

const selectContact = (contactId) => {
  selectedContactId.value = contactId
  const contact = contacts.find(c => c.id === contactId)
  if (contact) {
    selectedChatMessages.value = contact.messages || []
    chatPanelActive.value = true // Activate chat panel when contact is selected
  } else {
    selectedChatMessages.value = []
    chatPanelActive.value = false // Deactivate if contact not found
  }
}

const closeChatPanel = () => {
  chatPanelActive.value = false;
  selectedContactId.value = null; // Also reset selected contact
}

const sendMessage = () => {
  if (newMessageText.value.trim() !== '' && selectedContactId.value !== null) {
    const newMessage = {
      id: selectedChatMessages.value.length + 1,
      text: newMessageText.value,
      sender: 'agent',
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    }
    selectedChatMessages.value.push(newMessage)
    newMessageText.value = ''
  }
}

const endConversation = () => {
  if (selectedContactId.value !== null) {
    const isConfirmed = confirm('Are you sure you want to end this conversation?')
    if (isConfirmed) {
      const contact = contacts.find(contact => contact.id === selectedContactId.value);
      if (contact) {
        contact.status = 'ended';
        closeChatPanel();
      } else {
        console.warn('Contact not found when attempting to end conversation.');
      }
    }
  }
}

const handleSearch = () => {
  console.log('Searching for:', searchQuery.value)
}

const toggleTheme = () => {
  currentTheme.value = currentTheme.value === 'dark' ? 'light' : 'dark'
  localStorage.setItem('theme', currentTheme.value)
  document.documentElement.setAttribute('data-theme', currentTheme.value)
  
  const moonIcon = document.getElementById('moon-icon')
  const sunIcon = document.getElementById('sun-icon')
  
  if (currentTheme.value === 'light') {
    moonIcon.style.display = 'none'
    sunIcon.style.display = 'block'
  } else {
    moonIcon.style.display = 'block'
    sunIcon.style.display = 'none'
  }
}

const isSidebarCollapsed = ref(false);

const toggleSidebar = () => {
  isSidebarCollapsed.value = !isSidebarCollapsed.value;
};

const currentRoute = computed(() => route.path);

const selectedContactDetails = computed(() => {
  const contact = contacts.find(c => c.id === selectedContactId.value)
  return contact || null
})

const mainContentMarginLeft = computed(() => {
  if (window.innerWidth <= 768) {
    return '0px';
  } else if (isSidebarCollapsed.value) {
    return '80px'; // Collapsed sidebar width
  } else {
    return '250px'; // Full sidebar width
  }
});
</script>

<style scoped>
.dashboard-layout {
  display: flex;
  width: 100%;
  height: 100vh;
  background-color: var(--background-color);
  overflow: hidden;
}

.mobile-menu-btn {
  display: none;
  position: fixed;
  top: 10px;
  left: 10px;
  background-color: var(--content-bg);
  color: var(--text-color);
  border: 1px solid var(--border-color);
  border-radius: 50%;
  padding: 10px;
  cursor: pointer;
  z-index: 1000;
}

.sidebar {
  width: 250px;
  flex-shrink: 0;
  background-color: var(--sidebar-bg);
  color: var(--text-color);
  transition: width 0.3s ease, transform 0.3s ease;
  overflow-x: hidden;
  border-radius: 0 30px 30px 0;
  z-index: 100;
  height: 100%;
  display: flex;
  flex-direction: column;
  position: relative;
}

.sidebar.collapsed {
  width: 80px;
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
  flex-shrink: 0;
}

.nav-text {
  font-size: 14px;
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.sidebar.collapsed .nav-text {
  display: none;
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

.main-content {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  transition: margin-left 0.3s ease;
  display: flex;
  flex-direction: column;
}

.sidebar.collapsed + .main-content {
  margin-left: 80px;
}

.chats-page {
  padding: 0;
  display: flex;
  flex-direction: column;
  height: 100%;
  flex-grow: 1;
}

.chat-container {
  background-color: var(--card-bg);
  border-radius: 30px;
  padding: 20px;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.header {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
  gap: 20px;
}

.header h1 {
  font-size: 24px;
  font-weight: 600;
  margin: 0 auto 0 0;
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
}

.chat-content-area {
  display: flex;
  flex-direction: row;
  flex-grow: 1;
  height: 100%;
}

.chat-list-panel {
  width: 350px;
  flex-shrink: 0;
  border-right: 1px solid var(--border-color);
  overflow-y: auto;
  box-sizing: border-box;
  min-width: 0;
  transition: width 0.3s ease;
}

.chat-tabs {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.chat-tab {
  padding: 8px 16px;
  border-radius: 20px;
  background-color: var(--content-bg);
  color: var(--text-color);
  border: 1px solid var(--border-color);
  cursor: pointer;
  font-size: 14px;
  flex-shrink: 0;
}

.chat-tab.active {
  background-color: var(--accent-color);
  color: white;
  border-color: var(--accent-color);
}

.chat-tab.past {
  /* Specific styles for past conversations tab if needed */
}

.chat-search {
  margin-bottom: 20px;
}

.search-input {
  width: 100%;
  padding: 10px;
  border: 1px solid var(--border-color);
  border-radius: 20px;
  background-color: var(--content-bg);
  color: var(--text-color);
  font-size: 14px;
  outline: none;
}

.search-input::placeholder {
  color: var(--text-secondary);
}

.chat-contacts {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.chat-contact {
  display: flex;
  align-items: center;
  padding: 10px;
  border-radius: 10px;
  cursor: pointer;
  background-color: var(--background-color);
  transition: background-color 0.2s;
}

.chat-contact:hover {
  background-color: rgba(255, 255, 255, 0.05);
}

.chat-contact.active {
    background-color: rgba(255, 59, 48, 0.1);
}

.chat-contact.ended {
  opacity: 0.6;
}

.contact-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: var(--accent-color);
  color: white;
  display: flex;
  justify-content: center;
  align-items: center;
  font-weight: bold;
  font-size: 16px;
  margin-right: 15px;
  flex-shrink: 0;
}

.contact-info {
  flex: 1;
  min-width: 0;
}

.contact-name {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 3px;
  color: var(--text-color);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.contact-preview {
  font-size: 12px;
  color: var(--text-secondary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.contact-meta {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 5px;
  flex-shrink: 0;
  margin-left: 10px;
}

.contact-time {
  font-size: 10px;
  color: var(--text-secondary);
}

.contact-badge {
  background-color: var(--highlight-color);
  color: white;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 10px;
  font-weight: bold;
  flex-shrink: 0;
}

.chat-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
  box-shadow: none;
  border-left: none;
  padding-left: 20px;
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.chat-panel.active {
  display: flex;
  opacity: 1;
  transform: translateX(0);
}

.chat-panel:not(.active) {
  display: none;
}

.chat-panel-header {
  display: flex;
  align-items: center;
  padding: 15px 20px;
  background-color: var(--header-bg);
  border-bottom: 1px solid var(--border-color);
  flex-shrink: 0;
  z-index: 1;
}

.back-to-list {
  background: none;
  border: none;
  color: var(--text-color);
  font-size: 24px;
  cursor: pointer;
  margin-right: 15px;
  padding: 5px;
}

.chat-panel-header .contact-info {
    flex: 1;
    margin-right: 10px;
}

.chat-panel-header .contact-info .contact-name {
    font-size: 16px;
    font-weight: 600;
    color: var(--text-color);
}

.chat-panel-header .contact-status {
    font-size: 12px;
    color: var(--text-secondary);
}

.chat-panel-header .contact-avatar {
    width: 30px;
    height: 30px;
    font-size: 14px;
    margin-left: 0;
    margin-right: 10px;
    flex-shrink: 0;
}

.chat-messages {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.chat-message {
  display: flex;
  flex-direction: column;
  max-width: 80%;
}

.chat-message.user {
  align-self: flex-start;
}

.chat-message.agent {
  align-self: flex-end;
}

.message-bubble {
  padding: 10px 15px;
  border-radius: 15px;
  font-size: 14px;
  color: var(--text-color);
}

.chat-message.user .message-bubble {
  background-color: var(--background-color);
  border-bottom-left-radius: 5px;
}

.chat-message.agent .message-bubble {
  background-color: var(--accent-color);
  color: white;
  border-bottom-right-radius: 5px;
}

.message-time {
  font-size: 10px;
  color: var(--text-secondary);
  margin-top: 2px;
  align-self: flex-end;
}

.chat-input-area {
  display: flex;
  padding: 15px 20px;
  border-top: 1px solid var(--border-color);
  background-color: var(--header-bg);
  flex-shrink: 0;
  gap: 10px;
}

.chat-input-area input {
  flex: 1;
  padding: 10px 15px;
  border-radius: 20px;
  border: 1px solid var(--border-color);
  background-color: var(--background-color);
  color: var(--text-color);
  font-size: 14px;
  outline: none;
}

.chat-input-area input::placeholder {
  color: var(--text-secondary);
}

.chat-input-area button {
  padding: 10px 20px;
  border-radius: 20px;
  background-color: var(--accent-color);
  color: white;
  border: none;
  cursor: pointer;
  font-size: 14px;
}

.chat-input-area button:hover {
  background-color: var(--accent-hover);
}

.end-conversation {
  background-color: var(--background-color);
  color: var(--text-color);
  border: 1px solid var(--border-color);
  border-radius: 20px;
  padding: 5px 15px;
  font-size: 12px;
  cursor: pointer;
  margin-left: auto;
}

.end-conversation:hover {
  background-color: rgba(255, 59, 48, 0.2);
  color: var(--accent-color);
  border-color: var(--accent-color);
}

.close-panel {
  background: none;
  border: none;
  color: var(--text-color);
  font-size: 20px;
  cursor: pointer;
  padding: 5px;
  margin-left: 10px;
}

.close-panel:hover {
  color: var(--accent-color);
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
    margin-left: 0;
    display: flex;
    flex-direction: column;
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

  .chat-content-area {
    flex-direction: column;
    height: calc(100vh - 100px);
    flex-grow: 0;
  }

  .chat-list-panel {
    width: 100%;
    border-right: none;
    border-bottom: 1px solid var(--border-color);
    height: 50%;
    flex-shrink: 1;
  }

  .chat-panel {
    flex: 1;
    width: 100%;
    position: fixed;
    top: 0;
    left: 0;
    height: 100vh;
    z-index: 1000;
    background-color: var(--content-bg);
    transform: translateX(100%);
    transition: transform 0.3s ease;
    padding-left: 0;
  }

  .chat-panel.active {
    transform: translateX(0);
  }

  .chat-panel-header .back-to-list {
    display: block;
    padding: 10px;
    margin-right: 10px;
  }

  .chat-panel-header .end-conversation {
    margin-left: auto;
  }

  .chat-panel-header .close-panel {
    display: none;
  }

  .sidebar.mobile-open + .main-content {
      transform: translateX(250px);
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
    display: flex;
    flex-direction: column;
  }

  .sidebar-toggle {
    display: flex;
  }

  .chat-content-area {
    flex-direction: row;
    position: relative;
    flex-grow: 1;
    height: auto;
  }

  .chat-list-panel {
    width: 350px;
    flex: none;
    border-right: 1px solid var(--border-color);
    overflow-y: auto;
    box-sizing: border-box;
    min-width: 0;
  }

  .chat-panel {
    flex: 1;
    display: flex;
    flex-direction: column;
    min-width: 0;
    position: static;
    width: auto;
    box-shadow: none;
    border-left: none;
    padding-left: 20px;
  }

  .chat-panel.active {
    display: flex;
  }

  .chat-panel:not(.active) {
    display: none;
  }
}

.end-conversation {
  background-color: var(--background-color);
  color: var(--text-color);
  border: 1px solid var(--border-color);
  border-radius: 20px;
  padding: 5px 15px;
  font-size: 12px;
  cursor: pointer;
  margin-left: 10px;
}

.end-conversation:hover {
  background-color: rgba(255, 59, 48, 0.2);
  color: var(--accent-color);
  border-color: var(--accent-color);
}

.close-panel {
  background: none;
  border: none;
  color: var(--text-color);
  font-size: 20px;
  cursor: pointer;
  padding: 5px;
  margin-left: 10px;
}

.close-panel:hover {
  color: var(--accent-color);
}

.chat-tabs .chat-tab.past.active ~ .chat-content-area .chat-list-panel {
  flex: 1;
}

.chat-tabs .chat-tab.past.active ~ .chat-content-area .chat-panel {
  display: none;
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

@media (max-width: 768px) {
  .sidebar-toggle {
    display: flex;
  }
}

@media (min-width: 769px) {
  .sidebar-toggle {
    display: flex;
  }
}

.chat-tabs .chat-tab.past.active ~ .chat-content-area .chat-list-panel {
  flex: 1;
}

.chat-tabs .chat-tab.past.active ~ .chat-content-area .chat-panel {
  display: none;
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

@media (max-width: 768px) {
  .sidebar-toggle {
    display: flex;
  }
}

@media (min-width: 769px) {
  .sidebar-toggle {
    display: flex;
  }
}

/* Additional styles for mobile sidebar positioning */
@media (max-width: 768px) {
    .main-content {
        margin-left: 0;
    }

    .sidebar.mobile-open + .main-content {
        transform: translateX(250px);
    }
}

/* Add style to expand chat-list-panel when chat-panel is not active */
.chat-content-area:has(.chat-panel:not(.active)) .chat-list-panel {
    width: 100%;
}
</style>
