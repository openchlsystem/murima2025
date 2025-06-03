<template>
  <div class="dashboard-layout">
    <button class="mobile-menu-btn" id="mobile-menu-btn" @click="toggleMobileMenu">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M3 12H21M3 6H21M3 18H21" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </button>

    <div class="sidebar" id="sidebar" :class="{ 'collapsed': isSidebarCollapsed, 'mobile-open': mobileOpen }">
      <div class="sidebar-content">
        <div class="logo-container">
          <div class="logo">
            <img :src="logo" alt="OpenCHS Logo">
          </div>
        </div>
        
        <router-link to="/dashboard" class="nav-item active">
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
        
        <router-link to="/chats" class="nav-item">
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
            <!-- If user has profile picture, show it -->
            <!-- <img src="profile-picture.jpg" alt="User Profile"> -->
            <!-- Otherwise show default icon -->
            <svg viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 12C14.2091 12 16 10.2091 16 8C16 5.79086 14.2091 4 12 4C9.79086 4 8 5.79086 8 8C8 10.2091 9.79086 12 12 12Z"/>
              <path d="M12 14C7.58172 14 4 17.5817 4 22H20C20 17.5817 16.4183 14 12 14Z"/>
            </svg>
          </router-link>
        </div>
        
        <div class="status">
          <div class="status-dot"></div>
          <span>Status: Online</span>
        </div>
        
        <div class="button-container">
          <button class="join-queue-btn">Join Queue</button>
          <button class="logout-btn" @click="logout">Logout</button>
        </div>
      </div>
    </div>

    <button class="expand-btn" id="expand-btn" @click="expandSidebar" :class="{ 'visible': isSidebarCollapsed }">
      >
    </button>

    <div class="main-content" :class="{ 'sidebar-collapsed': isSidebarCollapsed }" :style="{ marginLeft: mainContentMarginLeft }">
      <div class="header">
        <button class="sidebar-toggle" @click="toggleSidebar">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M4 6H20M4 12H20M4 18H20" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
        <h1>Dashboard</h1>
        <button class="theme-toggle" @click="toggleTheme">
          <svg id="moon-icon" width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" v-show="currentTheme === 'dark'">
            <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <svg id="sun-icon" width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" v-show="currentTheme === 'light'">
            <circle cx="12" cy="12" r="5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <line x1="12" y1="1" x2="12" y2="3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <line x1="12" y1="21" x2="12" y2="23" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <line x1="4.22" y1="4.22" x2="5.64" y2="5.64" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <line x1="18.36" y1="18.36" x2="19.78" y2="19.78" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <line x1="1" y1="12" x2="3" y2="12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <line x1="21" y1="12" x2="23" y2="12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <line x1="4.22" y1="19.78" x2="5.64" y2="18.36" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <line x1="18.36" y1="5.64" x2="19.78" y2="4.22" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <span id="theme-text">{{ currentTheme === 'dark' ? 'Light Mode' : 'Dark Mode' }}</span>
        </button>
      </div>

      <div class="dashboard-grid">
        <div class="dashboard-card" v-for="(card, index) in dashboardCards" :key="index">
          <div class="card-header">
            <div class="card-title">{{ card.title }}</div>
            <div class="card-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path :d="card.iconPath" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
          </div>
          <div class="card-value">{{ card.value }}</div>
          <div class="card-subtitle">{{ card.subtitle }}</div>
        </div>
      </div>

      <div class="queue-activity">
        <div class="section-header">
          <div class="section-title">Queue Activity</div>
        </div>
        
        <table class="queue-table">
          <thead>
            <tr>
              <th>Agent Name</th>
              <th>Current Status</th>
              <th>Calls Handled</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="agent in agents" :key="agent.name">
              <td>{{ agent.name }}</td>
              <td>
                <span :class="['agent-status', `status-${agent.status}`]">
                  {{ agent.statusText }}
                </span>
              </td>
              <td>{{ agent.callsHandled }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="recent-calls">
        <div class="section-header">
          <div class="section-title">Recent Calls</div>
          <router-link to="/calls" class="view-all">View All</router-link>
        </div>
        
        <div class="call-list">
          <div v-for="call in recentCalls" :key="call.id" class="call-item">
            <div class="call-icon">
              <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07 19.5 19.5 0 01-6-6 19.79 19.79 0 01-3.07-8.67A2 2 0 014.11 2h3a2 2 0 012 1.72c.127.96.361 1.903.7 2.81a2 2 0 01-.45 2.11L8.09 9.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0122 16.92z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <div class="call-details">
              <div class="call-type">{{ call.type }}</div>
              <div class="call-time">{{ call.time }}</div>
            </div>
            <div :class="['call-status', `status-${call.status}`]">
              {{ call.statusText }}
            </div>
          </div>
        </div>
      </div>

      <div class="chart-container">
        <div class="chart-card">
          <div class="section-title">Call Volume Trends</div>
          <div class="chart-placeholder">
            <div class="line-chart">
              <div class="chart-grid">
                <div v-for="i in 5" :key="i" class="grid-line" :style="{ gridRow: i }"></div>
              </div>
              
              <div class="y-axis"></div>
              <div v-for="(label, index) in yLabels" :key="index" class="y-label" :style="{ bottom: `${20 + index * 57}px` }">
                {{ label }}
              </div>
              
              <div class="chart-axis"></div>
              
              <div class="chart-line">
                <div v-for="(point, index) in chartData" :key="index" class="chart-point">
                  <div class="point-dot" :style="{ bottom: `${point.value}px` }"></div>
                  <div class="point-line" :style="{ height: `${point.value}px`, bottom: 0 }"></div>
                  <div class="point-label">{{ point.label }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import logo from '../assets/Openchs logo-1.png'

export default {
  name: 'Dashboard',
  data() {
    return {
      logo,
      isSidebarCollapsed: false,
      mobileOpen: false,
      dashboardCards: [
        {
          title: 'Total Calls',
          iconPath: 'M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07 19.5 19.5 0 01-6-6 19.79 19.79 0 01-3.07-8.67A2 2 0 014.11 2h3a2 2 0 012 1.72c.127.96.361 1.903.7 2.81a2 2 0 01-.45 2.11L8.09 9.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0122 16.92z',
          value: '53',
          subtitle: '+12% from last week'
        },
        {
          title: 'Active Cases',
          iconPath: 'M22 12h-4l-3 9L9 3l-3 9H2',
          value: '24',
          subtitle: '+5% from last week'
        },
        {
          title: 'Pending Calls',
          iconPath: 'M12 6v6l4 2 M12 12m-10 0a10 10 0 1 0 20 0 10 10 0 1 0 -20 0',
          value: '5',
          subtitle: '-2% from last week'
        },
        {
          title: 'Completed Calls',
          iconPath: 'M22 11.08V12a10 10 0 11-5.93-9.14 M22 4L12 14.01l-3-3',
          value: '42',
          subtitle: '+8% from last week'
        }
      ],
      agents: [
        { name: 'Sarah Davis', status: 'available', statusText: 'Available', callsHandled: 34 },
        { name: 'Mark Reynolds', status: 'in-call', statusText: 'In Call', callsHandled: 28 },
        { name: 'Emily Chan', status: 'on-break', statusText: 'On Break', callsHandled: 15 },
        { name: 'David Lee', status: 'available', statusText: 'Available', callsHandled: 42 },
        { name: 'Sophia Clark', status: 'in-call', statusText: 'In Call', callsHandled: 30 }
      ],
      recentCalls: [
        { 
          id: 1, 
          type: 'Emergency Crisis: Domestic Violence', 
          time: 'Today, 09:00AM', 
          status: 'in-progress',
          statusText: 'In Progress'
        },
        { 
          id: 2, 
          type: 'Survivor Follow-Up: Safety Planning', 
          time: 'Today, 10:30AM', 
          status: 'pending',
          statusText: 'Pending'
        },
        { 
          id: 3, 
          type: 'Wellness Check-In: Mental Health Support', 
          time: 'Yesterday, 11:15AM', 
          status: 'completed',
          statusText: 'Completed'
        },
        { 
          id: 4, 
          type: 'Resource Request: Shelter Information', 
          time: 'Today, 04:45PM', 
          status: 'unassigned',
          statusText: 'Unassigned'
        }
      ],
      yLabels: [0, 10, 20, 30, 40],
      chartData: [
        { label: 'Mon', value: 60 },
        { label: 'Tue', value: 90 },
        { label: 'Wed', value: 120 },
        { label: 'Thu', value: 150 },
        { label: 'Fri', value: 100 },
        { label: 'Sat', value: 70 },
        { label: 'Sun', value: 40 }
      ],
      currentTheme: localStorage.getItem('theme') || 'dark',
    };
  },
  computed: {
    mainContentMarginLeft() {
      if (window.innerWidth <= 768) {
        return '0px';
      } else if (this.isSidebarCollapsed) {
        return '80px'; // Collapsed sidebar width
      } else {
        return '250px'; // Full sidebar width
      }
    }
  },
  methods: {
    toggleSidebar() {
      this.isSidebarCollapsed = !this.isSidebarCollapsed;
    },
    expandSidebar() {
      this.isSidebarCollapsed = false;
    },
    toggleMobileMenu() {
      this.mobileOpen = !this.mobileOpen;
    },
    joinQueue() {
      console.log('Joining queue');
      // Add the queue functionality here
    },
    logout() {
      console.log('Logging out');
      this.$router.push('/'); // Use Vue Router for navigation
    },
    animateChart() {
      setTimeout(() => {
        const chartPoints = this.$el.querySelectorAll('.point-dot, .point-line');
        chartPoints.forEach(point => {
          const originalBottom = point.style.bottom;
          point.style.bottom = '0';
          setTimeout(() => {
            point.style.transition = 'bottom 1s ease-out';
            point.style.bottom = originalBottom;
          }, 100);
        });
      }, 300);
    },
    setupOutsideClickListener() {
      document.addEventListener('click', (event) => {
        const isMobile = window.innerWidth <= 768;
        // const sidebar = document.getElementById('sidebar');
        const mobileMenuBtn = document.getElementById('mobile-menu-btn');
        
        if (isMobile && sidebar && !sidebar.contains(event.target) && event.target !== mobileMenuBtn) {
          this.mobileOpen = false;
        }
      });
    },
    setupResizeListener() {
      window.addEventListener('resize', () => {
        if (window.innerWidth > 768) {
          this.mobileOpen = false;
        }
      });
    },
    applyTheme(theme) {
      if (theme === 'light') {
          document.documentElement.setAttribute('data-theme', 'light');
      } else {
          document.documentElement.setAttribute('data-theme', 'dark');
      }
    },
    toggleTheme() {
      const currentTheme = document.documentElement.getAttribute('data-theme') || 'dark';
      const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
      
      localStorage.setItem('theme', newTheme);
      this.currentTheme = newTheme;
      this.applyTheme(newTheme);
    }
  },
  mounted() {
    // Apply theme from localStorage
    this.applyTheme(this.currentTheme);
    
    // Initialize status counts
    // this.updateStatusCounts(); // This method is not in dashboard.html

    // Set up event listeners
    this.setupOutsideClickListener();
    this.setupResizeListener();
    
    // Select the first call by default if calls exist
    // This logic is specific to the Calls page and not present in dashboard.html
    // const firstCallId = this.allCalls.length > 0 ? this.allCalls[0].id : null;
    // if (firstCallId) {
    //   this.selectCall(firstCallId);
    // }

    // Animate chart when component is mounted, based on dashboard.html script
    const chartPoints = this.$el.querySelectorAll('.point-dot, .point-line');
    chartPoints.forEach(point => {
        const originalBottom = point.style.bottom;
        point.style.bottom = '0';
        setTimeout(() => {
            point.style.transition = 'bottom 1s ease-out';
            point.style.bottom = originalBottom;
        }, 100);
    });

    // Add event listeners for sidebar toggling, based on dashboard.html script
    const sidebar = this.$el.querySelector('#sidebar');
    const toggleBtn = this.$el.querySelector('#toggle-btn');
    const expandBtn = this.$el.querySelector('#expand-btn');
    const mobileMenuBtn = this.$el.querySelector('#mobile-menu-btn');
    const html = document.documentElement;

    if (toggleBtn) {
        toggleBtn.addEventListener('click', () => {
            sidebar.classList.toggle('collapsed');
            if (sidebar.classList.contains('collapsed')) {
                toggleBtn.innerHTML = '&gt;';
            } else {
                toggleBtn.innerHTML = '&lt;';
            }
            // Also toggle the visibility of the expand button based on sidebar state
            if (expandBtn) {
                if (sidebar.classList.contains('collapsed')) {
                    expandBtn.style.display = 'flex';
                } else {
                    expandBtn.style.display = 'none';
                }
            }
        });
    }

    if (expandBtn) {
        expandBtn.addEventListener('click', () => {
            sidebar.classList.remove('collapsed');
            if (toggleBtn) {
                toggleBtn.innerHTML = '&lt;';
            }
             // Hide expand button when sidebar is not collapsed
            expandBtn.style.display = 'none';
        });
    }

     // Mobile menu toggle based on dashboard.html script
    if (mobileMenuBtn) {
        mobileMenuBtn.addEventListener('click', () => {
            sidebar.classList.toggle('mobile-open');
        });
    }

    // Close sidebar when clicking outside on mobile, based on dashboard.html script
    document.addEventListener('click', (event) => {
        const isMobile = window.innerWidth <= 768;
        if (isMobile && sidebar && !sidebar.contains(event.target) && event.target !== mobileMenuBtn && (!toggleBtn || !toggleBtn.contains(event.target))) {
            sidebar.classList.remove('mobile-open');
        }
    });

    // Handle window resize, based on dashboard.html script
    window.addEventListener('resize', () => {
        if (window.innerWidth > 768) {
            sidebar.classList.remove('mobile-open');
        }
         // Adjust expand button display on resize if sidebar is collapsed
        if (expandBtn && sidebar.classList.contains('collapsed')) {
             if (window.innerWidth > 768) {
                 expandBtn.style.display = 'flex';
             } else {
                 expandBtn.style.display = 'none';
             }
        }
    });

    // Theme toggle logic based on dashboard.html script
    const themeToggle = this.$el.querySelector('#theme-toggle');
    const themeText = this.$el.querySelector('#theme-text');
    const moonIcon = this.$el.querySelector('#moon-icon');
    const sunIcon = this.$el.querySelector('#sun-icon');

    function applyTheme(theme) {
        if (theme === 'light') {
            html.setAttribute('data-theme', 'light');
            if (themeText) themeText.textContent = 'Dark Mode';
            if (moonIcon) moonIcon.style.display = 'none';
            if (sunIcon) sunIcon.style.display = 'block';
        } else {
            html.setAttribute('data-theme', 'dark');
            if (themeText) themeText.textContent = 'Light Mode';
            if (moonIcon) moonIcon.style.display = 'block';
            if (sunIcon) sunIcon.style.display = 'none';
        }
    }

     // Check localStorage for saved theme preference and apply on mount
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        applyTheme(savedTheme);
    } else {
         // Apply default theme if no preference is saved
         applyTheme(html.getAttribute('data-theme') || 'dark');
    }

    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            const currentTheme = html.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

            localStorage.setItem('theme', newTheme);
            applyTheme(newTheme);
        });
    }

  },
};
</script>

