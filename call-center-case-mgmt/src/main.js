import { createApp } from 'vue'
import './assets/reset.css'
import './assets/root.css'
import App from './App.vue'
import router from './router/index.js'

createApp(App).mount('#app', router)
