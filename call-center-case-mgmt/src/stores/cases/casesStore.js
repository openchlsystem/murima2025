// casesStore.js - Store module for cases
import { defineStore } from 'pinia'
import axios from '@/utils/axios'

export const useCasesStore = defineStore('cases', {
  state: () => ({
    cases: [],
    caseTypes: [],
    caseStatuses: [],
    myAssignedCases: [],
    myTeamCases: [],
    caseDocuments: {},
    caseNotes: {},
    caseHistory: {},
    caseLinks: {},
    caseTemplates: [],
    slas: [],
    workflowRules: [],
    auditLogs: [],
    loading: false,
    error: null
  }),

  actions: {
    // Case Types
    async fetchCaseTypes() {
      try {
        const response = await axios.get('cases/case-types/')
        this.caseTypes = response.data
      } catch (error) {
        this.error = error.message
      }
    },

    async getCaseType(id) {
      try {
        const response = await axios.get(`cases/case-types/${id}/`)
        return response.data
      } catch (error) {
        this.error = error.message
      }
    },

    // Case Statuses
    async fetchCaseStatuses() {
      try {
        const response = await axios.get('cases/case-statuses/')
        this.caseStatuses = response.data
      } catch (error) {
        this.error = error.message
      }
    },

    async getCaseStatus(id) {
      try {
        const response = await axios.get(`cases/case-statuses/${id}/`)
        return response.data
      } catch (error) {
        this.error = error.message
      }
    },

    // Cases
    async fetchCases() {
      try {
        const response = await axios.get('cases/cases/')
        this.cases = response.data
      } catch (error) {
        this.error = error.message
      }
    },

    async getCase(id) {
      try {
        const response = await axios.get(`cases/cases/${id}/`)
        return response.data
      } catch (error) {
        this.error = error.message
      }
    },

    async createCase(caseData) {
      try {
        const response = await axios.post('cases/cases/', caseData)
        this.cases.push(response.data)
        return response.data
      } catch (error) {
        this.error = error.message
      }
    },

    async updateCase(id, caseData) {
      try {
        const response = await axios.put(`cases/cases/${id}/`, caseData)
        const index = this.cases.findIndex(c => c.id === id)
        if (index !== -1) this.cases[index] = response.data
        return response.data
      } catch (error) {
        this.error = error.message
      }
    },

    async deleteCase(id) {
      try {
        await axios.delete(`cases/cases/${id}/`)
        this.cases = this.cases.filter(c => c.id !== id)
      } catch (error) {
        this.error = error.message
      }
    },

    // My Assigned Cases
    async fetchMyAssignedCases() {
      try {
        const response = await axios.get('cases/my-assigned-cases/')
        this.myAssignedCases = response.data
      } catch (error) {
        this.error = error.message
      }
    },

    // My Team Cases
    async fetchMyTeamCases() {
      try {
        const response = await axios.get('cases/my-team-cases/')
        this.myTeamCases = response.data
      } catch (error) {
        this.error = error.message
      }
    },

    // Case Documents
    async fetchCaseDocuments(caseId) {
      try {
        const response = await axios.get(`cases/cases/${caseId}/documents/`)
        this.caseDocuments[caseId] = response.data
      } catch (error) {
        this.error = error.message
      }
    },

    // Case Notes
    async fetchCaseNotes(caseId) {
      try {
        const response = await axios.get(`cases/cases/${caseId}/notes/`)
        this.caseNotes[caseId] = response.data
      } catch (error) {
        this.error = error.message
      }
    },

    // Case History
    async fetchCaseHistory(caseId) {
      try {
        const response = await axios.get(`cases/cases/${caseId}/history/`)
        this.caseHistory[caseId] = response.data
      } catch (error) {
        this.error = error.message
      }
    },

    // Case Links
    async fetchCaseLinks(caseId) {
      try {
        const response = await axios.get(`cases/cases/${caseId}/links/`)
        this.caseLinks[caseId] = response.data
      } catch (error) {
        this.error = error.message
      }
    },

    // Case Templates
    async fetchCaseTemplates() {
      try {
        const response = await axios.get('cases/case-templates/')
        this.caseTemplates = response.data
      } catch (error) {
        this.error = error.message
      }
    },

    async getCaseTemplate(id) {
      try {
        const response = await axios.get(`cases/case-templates/${id}/`)
        return response.data
      } catch (error) {
        this.error = error.message
      }
    },

    // SLAs
    async fetchSLAs() {
      try {
        const response = await axios.get('cases/slas/')
        this.slas = response.data
      } catch (error) {
        this.error = error.message
      }
    },

    async getSLA(id) {
      try {
        const response = await axios.get(`cases/slas/${id}/`)
        return response.data
      } catch (error) {
        this.error = error.message
      }
    },

    // Workflow Rules
    async fetchWorkflowRules() {
      try {
        const response = await axios.get('cases/workflow-rules/')
        this.workflowRules = response.data
      } catch (error) {
        this.error = error.message
      }
    },

    async getWorkflowRule(id) {
      try {
        const response = await axios.get(`cases/workflow-rules/${id}/`)
        return response.data
      } catch (error) {
        this.error = error.message
      }
    },

    // Audit Logs
    async fetchAuditLogs() {
      try {
        const response = await axios.get('cases/audit-logs/')
        this.auditLogs = response.data
      } catch (error) {
        this.error = error.message
      }
    }
  },

  getters: {
    getCaseById: (state) => (id) => {
      return state.cases.find(c => c.id === id)
    },
    getCaseDocumentsById: (state) => (caseId) => {
      return state.caseDocuments[caseId] || []
    },
    getCaseNotesById: (state) => (caseId) => {
      return state.caseNotes[caseId] || []
    },
    getCaseHistoryById: (state) => (caseId) => {
      return state.caseHistory[caseId] || []
    },
    getCaseLinksById: (state) => (caseId) => {
      return state.caseLinks[caseId] || []
    }
  }
})
