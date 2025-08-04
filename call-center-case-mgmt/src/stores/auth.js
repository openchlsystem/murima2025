import { defineStore } from 'pinia'
import { ref } from 'vue'

// Define the 'auth' store using Pinia's Composition API style
export const useAuthStore = defineStore('auth', () => {
    // Reactive state variables for authentication tokens and user data
    const accessToken = ref(localStorage.getItem('access_token') || null)
    const refreshToken = ref(localStorage.getItem('refresh_token') || null)
    const user = ref(JSON.parse(localStorage.getItem('user') || 'null'))
    const sessionId = ref(localStorage.getItem('session_id') || null)

    /**
     * Sets authentication data after a successful login or token refresh.
     * Also persists the data to localStorage for session restoration.
     *
     * @param {Object} data - The auth response containing tokens and user info
     */
    function setAuthData(data) {
        accessToken.value = data.access_token
        refreshToken.value = data.refresh_token
        user.value = data.user
        sessionId.value = data.session_id

        // Save to localStorage for persistence across reloads
        localStorage.setItem('access_token', data.access_token)
        localStorage.setItem('refresh_token', data.refresh_token)
        localStorage.setItem('user', JSON.stringify(data.user))
        localStorage.setItem('session_id', data.session_id)
    }

    /**
     * Clears authentication data from state and localStorage.
     * Useful during logout or when token refresh fails.
     */
    function clearAuthData() {
        accessToken.value = null
        refreshToken.value = null
        user.value = null
        sessionId.value = null

        // Remove data from localStorage to fully clear the session
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        localStorage.removeItem('user')
        localStorage.removeItem('session_id')
    }

    // Expose state and actions to components
    return {
        accessToken,
        refreshToken,
        user,
        sessionId,
        setAuthData,
        clearAuthData
    }
})
