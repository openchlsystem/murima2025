<template>
    <div class="dropdown-wrapper">
        <button class="dropdown-button" @click="isOpen = !isOpen" @blur="isOpen = false">
            {{ selectedLabel || label }}
            <span class="dropdown-arrow">▼</span>
        </button>

        <div class="dropdown-menu" v-show="isOpen">
            <button v-for="(item, index) in items" :key="index" @click="selectItem(item)" @mousedown.prevent
                class="dropdown-item">
                {{ item.label }}
            </button>
        </div>
    </div>
</template>

<script>
    import { ref, onMounted } from 'vue'

    export default {
        name: 'DropdownMenu',
        props: {
            items: {
                type: Array,
                required: true,
            },
            modelValue: {
                type: [String, Number, Object],
                default: null,
            },
            label: {
                type: String,
                default: 'Select',
            },
        },
        emits: ['update:modelValue'],
        setup(props, { emit }) {
            const selectedLabel = ref('')
            const isOpen = ref(false)

            const selectItem = (item) => {
                emit('update:modelValue', item.value)
                selectedLabel.value = item.label
                isOpen.value = false
            }

            onMounted(() => {
                const selected = props.items.find((item) => item.value === props.modelValue)
                if (selected) selectedLabel.value = selected.label
            })

            return {
                selectedLabel,
                selectItem,
                isOpen,
            }
        },
    }
</script>

<style scoped>
    .dropdown-wrapper {
        position: fixed;
        right: 16px;
        top: 16px;
        display: inline-block;
        width: 200px;
        margin: 0 auto;
        font-family: Arial, sans-serif;
        font-size: 14px;
        color: #333;
        text-align: left;
        cursor: pointer;
        z-index: 1000;
    }

    .dropdown-button {
        padding: 8px 16px;
        border: 1px solid #ccc;
        border-radius: 4px;
        background: white;
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .dropdown-arrow {
        font-size: 12px;
    }

    .dropdown-menu {
        position: absolute;
        top: 100%;
        left: 0;
        margin-top: 4px;
        border: 1px solid #ccc;
        border-radius: 4px;
        background: white;
        min-width: 160px;
        z-index: 1;
    }

    .dropdown-item {
        display: block;
        width: 100%;
        padding: 8px 16px;
        text-align: left;
        background: none;
        border: none;
        cursor: pointer;
    }

    .dropdown-item:hover {
        background: #f0f0f0;
    }
</style>