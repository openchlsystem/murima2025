<template>
    <div class="reference-data-crud">
        <!-- Tabs Navigation -->
        <div class="tabs-header">
            <button @click="activeTab = 'entries'" :class="{ active: activeTab === 'entries' }" class="tab-btn">
                Entries
            </button>
            <button @click="activeTab = 'types'" :class="{ active: activeTab === 'types' }" class="tab-btn">
                Types
            </button>
            <button @click="activeTab = 'history'" :class="{ active: activeTab === 'history' }" class="tab-btn">
                History
            </button>

            <div class="actions">
                <button v-if="activeTab === 'entries'" @click="openCreateForm" class="btn btn-primary">
                    <i class="fas fa-plus"></i> Add New Entry
                </button>
                <button v-if="activeTab === 'types'" @click="openCreateTypeForm" class="btn btn-primary">
                    <i class="fas fa-plus"></i> Add New Type
                </button>
            </div>
        </div>

        <!-- Tab Content -->
        <div class="tab-content">
            <!-- Entries Tab -->
            <div v-if="activeTab === 'entries'" class="tab-pane">
                <div class="filters mb-3">
                    <div class="row">
                        <div class="col-md-4">
                            <label>Data Type</label>
                            <select v-model="filters.dataType" class="form-control" @change="fetchData">
                                <option value="">All Types</option>
                                <option v-for="type in referenceDataTypes" :value="type?.id" :key="type?.id">
                                    {{ type?.name || 'Unnamed Type' }}
                                </option>
                            </select>
                        </div>
                        <div class="col-md-4">
                            <label>Status</label>
                            <select v-model="filters.isActive" class="form-control" @change="fetchData">
                                <option value="">All</option>
                                <option value="true">Active</option>
                                <option value="false">Inactive</option>
                            </select>
                        </div>
                        <div class="col-md-4">
                            <label>Search</label>
                            <input type="text" v-model="filters.search" class="form-control"
                                placeholder="Search by code or display value" @input="debounceFetch" />
                        </div>
                    </div>
                </div>

                <div class="table-responsive">
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>Type</th>
                                <th>Code</th>
                                <th>Display Value</th>
                                <th>Status</th>
                                <th>Sort Order</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            <template v-if="referenceData?.length">
                                <tr v-for="item in referenceData" :key="item?.id || Math.random()">
                                    <td>{{ getDataTypeName(item?.data_type) || '-' }}</td>
                                    <td>{{ item?.code || '-' }}</td>
                                    <td>{{ item?.display_value || '-' }}</td>
                                    <td>
                                        <span :class="['status-badge', item?.is_active ? 'active' : 'inactive']">
                                            {{ item?.is_active ? 'Active' : 'Inactive' }}
                                        </span>
                                    </td>
                                    <td>{{ item?.sort_order ?? '-' }}</td>
                                    <td>
                                        <div class="table-actions">
                                            <button v-if="item" class="action-btn edit-btn" @click="openEditForm(item)"
                                                title="Edit">
                                                <i class="fas fa-edit"></i>
                                            </button>
                                            <button v-if="item" class="action-btn delete-btn"
                                                @click="confirmDelete(item)" title="Delete">
                                                <i class="fas fa-trash"></i>
                                            </button>
                                        </div>
                                    </td>
                                </tr>
                            </template>
                            <tr v-else>
                                <td colspan="6" class="text-center py-4">No entries found</td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <div class="pagination" v-if="pagination.totalPages > 1">
                    <button @click="changePage(pagination.currentPage - 1)" :disabled="pagination.currentPage === 1"
                        class="btn btn-outline-primary">
                        Previous
                    </button>
                    <span class="mx-3">
                        Page {{ pagination.currentPage }} of {{ pagination.totalPages }}
                    </span>
                    <button @click="changePage(pagination.currentPage + 1)"
                        :disabled="pagination.currentPage === pagination.totalPages" class="btn btn-outline-primary">
                        Next
                    </button>
                </div>
            </div>

            <!-- Types Tab -->
            <div v-if="activeTab === 'types'" class="tab-pane">
                <div class="table-responsive">
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>Name</th>
                                <th>Description</th>
                                <th>Code</th>
                                <th>System Managed</th>
                                <th>Tenant Specific</th>
                                <th>Metadata Keys</th>
                                <th>Validation</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            <template v-if="referenceDataTypes?.length">
                                <tr v-for="type in referenceDataTypes" :key="type?.id || Math.random()">
                                    <td>{{ type?.name || '-' }}</td>
                                    <td>{{ type?.description || '-' }}</td>
                                    <td>{{ type?.code || '-' }}</td>
                                    <td>
                                        <span :class="['status-badge', type?.is_system_managed ? 'system' : 'custom']">
                                            {{ type?.is_system_managed ? 'System' : 'Custom' }}
                                        </span>
                                    </td>
                                    <td>
                                        <span :class="['status-badge', type?.is_tenant_specific ? 'active' : 'inactive']">
                                            {{ type?.is_tenant_specific ? 'Yes' : 'No' }}
                                        </span>
                                    </td>
                                    <td>
                                        <span v-if="type?.allowed_metadata_keys?.length">
                                            {{ type.allowed_metadata_keys.join(', ') }}
                                        </span>
                                        <span v-else class="text-muted">None</span>
                                    </td>
                                    <td>
                                        <span v-if="type?.validation_schema">
                                            <span v-if="type.validation_schema.required?.length">
                                                Required: {{ type.validation_schema.required.join(', ') }}
                                            </span>
                                            <span v-else class="text-muted">None</span>
                                        </span>
                                        <span v-else class="text-muted">None</span>
                                    </td>
                                    <td>
                                        <div class="table-actions">
                                            <button v-if="type && !type.is_system_managed" class="action-btn edit-btn"
                                                @click="openEditTypeForm(type)" title="Edit">
                                                <i class="fas fa-edit"></i>
                                            </button>
                                            <button v-if="type && !type.is_system_managed" class="action-btn delete-btn"
                                                @click="confirmDeleteType(type)" title="Delete">
                                                <i class="fas fa-trash"></i>
                                            </button>
                                        </div>
                                    </td>
                                </tr>
                            </template>
                            <tr v-else>
                                <td colspan="8" class="text-center py-4">No types found</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- History Tab -->
            <div v-if="activeTab === 'history'" class="tab-pane">
                <div class="table-responsive">
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>Date</th>
                                <th>Action</th>
                                <th>User</th>
                                <th>Type</th>
                                <th>Details</th>
                            </tr>
                        </thead>
                        <tbody>
                            <template v-if="historyLogs?.length">
                                <tr v-for="log in historyLogs" :key="log?.id || Math.random()">
                                    <td>{{ log?.timestamp ? formatDate(log.timestamp) : '-' }}</td>
                                    <td>
                                        <span :class="['status-badge', log?.action?.toLowerCase() || '']">
                                            {{ log?.action || '-' }}
                                        </span>
                                    </td>
                                    <td>{{ log?.user || '-' }}</td>
                                    <td>{{ log?.object_type || '-' }}</td>
                                    <td>{{ log?.details || '-' }}</td>
                                </tr>
                            </template>
                            <tr v-else>
                                <td colspan="5" class="text-center py-4">No history records found</td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <div class="pagination" v-if="historyPagination.totalPages > 1">
                    <button @click="changeHistoryPage(historyPagination.currentPage - 1)"
                        :disabled="historyPagination.currentPage === 1" class="btn btn-outline-primary">
                        Previous
                    </button>
                    <span class="mx-3">
                        Page {{ historyPagination.currentPage }} of {{ historyPagination.totalPages }}
                    </span>
                    <button @click="changeHistoryPage(historyPagination.currentPage + 1)"
                        :disabled="historyPagination.currentPage === historyPagination.totalPages"
                        class="btn btn-outline-primary">
                        Next
                    </button>
                </div>
            </div>
        </div>

        <!-- Entry Form Modal -->
        <Modal v-if="showEntryForm" @close="closeEntryForm">
            <template #header>
                <h3>{{ formTitle }}</h3>
            </template>
            <template #body>
                <form @submit.prevent="submitForm">
                    <div class="row">
                        <div class="col-md-6">
                            <div class="mb-3">
                                <label class="form-label">Data Type *</label>
                                <select v-model="formData.data_type" class="form-control" :disabled="isEditing"
                                    required>
                                    <option value="">Select a data type</option>
                                    <option v-for="type in referenceDataTypes" :value="type.id" :key="type.id">
                                        {{ type.name }}
                                    </option>
                                </select>
                            </div>
                        </div>

                        <div class="col-md-6">
                            <div class="mb-3">
                                <label class="form-label">Code *</label>
                                <input type="text" v-model="formData.code" class="form-control" required
                                    :disabled="isSystemManaged" />
                            </div>
                        </div>
                    </div>

                    <div class="row">
                        <div class="col-md-6">
                            <div class="mb-3">
                                <label class="form-label">Display Value *</label>
                                <input type="text" v-model="formData.display_value" class="form-control" required />
                            </div>
                        </div>

                        <div class="col-md-6">
                            <div class="mb-3">
                                <label class="form-label">Parent</label>
                                <select v-model="formData.parent" class="form-control" :disabled="!hasParentOptions">
                                    <option value="">None</option>
                                    <option v-for="parent in parentOptions" :value="parent.id" :key="parent.id">
                                        {{ parent.display_value }} ({{ parent.code }})
                                    </option>
                                </select>
                            </div>
                        </div>
                    </div>

                    <div class="mb-3">
                        <label class="form-label">Description</label>
                        <textarea v-model="formData.description" class="form-control" rows="3"></textarea>
                    </div>

                    <div class="row">
                        <div class="col-md-4">
                            <div class="mb-3">
                                <label class="form-label">Sort Order</label>
                                <input type="number" v-model="formData.sort_order" class="form-control" min="0" />
                            </div>
                        </div>

                        <div class="col-md-4">
                            <div class="mb-3 form-check">
                                <input type="checkbox" v-model="formData.is_active" class="form-check-input"
                                    id="isActiveCheck" />
                                <label class="form-check-label" for="isActiveCheck">Active</label>
                            </div>
                        </div>
                    </div>

                    <div class="mb-3">
                        <label class="form-label">Metadata</label>
                        <div class="metadata-editor">
                            <div v-for="(value, key) in formData.metadata" :key="key" class="metadata-item mb-2">
                                <div class="input-group">
                                    <span class="input-group-text">{{ key }}</span>
                                    <input type="text" v-model="formData.metadata[key]" class="form-control"
                                        :placeholder="`Enter ${key} value`" />
                                </div>
                            </div>
                            <div v-if="!Object.keys(formData.metadata).length" class="text-muted">
                                No metadata fields defined for this data type
                            </div>
                        </div>
                    </div>
                </form>
            </template>
            <template #footer>
                <button type="button" @click="closeEntryForm" class="btn btn-secondary me-2">
                    Cancel
                </button>
                <button type="submit" @click="submitForm" class="btn btn-primary">
                    {{ isEditing ? 'Update' : 'Create' }}
                </button>
            </template>
        </Modal>

        <!-- Type Form Modal -->
        <Modal v-if="showTypeForm" @close="closeTypeForm">
            <template #header>
                <h3>{{ typeFormTitle }}</h3>
            </template>
            <template #body>
                <form @submit.prevent="submitTypeForm">
                    <div class="row">
                        <div class="col-md-6">
                            <div class="mb-3">
                                <label class="form-label">Name *</label>
                                <input type="text" v-model="typeFormData.name" class="form-control" required />
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="mb-3">
                                <label class="form-label">Code *</label>
                                <input type="text" v-model="typeFormData.code" class="form-control" required />
                            </div>
                        </div>
                    </div>

                    <div class="mb-3">
                        <label class="form-label">Description</label>
                        <textarea v-model="typeFormData.description" class="form-control" rows="3"></textarea>
                    </div>

                    <div class="mb-3">
                        <label class="form-label">Allowed Metadata Keys (comma separated)</label>
                        <input type="text" v-model="typeFormData.allowed_metadata_keys_str" class="form-control"
                            placeholder="key1, key2, key3" />
                    </div>

                    <div class="mb-3 form-check">
                        <input type="checkbox" v-model="typeFormData.is_system_managed" class="form-check-input"
                            id="systemManagedCheck" />
                        <label class="form-check-label" for="systemManagedCheck">System Managed</label>
                    </div>
                </form>
            </template>
            <template #footer>
                <button type="button" @click="closeTypeForm" class="btn btn-secondary me-2">
                    Cancel
                </button>
                <button type="submit" @click="submitTypeForm" class="btn btn-primary">
                    {{ isEditingType ? 'Update' : 'Create' }}
                </button>
            </template>
        </Modal>

        <!-- Delete Confirmation Modal -->
        <Modal v-if="showDeleteModal" @close="showDeleteModal = false">
            <template #header>
                <h3>Confirm Deletion</h3>
            </template>
            <template #body>
                <p>
                    Are you sure you want to delete
                    <strong>{{ itemToDelete.display_value || itemToDelete.name }}</strong> ({{ itemToDelete.code }})?
                </p>
                <p class="text-danger">
                    This action cannot be undone.
                </p>
            </template>
            <template #footer>
                <button type="button" @click="showDeleteModal = false" class="btn btn-secondary">
                    Cancel
                </button>
                <button type="button" @click="deleteItem" class="btn btn-danger">
                    Delete
                </button>
            </template>
        </Modal>
    </div>
