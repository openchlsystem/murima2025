import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '@/stores/auth'; // ✅ Make sure path is correct

import Login from '../pages/Login.vue';
import Dashboard from '../pages/Dashboard.vue';
import Calls from '../pages/Calls.vue';
import Cases from '../pages/Cases.vue';
import Chats from '../pages/Chats.vue';
import QAStatistics from '../pages/QAStatistics.vue';
import Wallboard from '../pages/Wallboard.vue';
import Settings from '../pages/Settings.vue';
import EditProfile from '../pages/EditProfile.vue';
import CaseCreation from '../pages/CaseCreation.vue';
import SuperAdmin from '../pages/SuperAdminDashboard.vue';
import AdminPanel from '../pages/AdminPanel.vue';
import TestCall from '../pages/TestCall.vue';

const routes = [
  { path: '/', component: Login },
  { path: '/dashboard', component: Dashboard, meta: { requiresAuth: true } },
  { path: '/calls', component: Calls, meta: { requiresAuth: true } },
  { path: '/cases', component: Cases, meta: { requiresAuth: true } },
  { path: '/chats', component: Chats, meta: { requiresAuth: true } },
  { path: '/qa-statistics', component: QAStatistics, meta: { requiresAuth: true } },
  { path: '/wallboard', component: Wallboard, meta: { requiresAuth: true } },
  { path: '/settings', component: Settings, meta: { requiresAuth: true } },
  { path: '/edit-profile', component: EditProfile, meta: { requiresAuth: true } },
  { path: '/case-creation', component: CaseCreation, meta: { requiresAuth: true } },
  { path: '/superadmin', component: SuperAdmin, meta: { requiresAuth: true } },
  { path: '/admin', component: AdminPanel, meta: { requiresAuth: true } },
  { path: '/test-call', component: TestCall, meta: { requiresAuth: true } },
];

export const router = createRouter({
  history: createWebHistory(),
  routes
});

// ✅ Global navigation guard to protect routes
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();

  if (to.meta.requiresAuth && !authStore.accessToken) {
    next({
      path: '/',
      query: { redirect: to.fullPath }
    });
  } else {
    next();
  }
});
