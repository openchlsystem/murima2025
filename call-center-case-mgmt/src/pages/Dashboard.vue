<template>
  <div>
    <!-- SidePanel Component -->
    <SidePanel 
      :userRole="userRole" 
      :serverConnected="serverConnected"
      :isExtensionRegistered="isExtensionRegistered"
      :isConnectingToExtension="isConnectingToExtension"
      :serverConnectionError="serverConnectionError"
      :extensionError="extensionError"
      :currentCall="currentCall" 
      @start-calls="handleStartCalls" 
      @retry-server-connection="handleRetryServerConnection"
      @logout="handleLogout"
      @sidebar-toggle="handleSidebarToggle" 
    />

    <!-- Add router-view -->
    <router-view></router-view>

    <!-- Main Content -->
    <div class="main-content">
      <div class="header">
        <h1 class="page-title">Dashboard</h1>
        <button class="theme-toggle" @click="toggleTheme" id="theme-toggle">
          <svg v-if="currentTheme === 'dark'" id="moon-icon" width="24" height="24" viewBox="0 0 24 24" fill="none"
            xmlns="http://www.w3.org/2000/svg">
            <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" stroke="currentColor" stroke-width="2"
              stroke-linecap="round" stroke-linejoin="round" />
          </svg>
          <svg v-else id="sun-icon" width="24" height="24" viewBox="0 0 24 24" fill="none"
            xmlns="http://www.w3.org/2000/svg">
            <circle cx="12" cy="12" r="5" stroke="currentColor" stroke-width="2" stroke-linecap="round"
              stroke-linejoin="round" />
            <line x1="12" y1="1" x2="12" y2="3" stroke="currentColor" stroke-width="2" stroke-linecap="round"
              stroke-linejoin="round" />
            <line x1="12" y1="21" x2="12" y2="23" stroke="currentColor" stroke-width="2" stroke-linecap="round"
              stroke-linejoin="round" />
            <line x1="4.22" y1="4.22" x2="5.64" y2="5.64" stroke="currentColor" stroke-width="2" stroke-linecap="round"
              stroke-linejoin="round" />
            <line x1="18.36" y1="18.36" x2="19.78" y2="19.78" stroke="currentColor" stroke-width="2"
              stroke-linecap="round" stroke-linejoin="round" />
            <line x1="1" y1="12" x2="3" y2="12" stroke="currentColor" stroke-width="2" stroke-linecap="round"
              stroke-linejoin="round" />
            <line x1="21" y1="12" x2="23" y2="12" stroke="currentColor" stroke-width="2" stroke-linecap="round"
              stroke-linejoin="round" />
            <line x1="4.22" y1="19.78" x2="5.64" y2="18.36" stroke="currentColor" stroke-width="2"
              stroke-linecap="round" stroke-linejoin="round" />
            <line x1="18.36" y1="5.64" x2="19.78" y2="4.22" stroke="currentColor" stroke-width="2"
              stroke-linecap="round" stroke-linejoin="round" />
          </svg>
          <span id="theme-text">{{ currentTheme === 'dark' ? 'Light Mode' : 'Dark Mode' }}</span>
        </button>
      </div>

      <div class="main-scroll-content">
        <!-- Call Status Card -->
        <div class="call-status-container" :class="{ 'active-call': activeCall }">
          <div class="call-status-card">
            <div class="call-status-header">
              <div class="call-status-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path
                    d="M22 16.92V19C22 20.1046 21.1046 21 20 21C10.6112 21 3 13.3888 3 4C3 2.89543 3.89543 2 5 2H7.08C7.55607 2 7.95823 2.33718 8.02513 2.80754L8.7 7.5C8.76694 7.97036 8.53677 8.42989 8.12 8.67L6.5 9.5C7.84 12.16 11.84 16.16 14.5 17.5L15.33 15.88C15.5701 15.4632 16.0296 15.2331 16.5 15.3L21.1925 16.0249C21.6628 16.0918 22 16.4939 22 16.97V16.92Z"
                    stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                </svg>
              </div>
              <div class="call-status-title">
                {{ callStatusText }}
              </div>
            </div>

            <!-- Incoming Call UI -->
            <div v-if="incomingCall" class="incoming-call-controls">
              <div class="caller-info">
                <div class="caller-name">{{ incomingCall.callerName || 'Unknown Caller' }}</div>
                <div class="caller-number">{{ incomingCall.callerId || 'Private Number' }}</div>
              </div>
              <div class="call-buttons">
                <button class="answer-btn" @click="answerIncomingCall">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path
                      d="M22 16.92V19C22 20.1046 21.1046 21 20 21C10.6112 21 3 13.3888 3 4C3 2.89543 3.89543 2 5 2H7.08C7.55607 2 7.95823 2.33718 8.02513 2.80754L8.7 7.5C8.76694 7.97036 8.53677 8.42989 8.12 8.67L6.5 9.5C7.84 12.16 11.84 16.16 14.5 17.5L15.33 15.88C15.5701 15.4632 16.0296 15.2331 16.5 15.3L21.1925 16.0249C21.6628 16.0918 22 16.4939 22 16.97V16.92Z"
                      stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                  </svg>
                  Answer
                </button>
                <button class="reject-btn" @click="rejectIncomingCall">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                      stroke-linejoin="round" />
                  </svg>
                  Reject
                </button>
              </div>
            </div>

            <!-- Active Call UI -->
            <div v-if="activeCall" class="active-call-controls">
              <div class="call-info">
                <div class="call-duration">{{ callDuration }}</div>
                <div class="caller-info">
                  <div class="caller-name">{{ activeCall.callerName || 'Unknown Caller' }}</div>
                  <div class="caller-number">{{ activeCall.callerId || 'Private Number' }}</div>
                </div>
              </div>
              <div class="call-actions">
                <button class="mute-btn" @click="toggleMute" :class="{ active: isMuted }">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path
                      d="M12 1C13.1046 1 14 1.89543 14 3V8C14 9.10457 13.1046 10 12 10H10C8.89543 10 8 9.10457 8 8V3C8 1.89543 8.89543 1 10 1H12Z"
                      stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                    <path d="M6 8H4C2.89543 8 2 8.89543 2 10V14C2 15.1046 2.89543 16 4 16H6L10 20V4L6 8Z"
                      stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                    <path v-if="isMuted" d="M16 10L22 4M22 10L16 4" stroke="currentColor" stroke-width="2"
                      stroke-linecap="round" stroke-linejoin="round" />
                  </svg>
                </button>
                <button class="transfer-btn" @click="showTransferDialog">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M17 2L22 7L17 12M7 12L2 7L7 2" stroke="currentColor" stroke-width="2"
                      stroke-linecap="round" stroke-linejoin="round" />
                    <path
                      d="M22 7H9C7.89543 7 7 7.89543 7 9V15C7 16.1046 7.89543 17 9 17H15C16.1046 17 17 16.1046 17 15V9"
                      stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                  </svg>
                </button>
                <button class="hangup-btn" @click="endCall">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path
                      d="M22 16.92V19C22 20.1046 21.1046 21 20 21C10.6112 21 3 13.3888 3 4C3 2.89543 3.89543 2 5 2H7.08C7.55607 2 7.95823 2.33718 8.02513 2.80754L8.7 7.5C8.76694 7.97036 8.53677 8.42989 8.12 8.67L6.5 9.5C7.84 12.16 11.84 16.16 14.5 17.5L15.33 15.88C15.5701 15.4632 16.0296 15.2331 16.5 15.3L21.1925 16.0249C21.6628 16.0918 22 16.4939 22 16.97V16.92Z"
                      stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                    <path d="M17 7L7 17M7 7L17 17" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                      stroke-linejoin="round" />
                  </svg>
                </button>
              </div>
            </div>

            <!-- Extension Status -->
            <div v-if="!activeCall && !incomingCall" class="extension-status">
              <div class="extension-state">
                {{ extensionStatusText }}
              </div>
            </div>
          </div>
        </div>

        <!-- Dashboard Grid -->
        <div class="dashboard-grid">
          <div class="dashboard-card">
            <div class="card-header">
              <div class="card-title">Total Calls</div>
              <div class="card-icon">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path
                    d="M22 16.92V19C22 20.1046 21.1046 21 20 21C10.6112 21 3 13.3888 3 4C3 2.89543 3.89543 2 5 2H7.08C7.55607 2 7.95823 2.33718 8.02513 2.80754L8.7 7.5C8.76694 7.97036 8.53677 8.42989 8.12 8.67L6.5 9.5C7.84 12.16 11.84 16.16 14.5 17.5L15.33 15.88C15.5701 15.4632 16.0296 15.2331 16.5 15.3L21.1925 16.0249C21.6628 16.0918 22 16.4939 22 16.97V16.92Z"
                    stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                </svg>
              </div>
            </div>
            <div class="card-value">53</div>
            <div class="card-subtitle">+12% from last week</div>
          </div>

          <div class="dashboard-card">
            <div class="card-header">
              <div class="card-title">Active Cases</div>
              <div class="card-icon">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M22 12h-4l-3 9L9 3l-3 9H2" stroke="white" stroke-width="2" stroke-linecap="round"
                    stroke-linejoin="round" />
                </svg>
              </div>
            </div>
            <div class="card-value">24</div>
            <div class="card-subtitle">+5% from last week</div>
          </div>

          <div class="dashboard-card">
            <div class="card-header">
              <div class="card-title">Pending Calls</div>
              <div class="card-icon">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <circle cx="12" cy="12" r="10" stroke="white" stroke-width="2" stroke-linecap="round"
                    stroke-linejoin="round" />
                  <path d="M12 6v6l4 2" stroke="white" stroke-width="2" stroke-linecap="round"
                    stroke-linejoin="round" />
                </svg>
              </div>
            </div>
            <div class="card-value">5</div>
            <div class="card-subtitle">-2% from last week</div>
          </div>

          <div class="dashboard-card">
            <div class="card-header">
              <div class="card-title">Completed Calls</div>
              <div class="card-icon">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M22 11.08V12a10 10 0 11-5.93-9.14" stroke="white" stroke-width="2" stroke-linecap="round"
                    stroke-linejoin="round" />
                  <path d="M22 4L12 14.01l-3-3" stroke="white" stroke-width="2" stroke-linecap="round"
                    stroke-linejoin="round" />
                </svg>
              </div>
            </div>
            <div class="card-value">42</div>
            <div class="card-subtitle">+8% from last week</div>
          </div>

          <!-- New Prank Calls Card -->
          <div class="dashboard-card">
            <div class="card-header">
              <div class="card-title">Prank Calls</div>
              <div class="card-icon prank-calls">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M12 2L13.09 8.26L22 9L13.09 9.74L12 16L10.91 9.74L2 9L10.91 8.26L12 2Z" stroke="white"
                    stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                  <path d="M8 21L9 19L11 20L9 21L8 21Z" stroke="white" stroke-width="2" stroke-linecap="round"
                    stroke-linejoin="round" />
                  <path d="M19 21L20 19L22 20L20 21L19 21Z" stroke="white" stroke-width="2" stroke-linecap="round"
                    stroke-linejoin="round" />
                </svg>
              </div>
            </div>
            <div class="card-value">7</div>
            <div class="card-subtitle">-15% from last week</div>
          </div>

          <!-- New Counsellors Online Card -->
          <div class="dashboard-card">
            <div class="card-header">
              <div class="card-title">Counsellors Online</div>
              <div class="card-icon counsellors-online">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path
                    d="M17 21V19C17 17.9391 16.5786 16.9217 15.8284 16.1716C15.0783 15.4214 14.0609 15 13 15H5C3.93913 15 2.92172 15.4214 2.17157 16.1716C1.42143 16.9217 1 17.9391 1 19V21"
                    stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                  <circle cx="9" cy="7" r="4" stroke="white" stroke-width="2" stroke-linecap="round"
                    stroke-linejoin="round" />
                  <path
                    d="M23 21V19C23 18.1645 22.7155 17.3541 22.2094 16.6977C21.7033 16.0414 20.9999 15.5735 20.2 15.3613"
                    stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                  <path
                    d="M16 3.13C16.8003 3.3422 17.5037 3.81014 18.0098 4.46645C18.5159 5.12277 18.8004 5.93317 18.8004 6.76875C18.8004 7.60433 18.5159 8.41473 18.0098 9.07105C17.5037 9.72736 16.8003 10.1953 16 10.4075"
                    stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                </svg>
              </div>
            </div>
            <div class="card-value">12</div>
            <div class="card-subtitle">Currently available</div>
          </div>
        </div>

        <!-- Agent Activity (renamed from Queue Activity) -->
        <div class="agent-activity">
          <div class="section-header">
            <div class="section-title">Agent Activity</div>
          </div>

          <table class="agent-table">
            <thead>
              <tr>
                <th>Agent Name</th>
                <th>Current Status</th>
                <th>Calls Handled</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="agent in agentList" :key="agent.name">
                <td>{{ agent.name }}</td>
                <td><span class="agent-status" :class="agent.statusClass">{{ agent.status }}</span></td>
                <td>{{ agent.calls }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Recent Calls -->
        <div class="recent-calls">
          <div class="section-header">
            <div class="section-title">Recent Calls</div>
            <button class="view-all" @click="navigateToCalls">View All</button>
          </div>

          <div class="call-list">
            <div v-for="call in recentCalls" :key="call.id" class="call-item">
              <div class="call-icon">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path
                    d="M22 16.92V19C22 20.1046 21.1046 21 20 21C10.6112 21 3 13.3888 3 4C3 2.89543 3.89543 2 5 2H7.08C7.55607 2 7.95823 2.33718 8.02513 2.80754L8.7 7.5C8.76694 7.97036 8.53677 8.42989 8.12 8.67L6.5 9.5C7.84 12.16 11.84 16.16 14.5 17.5L15.33 15.88C15.5701 15.4632 16.0296 15.2331 16.5 15.3L21.1925 16.0249C21.6628 16.0918 22 16.4939 22 16.97V16.92Z"
                    stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                </svg>
              </div>
              <div class="call-details">
                <div class="call-type">{{ call.type }}</div>
                <div class="call-time">{{ call.time }}</div>
              </div>
              <div class="call-status" :class="call.statusClass">{{ call.status }}</div>
            </div>
          </div>
        </div>

        <!-- Enhanced Chart Container -->
        <div class="chart-container">
          <div class="chart-card">
            <div class="chart-header">
              <div class="section-title">Call Volume Trends</div>
              <div class="chart-controls">
                <button v-for="period in chartPeriods" :key="period.value" class="chart-period-btn"
                  :class="{ active: selectedPeriod === period.value }" @click="changePeriod(period.value)">
                  {{ period.label }}
                </button>
              </div>
            </div>
            <div class="chart-stats">
              <div class="chart-stat">
                <div class="stat-label">Total Calls</div>
                <div class="stat-value">{{ totalCalls }}</div>
                <div class="stat-change" :class="{ positive: callsChange > 0, negative: callsChange < 0 }">
                  <svg v-if="callsChange > 0" width="12" height="12" viewBox="0 0 24 24" fill="none"
                    xmlns="http://www.w3.org/2000/svg">
                    <path d="M7 14L12 9L17 14" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                      stroke-linejoin="round" />
                  </svg>
                  <svg v-else width="12" height="12" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M7 10L12 15L17 10" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                      stroke-linejoin="round" />
                  </svg>
                  {{ Math.abs(callsChange) }}%
                </div>
              </div>
              <div class="chart-stat">
                <div class="stat-label">Peak Hour</div>
                <div class="stat-value">{{ peakHour }}</div>
                <div class="stat-description">{{ peakCalls }} calls</div>
              </div>
              <div class="chart-stat">
                <div class="stat-label">Average Response</div>
                <div class="stat-value">{{ avgResponse }}</div>
                <div class="stat-description">Response time</div>
              </div>
            </div>
            <div class="chart-placeholder">
              <div class="enhanced-chart">
                <!-- Y-axis labels -->
                <div class="y-axis-labels">
                  <div v-for="(label, index) in yAxisLabels" :key="index" class="y-label"
                    :style="{ bottom: (index * 25) + '%' }">
                    {{ label }}
                  </div>
                </div>

                <!-- Chart grid -->
                <div class="chart-grid">
                  <div v-for="i in 5" :key="i" class="grid-line-horizontal" :style="{ bottom: ((i - 1) * 25) + '%' }">
                  </div>
                  <div v-for="i in chartData.length" :key="i" class="grid-line-vertical"
                    :style="{ left: ((i - 1) * (100 / (chartData.length - 1))) + '%' }"></div>
                </div>

                <!-- Chart area -->
                <div class="chart-area">
                  <!-- Area fill -->
                  <svg class="chart-svg" viewBox="0 0 100 100" preserveAspectRatio="none">
                    <defs>
                      <linearGradient id="chartGradient" x1="0%" y1="0%" x2="0%" y2="100%">
                        <stop offset="0%" :style="{ stopColor: 'var(--accent-color)', stopOpacity: 0.3 }" />
                        <stop offset="100%" :style="{ stopColor: 'var(--accent-color)', stopOpacity: 0.05 }" />
                      </linearGradient>
                    </defs>
                    <path :d="areaPath" fill="url(#chartGradient)" />
                    <path :d="linePath" stroke="var(--accent-color)" stroke-width="0.5" fill="none" />
                  </svg>

                  <!-- Data points -->
                  <div v-for="(point, index) in chartData" :key="index" class="chart-point" :style="{
                    left: (index * (100 / (chartData.length - 1))) + '%',
                    bottom: point.percentage + '%'
                  }" @mouseenter="showTooltip(point, $event)" @mouseleave="hideTooltip">
                    <div class="point-dot"></div>
                  </div>
                </div>

                <!-- X-axis labels -->
                <div class="x-axis-labels">
                  <div v-for="(point, index) in chartData" :key="index" class="x-label"
                    :style="{ left: (index * (100 / (chartData.length - 1))) + '%' }">
                    {{ point.label }}
                  </div>
                </div>
              </div>
            </div>

            <!-- Tooltip -->
            <div v-if="tooltip.show" class="chart-tooltip" :style="{ left: tooltip.x + 'px', top: tooltip.y + 'px' }">
              <div class="tooltip-title">{{ tooltip.data.label }}</div>
              <div class="tooltip-value">{{ tooltip.data.value }} calls</div>
              <div class="tooltip-time">{{ tooltip.data.time }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Transfer Dialog -->
    <teleport to="body">
      <div v-if="transferDialog" class="transfer-dialog">
        <div class="transfer-dialog-content">
          <h3 class="transfer-dialog-title">Transfer Call</h3>
          <input v-model="transferTarget" class="transfer-input" placeholder="Enter extension number"
            @keyup.enter="transferCallToTarget">
          <div class="transfer-dialog-buttons">
            <button class="transfer-cancel-btn" @click="transferDialog = false">
              Cancel
            </button>
            <button class="transfer-confirm-btn" @click="transferCallToTarget">
              Transfer
            </button>
          </div>
        </div>
      </div>
    </teleport>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import SidePanel from '@/components/SidePanel.vue'
import {
  testServerConnection,
  initSIP,
  registerExtension,
  unregisterExtension,
  answerCall,
  rejectCall,
  hangupCall,
  muteCall,
  transferCall,
  sendDTMF,
  on,
  off,
  cleanup,
  getCallStatus,
  getRegistrationStatus
} from '@/utils/sipClient.js'

// Router setup
const route = useRoute()
const router = useRouter()

// Theme and UI state
const currentTheme = ref('dark')
const userRole = ref('super-admin')

// Server connection state
const serverStatus = ref({
  isTestingConnection: false,
  isServerAccessible: false,
  connectionError: null
})

// Extension registration state
const extensionStatus = ref({
  isRegistered: false,
  isConnecting: false,
  error: null
})

// Call state
const callState = ref({
  incoming: null,
  active: null,
  isMuted: false,
  duration: '00:00:00',
  transferDialog: false,
  transferTarget: ''
})

// Dashboard data
const agentList = ref([
  { name: 'Sarah Davis', status: 'Ready for Calls', statusClass: 'status-available', calls: 34 },
  { name: 'Mark Reynolds', status: 'In Call', statusClass: 'status-in-call', calls: 28 },
  { name: 'Emily Chan', status: 'On Break', statusClass: 'status-on-break', calls: 15 },
  { name: 'David Lee', status: 'Ready for Calls', statusClass: 'status-available', calls: 42 },
  { name: 'Sophia Clark', status: 'In Call', statusClass: 'status-in-call', calls: 30 }
])

const recentCalls = ref([
  {
    id: 1,
    type: 'Emergency Crisis: Domestic Violence',
    time: 'Today, 09:00AM',
    status: 'In Progress',
    statusClass: 'status-in-progress'
  },
  {
    id: 2,
    type: 'Survivor Follow-Up: Safety Planning',
    time: 'Today, 10:30AM',
    status: 'Pending',
    statusClass: 'status-pending'
  },
  {
    id: 3,
    type: 'Wellness Check-In: Mental Health Support',
    time: 'Yesterday, 11:15AM',
    status: 'Completed',
    statusClass: 'status-completed'
  },
  {
    id: 4,
    type: 'Resource Request: Shelter Information',
    time: 'Today, 04:45PM',
    status: 'Unassigned',
    statusClass: 'status-unassigned'
  }
])

// Chart state
const selectedPeriod = ref('7d')
const tooltip = ref({
  show: false,
  x: 0,
  y: 0,
  data: {}
})

const chartPeriods = ref([
  { label: '7D', value: '7d' },
  { label: '30D', value: '30d' },
  { label: '3M', value: '3m' },
  { label: '1Y', value: '1y' }
])

const chartDataSets = ref({
  '7d': [
    { label: 'Mon', value: 15, time: '9:00 AM - 5:00 PM' },
    { label: 'Tue', value: 23, time: '9:00 AM - 5:00 PM' },
    { label: 'Wed', value: 31, time: '9:00 AM - 5:00 PM' },
    { label: 'Thu', value: 38, time: '9:00 AM - 5:00 PM' },
    { label: 'Fri', value: 25, time: '9:00 AM - 5:00 PM' },
    { label: 'Sat', value: 18, time: '10:00 AM - 4:00 PM' },
    { label: 'Sun', value: 12, time: '12:00 PM - 4:00 PM' }
  ],
  '30d': [
    { label: 'Week 1', value: 142, time: 'Jan 1-7' },
    { label: 'Week 2', value: 168, time: 'Jan 8-14' },
    { label: 'Week 3', value: 195, time: 'Jan 15-21' },
    { label: 'Week 4', value: 178, time: 'Jan 22-28' }
  ],
  '3m': [
    { label: 'Jan', value: 683, time: 'January 2024' },
    { label: 'Feb', value: 721, time: 'February 2024' },
    { label: 'Mar', value: 658, time: 'March 2024' }
  ],
  '1y': [
    { label: 'Q1', value: 2062, time: 'Jan-Mar 2024' },
    { label: 'Q2', value: 2341, time: 'Apr-Jun 2024' },
    { label: 'Q3', value: 2198, time: 'Jul-Sep 2024' },
    { label: 'Q4', value: 2456, time: 'Oct-Dec 2024' }
  ]
})

// Call timer
let callTimer = null
let callStartTime = null

// Computed properties for SidePanel
const serverConnected = computed(() => serverStatus.value.isServerAccessible)
const isExtensionRegistered = computed(() => extensionStatus.value.isRegistered)
const isConnectingToExtension = computed(() => extensionStatus.value.isConnecting)
const serverConnectionError = computed(() => serverStatus.value.connectionError)
const extensionError = computed(() => extensionStatus.value.error)
const currentCall = computed(() => callState.value.active || callState.value.incoming)

// Computed properties for call status
const callStatusText = computed(() => {
  if (callState.value.incoming) return 'Incoming Call'
  if (callState.value.active) return 'Active Call'
  if (!serverConnected.value) return 'Server Disconnected'
  if (isConnectingToExtension.value) return 'Connecting...'
  if (isExtensionRegistered.value) return 'Ready for Calls'
  return 'Not Ready for Calls'
})

const extensionStatusText = computed(() => {
  if (!serverConnected.value) return 'Server Required'
  if (isConnectingToExtension.value) return 'Registering Extension...'
  if (extensionError.value) return 'Registration Failed'
  if (isExtensionRegistered.value) return 'Ready to receive calls'
  return 'Start calls to become accessible'
})

// Computed properties for UI data
const incomingCall = computed(() => callState.value.incoming)
const activeCall = computed(() => callState.value.active)
const isMuted = computed(() => callState.value.isMuted)
const callDuration = computed(() => callState.value.duration)
const transferDialog = computed(() => callState.value.transferDialog)
const transferTarget = computed({
  get: () => callState.value.transferTarget,
  set: (value) => callState.value.transferTarget = value
})

// Chart computed properties
const chartData = computed(() => {
  const data = chartDataSets.value[selectedPeriod.value]
  const maxValue = Math.max(...data.map(d => d.value))
  return data.map(d => ({
    ...d,
    percentage: (d.value / maxValue) * 80 + 10
  }))
})

const yAxisLabels = computed(() => {
  const data = chartDataSets.value[selectedPeriod.value]
  const maxValue = Math.max(...data.map(d => d.value))
  const step = Math.ceil(maxValue / 4)
  return [0, step, step * 2, step * 3, maxValue]
})

const linePath = computed(() => {
  const points = chartData.value.map((point, index) => {
    const x = (index * (100 / (chartData.value.length - 1)))
    const y = 100 - point.percentage
    return `${x},${y}`
  })
  return `M ${points.join(' L ')}`
})

const areaPath = computed(() => {
  const points = chartData.value.map((point, index) => {
    const x = (index * (100 / (chartData.value.length - 1)))
    const y = 100 - point.percentage
    return `${x},${y}`
  })
  const firstPoint = points[0].split(',')
  const lastPoint = points[points.length - 1].split(',')
  return `M ${firstPoint[0]},100 L ${points.join(' L ')} L ${lastPoint[0]},100 Z`
})

const totalCalls = computed(() => {
  return chartDataSets.value[selectedPeriod.value].reduce((sum, d) => sum + d.value, 0)
})

const callsChange = computed(() => {
  return selectedPeriod.value === '7d' ? 12 : selectedPeriod.value === '30d' ? 8 : selectedPeriod.value === '3m' ? -3 : 15
})

const peakHour = computed(() => {
  const peaks = {
    '7d': '2:00 PM',
    '30d': 'Week 3',
    '3m': 'February',
    '1y': 'Q4'
  }
  return peaks[selectedPeriod.value]
})

const peakCalls = computed(() => {
  return Math.max(...chartDataSets.value[selectedPeriod.value].map(d => d.value))
})

const avgResponse = computed(() => {
  const responses = {
    '7d': '2.3m',
    '30d': '2.1m',
    '3m': '2.5m',
    '1y': '2.2m'
  }
  return responses[selectedPeriod.value]
})

// Server connection methods
const testAsteriskConnection = async () => {
  try {
    serverStatus.value.isTestingConnection = true
    serverStatus.value.connectionError = null
    
    const sipDetails = JSON.parse(localStorage.getItem('sipConnectionDetails'))
    
    if (!sipDetails?.websocketURL) {
      throw new Error('Missing Asterisk server details')
    }

    console.log('Testing Asterisk server connection...')
    
    const isAccessible = await testServerConnection(sipDetails.websocketURL)
    
    if (isAccessible) {
      serverStatus.value.isServerAccessible = true
      console.log('Asterisk server is accessible')
    } else {
      throw new Error('Asterisk server is not responding')
    }

  } catch (error) {
    console.error('Server connection test failed:', error)
    serverStatus.value.connectionError = error.message
    serverStatus.value.isServerAccessible = false
  } finally {
    serverStatus.value.isTestingConnection = false
  }
}

const handleRetryServerConnection = () => {
  testAsteriskConnection()
}

// Extension registration methods
const startCallsService = async () => {
  try {
    extensionStatus.value.isConnecting = true
    extensionStatus.value.error = null
    
    const sipDetails = JSON.parse(localStorage.getItem('sipConnectionDetails'))
    
    console.log('Starting calls service - initializing SIP and registering extension...')
    
    // Initialize SIP client
    await initSIP({
      Desc: sipDetails.Desc || 'Agent Extension',
      sipUri: sipDetails.uri,
      password: sipDetails.password,
      websocketURL: sipDetails.websocketURL,
      debug: true
    })
    
    // Set up SIP event listeners
    setupSipEventListeners()
    
    // Register extension to receive calls
    await registerExtension()
    
    extensionStatus.value.isRegistered = true
    console.log('Extension registered - ready to receive calls')
    
  } catch (error) {
    console.error('Failed to start calls service:', error)
    extensionStatus.value.error = error.message
    extensionStatus.value.isRegistered = false
  } finally {
    extensionStatus.value.isConnecting = false
  }
}

const stopCallsService = async () => {
  try {
    extensionStatus.value.isConnecting = true
    
    console.log('Stopping calls service - unregistering extension...')
    
    // Unregister extension
    await unregisterExtension()
    
    extensionStatus.value.isRegistered = false
    console.log('Extension unregistered - no longer receiving calls')
    
  } catch (error) {
    console.error('Failed to stop calls service:', error)
    extensionStatus.value.error = error.message
  } finally {
    extensionStatus.value.isConnecting = false
  }
}

const handleStartCalls = async () => {
  // If there's an active call, hang it up
  if (callState.value.active) {
    try {
      await hangupCall()
    } catch (error) {
      console.error('Failed to end call:', error)
    }
    return
  }
  
  // Toggle extension registration
  if (extensionStatus.value.isRegistered) {
    await stopCallsService()
  } else {
    await startCallsService()
  }
}

// SIP event listeners setup
const setupSipEventListeners = () => {
  // Extension registration events
  on('onRegistered', () => {
    console.log('SIP extension registered successfully')
    extensionStatus.value.isRegistered = true
    extensionStatus.value.isConnecting = false
    extensionStatus.value.error = null
  })

  on('onUnregistered', () => {
    console.log('SIP extension unregistered')
    extensionStatus.value.isRegistered = false
    extensionStatus.value.isConnecting = false
  })

  on('onRegistrationFailed', (error) => {
    console.error('SIP registration failed:', error)
    extensionStatus.value.isRegistered = false
    extensionStatus.value.isConnecting = false
    extensionStatus.value.error = `Registration failed: ${error.cause || error}`
  })

  // Incoming call events
  on('onIncomingCall', (session) => {
    console.log('Incoming call received')
    callState.value.incoming = {
      session,
      callerId: session.remote_identity.uri.user,
      callerName: session.remote_identity.display_name || session.remote_identity.uri.user,
      status: 'incoming'
    }
  })

  // Call events
  on('onCallAnswered', (session) => {
    console.log('Call answered')
    callState.value.active = {
      session,
      callerId: session.remote_identity.uri.user,
      callerName: session.remote_identity.display_name || session.remote_identity.uri.user,
      status: 'active'
    }
    callState.value.incoming = null
    startCallTimer()
  })

  on('onCallEnded', () => {
    console.log('Call ended')
    callState.value.active = null
    callState.value.incoming = null
    callState.value.isMuted = false
    stopCallTimer()
  })

  on('onCallRejected', () => {
    console.log('Call rejected')
    callState.value.incoming = null
  })

  // Connection events
  on('onDisconnected', () => {
    console.log('SIP disconnected')
    extensionStatus.value.isRegistered = false
    extensionStatus.value.isConnecting = false
    serverStatus.value.isServerAccessible = false
  })
}

// Call control methods
const answerIncomingCall = async () => {
  try {
    console.log('Answering incoming call...')
    await answerCall()
  } catch (error) {
    console.error('Failed to answer call:', error)
  }
}

const rejectIncomingCall = async () => {
  try {
    console.log('Rejecting incoming call...')
    await rejectCall()
    callState.value.incoming = null
  } catch (error) {
    console.error('Failed to reject call:', error)
  }
}

const endCall = async () => {
  try {
    console.log('Ending active call...')
    await hangupCall()
  } catch (error) {
    console.error('Failed to end call:', error)
  }
}

const toggleMute = async () => {
  try {
    const newMuteState = !callState.value.isMuted
    await muteCall(newMuteState)
    callState.value.isMuted = newMuteState
    console.log(newMuteState ? 'Call muted' : 'Call unmuted')
  } catch (error) {
    console.error('Failed to toggle mute:', error)
  }
}

const showTransferDialog = () => {
  callState.value.transferDialog = true
}

const transferCallToTarget = async () => {
  if (!callState.value.transferTarget.trim()) return
  
  try {
    await transferCall(callState.value.transferTarget)
    callState.value.transferDialog = false
    callState.value.transferTarget = ''
    console.log('Call transferred successfully')
  } catch (error) {
    console.error('Failed to transfer call:', error)
  }
}

// Call timer management
const startCallTimer = () => {
  callStartTime = Date.now()
  callTimer = setInterval(() => {
    const elapsed = Date.now() - callStartTime
    const hours = Math.floor(elapsed / 3600000)
    const minutes = Math.floor((elapsed % 3600000) / 60000)
    const seconds = Math.floor((elapsed % 60000) / 1000)
    
    callState.value.duration = 
      `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`
  }, 1000)
}

const stopCallTimer = () => {
  if (callTimer) {
    clearInterval(callTimer)
    callTimer = null
  }
  callState.value.duration = '00:00:00'
}

// Sidebar event handlers
const handleLogout = async () => {
  // Clean up SIP connections before logout
  if (extensionStatus.value.isRegistered) {
    try {
      await stopCallsService()
    } catch (error) {
      console.error('Error stopping calls during logout:', error)
    }
  }
  
  cleanup()
  console.log('Logging out...')
  alert('Logged out successfully!')
}

const handleSidebarToggle = (collapsed) => {
  console.log('Sidebar toggled:', collapsed)
  // Update CSS variable for main content margin
  document.documentElement.style.setProperty('--sidebar-width', collapsed ? '20px' : '250px')
}

// Dashboard navigation methods
const navigateToCalls = () => {
  router.push('/calls')
}

// Chart methods
const changePeriod = (period) => {
  selectedPeriod.value = period
}

const showTooltip = (data, event) => {
  const rect = event.target.getBoundingClientRect()
  const container = event.target.closest('.chart-card').getBoundingClientRect()

  tooltip.value = {
    show: true,
    x: rect.left - container.left + rect.width / 2,
    y: rect.top - container.top - 10,
    data: data
  }
}

const hideTooltip = () => {
  tooltip.value.show = false
}

// Theme management
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
    root.style.setProperty('--logo-bg', '#ffffff')
    root.style.setProperty('--logo-color', '#333')
    root.setAttribute('data-theme', 'light')
  } else {
    root.style.setProperty('--background-color', '#0a0a0a')
    root.style.setProperty('--sidebar-bg', '#111')
    root.style.setProperty('--content-bg', '#222')
    root.style.setProperty('--text-color', '#fff')
    root.style.setProperty('--text-secondary', '#aaa')
    root.style.setProperty('--border-color', '#333')
    root.style.setProperty('--card-bg', '#222')
    root.style.setProperty('--logo-bg', '#fff')
    root.style.setProperty('--logo-color', '#0a0a0a')
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
  root.style.setProperty('--prank-color', '#9C27B0')
  root.style.setProperty('--counsellor-color', '#2196F3')
}

