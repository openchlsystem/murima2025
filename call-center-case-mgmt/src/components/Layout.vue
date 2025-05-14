
<template>
  <div class="layout">
    <div class="layout-container">
      <!-- Left collapsible sidebar -->
      <div class="sidebar" :class="{ collapsed: isCollapsed }">
        <button class="collapse-btn" @click="toggleSidebar">
          <span v-if="isCollapsed">›</span>
          <span v-else>‹</span>
        </button>
        <div class="sidebar-content" v-show="!isCollapsed">
          <slot name="sidebar"></slot>
        </div>
      </div>

      <!-- Main content area -->
      <div class="main-content">
        <slot></slot>
      </div>
    </div>
  </div>
</template>

<script>
import SideBar from './SideBar.vue'
export default {
  name: 'Layout',
  data() {
    return {
      isCollapsed: false
    }
  },
  methods: {
    toggleSidebar() {
      this.isCollapsed = !this.isCollapsed
    }
  }
}
</script>

<style scoped>
.layout {
  width: 100%;
  height: 100vh;
}

.layout-container {
  display: flex;
  height: 100%;
}

.sidebar {
  position: relative;
  background-color: #f5f5f5;
  width: 250px;
  transition: width 0.3s ease;
}

.sidebar.collapsed {
  width: 50px;
}

.collapse-btn {
  position: absolute;
  right: -15px;
  top: 20px;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background-color: #fff;
  border: 1px solid #ddd;
  cursor: pointer;
  z-index: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.sidebar-content {
  padding: 20px;
  overflow-y: auto;
  height: 100%;
}

.main-content {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}
</style>
