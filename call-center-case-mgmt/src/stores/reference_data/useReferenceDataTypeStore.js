// stores/useReferenceDataTypeStore.js
import { defineStore } from 'pinia'
import axios from 'axios'

export const useReferenceDataTypeStore = defineStore('referenceDataType', {
    state: () => ({
        types: [],
        currentType: null,
        isLoading: false,
        error: null,
    }),

    actions: {
        async fetchTypes() {
            this.isLoading = true
            try {
                const res = await axios.get('/reference-data/types/')
                this.types = res.data
            } catch (err) {
                this.error = err
            } finally {
                this.isLoading = false
            }
        },

        async fetchType(id) {
            this.isLoading = true
            try {
                const res = await axios.get(`/reference-data/types/${id}/`)
                this.currentType = res.data
            } catch (err) {
                this.error = err
            } finally {
                this.isLoading = false
            }
        },

        async createType(payload) {
            try {
                const res = await axios.post('/reference-data/types/', payload)
                this.types.push(res.data)
                return res.data
            } catch (err) {
                this.error = err
                throw err
            }
        },

        async updateType(id, payload) {
            try {
                const res = await axios.put(`/reference-data/types/${id}/`, payload)
                const index = this.types.findIndex(t => t.id === id)
                if (index !== -1) this.types[index] = res.data
                return res.data
            } catch (err) {
                this.error = err
                throw err
            }
        },

        async deleteType(id) {
            try {
                await axios.delete(`/reference-data/types/${id}/`)
                this.types = this.types.filter(t => t.id !== id)
            } catch (err) {
                this.error = err
                throw err
            }
        }
    }
})
