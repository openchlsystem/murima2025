<template>
    <div class="csv-import">
        <h2>Import Reference Data from CSV</h2>

        <section class="upload-area" @dragover.prevent="dragover" @drop.prevent="drop">
            <input type="file" id="csvFileInput" ref="fileInput" accept=".csv" @change="handleFileSelect"
                class="file-input" />
            <label for="csvFileInput" class="upload-label">
                <template v-if="!fileSelected">
                    <i class="fas fa-cloud-upload-alt"></i>
                    <p>Drag & drop your CSV file here or click to browse</p>
                    <small>Only CSV files accepted</small>
                </template>
                <template v-else>
                    <i class="fas fa-file-csv"></i>
                    <p>{{ selectedFile.name }}</p>
                    <small>{{ formatFileSize(selectedFile.size) }}</small>
                </template>
            </label>
        </section>

        <section class="actions">
            <button @click="uploadFile" :disabled="!fileSelected || isUploading" class="submit-btn">
                <span v-if="!isUploading">Upload CSV</span>
                <span v-else><i class="fas fa-spinner fa-spin"></i> Uploading...</span>
            </button>

            <button @click="processFile" :disabled="!fileUploaded || isProcessing" class="submit-btn">
                <span v-if="!isProcessing">Process File</span>
                <span v-else><i class="fas fa-spinner fa-spin"></i> Processing...</span>
            </button>

            <button @click="resetForm" class="reset-btn" :disabled="isUploading || isProcessing">
                Reset
            </button>

            <a href="/path-to-sample.csv" download class="sample-link">
                Download Sample CSV
            </a>
        </section>

        <section v-if="importResult" class="result" :class="resultStatusClass">
            <h3>Import Results</h3>
            <p v-if="importResult.status === 'success'">
                ✅ Successfully imported {{ importResult.created_count }} records
            </p>
            <template v-else-if="importResult.status === 'partial_success'">
                <p>⚠ Imported {{ importResult.created_count }} records with {{ importResult.error_count }} errors</p>
                <div v-if="importResult.errors.length > 0" class="error-details">
                    <h4>Errors:</h4>
                    <ul>
                        <li v-for="(error, index) in importResult.errors" :key="index">
                            Row {{ error.row }} ({{ error.name || 'No name' }}): {{ error.error }}
                        </li>
                    </ul>
                </div>
            </template>
            <template v-else>
                <p>❌ Import failed</p>
                <p v-if="importResult.error">{{ importResult.error }}</p>
                <p v-if="importResult.details">Details: {{ importResult.details }}</p>
            </template>
        </section>
    </div>
</template>

<script>
    import { ref, computed } from 'vue';
    import axiosInstance from '@/utils/axios';

    export default {
        name: 'CsvImport',
        setup() {
            // Refs
            const fileInput = ref(null);
            const selectedFile = ref(null);
            const fileSelected = ref(false);
            const isUploading = ref(false);
            const isProcessing = ref(false);
            const fileUploaded = ref(false);
            const importResult = ref(null);
            const fileReference = ref(null); // Stores file reference from backend

            // Computed
            const resultStatusClass = computed(() => {
                if (!importResult.value) return '';
                switch (importResult.value.status) {
                    case 'success': return 'success';
                    case 'partial_success': return 'warning';
                    default: return 'error';
                }
            });

            // Methods
            const handleFileSelect = (event) => {
                const files = event.target.files || event.dataTransfer.files;
                if (files.length === 0) return;

                const file = files[0];
                if (!file.name.endsWith('.csv')) {
                    importResult.value = {
                        status: 'error',
                        error: 'Invalid file type',
                        details: 'Please upload a CSV file'
                    };
                    return;
                }

                selectedFile.value = file;
                fileSelected.value = true;
                fileUploaded.value = false;
                fileReference.value = null;
                importResult.value = null;
            };

            const dragover = (event) => {
                event.currentTarget.classList.add('dragover');
            };

            const drop = (event) => {
                event.currentTarget.classList.remove('dragover');
                handleFileSelect(event);
            };

            const formatFileSize = (bytes) => {
                if (bytes === 0) return '0 Bytes';
                const k = 1024;
                const sizes = ['Bytes', 'KB', 'MB', 'GB'];
                const i = Math.floor(Math.log(bytes) / Math.log(k));
                return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
            };

            const resetForm = () => {
                if (fileInput.value) fileInput.value.value = '';
                selectedFile.value = null;
                fileSelected.value = false;
                fileUploaded.value = false;
                importResult.value = null;
                fileReference.value = null;
            };

            const uploadFile = async () => {
                if (!selectedFile.value) return;

                isUploading.value = true;
                importResult.value = null;

                const formData = new FormData();
                formData.append('file', selectedFile.value);

                try {
                    const response = await axiosInstance.post('/reference-data/import-csv-upload/', formData, {
                        headers: {
                            'Content-Type': 'multipart/form-data'
                        }
                    });

                    if (response.status >= 200 && response.status < 300) {
                        fileUploaded.value = true;
                        // Extract file path from response in different possible formats
                        fileReference.value = response.data?.file_path ||
                            response.data?.path ||
                            response.data?.file_reference ||
                            response.data?.data?.file_path;

                        if (!fileReference.value) {
                            console.error('File path not found in response:', response.data);
                            throw new Error('Server did not return file path');
                        }
                    } else {
                        throw new Error(`Unexpected response status: ${response.status}`);
                    }
                } catch (error) {
                    console.error('Upload error:', error);
                    importResult.value = {
                        status: 'error',
                        error: 'Upload failed',
                        details: error.response?.data?.error || error.message
                    };
                    fileUploaded.value = false;
                } finally {
                    isUploading.value = false;
                }
            };

            const processFile = async () => {
                if (!fileReference.value) {
                    importResult.value = {
                        status: 'error',
                        error: 'Processing failed',
                        details: 'No file reference available. Please upload again.'
                    };
                    return;
                }

                isProcessing.value = true;

                try {
                    const response = await axiosInstance.post('/reference-data/import-csv-process/', {
                        file_path: fileReference.value
                    });

                    // Handle different successful response formats
                    if (response.status === 200 || response.status === 201) {
                        if (response.data.created_count > 0) {
                            importResult.value = {
                                status: 'success',
                                created_count: response.data.created_count,
                                error_count: response.data.error_count || 0,
                                errors: response.data.errors || []
                            };
                        } else if (response.data.message) {
                            // Handle cases where backend returns just a message
                            importResult.value = {
                                status: 'error',
                                error: 'No data processed',
                                details: response.data.message
                            };
                        } else {
                            importResult.value = {
                                status: 'error',
                                error: 'No data processed',
                                details: 'The file was processed but no records were imported'
                            };
                        }
                    } else {
                        throw new Error(`Unexpected response status: ${response.status}`);
                    }
                } catch (error) {
                    console.error('Process error:', error);
                    importResult.value = {
                        status: 'error',
                        error: 'Processing failed',
                        details: error.response?.data?.error ||
                            error.response?.data?.message ||
                            error.message
                    };
                } finally {
                    isProcessing.value = false;
                }
            };

            return {
                fileInput,
                selectedFile,
                fileSelected,
                fileUploaded,
                isUploading,
                isProcessing,
                importResult,
                resultStatusClass,
                handleFileSelect,
                dragover,
                drop,
                formatFileSize,
                resetForm,
                uploadFile,
                processFile
            };
        }
    };