</template>

<script>
    import { ref, computed, onMounted, watch } from 'vue';
    import axiosInstance from '@/utils/axios';
    import Modal from '@/components/modals/Modal.vue'; // Make sure you have a modal component

    export default {
        name: 'ReferenceDataCrud',
        components: {
            Modal
        },
        setup() {
            // State
            const activeTab = ref('entries');
            const referenceData = ref([]);
            const referenceDataTypes = ref([]);
            const historyLogs = ref([]);
            const parentOptions = ref([]);
            const formData = ref({
                id: null,
                data_type: '',
                code: '',
                display_value: '',
                description: '',
                is_active: true,
                sort_order: 0,
                metadata: {},
                parent: null,
                version: 1
            });

            const typeFormData = ref({
                id: null,
                name: '',
                code: '',
                description: '',
                allowed_metadata_keys: [],
                allowed_metadata_keys_str: '',
                is_system_managed: false,
                version: 1
            });

            const itemToDelete = ref(null);
            const showDeleteModal = ref(false);
            const showEntryForm = ref(false);
            const showTypeForm = ref(false);
            const isEditing = ref(false);
            const isEditingType = ref(false);
            const isSystemManaged = ref(false);

            // Filters and pagination
            const filters = ref({
                dataType: '',
                isActive: '',
                search: ''
            });

            const pagination = ref({
                currentPage: 1,
                pageSize: 10,
                totalItems: 0,
                totalPages: 1
            });

            const historyPagination = ref({
                currentPage: 1,
                pageSize: 10,
                totalItems: 0,
                totalPages: 1
            });

            // Computed properties
            const formTitle = computed(() => {
                return isEditing.value ? 'Edit Reference Data' : 'Create New Reference Data';
            });

            const typeFormTitle = computed(() => {
                return isEditingType.value ? 'Edit Data Type' : 'Create New Data Type';
            });

            const hasParentOptions = computed(() => {
                return parentOptions.value.length > 0;
            });

            // Methods
            const fetchData = async () => {
                try {
                    const params = {
                        page: pagination.value.currentPage,
                        page_size: pagination.value.pageSize,
                        ...filters.value
                    };

                    const response = await axiosInstance.get('/reference-data/entries/', { params });
                    referenceData.value = response.data.results;
                    pagination.value = {
                        ...pagination.value,
                        totalItems: response.data.count,
                        totalPages: Math.ceil(response.data.count / pagination.value.pageSize)
                    };
                } catch (error) {
                    if (error.message?.includes('logged in')) return; // Suppress expected 401
                    console.error('Error fetching reference data:', error);
                    alert('Failed to load reference data');
                }
            };

            const fetchDataTypes = async () => {
                try {
                    const response = await axiosInstance.get('/reference-data/types/');
                    referenceDataTypes.value = response.data.results;
                    console.log('Reference Data Types:', referenceDataTypes.value);
                } catch (error) {
                    console.error('Error fetching reference data types:', error);
                    alert('Failed to load reference data types');
                }
            };

            const fetchHistory = async () => {
                try {
                    const params = {
                        page: historyPagination.value.currentPage,
                        page_size: historyPagination.value.pageSize
                    };

                    const response = await axiosInstance.get('/reference-data/history/', { params });
                    historyLogs.value = response.data.results;
                    historyPagination.value = {
                        ...historyPagination.value,
                        totalItems: response.data.count,
                        totalPages: Math.ceil(response.data.count / historyPagination.value.pageSize)
                    };
                } catch (error) {
                    console.error('Error fetching history:', error);
                    alert('Failed to load history');
                }
            };

            const fetchParentOptions = async (dataTypeId) => {
                if (!dataTypeId) {
                    parentOptions.value = [];
                    return;
                }

                try {
                    const response = await axiosInstance.get(`/reference-data/?data_type=${dataTypeId}`);
                    parentOptions.value = response.data.results;
                } catch (error) {
                    console.error('Error fetching parent options:', error);
                    parentOptions.value = [];
                }
            };

            const getDataTypeName = (dataTypeId) => {
                const type = referenceDataTypes.value.find(t => t.id === dataTypeId);
                return type ? type.name : 'Unknown';
            };

            const formatDate = (dateString) => {
                return new Date(dateString).toLocaleString();
            };

            // Entry Form Methods
            const openCreateForm = () => {
                resetForm();
                isEditing.value = false;
                showEntryForm.value = true;
            };

            const openEditForm = (item) => {
                formData.value = {
                    id: item.id,
                    data_type: item.data_type,
                    code: item.code,
                    display_value: item.display_value,
                    description: item.description,
                    is_active: item.is_active,
                    sort_order: item.sort_order,
                    metadata: { ...item.metadata },
                    parent: item.parent?.id || null,
                    version: item.version
                };

                const dataType = referenceDataTypes.value.find(t => t.id === item.data_type);
                isSystemManaged.value = dataType?.is_system_managed || false;

                fetchParentOptions(item.data_type);
                isEditing.value = true;
                showEntryForm.value = true;
            };

            const closeEntryForm = () => {
                showEntryForm.value = false;
            };

            const resetForm = () => {
                formData.value = {
                    id: null,
                    data_type: '',
                    code: '',
                    display_value: '',
                    description: '',
                    is_active: true,
                    sort_order: 0,
                    metadata: {},
                    parent: null,
                    version: 1
                };
                isSystemManaged.value = false;
            };

            const submitForm = async () => {
                try {
                    const payload = { ...formData.value };

                    if (isEditing.value) {
                        await axios.put(`/reference-data/${payload.id}/`, payload);
                    } else {
                        await axios.post('/reference-data/', payload);
                    }

                    fetchData();
                    showEntryForm.value = false;
                } catch (error) {
                    console.error('Error saving reference data:', error);
                    alert(`Failed to save: ${error.response?.data?.detail || error.message}`);
                }
            };

            // Type Form Methods
            const openCreateTypeForm = () => {
                resetTypeForm();
                isEditingType.value = false;
                showTypeForm.value = true;
            };

            const openEditTypeForm = (type) => {
                typeFormData.value = {
                    id: type.id,
                    name: type.name,
                    code: type.code,
                    description: type.description,
                    allowed_metadata_keys: [...(type.allowed_metadata_keys || [])],
                    allowed_metadata_keys_str: type.allowed_metadata_keys ? type.allowed_metadata_keys.join(', ') : '',
                    is_system_managed: type.is_system_managed,
                    version: type.version
                };
                isEditingType.value = true;
                showTypeForm.value = true;
            };

            const closeTypeForm = () => {
                showTypeForm.value = false;
            };

            const resetTypeForm = () => {
                typeFormData.value = {
                    id: null,
                    name: '',
                    code: '',
                    description: '',
                    allowed_metadata_keys: [],
                    allowed_metadata_keys_str: '',
                    is_system_managed: false,
                    version: 1
                };
            };

            const submitTypeForm = async () => {
                try {
                    const payload = {
                        ...typeFormData.value,
                        allowed_metadata_keys: typeFormData.value.allowed_metadata_keys_str
                            .split(',')
                            .map(key => key.trim())
                            .filter(key => key)
                    };

                    if (isEditingType.value) {
                        await axios.put(`/reference-data/types/${payload.id}/`, payload);
                    } else {
                        await axios.post('/reference-data/types/', payload);
                    }

                    fetchDataTypes();
                    showTypeForm.value = false;
                } catch (error) {
                    console.error('Error saving data type:', error);
                    alert(`Failed to save: ${error.response?.data?.detail || error.message}`);
                }
            };

            // Delete Methods
            const confirmDelete = (item) => {
                itemToDelete.value = item;
                showDeleteModal.value = true;
            };

            const confirmDeleteType = (type) => {
                itemToDelete.value = type;
                showDeleteModal.value = true;
            };

            const deleteItem = async () => {
                try {
                    if (activeTab.value === 'entries') {
                        await axios.delete(`/reference-data/${itemToDelete.value.id}/`);
                        fetchData();
                    } else if (activeTab.value === 'types') {
                        await axios.delete(`/reference-data/types/${itemToDelete.value.id}/`);
                        fetchDataTypes();
                    }
                    showDeleteModal.value = false;
                } catch (error) {
                    console.error('Error deleting:', error);
                    alert('Failed to delete item');
                }
            };

            // Pagination Methods
            const changePage = (page) => {
                if (page >= 1 && page <= pagination.value.totalPages) {
                    pagination.value.currentPage = page;
                    fetchData();
                }
            };

            const changeHistoryPage = (page) => {
                if (page >= 1 && page <= historyPagination.value.totalPages) {
                    historyPagination.value.currentPage = page;
                    fetchHistory();
                }
            };

            const debounceFetch = () => {
                // Implement debounce logic here
                fetchData();
            };

            // Watchers
            watch(() => formData.value.data_type, (newVal) => {
                if (newVal) {
                    const dataType = referenceDataTypes.value.find(t => t.id === newVal);
                    if (dataType) {
                        const metadata = {};
                        if (dataType.allowed_metadata_keys) {
                            dataType.allowed_metadata_keys.forEach(key => {
                                metadata[key] = formData.value.metadata[key] || '';
                            });
                        }
                        formData.value.metadata = metadata;
                        isSystemManaged.value = dataType.is_system_managed;
                        fetchParentOptions(newVal);
                    }
                }
            });

            watch(activeTab, (newTab) => {
                if (newTab === 'history') {
                    fetchHistory();
                }
            });

            // Lifecycle hooks
            onMounted(() => {
                fetchData();
                fetchDataTypes();
            });

            return {
                activeTab,
                referenceData,
                referenceDataTypes,
                historyLogs,
                parentOptions,
                formData,
                typeFormData,
                itemToDelete,
                showDeleteModal,
                showEntryForm,
                showTypeForm,
                isEditing,
                isEditingType,
                isSystemManaged,
                filters,
                pagination,
                historyPagination,
                formTitle,
                typeFormTitle,
                hasParentOptions,
                fetchData,
                fetchDataTypes,
                fetchHistory,
                getDataTypeName,
                formatDate,
                openCreateForm,
                openEditForm,
                closeEntryForm,
                submitForm,
                openCreateTypeForm,
                openEditTypeForm,
                closeTypeForm,
                submitTypeForm,
                confirmDelete,
                confirmDeleteType,
                deleteItem,
                changePage,
                changeHistoryPage,
                debounceFetch
            };
        }
    };
