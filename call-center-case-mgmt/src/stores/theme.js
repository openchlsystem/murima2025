import { defineStore } from 'pinia'
import { ref, watch } from 'vue'
import { applyTheme, getCurrentTheme } from '../utils/theme.js'

export const useThemeStore = defineStore('theme', () => {
  // State
  const currentTheme = ref('light')
  const isInitialized = ref(false)

  // Initialize theme from localStorage or default
  const initializeTheme = () => {
    if (isInitialized.value) return
    
    const savedTheme = localStorage.getItem('theme') || 'light'
    currentTheme.value = savedTheme
    applyTheme(currentTheme.value)
    isInitialized.value = true
  }

  // Toggle theme
  const toggleTheme = () => {
    const newTheme = currentTheme.value === 'dark' ? 'light' : 'dark'
    setTheme(newTheme)
  }

  // Set specific theme
  const setTheme = (theme) => {
    currentTheme.value = theme
    localStorage.setItem('theme', theme)
    applyTheme(theme)
  }

  // Watch for theme changes and apply them
  watch(currentTheme, (newTheme) => {
    applyTheme(newTheme)
  })

  return {
    currentTheme,
    isInitialized,
    initializeTheme,
    toggleTheme,
    setTheme
  }
}) 