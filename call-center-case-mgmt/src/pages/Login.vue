<template>
  <div class="login-container">
    <div class="login-card">
      <div class="logo-container">
        <img src="/Openchs logo-1.png" alt="OpenCHS Logo" class="logo">
      </div>
      
      <h1>Log in to your account</h1>
      
      <div class="input-group">
        <input type="email" placeholder="Email" v-model="email">
      </div>
      
      <div class="input-group">
        <input type="password" placeholder="Password" v-model="password">
        <a href="#" class="forgot-password" @click.prevent="handleForgotPassword">Forgot Password?</a>
      </div>
      
      <button class="login-button" @click="handleLogin">Log in</button>
      
      <div class="help-text">
        Reach out to us? <a href="#" class="help-link" @click.prevent="handleHelp">Help</a>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const email = ref('')
const password = ref('')

const handleLogin = async () => {
  try {
    // TODO: Implement actual login logic
    await router.push('/dashboard')
  } catch (error) {
    console.error('Login failed:', error)
  }
}

const handleForgotPassword = () => {
  // TODO: Implement forgot password logic
  console.log('Forgot password clicked')
}

const handleHelp = () => {
  // TODO: Implement help logic
  console.log('Help clicked')
}
</script>

<style>
:root {
  --background-color: #1a1a1a;
  --content-bg: #2a2a2a;
  --text-color: #ffffff;
  --text-secondary: #999999;
  --border-color: #3a3a3a;
  --accent-color: #964B00;
  --accent-hover: #b25900;
  --input-bg: #3a3a3a;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Inter', sans-serif;
  font-weight: 600;
}

.login-container {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: var(--background-color);
  padding: 20px;
}

.login-card {
  background-color: var(--content-bg);
  width: 400px;
  padding: 40px;
  border-radius: 24px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

.logo-container {
  text-align: center;
  margin-bottom: 24px;
}

.logo {
  width: 48px;
  height: 48px;
  object-fit: contain;
}

h1 {
  font-size: 20px;
  margin-bottom: 32px;
  color: var(--text-color);
  text-align: center;
  font-weight: 500;
}

.input-group {
  margin-bottom: 24px;
  position: relative;
}

input {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid var(--border-color);
  border-radius: 12px;
  font-size: 14px;
  background-color: var(--input-bg);
  color: var(--text-color);
  transition: border-color 0.2s;
  font-weight: 600;
}

input:focus {
  border-color: var(--accent-color);
  outline: none;
}

input::placeholder {
  color: var(--text-secondary);
}

.forgot-password {
  position: absolute;
  right: 0;
  top: calc(100% + 8px);
  font-size: 13px;
  color: var(--accent-color);
  text-decoration: none;
}

.login-button {
  width: 100%;
  padding: 12px;
  background-color: var(--accent-color);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  margin: 32px 0 24px;
  transition: background-color 0.2s;
}

.login-button:hover {
  background-color: var(--accent-hover);
}

.help-text {
  text-align: center;
  font-size: 13px;
  color: var(--text-color);
}

.help-link {
  color: var(--accent-color);
  text-decoration: none;
  margin-left: 4px;
}
</style>