import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import { router } from './router'
import { useThemeStore } from './stores/theme.js'
import axiosInstance from './utils/axios.js'

const app = createApp(App)
const pinia = createPinia()

// Add error handling
app.config.errorHandler = (err, vm, info) => {
  console.error('Vue Error:', err)
  console.error('Error Info:', info)
}

// Add global error handler
window.addEventListener('error', (event) => {
  console.error('Global Error:', event.error)
})

app.use(pinia)
app.use(router)
app.use(axiosInstance)
// app.use(i18n)

// Initialize theme store
const themeStore = useThemeStore()
themeStore.initializeTheme()

// Add debugging
console.log('Mounting app...')
app.mount('#app')
console.log('App mounted')
