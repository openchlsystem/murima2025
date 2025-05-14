<template>
  <aside class="sidebar">
    <div class="sidebar-header">
      <!-- <img src="@/assets/logo.svg" alt="Logo" class="logo" /> -->
    </div>

    <nav class="sidebar-nav">
      <router-link to="/dashboard" class="nav-item">
        <i class="fas fa-home"></i>
        <span>Dashboard</span>
      </router-link>

      <div class="nav-group">
        <h3 class="nav-title">Communication</h3>
        <router-link to="/calls" class="nav-item">
          <i class="fas fa-phone"></i>
          <span>Calls</span>
        </router-link>
        <router-link to="/messages" class="nav-item">
          <i class="fas fa-comment"></i>
          <span>Messages</span>
        </router-link>
      </div>

      <div class="nav-group">
        <h3 class="nav-title">Management</h3>
        <router-link to="/cases" class="nav-item">
          <i class="fas fa-folder"></i>
          <span>Cases</span>
        </router-link>
        <router-link to="/admin" class="nav-item">
          <i class="fas fa-users"></i>
          <span>User Management</span>
        </router-link>
      </div>

      <div class="nav-group">
        <h3 class="nav-title">Analytics</h3>
        <router-link to="/analytics" class="nav-item">
          <i class="fas fa-chart-bar"></i>
          <span>Reports</span>
        </router-link>
      </div>
    </nav>
  </aside>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const isCollapsed = ref(false)
</script>

<style scoped>
.sidebar {
  min-width: 260px;
  min-height: 100vh;
  background-color: #1a1a1a;
  color: #ffffff;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  transition: width 0.3s ease;
}

.sidebar-header {
  padding: 1rem 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.logo {
  height: 40px;
}

.sidebar-nav {
  margin-top: 2rem;
  padding: 0 1rem;
}

.nav-group {
  margin-bottom: 2rem;
}

.nav-title {
  font-size: 0.75rem;
  text-transform: uppercase;
  color: #666;
  margin-bottom: 0.5rem;
  padding-left: 0.5rem;
}

.nav-item {
  display: flex;
  align-items: center;
  padding: 0.75rem 1rem;
  color: #ffffff;
  text-decoration: none;
  border-radius: 0.5rem;
  margin-bottom: 0.25rem;
  transition: background-color 0.2s ease;
}

.nav-item:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.nav-item.active {
  background-color: rgba(255, 255, 255, 0.2);
}

.nav-item i {
  margin-right: 0.75rem;
  width: 20px;
  text-align: center;
}

.nav-item span {
  font-size: 0.875rem;
}
</style>
