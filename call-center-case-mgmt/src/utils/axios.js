import axios from 'axios';
import { useAuthStore } from '@/stores/auth';

// Auto-detect baseURL
const isLocalhost = window.location.hostname === 'localhost' ||
  window.location.hostname === '127.0.0.1' ||
  window.location.hostname === '0.0.0.0';

const baseURL = import.meta.env.VITE_API_URL ||
  (isLocalhost ? 'http://acme-healthcare.localhost:8520/api/v1' : window.location.origin);

const axiosInstance = axios.create({
  baseURL,
  timeout: 10000, // 10 seconds timeout
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
});

// Request interceptor
axiosInstance.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore();

    // Log request details in development
    if (import.meta.env.DEV) {
      console.log('Request:', {
        url: config.url,
        method: config.method,
        data: config.data,
        params: config.params
      });
    }

    // Add authorization token if available
    if (authStore.accessToken) {
      config.headers.Authorization = `Bearer ${authStore.accessToken}`;
    }

    return config;
  },
  (error) => {
    if (import.meta.env.DEV) {
      console.error('Request Error Interceptor:', error);
    }
    return Promise.reject(error);
  }
);

// Response interceptor
axiosInstance.interceptors.response.use(
  (response) => {
    const authStore = useAuthStore();

    // If this is a login response, store the auth data
    if (response.config.url.includes('/auth/login/') && response.data.access_token) {
      authStore.setAuthData(response.data);
    }

    // Log response details in development
    if (import.meta.env.DEV) {
      console.log('Response:', {
        status: response.status,
        data: response.data,
        url: response.config.url
      });
    }
    return response;
  },
  async (error) => {
    const authStore = useAuthStore();

    if (import.meta.env.DEV) {
      console.error('Response Error Interceptor:', error);
    }

    const originalRequest = error.config;
    const status = error.response?.status;

    // Handle token refresh when access token expires
    if (status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        if (!authStore.refreshToken) {
          throw new Error('No refresh token available');
        }

        // Request new access token
        const response = await axios.post(`${baseURL}/auth/token/refresh/`, {
          refresh: authStore.refreshToken
        });

        // Update auth store with new tokens
        authStore.setAuthData({
          access_token: response.data.access,
          refresh_token: response.data.refresh || authStore.refreshToken, // Keep old refresh if new one isn't provided
          user: authStore.user,
          session_id: authStore.sessionId
        });

        // Update authorization header
        originalRequest.headers.Authorization = `Bearer ${response.data.access}`;

        // Retry original request
        return axiosInstance(originalRequest);
      } catch (refreshError) {
        // Token refresh failed - clear auth data
        authStore.clearAuthData();

        if (!window.location.pathname.includes('/login')) {
          window.location.href = '/login?redirect=' + encodeURIComponent(window.location.pathname);
        }
        return Promise.reject(refreshError);
      }
    }

    // Handle other error cases
    if (status === 403) {
      return Promise.reject(new Error('You do not have permission to access this resource.'));
    }

    if (status === 404) {
      return Promise.reject(new Error('The requested resource was not found.'));
    }

    if (status === 429) {
      const retryAfter = error.response.headers['retry-after'] || 5;
      return Promise.reject(new Error(`Too many requests. Please try again after ${retryAfter} seconds.`));
    }

    if (status >= 500) {
      return Promise.reject(new Error('A server error occurred. Please try again later.'));
    }

    if (error.code === 'ECONNABORTED') {
      return Promise.reject(new Error('Request timeout. Please check your network connection.'));
    }

    if (!error.response) {
      return Promise.reject(new Error('Network error. Please check your internet connection.'));
    }

    return Promise.reject(error);
  }
);

export default axiosInstance;