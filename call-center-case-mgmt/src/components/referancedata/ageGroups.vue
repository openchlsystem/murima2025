<template>
    <div class="reference-data-crud">


        <!-- List View -->
        <div v-if="viewMode === 'list'">
            <div class="header">
                <h2>Reference Data</h2>
                <button @click="openCreateForm" class="btn btn-primary">
                    <i class="fas fa-plus"></i> Add New
                </button>
            </div>

            <div class="filters mb-3">
                <div class="row">
                    <div class="col-md-4">
                        <label>Data Type</label>
                        <select v-model="filters.dataType" class="form-control" @change="fetchData">
                            <option value="">All Types</option>
                            <option v-for="type in referenceDataTypes" :value="type.id" :key="type.id">
                                {{ type.name }}
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
                <table class="table table-striped">
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
                        <tr v-for="item in referenceData" :key="item.id">
                            <td>{{ getDataTypeName(item.data_type) }}</td>
                            <td>{{ item.code }}</td>
                            <td>{{ item.display_value }}</td>
                            <td>
                                <span :class="['badge', item.is_active ? 'bg-success' : 'bg-secondary']">
                                    {{ item.is_active ? 'Active' : 'Inactive' }}
                                </span>
                            </td>
                            <td>{{ item.sort_order }}</td>
                            <td>
                                <button @click="openEditForm(item)" class="btn btn-sm btn-primary me-2">
                                    <i class="fas fa-edit"></i>
                                </button>
                                <button @click="confirmDelete(item)" class="btn btn-sm btn-danger">
                                    <i class="fas fa-trash"></i>
                                </button>
                            </td>
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

        <!-- Create/Edit Form -->
        <div v-if="viewMode === 'form'">
            <h2>{{ formTitle }}</h2>

            <form @submit.prevent="submitForm">
                <div class="row">
                    <div class="col-md-6">
                        <div class="mb-3">
                            <label class="form-label">Data Type *</label>
                            <select v-model="formData.data_type" class="form-control" :disabled="isEditing" required>
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

                <div class="form-actions">
                    <button type="button" @click="cancelForm" class="btn btn-secondary me-2">
                        Cancel
                    </button>
                    <button type="submit" class="btn btn-primary">
                        {{ isEditing ? 'Update' : 'Create' }}
                    </button>
                </div>
            </form>
        </div>

        <!-- Delete Confirmation Modal -->
        <div v-if="showDeleteModal" class="modal-backdrop show"></div>
        <div v-if="showDeleteModal" class="modal show" tabindex="-1" style="display: block">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Confirm Deletion</h5>
                        <button type="button" class="btn-close" @click="showDeleteModal = false"></button>
                    </div>
                    <div class="modal-body">
                        <p>
                            Are you sure you want to delete
                            <strong>{{ itemToDelete.display_value }}</strong> ({{ itemToDelete.code }})?
                        </p>
                        <p class="text-danger">
                            This action cannot be undone.
                        </p>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" @click="showDeleteModal = false">
                            Cancel
                        </button>
                        <button type="button" class="btn btn-danger" @click="deleteItem">
                            Delete
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import { ref, computed, onMounted, watch } from 'vue';
    import axios from '@/utils/axios'; // Adjust the import path as necessary
    // import { debounce } from 'lodash';

    export default {
        name: 'ReferenceDataCrud',
        setup() {
            // State
            const viewMode = ref('list');
            const referenceData = ref([]);
            const referenceDataTypes = ref([]);
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
            const itemToDelete = ref(null);
            const showDeleteModal = ref(false);
            const isEditing = ref(false);
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

            // Computed properties
            const formTitle = computed(() => {
                return isEditing.value ? 'Edit Reference Data' : 'Create New Reference Data';
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

                    const response = await axios.get('/reference-data/ entries/', { params });
                    referenceData.value = response.data.results;
                    pagination.value = {
                        ...pagination.value,
                        totalItems: response.data.count,
                        totalPages: Math.ceil(response.data.count / pagination.value.pageSize)
                    };
                } catch (error) {
                    console.error('Error fetching reference data:', error);
                    alert('Failed to load reference data');
                }
            };

            const fetchDataTypes = async () => {
                try {
                    const response = await axios.get('/reference-data/types/');
                    referenceDataTypes.value = response.data;
                } catch (error) {
                    console.error('Error fetching reference data types:', error);
                    alert('Failed to load reference data types');
                }
            };

            const fetchParentOptions = async (dataTypeId) => {
                if (!dataTypeId) {
                    parentOptions.value = [];
                    return;
                }

                try {
                    const response = await axios.get(`/reference-data/?data_type=${dataTypeId}`);
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

            const openCreateForm = () => {
                resetForm();
                isEditing.value = false;
                viewMode.value = 'form';
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

                // Check if this is a system-managed type
                const dataType = referenceDataTypes.value.find(t => t.id === item.data_type);
                isSystemManaged.value = dataType?.is_system_managed || false;

                // Load parent options for this data type
                fetchParentOptions(item.data_type);

                isEditing.value = true;
                viewMode.value = 'form';
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

            const cancelForm = () => {
                viewMode.value = 'list';
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
                    viewMode.value = 'list';
                } catch (error) {
                    console.error('Error saving reference data:', error);
                    alert(`Failed to save: ${error.response?.data?.detail || error.message}`);
                }
            };

            const confirmDelete = (item) => {
                itemToDelete.value = item;
                showDeleteModal.value = true;
            };

            const deleteItem = async () => {
                try {
                    await axios.delete(`/reference-data/${itemToDelete.value.id}/`);
                    showDeleteModal.value = false;
                    fetchData();
                } catch (error) {
                    console.error('Error deleting reference data:', error);
                    alert('Failed to delete item');
                }
            };

            const changePage = (page) => {
                if (page >= 1 && page <= pagination.value.totalPages) {
                    pagination.value.currentPage = page;
                    fetchData();
                }
            };

            // const debounceFetch = debounce(fetchData, 500);

            // Watchers
            watch(() => formData.value.data_type, (newVal) => {
                if (newVal) {
                    // When data type changes, fetch allowed metadata fields
                    const dataType = referenceDataTypes.value.find(t => t.id === newVal);
                    if (dataType) {
                        // Initialize metadata object with allowed keys
                        const metadata = {};
                        if (dataType.allowed_metadata_keys) {
                            dataType.allowed_metadata_keys.forEach(key => {
                                metadata[key] = formData.value.metadata[key] || '';
                            });
                        }
                        formData.value.metadata = metadata;

                        // Check if system managed
                        isSystemManaged.value = dataType.is_system_managed;

                        // Load parent options
                        fetchParentOptions(newVal);
                    }
                }
            });

            // Lifecycle hooks
            onMounted(() => {
                fetchData();
                fetchDataTypes();
            });

            return {
                viewMode,
                referenceData,
                referenceDataTypes,
                parentOptions,
                formData,
                itemToDelete,
                showDeleteModal,
                isEditing,
                isSystemManaged,
                filters,
                pagination,
                formTitle,
                hasParentOptions,
                fetchData,
                getDataTypeName,
                openCreateForm,
                openEditForm,
                cancelForm,
                submitForm,
                confirmDelete,
                deleteItem,
                changePage,
                debounceFetch
            };
        }
    };
</script>

<style scoped>
    .reference-data-crud {
        padding: 20px;
        color: red;
    }

    .header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
        color: red;
    }

    .table-responsive {
        margin-bottom: 20px;
        color: red;
    }

    .pagination {
        display: flex;
        justify-content: center;
        align-items: center;
        color: red;
    }

    .metadata-editor {
        border: 1px solid #ddd;
        padding: 10px;
        border-radius: 4px;
        color: red;
    }

    .metadata-item {
        margin-bottom: 5px;
        color: red;
    }

    .form-actions {
        margin-top: 20px;
        text-align: right;
        color: red;
    }

    .modal-backdrop {
        opacity: 0.5;
        color: red;
    }
</style>