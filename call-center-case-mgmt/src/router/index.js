import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue' // Adjust the path as needed

const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home
    },
    // Add more routes here
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router