</script>


<style scoped>
    .csv-import {
        max-width: 800px;
        margin: 0 auto;
        padding: 2rem;
        background: #fff;
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }

    h2 {
        text-align: center;
        margin-bottom: 1.5rem;
        color: #2c3e50;
    }

    .upload-area {
        border: 2px dashed #ccc;
        border-radius: 6px;
        padding: 2rem;
        text-align: center;
        margin-bottom: 1.5rem;
        transition: all 0.3s;
        background: #f9f9f9;
    }

    .upload-area.dragover {
        border-color: #42b983;
        background: #f0fff4;
    }

    .file-input {
        display: none;
    }

    .upload-label {
        display: block;
        cursor: pointer;
    }

    .upload-label i {
        font-size: 3rem;
        color: #42b983;
        margin-bottom: 0.5rem;
    }

    .upload-label .fa-file-csv {
        color: #2c3e50;
    }

    .actions {
        display: flex;
        justify-content: center;
        gap: 1rem;
        margin-bottom: 1.5rem;
        flex-wrap: wrap;
    }

    button {
        padding: 0.5rem 1.5rem;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        font-weight: 500;
        transition: all 0.2s;
    }

    .submit-btn {
        background: #42b983;
        color: white;
    }

    .submit-btn:hover:not(:disabled) {
        background: #369f6e;
    }

    .submit-btn:disabled {
        background: #a0d9bb;
        cursor: not-allowed;
    }

    .reset-btn {
        background: #f0f0f0;
        color: #2c3e50;
    }

    .reset-btn:hover:not(:disabled) {
        background: #e0e0e0;
    }

    .sample-link {
        color: #42b983;
        text-decoration: none;
        display: flex;
        align-items: center;
    }

    .sample-link:hover {
        text-decoration: underline;
    }

    .result {
        margin-top: 1.5rem;
        padding: 1rem;
        border-radius: 6px;
    }

    .result.success {
        background: #f0fff4;
        border: 1px solid #c6f6d5;
        color: #22543d;
    }

    .result.warning {
        background: #fffaf0;
        border: 1px solid #feebc8;
        color: #7b341e;
    }

    .result.error {
        background: #fff5f5;
        border: 1px solid #fed7d7;
        color: #9b2c2c;
    }

    .error-details {
        margin-top: 1rem;
        max-height: 200px;
        overflow-y: auto;
        border-top: 1px solid #feebc8;
        padding-top: 1rem;
    }

    .error-details ul {
        list-style-type: none;
        padding: 0;
        margin: 0;
    }

    .error-details li {
        padding: 0.25rem 0;
        border-bottom: 1px solid #feebc8;
    }

    .fa-spin {
        margin-right: 0.5rem;
    }

    /* Responsive adjustments */
    @media (max-width: 600px) {
        .actions {
            flex-direction: column;
            align-items: center;
        }

        .actions button,
        .actions a {
            width: 100%;
            text-align: center;
        }
    }
</style>