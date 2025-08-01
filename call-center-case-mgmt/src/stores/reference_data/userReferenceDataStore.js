// stores/useReferenceDataStore.js
import { defineStore } from 'pinia'
import axios from 'axios'

export const useReferenceDataStore = defineStore('referenceData', {
    state: () => ({
        entries: [],
        currentEntry: null,
        history: [],
        isLoading: false,
        error: null,
    }),

    actions: {
        async fetchEntries() {
            this.isLoading = true
            try {
                const res = await axios.get('/reference-data/entries/')
                this.entries = res.data
            } catch (err) {
                this.error = err
            } finally {
                this.isLoading = false
            }
        },

        async fetchEntry(id) {
            this.isLoading = true
            try {
                const res = await axios.get(`/reference-data/entries/${id}/`)
                this.currentEntry = res.data
            } catch (err) {
                this.error = err
            } finally {
                this.isLoading = false
            }
        },

        async createEntry(payload) {
            try {
                const res = await axios.post('/reference-data/entries/', payload)
                this.entries.push(res.data)
                return res.data
            } catch (err) {
                this.error = err
                throw err
            }
        },

        async updateEntry(id, payload) {
            try {
                const res = await axios.put(`/reference-data/entries/${id}/`, payload)
                const index = this.entries.findIndex(e => e.id === id)
                if (index !== -1) this.entries[index] = res.data
                return res.data
            } catch (err) {
                this.error = err
                throw err
            }
        },

        async deleteEntry(id) {
            try {
                await axios.delete(`/reference-data/entries/${id}/`)
                this.entries = this.entries.filter(e => e.id !== id)
            } catch (err) {
                this.error = err
                throw err
            }
        },

        async fetchEntryHistory() {
            this.isLoading = true
            try {
                const res = await axios.get('/reference-data/history/')
                this.history = res.data
            } catch (err) {
                this.error = err
            } finally {
                this.isLoading = false
            }
        },

        async fetchHistoryDetail(id) {
            try {
                const res = await axios.get(`/reference-data/history/${id}/`)
                return res.data
            } catch (err) {
                this.error = err
                throw err
            }
        }
    }
})