<style scoped>
:root {
  /* Dark theme variables */
  --background-color: #0a0a0a;
  --sidebar-bg: #111;
  --content-bg: #222;
  --text-color: #fff; /* Ensure text color is white in dark mode */
  --text-secondary: #aaa;
  --border-color: #333;
  --accent-color: #964B00;
  --accent-hover: #b25900;
  --danger-color: #ff3b30;
  --success-color: #4CAF50;
  --pending-color: #FFA500;
  --unassigned-color: #808080;
  --highlight-color: #ff3b30;
  --header-bg: #333;
  --card-bg: #222;
}

[data-theme="light"] {
  --background-color: #f5f5f5;
  --sidebar-bg: #ffffff;
  --content-bg: #ffffff;
  --text-color: #333; /* Ensure text color is dark in light mode */
  --text-secondary: #666;
  --border-color: #ddd;
  --accent-color: #964B00;
  --accent-hover: #b25900;
  --danger-color: #ff3b30;
  --success-color: #4CAF50;
  --pending-color: #FFA500;
  --unassigned-color: #808080;
  --highlight-color: #ff3b30;
  --header-bg: #f0f0f0;
  --card-bg: #ffffff;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Inter', sans-serif;
}

body {
  margin: 0;
  min-width: 320px;
  min-height: 100vh;
  transition: background-color 0.3s, color 0.3s;
  overflow-x: hidden;
  color: var(--text-color); /* Ensure body text uses theme color */
}

