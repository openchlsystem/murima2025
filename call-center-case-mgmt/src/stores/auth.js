import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAuthStore = defineStore('auth', () => {
    const accessToken = ref(localStorage.getItem('access_token') || null)
    const refreshToken = ref(localStorage.getItem('refresh_token') || null)
    const user = ref(JSON.parse(localStorage.getItem('user') || 'null'))
    const sessionId = ref(localStorage.getItem('session_id') || null)

    function setAuthData(data) {
        accessToken.value = data.access_token
        refreshToken.value = data.refresh_token
        user.value = data.user
        sessionId.value = data.session_id

        // Persist to localStorage
        localStorage.setItem('access_token', data.access_token)
        localStorage.setItem('refresh_token', data.refresh_token)
        localStorage.setItem('user', JSON.stringify(data.user))
        localStorage.setItem('session_id', data.session_id)
    }

    function clearAuthData() {
        accessToken.value = null
        refreshToken.value = null
        user.value = null
        sessionId.value = null

        // Clear localStorage
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        localStorage.removeItem('user')
        localStorage.removeItem('session_id')
    }

    return {
        accessToken,
        refreshToken,
        user,
        sessionId,
        setAuthData,
        clearAuthData
    }
})