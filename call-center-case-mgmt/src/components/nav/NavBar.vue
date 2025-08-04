<template>
    <nav class="bg-white border-b border-gray-200 shadow-sm px-4 py-2 flex items-center justify-between">
        <!-- Left slot: brand / logo -->
        <div class="flex items-center space-x-2">
            <slot name="left">
                <router-link to="/" class="text-xl font-bold text-blue-600">MyApp</router-link>
            </slot>
        </div>

        <!-- Center slot: nav items -->
        <div class="hidden md:flex space-x-6">
            <slot name="center">
                <router-link v-for="(item, i) in items" :key="i" :to="item.to"
                    class="text-gray-700 hover:text-blue-600 font-medium" active-class="text-blue-600 underline">
                    {{ item.label }}
                </router-link>
            </slot>
        </div>

        <!-- Right slot: buttons / profile / dropdown -->
        <div class="flex items-center space-x-2">
            <slot name="right">
                <!-- Example right item -->
                <button class="px-3 py-1 bg-blue-600 text-white rounded hover:bg-blue-700">Login</button>
            </slot>
        </div>

        <!-- Mobile toggle -->
        <button @click="toggleMobile" class="md:hidden ml-2 text-gray-600 focus:outline-none">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path v-if="!isMobileOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M4 6h16M4 12h16M4 18h16" />
                <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
        </button>
    </nav>

    <!-- Mobile menu -->
    <div v-if="isMobileOpen" class="md:hidden px-4 py-2 space-y-2 bg-white border-b border-gray-200 shadow-sm">
        <slot name="mobile">
            <router-link v-for="(item, i) in items" :key="i" :to="item.to"
                class="block text-gray-700 hover:text-blue-600" @click="closeMobile">
                {{ item.label }}
            </router-link>
        </slot>
    </div>
</template>

<script setup>
    import { ref } from 'vue'

    const props = defineProps({
        items: {
            type: Array,
            default: () => [],
            // Example: [{ label: 'Home', to: '/' }, { label: 'About', to: '/about' }]
        },
    })

    const isMobileOpen = ref(false)

    const toggleMobile = () => {
        isMobileOpen.value = !isMobileOpen.value
    }

    const closeMobile = () => {
        isMobileOpen.value = false
    }
</script>