.dashboard-layout {
  display: flex;
  min-height: 100vh;
  background-color: var(--background-color);
  color: var(--text-color);
  transition: background-color 0.3s, color 0.3s;
  width: 100%;
}

.sidebar {
  width: 250px;
  flex-shrink: 0;
  background-color: var(--sidebar-bg);
  color: var(--text-color);
  transition: width 0.3s ease, background-color 0.3s;
  overflow-x: hidden;
  border-radius: 0 30px 30px 0;
  z-index: 100;
  height: 100vh;
  /* position handled in media query */
}

.sidebar.collapsed {
  width: 80px;
}

.expand-btn {
  position: fixed;
  top: 50px;
  left: 5px;
  width: 30px;
  height: 30px;
  background-color: var(--text-color);
  border-radius: 50%;
  display: none;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  z-index: 101;
  border: 1px solid var(--border-color);
  color: var(--background-color);
  font-weight: bold;
  font-size: 14px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.sidebar.collapsed ~ .main-content .expand-btn {
    display: flex;
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
  justify-content: center; /* Ensure horizontal centering */
  align-items: center; /* Ensure vertical centering */
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
}

.nav-text {
  font-size: 14px;
  font-weight: 500;
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

.user-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.user-avatar svg {
  width: 30px;
  height: 30px;
  fill: var(--background-color);
}

.status {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  margin: 0 20px 15px;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: var(--success-color);
  margin-right: 5px;
}

.button-container {
  padding: 0 20px;
}

.join-queue-btn {
  background-color: var(--accent-color);
  color: white;
  border: none;
  border-radius: 30px;
  padding: 10px;
  width: 100%;
  font-weight: 600;
  cursor: pointer;
  margin-bottom: 10px;
  transition: background-color 0.3s;
}

.join-queue-btn:hover {
  background-color: var(--accent-hover);
}

.logout-btn {
  background-color: #800000; /* Maroon background */
  color: white;
  border: 1px solid #800000; /* Maroon border */
  border-radius: 30px;
  padding: 10px;
  width: 100%;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s, border-color 0.3s; /* Add border-color transition */
}

.logout-btn:hover {
  background-color: var(--danger-color); /* Red background on hover */
  border-color: var(--danger-color); /* Red border on hover */
}

.main-content {
  flex: 1; /* Allow main content to take remaining space */
  padding: 20px;
  min-height: 100vh;
  background-color: var(--background-color);
  color: var(--text-color); /* Explicitly set text color for main content */
  transition: background-color 0.3s, margin-left 0.3s ease, color 0.3s ease; /* Add color transition */
  overflow-y: auto;
}

/* Add styles for specific text elements within main-content */
.main-content h1,
.main-content h2,
.main-content h3,
.main-content h4,
.main-content h5,
.main-content h6 {
  color: var(--text-color); /* Ensure headers use theme color */
  transition: color 0.3s ease; /* Add transition */
}

.main-content .card-title {
  color: var(--text-color); /* Ensure card titles use theme color */
  transition: color 0.3s ease; /* Add transition */
}

.main-content .card-value {
    color: var(--text-color); /* Ensure card values use theme color */
    transition: color 0.3s ease; /* Add transition */
}

.main-content .card-subtitle {
  color: var(--text-secondary); /* Ensure card subtitles use secondary theme color */
  transition: color 0.3s ease; /* Add transition */
}

.main-content .section-title {
    color: var(--text-color); /* Ensure section titles use theme color */
    transition: color 0.3s ease; /* Add transition */
}

.main-content .queue-table th {
  text-align: left;
  padding: 12px 15px;
  font-size: 14px;
  font-weight: 600;
  color: var(--text-secondary); /* Use text-secondary for table headers */
  border-bottom: 1px solid var(--border-color);
  transition: color 0.3s ease; /* Add transition */
}

.main-content .queue-table td {
  padding: 12px 15px;
  font-size: 14px;
  border-bottom: 1px solid var(--border-color);
  color: var(--text-color); /* Ensure table data text uses theme color */
  transition: color 0.3s ease;
}

.main-content .call-type {
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 5px;
  color: var(--text-color); /* Ensure call type uses theme color */
  transition: color 0.3s ease; /* Add transition */
}

.main-content .call-time {
  font-size: 12px;
  color: var(--text-secondary); /* Use text-secondary for call time */
  transition: color 0.3s ease; /* Add transition */
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.header h1 {
  font-size: 24px;
  font-weight: 600;
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
  transition: background-color 0.3s, color 0.3s, border-color 0.3s;
}

.theme-toggle:hover {
  background-color: var(--border-color);
}

.theme-toggle svg {
  width: 16px;
  height: 16px;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.dashboard-card {
  background-color: var(--card-bg);
  border-radius: 30px;
  padding: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s, box-shadow 0.2s, background-color 0.3s;
  color: var(--text-color); /* Ensure card text uses theme color */
}

.dashboard-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.card-title {
  font-size: 16px;
  font-weight: 600;
}

.card-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: var(--accent-color);
  display: flex;
  justify-content: center;
  align-items: center;
}

.card-icon svg {
  width: 20px;
  height: 20px;
  stroke: white;
}

.card-value {
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 5px;
}

.card-subtitle {
  font-size: 12px;
  color: var(--text-secondary);
}

.recent-calls {
  background-color: var(--card-bg);
  border-radius: 30px;
  padding: 20px;
  margin-bottom: 30px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: background-color 0.3s;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.section-title {
  font-size: 18px;
  font-weight: 600;
}

.view-all {
  font-size: 14px;
  color: var(--accent-color);
  text-decoration: none;
}

.call-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.call-item {
  display: flex;
  align-items: center;
  padding: 15px;
  background-color: var(--content-bg);
  border-radius: 20px;
  transition: transform 0.2s, background-color 0.3s ease;
  color: var(--text-color); /* Ensure call item text uses theme color */
}

.call-item:hover {
  transform: translateX(5px);
}

.call-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: var(--content-bg);
  display: flex;
  justify-content: center;
  align-items: center;
  margin-right: 15px;
}

.call-icon svg {
  width: 20px;
  height: 20px;
  stroke: var(--text-color);
}

.call-details {
  flex: 1;
  color: var(--text-color);
}

.call-type {
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 5px;
}

.call-time {
  font-size: 12px;
  color: var(--text-secondary);
}

.call-status {
  padding: 5px 15px;
  border-radius: 30px;
  font-size: 12px;
  font-weight: 500;
  color: white;
}

.status-completed {
  background-color: var(--success-color);
}

.status-in-progress {
  background-color: var(--accent-color);
}

.status-pending {
  background-color: var(--pending-color);
}

.status-unassigned {
  background-color: var(--unassigned-color);
}

.chart-container {
  margin-bottom: 30px;
}

.chart-card {
  background-color: var(--card-bg);
  border-radius: 30px;
  padding: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: background-color 0.3s;
}

.chart-placeholder {
  width: 100%;
  height: 300px;
  background-color: var(--background-color);
  border-radius: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 15px;
  transition: background-color 0.3s;
  position: relative;
  overflow: hidden;
}

.chart-placeholder p {
  font-size: 14px;
  color: var(--text-secondary);
}

/* Line chart styles */
.line-chart {
  width: 100%;
  height: 100%;
  padding: 20px;
  position: relative;
}

.chart-grid {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: grid;
  grid-template-rows: repeat(5, 1fr);
  grid-template-columns: repeat(7, 1fr);
}

.grid-line {
  border-bottom: 1px dashed var(--border-color);
  width: 100%;
  height: 0;
}

.chart-line {
  position: absolute;
  bottom: 50px;
  left: 40px;
  width: calc(100% - 80px);
  height: 200px;
  display: flex;
  align-items: flex-end;
}

.chart-point {
  flex: 1;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  align-items: center;
  position: relative;
}

.point-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: var(--accent-color);
  position: absolute;
  z-index: 2;
}

.point-line {
  width: 2px;
  background-color: var(--accent-color);
  position: absolute;
  bottom: 0;
  z-index: 1;
}

.point-label {
  position: absolute;
  bottom: -30px;
  font-size: 10px;
  color: var(--text-secondary);
}

.chart-axis {
  position: absolute;
  bottom: 20px;
  left: 40px;
  width: calc(100% - 80px);
  height: 1px;
  background-color: var(--border-color);
}

.y-axis {
  position: absolute;
  bottom: 20px;
  left: 40px;
  width: 1px;
  height: 230px;
  background-color: var(--border-color);
}

.y-label {
  position: absolute;
  left: 10px;
  font-size: 10px;
  color: var(--text-secondary);
}

/* Queue Activity Table */
.queue-activity {
  background-color: var(--card-bg);
  border-radius: 30px;
  padding: 20px;
  margin-bottom: 30px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: background-color 0.3s;
}

.queue-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  margin-top: 15px;
}

.queue-table th {
  text-align: left;
  padding: 12px 15px;
  font-size: 14px;
  font-weight: 600;
  color: var(--text-secondary);
  border-bottom: 1px solid var(--border-color);
}

.queue-table td {
  padding: 12px 15px;
  font-size: 14px;
  border-bottom: 1px solid var(--border-color);
  color: var(--text-color); /* Ensure table data text uses theme color */
  transition: color 0.3s ease;
}

.queue-table tr:last-child td {
  border-bottom: none;
}

.agent-status {
  display: inline-block;
  padding: 5px 15px;
  border-radius: 30px;
  font-size: 12px;
  font-weight: 500;
  background-color: var(--content-bg);
  color: var(--text-color);
  text-align: center;
  min-width: 100px;
  transition: background-color 0.3s ease, color 0.3s ease;
}

.status-available {
  background-color: var(--success-color);
  color: white;
}

.status-in-call {
  background-color: var(--accent-color);
  color: white;
}

.status-on-break {
  background-color: var(--pending-color);
  color: white;
}

/* Mobile menu button */
.mobile-menu-btn {
  display: none;
  position: fixed;
  top: 20px;
  left: 20px;
  z-index: 101;
  background-color: var(--content-bg);
  color: var(--text-color);
  border: none;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background-color 0.3s, color 0.3s;
}

/* Responsive styles */
@media (max-width: 768px) {
  .sidebar {
    position: fixed; /* Fixed position for mobile sidebar */
    transform: translateX(-250px); /* Hide by default on mobile */
    height: 100vh;
    width: 250px;
    border-radius: 0;
  }
  
  .sidebar.mobile-open {
    transform: translateX(0); /* Show when mobile-open */
  }
  
  .main-content {
    margin-left: 0 !important; /* No margin on mobile */
    width: 100% !important;
    padding: 15px;
  }
  
  .sidebar.collapsed + .main-content {
    margin-left: 0 !important;
  }
  
  .sidebar.mobile-open + .main-content {
     margin-left: 0 !important;
  }

  .mobile-menu-btn {
    display: flex;
  }
}

@media (min-width: 769px) {
  .sidebar {
    position: fixed;
    top: 0;
    bottom: 0;
    left: 0;
    width: 250px;
    transition: left 0.3s ease, width 0.3s ease; /* Transition left and width */
  }

  .sidebar.collapsed {
    left: -170px; /* Hide 170px of the sidebar */
    width: 250px; /* Keep the width for smooth transition */
  }

  .main-content {
    /* margin-left handled by computed style */
  }

  .mobile-menu-btn {
    display: none;
  }
}
</style>