const toggleTheme = () => {
  currentTheme.value = currentTheme.value === 'dark' ? 'light' : 'dark'
  localStorage.setItem('theme', currentTheme.value)
  applyTheme(currentTheme.value)
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
  
  // Test server accessibility on component mount
  testAsteriskConnection()
})

onBeforeUnmount(() => {
  // Clean up call timer
  stopCallTimer()
  
  // Clean up SIP connections and event listeners
  cleanup()
  
  off('onRegistered')
  off('onUnregistered')
  off('onRegistrationFailed')
  off('onIncomingCall')
  off('onCallAnswered')
  off('onCallEnded')
  off('onCallRejected')
  off('onDisconnected')
})
</script>


<style>
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
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
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

/* Call Status Card */
.call-status-container {
  margin-bottom: 25px;
  transition: all 0.3s ease;
}

.call-status-container.active-call {
  transform: scale(1.02);
}

.call-status-card {
  background: linear-gradient(135deg, var(--card-bg), rgba(150, 75, 0, 0.05));
  border-radius: 20px;
  padding: 25px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(150, 75, 0, 0.1);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.call-status-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, var(--accent-color), var(--accent-hover));
  opacity: 0;
  transition: opacity 0.3s ease;
}

.call-status-container.active-call .call-status-card::before {
  opacity: 1;
}

