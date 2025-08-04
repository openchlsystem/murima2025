<template>
    <div v-if="show" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
        <div class="bg-white rounded-lg shadow-xl max-w-lg w-full p-6 relative">
            <!-- Close button -->
            <button @click="emitClose" class="absolute top-3 right-3 text-gray-400 hover:text-gray-600">
                ✕
            </button>

            <!-- Modal Header -->
            <div v-if="title" class="mb-4 text-xl font-semibold text-gray-800">
                {{ title }}
            </div>

            <!-- Modal Body -->
            <div class="text-gray-700">
                <slot />
            </div>

            <!-- Modal Footer -->
            <div v-if="$slots.footer" class="mt-6 flex justify-end space-x-2">
                <slot name="footer" />
            </div>
        </div>
    </div>
</template>

<script setup>
    defineProps({
        show: Boolean,
        title: String,
    })

    const emit = defineEmits(['close'])

    function emitClose() {
        emit('close')
    }
</script>