</script>

<style scoped>
    .reference-data-crud {
        padding: 20px;
        background: #fff;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    .tabs-header {
        display: flex;
        border-bottom: 1px solid #e0e0e0;
        margin-bottom: 20px;
        padding-bottom: 10px;
        align-items: center;
    }

    .tab-btn {
        padding: 8px 16px;
        margin-right: 8px;
        background: none;
        border: none;
        border-bottom: 2px solid transparent;
        cursor: pointer;
        font-weight: 500;
        color: #666;
        transition: all 0.2s;
    }

    .tab-btn:hover {
        color: #333;
    }

    .tab-btn.active {
        color: #007bff;
        border-bottom-color: #007bff;
    }

    .actions {
        margin-left: auto;
    }

    .data-table {
        width: 100%;
        border-collapse: collapse;
    }

    .data-table th {
        background-color: #f8f9fa;
        padding: 12px 15px;
        text-align: left;
        font-weight: 600;
        color: #495057;
        border-bottom: 2px solid #e9ecef;
    }

    .data-table td {
        padding: 12px 15px;
        border-bottom: 1px solid #e9ecef;
        vertical-align: middle;
    }

    .data-table tr:hover {
        background-color: #f8f9fa;
    }

    .status-badge {
        display: inline-block;
        padding: 4px 8px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 500;
    }

    .status-badge.active {
        background-color: #d4edda;
        color: #155724;
    }

    .status-badge.inactive {
        background-color: #f8d7da;
        color: #721c24;
    }

    .status-badge.system {
        background-color: #d1ecf1;
        color: #0c5460;
    }

    .status-badge.custom {
        background-color: #fff3cd;
        color: #856404;
    }

    .status-badge.create,
    .status-badge.update {
        background-color: #d4edda;
        color: #155724;
    }

    .status-badge.delete {
        background-color: #f8d7da;
        color: #721c24;
    }

    .table-actions {
        display: flex;
        gap: 8px;
    }

    .action-btn {
        background: none;
        border: none;
        width: 32px;
        height: 32px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: background-color 0.2s;
    }

    .action-btn:hover {
        background-color: rgba(0, 0, 0, 0.05);
    }

    .edit-btn {
        color: #007bff;
    }

    .edit-btn:hover {
        background-color: rgba(0, 123, 255, 0.1);
    }

    .delete-btn {
        color: #dc3545;
    }

    .delete-btn:hover {
        background-color: rgba(220, 53, 69, 0.1);
    }

    .pagination {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 20px;
    }

    .metadata-editor {
        border: 1px solid #e9ecef;
        padding: 10px;
        border-radius: 4px;
        background-color: #f8f9fa;
    }

    .metadata-item .input-group-text {
        min-width: 120px;
        justify-content: flex-start;
        background-color: #e9ecef;
    }

    .filters {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 4px;
        margin-bottom: 20px;
    }

    .filters label {
        font-weight: 500;
        margin-bottom: 5px;
        display: block;
    }
</style>