.call-status-header {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 20px;
}

.call-status-icon {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--accent-color), var(--accent-hover));
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(150, 75, 0, 0.3);
}

.call-status-icon svg {
  stroke: white;
  width: 24px;
  height: 24px;
}

.call-status-title {
  font-size: 20px;
  font-weight: 700;
  color: var(--text-color);
}

/* Incoming Call Controls */
.incoming-call-controls {
  background: linear-gradient(135deg, #d4edda, #c3e6cb);
  border-radius: 15px;
  padding: 20px;
  border: 2px solid var(--success-color);
  animation: callPulse 2s infinite;
}

@keyframes callPulse {
  0%, 100% { 
    box-shadow: 0 0 0 0 rgba(40, 167, 69, 0.4);
  }
  50% { 
    box-shadow: 0 0 0 15px rgba(40, 167, 69, 0);
  }
}

.caller-info {
  text-align: center;
  margin-bottom: 20px;
}

.caller-name {
  font-size: 20px;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 5px;
}

.caller-number {
  font-size: 14px;
  color: #6c757d;
  font-weight: 600;
}

.call-buttons {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}

.answer-btn, .reject-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 15px 20px;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.answer-btn {
  background: linear-gradient(135deg, var(--success-color), #218838);
  color: white;
  box-shadow: 0 4px 12px rgba(40, 167, 69, 0.3);
}

.answer-btn:hover {
  background: linear-gradient(135deg, #218838, #1e7e34);
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(40, 167, 69, 0.4);
}

.reject-btn {
  background: linear-gradient(135deg, var(--danger-color), #c82333);
  color: white;
  box-shadow: 0 4px 12px rgba(220, 53, 69, 0.3);
}

.reject-btn:hover {
  background: linear-gradient(135deg, #c82333, #a71e2a);
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(220, 53, 69, 0.4);
}

/* Active Call Controls */
.active-call-controls {
  background: linear-gradient(135deg, rgba(0, 123, 255, 0.1), rgba(0, 123, 255, 0.05));
  border-radius: 15px;
  padding: 20px;
  border: 2px solid var(--accent-color);
}

.call-info {
  text-align: center;
  margin-bottom: 20px;
}

.call-duration {
  font-size: 24px;
  font-weight: 700;
  color: var(--accent-color);
  margin-bottom: 10px;
  font-family: 'Courier New', monospace;
}

.call-actions {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}

.mute-btn, .transfer-btn, .hangup-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 12px;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 600;
}

.mute-btn {
  background: linear-gradient(135deg, #6c757d, #5a6268);
  color: white;
  box-shadow: 0 3px 8px rgba(108, 117, 125, 0.3);
}

.mute-btn.active {
  background: linear-gradient(135deg, #ffc107, #e0a800);
  color: #212529;
  box-shadow: 0 3px 8px rgba(255, 193, 7, 0.3);
}

.mute-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 5px 12px rgba(108, 117, 125, 0.4);
}

.transfer-btn {
  background: linear-gradient(135deg, var(--accent-color), var(--accent-hover));
  color: white;
  box-shadow: 0 3px 8px rgba(150, 75, 0, 0.3);
}

.transfer-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 5px 12px rgba(150, 75, 0, 0.4);
}

.hangup-btn {
  background: linear-gradient(135deg, var(--danger-color), #c82333);
  color: white;
  box-shadow: 0 3px 8px rgba(220, 53, 69, 0.3);
}

.hangup-btn:hover {
  background: linear-gradient(135deg, #c82333, #a71e2a);
  transform: translateY(-1px);
  box-shadow: 0 5px 12px rgba(220, 53, 69, 0.4);
}

/* Extension Status */
.extension-status {
  text-align: center;
  padding: 20px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 15px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.extension-state {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-secondary);
}

/* Dashboard Grid */
.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.dashboard-card {
  background-color: var(--card-bg);
  border-radius: 20px;
  padding: 25px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  border: 1px solid rgba(255, 255, 255, 0.1);
  position: relative;
  overflow: hidden;
}

.dashboard-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 4px;
  background: linear-gradient(90deg, var(--accent-color), var(--accent-hover));
  transform: scaleX(0);
  transition: transform 0.3s ease;
}

.dashboard-card:hover::before {
  transform: scaleX(1);
}

.dashboard-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 16px 48px rgba(0, 0, 0, 0.2);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.card-title {
  font-size: 16px;
  font-weight: 700;
  color: var(--text-color);
}

.card-icon {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--accent-color), var(--accent-hover));
  display: flex;
  justify-content: center;
  align-items: center;
  box-shadow: 0 4px 12px rgba(150, 75, 0, 0.3);
}

.card-icon.prank-calls {
  background: linear-gradient(135deg, var(--prank-color), #7b1fa2);
}

.card-icon.counsellors-online {
  background: linear-gradient(135deg, var(--counsellor-color), #1976d2);
}

.card-icon svg {
  stroke: white;
  width: 20px;
  height: 20px;
}

.card-value {
  font-size: 36px;
  font-weight: 800;
  margin-bottom: 8px;
  color: var(--text-color);
  font-family: system-ui, -apple-system, sans-serif;
}

.card-subtitle {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-secondary);
}

/* Agent Activity & Recent Calls */
.agent-activity,
.recent-calls {
  background-color: var(--card-bg);
  border-radius: 20px;
  padding: 25px;
  margin-bottom: 30px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  transition: background-color 0.3s;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
}

.section-title {
  font-size: 22px;
  font-weight: 700;
  color: var(--text-color);
}

.view-all {
  font-size: 14px;
  font-weight: 600;
  color: var(--accent-color);
  background: none;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none;
  padding: 8px 16px;
  border-radius: 20px;
  background: rgba(150, 75, 0, 0.1);
}

.view-all:hover {
  background: rgba(150, 75, 0, 0.2);
  transform: translateY(-1px);
}

/* Agent Table */
.agent-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  margin-top: 15px;
}

.agent-table th {
  text-align: left;
  padding: 15px 20px;
  font-size: 14px;
  font-weight: 700;
  color: var(--text-secondary);
  border-bottom: 2px solid var(--border-color);
  background: rgba(255, 255, 255, 0.02);
}

.agent-table td {
  padding: 15px 20px;
  font-size: 14px;
  font-weight: 600;
  border-bottom: 1px solid var(--border-color);
  transition: background-color 0.3s ease;
}

.agent-table tr:hover td {
  background-color: rgba(255, 255, 255, 0.02);
}

.agent-table tr:last-child td {
  border-bottom: none;
}

.agent-status {
  display: inline-block;
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 700;
  text-align: center;
  min-width: 120px;
  color: white;
}

.status-available {
  background: linear-gradient(135deg, var(--success-color), #218838);
  box-shadow: 0 2px 8px rgba(40, 167, 69, 0.3);
}

.status-in-call {
  background: linear-gradient(135deg, var(--accent-color), var(--accent-hover));
  box-shadow: 0 2px 8px rgba(150, 75, 0, 0.3);
}

.status-on-break {
  background: linear-gradient(135deg, var(--pending-color), #e0a800);
  box-shadow: 0 2px 8px rgba(255, 165, 0, 0.3);
}

/* Call List */
.call-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.call-item {
  display: flex;
  align-items: center;
  padding: 20px;
  background: linear-gradient(135deg, var(--background-color), rgba(255, 255, 255, 0.02));
  border-radius: 15px;
  transition: all 0.3s ease;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.call-item:hover {
  transform: translateX(8px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  border-color: rgba(150, 75, 0, 0.2);
}

.call-icon {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--content-bg), rgba(255, 255, 255, 0.1));
  display: flex;
  justify-content: center;
  align-items: center;
  margin-right: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.call-icon svg {
  stroke: var(--text-color);
  width: 20px;
  height: 20px;
}

.call-details {
  flex: 1;
}

.call-type {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 6px;
  color: var(--text-color);
}

.call-time {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-secondary);
}

.call-status {
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 700;
  color: white;
  text-align: center;
  min-width: 100px;
}

.status-completed {
  background: linear-gradient(135deg, var(--success-color), #218838);
}

.status-in-progress {
  background: linear-gradient(135deg, var(--accent-color), var(--accent-hover));
}

.status-pending {
  background: linear-gradient(135deg, var(--pending-color), #e0a800);
}

.status-unassigned {
  background: linear-gradient(135deg, var(--unassigned-color), #6c757d);
}

/* Enhanced Chart Styles */
.chart-container {
  margin-bottom: 30px;
}

.chart-card {
  background-color: var(--card-bg);
  border-radius: 20px;
  padding: 30px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  transition: background-color 0.3s;
  position: relative;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
}

.chart-controls {
  display: flex;
  gap: 8px;
}

.chart-period-btn {
  background-color: var(--background-color);
  color: var(--text-secondary);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 8px 16px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.chart-period-btn:hover {
  color: var(--text-color);
  border-color: var(--accent-color);
  background-color: rgba(150, 75, 0, 0.1);
}

.chart-period-btn.active {
  background: linear-gradient(135deg, var(--accent-color), var(--accent-hover));
  color: white;
  border-color: var(--accent-color);
  box-shadow: 0 2px 8px rgba(150, 75, 0, 0.3);
}

.chart-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
  padding: 20px;
  background: linear-gradient(135deg, var(--background-color), rgba(255, 255, 255, 0.02));
  border-radius: 15px;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.chart-stat {
  text-align: center;
}

.stat-label {
  font-size: 12px;
  font-weight: 600;
  color: var(--text-secondary);
  margin-bottom: 8px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.stat-value {
  font-size: 24px;
  font-weight: 700;
  color: var(--text-color);
  margin-bottom: 5px;
  font-family: system-ui, -apple-system, sans-serif;
}

.stat-change {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  font-size: 11px;
  font-weight: 600;
}

.stat-change.positive {
  color: var(--success-color);
}

.stat-change.negative {
  color: var(--danger-color);
}

.stat-description {
  font-size: 11px;
  font-weight: 600;
  color: var(--text-secondary);
}

.chart-placeholder {
  width: 100%;
  height: 350px;
  background: linear-gradient(135deg, var(--background-color), rgba(255, 255, 255, 0.02));
  border-radius: 15px;
  padding: 20px;
  position: relative;
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.enhanced-chart {
  width: 100%;
  height: 100%;
  position: relative;
}

.y-axis-labels {
  position: absolute;
  left: 0;
  top: 0;
  height: 100%;
  width: 40px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 10px 0;
}

.y-label {
  font-size: 11px;
  font-weight: 600;
  color: var(--text-secondary);
  text-align: right;
  padding-right: 8px;
  position: absolute;
  transform: translateY(-50%);
}

.chart-grid {
  position: absolute;
  left: 50px;
  top: 10px;
  right: 10px;
  bottom: 40px;
}

.grid-line-horizontal {
  position: absolute;
  left: 0;
  right: 0;
  height: 1px;
  background-color: var(--border-color);
  opacity: 0.3;
}

.grid-line-vertical {
  position: absolute;
  top: 0;
  bottom: 0;
  width: 1px;
  background-color: var(--border-color);
  opacity: 0.2;
}

.chart-area {
  position: absolute;
  left: 50px;
  top: 10px;
  right: 10px;
  bottom: 40px;
}

.chart-svg {
  width: 100%;
  height: 100%;
  position: absolute;
  top: 0;
  left: 0;
}

.chart-point {
  position: absolute;
  transform: translate(-50%, 50%);
  cursor: pointer;
  z-index: 10;
}

.point-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--accent-color), var(--accent-hover));
  border: 3px solid var(--card-bg);
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(150, 75, 0, 0.3);
}

.chart-point:hover .point-dot {
  width: 16px;
  height: 16px;
  border-width: 4px;
  box-shadow: 0 4px 16px rgba(150, 75, 0, 0.4), 0 0 0 6px rgba(150, 75, 0, 0.2);
}

.x-axis-labels {
  position: absolute;
  left: 50px;
  right: 10px;
  bottom: 0;
  height: 40px;
  display: flex;
  align-items: center;
}

.x-label {
  position: absolute;
  transform: translateX(-50%);
  font-size: 11px;
  font-weight: 600;
  color: var(--text-secondary);
  text-align: center;
}

.chart-tooltip {
  position: absolute;
  background: linear-gradient(135deg, var(--content-bg), rgba(255, 255, 255, 0.1));
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 12px 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  z-index: 1000;
  pointer-events: none;
  transform: translate(-50%, -100%);
  margin-top: -8px;
  backdrop-filter: blur(10px);
}

.tooltip-title {
  font-size: 12px;
  font-weight: 700;
  color: var(--text-color);
  margin-bottom: 4px;
}

.tooltip-value {
  font-size: 16px;
  font-weight: 700;
  color: var(--accent-color);
  margin-bottom: 4px;
}

.tooltip-time {
  font-size: 10px;
  font-weight: 600;
  color: var(--text-secondary);
}

/* Transfer Dialog */
.transfer-dialog {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  backdrop-filter: blur(5px);
}

.transfer-dialog-content {
  background-color: var(--card-bg);
  border-radius: 20px;
  padding: 30px;
  width: 90%;
  max-width: 400px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.transfer-dialog-title {
  font-size: 20px;
  font-weight: 700;
  margin-bottom: 20px;
  text-align: center;
  color: var(--text-color);
}

.transfer-input {
  width: 100%;
  padding: 15px;
  border: 2px solid var(--border-color);
  border-radius: 10px;
  font-size: 16px;
  background-color: var(--background-color);
  color: var(--text-color);
  margin-bottom: 20px;
  transition: border-color 0.3s ease;
}

.transfer-input:focus {
  outline: none;
  border-color: var(--accent-color);
  box-shadow: 0 0 0 3px rgba(150, 75, 0, 0.1);
}

.transfer-dialog-buttons {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}

.transfer-cancel-btn,
.transfer-confirm-btn {
  padding: 15px;
  border: none;
  border-radius: 10px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.transfer-cancel-btn {
  background-color: var(--unassigned-color);
  color: white;
}

.transfer-cancel-btn:hover {
  background-color: #5a6268;
  transform: translateY(-1px);
}

.transfer-confirm-btn {
  background: linear-gradient(135deg, var(--accent-color), var(--accent-hover));
  color: white;
}

.transfer-confirm-btn:hover {
  background: linear-gradient(135deg, var(--accent-hover), #a0520d);
  transform: translateY(-1px);
}

/* Responsive Design */
@media (max-width: 1024px) {
  .main-content {
    margin-left: 0;
    width: 100%;
  }

  .dashboard-grid {
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 15px;
  }

  .chart-stats {
    grid-template-columns: repeat(2, 1fr);
    gap: 15px;
  }

  .chart-header {
    flex-direction: column;
    gap: 15px;
    align-items: flex-start;
  }

  .call-actions {
    grid-template-columns: 1fr 1fr;
    gap: 10px;
  }

  .call-actions .transfer-btn {
    grid-column: 1 / -1;
  }
}
@media (max-width: 768px) {
  .header {
    padding: 15px;
  }

  .main-scroll-content {
    padding: 15px;
  }

  .dashboard-grid {
    grid-template-columns: 1fr;
    gap: 15px;
  }

  .page-title {
    font-size: 24px;
  }

  .theme-toggle {
    padding: 6px 12px;
    font-size: 12px;
  }

  .call-status-card {
    padding: 20px;
  }

  .call-status-icon {
    width: 40px;
    height: 40px;
  }

  .call-status-title {
    font-size: 18px;
  }

  .caller-name {
    font-size: 18px;
  }

  .call-duration {
    font-size: 20px;
  }

  .card-value {
    font-size: 28px;
  }

  .section-title {
    font-size: 18px;
  }

  .chart-controls {
    flex-wrap: wrap;
    gap: 6px;
  }

  .chart-period-btn {
    padding: 6px 12px;
    font-size: 11px;
  }

  .chart-stats {
    grid-template-columns: 1fr;
    gap: 15px;
  }

  .chart-placeholder {
    height: 280px;
  }

  .call-item {
    padding: 15px;
  }

  .call-icon {
    width: 40px;
    height: 40px;
    margin-right: 15px;
  }

  .agent-table th,
  .agent-table td {
    padding: 12px 15px;
    font-size: 13px;
  }

  .agent-status {
    min-width: 100px;
    padding: 6px 12px;
    font-size: 11px;
  }
}

@media (max-width: 480px) {
  .main-scroll-content {
    padding: 10px;
  }

  .page-title {
    font-size: 20px;
  }

  .theme-toggle {
    padding: 4px 8px;
    font-size: 11px;
  }

  .theme-toggle span {
    display: none;
  }

  .call-status-card {
    padding: 15px;
  }

  .call-status-header {
    flex-direction: column;
    text-align: center;
    gap: 10px;
  }

  .call-buttons {
    grid-template-columns: 1fr;
    gap: 10px;
  }

  .call-actions {
    grid-template-columns: 1fr;
    gap: 8px;
  }

  .dashboard-card {
    padding: 20px;
  }

  .card-value {
    font-size: 24px;
  }

  .card-icon {
    width: 40px;
    height: 40px;
  }

  .section-title {
    font-size: 16px;
  }

  .chart-controls {
    width: 100%;
    justify-content: center;
  }

  .chart-period-btn {
    flex: 1;
    min-width: 60px;
  }

  .chart-placeholder {
    height: 250px;
    padding: 15px;
  }

  .call-item {
    flex-direction: column;
    text-align: center;
    gap: 15px;
  }

  .call-icon {
    margin-right: 0;
    align-self: center;
  }

  .agent-table {
    font-size: 12px;
  }

  .agent-table th,
  .agent-table td {
    padding: 10px 8px;
  }

  .agent-status {
    min-width: 80px;
    padding: 4px 8px;
    font-size: 10px;
  }

  .transfer-dialog-content {
    padding: 20px;
    margin: 20px;
  }

  .transfer-dialog-title {
    font-size: 18px;
  }

  .transfer-input {
    padding: 12px;
    font-size: 14px;
  }

  .transfer-dialog-buttons {
    grid-template-columns: 1fr;
    gap: 10px;
  }
}

/* Dark mode specific adjustments */
@media (prefers-color-scheme: dark) {
  .call-status-card {
    background: linear-gradient(135deg, var(--card-bg), rgba(150, 75, 0, 0.08));
  }
  
  .incoming-call-controls {
    background: linear-gradient(135deg, rgba(40, 167, 69, 0.2), rgba(40, 167, 69, 0.1));
  }
  
  .active-call-controls {
    background: linear-gradient(135deg, rgba(150, 75, 0, 0.2), rgba(150, 75, 0, 0.1));
  }
  
  .dashboard-card::before {
    opacity: 0.8;
  }
  
  .chart-tooltip {
    background: linear-gradient(135deg, rgba(34, 34, 34, 0.95), rgba(34, 34, 34, 0.9));
  }
}

/* High contrast mode */
@media (prefers-contrast: high) {
  .call-status-card,
  .dashboard-card,
  .agent-activity,
  .recent-calls,
  .chart-card {
    border: 2px solid var(--text-color);
  }
  
  .answer-btn,
  .reject-btn,
  .mute-btn,
  .transfer-btn,
  .hangup-btn {
    border: 2px solid currentColor;
  }
  
  .agent-status,
  .call-status {
    border: 1px solid var(--text-color);
  }
  
  .chart-period-btn {
    border: 2px solid var(--text-color);
  }
}

/* Reduced motion */
@media (prefers-reduced-motion: reduce) {
  .call-status-card,
  .dashboard-card,
  .call-item,
  .answer-btn,
  .reject-btn,
  .mute-btn,
  .transfer-btn,
  .hangup-btn,
  .theme-toggle,
  .view-all,
  .chart-period-btn,
  .chart-point,
  .transfer-cancel-btn,
  .transfer-confirm-btn {
    transition: none;
  }
  
  .call-status-container.active-call {
    transform: none;
  }
  
  .dashboard-card:hover,
  .call-item:hover,
  .answer-btn:hover,
  .reject-btn:hover,
  .mute-btn:hover,
  .transfer-btn:hover,
  .hangup-btn:hover {
    transform: none;
  }
  
  .callPulse,
  .point-dot {
    animation: none;
  }
}

/* Print styles */
@media print {
  .call-status-container,
  .theme-toggle,
  .call-buttons,
  .call-actions,
  .transfer-dialog {
    display: none;
  }
  
  .main-content {
    margin-left: 0;
  }
  
  .dashboard-grid {
    break-inside: avoid;
  }
  
  .dashboard-card {
    break-inside: avoid;
    box-shadow: none;
    border: 1px solid #ccc;
  }
}
</style>