<template>
  <div>
    <!-- SidePanel Component -->
    <SidePanel :userRole="userRole" :isInQueue="isInQueue" :isProcessingQueue="isProcessingQueue"
      :currentCall="currentCall" @toggle-queue="handleQueueToggle" @logout="handleLogout"
      @sidebar-toggle="handleSidebarToggle" />

    <!-- Main Content -->

    <div class="main-content">
      <h2>Referral </h2>
      <ReferenceDataCrud />
    </div>
  </div>
</template>

<script>

  import { useRouter } from 'vue-router'
  import SidePanel from '@/components/SidePanel.vue'
  import ReferenceDataCrud from '@/components/referancedata/ageGroups.vue'

  export default {
    components: {
      SidePanel,
      ReferenceDataCrud
    },
    setup() {
      // Router instance  
      return {
        useRouter
      }
    }
  }




</script>

<style>

  /* Global styles - not scoped */
  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: 'Inter', sans-serif;
  }

  body {
    background-color: var(--background-color);
    color: var(--text-color);
    display: flex;
    min-height: 100vh;
    transition: background-color 0.3s, color 0.3s;
    overflow: hidden;
  }

  .main-content {
    flex: 1;
    margin-left: var(--sidebar-width, 250px);
    height: 100vh;
    background-color: var(--background-color);
    transition: margin-left 0.3s ease, background-color 0.3s;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }

  .calls-container {
    flex: 1;
    padding: 20px;
    overflow-y: auto;
    overflow-x: hidden;
    scrollbar-width: thin;
    scrollbar-color: rgba(255, 255, 255, 0.3) transparent;
  }

  .calls-container::-webkit-scrollbar {
    width: 8px;
  }

  .calls-container::-webkit-scrollbar-track {
    background: transparent;
  }

  .calls-container::-webkit-scrollbar-thumb {
    background-color: rgba(255, 255, 255, 0.3);
    border-radius: 4px;
  }

  .calls-container::-webkit-scrollbar-thumb:hover {
    background-color: rgba(255, 255, 255, 0.5);
  }

  .header {
    margin-bottom: 25px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-shrink: 0;
  }

  .header-actions {
    display: flex;
    align-items: center;
    gap: 20px;
  }

  .page-title {
    font-size: 28px;
    font-weight: 700;
  }

  .theme-toggle {
    background-color: var(--content-bg);
    color: var(--text-color);
    border: 1px solid var(--border-color);
    border-radius: 30px;
    padding: 8px 15px;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 8px;
    transition: all 0.3s ease;
    white-space: nowrap;
    min-width: 120px;
  }

  .theme-toggle:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }

  .theme-toggle svg {
    width: 16px;
    height: 16px;
  }

  .new-call-btn {
    background-color: var(--success-color);
    color: white;
    border: none;
    border-radius: 30px;
    padding: 8px 15px;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 8px;
    transition: all 0.3s ease;
    white-space: nowrap;
    min-width: 100px;
  }

  .new-call-btn:hover {
    background-color: #45a049;
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }

  .new-call-btn svg {
    width: 16px;
    height: 16px;
  }

  .view-tabs {
    display: flex;
    border-bottom: 1px solid var(--border-color);
    margin-bottom: 25px;
    overflow-x: auto;
    white-space: nowrap;
    flex-shrink: 0;
  }

  .view-tab {
    padding: 12px 24px;
    cursor: pointer;
    font-size: 14px;
    font-weight: 600;
    color: var(--text-secondary);
    position: relative;
    transition: all 0.3s ease;
  }

  .view-tab:hover {
    color: var(--text-color);
  }

  .view-tab.active {
    color: var(--text-color);
    font-weight: 700;
  }

  .view-tab.active::after {
    content: '';
    position: absolute;
    bottom: -1px;
    left: 0;
    width: 100%;
    height: 2px;
    background-color: var(--accent-color);
  }

  /* Status Cards - Horizontal Layout */
  .status-cards {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
    margin-bottom: 25px;
    padding: 0;
  }

  .status-card {
    background-color: var(--content-bg);
    border-radius: 15px;
    padding: 20px;
    border: 1px solid var(--border-color);
    transition: all 0.3s ease;
  }

  .status-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  }

  .status-card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
  }

  .status-card-label {
    font-size: 14px;
    font-weight: 700;
    color: var(--text-color);
  }

  .status-card-count {
    font-size: 24px;
    font-weight: 800;
    color: var(--accent-color);
  }

  .status-card-progress {
    height: 6px;
    background-color: var(--border-color);
    border-radius: 3px;
    overflow: hidden;
  }

  .status-card-progress-fill {
    height: 100%;
    background-color: var(--accent-color);
    border-radius: 3px;
    transition: width 0.3s ease;
  }

  .view-container {
    flex: 1;
    overflow-y: auto;
    overflow-x: hidden;
    scrollbar-width: thin;
    scrollbar-color: rgba(255, 255, 255, 0.3) transparent;
  }

  .view-container::-webkit-scrollbar {
    width: 8px;
  }

  .view-container::-webkit-scrollbar-track {
    background: transparent;
  }

  .view-container::-webkit-scrollbar-thumb {
    background-color: rgba(255, 255, 255, 0.3);
    border-radius: 4px;
  }

  .view-container::-webkit-scrollbar-thumb:hover {
    background-color: rgba(255, 255, 255, 0.5);
  }

  .time-section {
    margin-bottom: 35px;
  }

  .time-section-title {
    font-size: 18px;
    font-weight: 700;
    margin-bottom: 20px;
    color: var(--text-color);
  }

  .call-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .call-item {
    display: flex;
    align-items: flex-start;
    cursor: pointer;
    padding: 15px;
    border-radius: 15px;
    transition: all 0.3s ease;
    position: relative;
  }

  .call-item:hover {
    background-color: rgba(255, 255, 255, 0.05);
    transform: translateX(5px);
  }

  .call-item.selected {
    background-color: rgba(255, 59, 48, 0.1);
    border: 1px solid var(--highlight-color);
  }

  .call-item.selected .call-type {
    color: var(--highlight-color);
    font-weight: 700;
  }

  .timeline-connector::after {
    content: '';
    position: absolute;
    top: 45px;
    left: 30px;
    width: 1px;
    height: calc(100% + 12px);
    background-color: var(--border-color);
    z-index: 1;
  }

  .call-icon {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background-color: var(--content-bg);
    display: flex;
    justify-content: center;
    align-items: center;
    margin-right: 15px;
    margin-top: 2px;
    flex-shrink: 0;
    position: relative;
    z-index: 2;
    border: 2px solid var(--background-color);
  }

  .call-icon svg {
    width: 18px;
    height: 18px;
    stroke: var(--text-color);
  }

  .call-details {
    flex: 1;
  }

  .call-type {
    font-size: 15px;
    font-weight: 600;
    margin-bottom: 6px;
    line-height: 1.4;
  }

  .call-time {
    font-size: 13px;
    font-weight: 600;
    color: var(--text-secondary);
    margin-bottom: 4px;
  }

  .call-meta {
    display: flex;
    gap: 12px;
    align-items: center;
  }

  .case-link {
    font-size: 12px;
    font-weight: 600;
    color: var(--accent-color);
    text-decoration: none;
    padding: 2px 8px;
    background-color: rgba(150, 75, 0, 0.1);
    border-radius: 8px;
  }

  .case-link:hover {
    text-decoration: underline;
  }

  .call-id {
    font-size: 14px;
    font-weight: 700;
    color: var(--text-color);
  }

  .priority-badge {
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    padding: 4px 8px;
    border-radius: 8px;
    color: white;
  }

  .priority-badge.critical {
    background-color: var(--critical-color);
  }

  .priority-badge.high {
    background-color: var(--high-color);
  }

  .priority-badge.medium {
    background-color: var(--medium-color);
  }

  .priority-badge.low {
    background-color: var(--low-color);
  }

  /* Queue Section */
  .queue-section {
    padding: 20px;
    background-color: var(--card-bg);
    border-radius: 20px;
    margin-bottom: 20px;
  }

  .queue-title {
    font-size: 20px;
    font-weight: 700;
    margin-bottom: 20px;
  }

  .queue-stats {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 15px;
    margin-bottom: 30px;
  }

  .queue-stat {
    text-align: center;
    padding: 15px;
    background-color: var(--background-color);
    border-radius: 12px;
  }

  .stat-value {
    font-size: 24px;
    font-weight: 800;
    color: var(--accent-color);
    margin-bottom: 5px;
  }

  .stat-label {
    font-size: 12px;
    font-weight: 600;
    color: var(--text-secondary);
    text-transform: uppercase;
  }

  .queue-subtitle {
    font-size: 16px;
    font-weight: 700;
    margin-bottom: 15px;
  }

  .queue-call-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .queue-call-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px;
    background-color: var(--background-color);
    border-radius: 12px;
    transition: all 0.3s ease;
  }

  .queue-call-item:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }

  .queue-call-info {
    flex: 1;
  }

  .queue-call-type {
    font-size: 14px;
    font-weight: 600;
    margin-bottom: 5px;
  }

  .queue-call-details {
    display: flex;
    gap: 15px;
    font-size: 12px;
    font-weight: 600;
    color: var(--text-secondary);
  }

  .queue-call-actions {
    display: flex;
    gap: 8px;
  }

  .queue-action-btn {
    background-color: var(--success-color);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 6px 12px;
    font-size: 12px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
  }

  .queue-action-btn:hover {
    background-color: #45a049;
    transform: translateY(-1px);
  }

  /* Table view styles */
  .calls-table-container {
    overflow-x: auto;
    border-radius: 30px;
    background-color: var(--content-bg);
    margin-bottom: 20px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }

  .calls-table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
  }

  .calls-table th {
    text-align: left;
    padding: 18px 20px;
    background-color: var(--header-bg);
    font-weight: 700;
    font-size: 14px;
    position: sticky;
    top: 0;
    z-index: 10;
    color: var(--text-color);
  }

  .calls-table th:first-child {
    border-top-left-radius: 30px;
  }

  .calls-table th:last-child {
    border-top-right-radius: 30px;
  }

  .calls-table td {
    padding: 18px 20px;
    border-bottom: 1px solid var(--border-color);
    font-size: 14px;
    font-weight: 600;
    transition: all 0.3s ease;
  }

  .calls-table tr:hover td {
    background-color: rgba(255, 255, 255, 0.05);
  }

  .calls-table tr:last-child td {
    border-bottom: none;
  }

  .calls-table tr:last-child td:first-child {
    border-bottom-left-radius: 30px;
  }

  .calls-table tr:last-child td:last-child {
    border-bottom-right-radius: 30px;
  }

  .calls-table tr.selected td {
    background-color: rgba(255, 59, 48, 0.1);
    color: var(--highlight-color);
    font-weight: 700;
  }

  .status-badge {
    color: #fff;
    padding: 6px 16px;
    border-radius: 30px;
    font-size: 12px;
    display: inline-block;
    font-weight: 700;
    text-align: center;
    min-width: 100px;
    transition: all 0.3s ease;
  }

  .status-badge.in-progress {
    background-color: var(--accent-color);
  }

  .status-badge.pending {
    background-color: var(--pending-color);
  }

  .status-badge.unassigned {
    background-color: var(--unassigned-color);
  }

  .status-badge.completed {
    background-color: var(--success-color);
  }

  .status-badge.open {
    background-color: var(--success-color);
  }

  .table-actions {
    display: flex;
    gap: 8px;
  }

  .action-btn {
    background-color: var(--accent-color);
    color: white;
    border: none;
    border-radius: 6px;
    padding: 6px 8px;
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .action-btn:hover {
    background-color: var(--accent-hover);
    transform: scale(1.1);
  }

  .action-btn.view-btn {
    background-color: var(--medium-color);
  }

  .action-btn.link-btn {
    background-color: var(--high-color);
  }

  .action-btn.case-btn {
    background-color: var(--success-color);
  }

  /* Call details panel */
  .call-details-panel {
    position: fixed;
    top: 0;
    right: 0;
    width: 400px;
    height: 100vh;
    background-color: var(--content-bg);
    border-left: 1px solid var(--border-color);
    z-index: 1000;
    transition: transform 0.3s ease;
    box-shadow: -5px 0 15px rgba(0, 0, 0, 0.1);
    border-radius: 30px 0 0 30px;
    transform: translateX(100%);
    overflow-y: auto;
    overflow-x: hidden;
    display: flex;
    flex-direction: column;
    scrollbar-width: thin;
    scrollbar-color: rgba(255, 255, 255, 0.3) transparent;
  }

  .call-details-panel::-webkit-scrollbar {
    width: 8px;
  }

  .call-details-panel::-webkit-scrollbar-track {
    background: transparent;
  }

  .call-details-panel::-webkit-scrollbar-thumb {
    background-color: rgba(255, 255, 255, 0.3);
    border-radius: 4px;
  }

  .call-details-panel::-webkit-scrollbar-thumb:hover {
    background-color: rgba(255, 255, 255, 0.5);
  }

  .call-details-panel.active {
    transform: translateX(0);
  }

  .call-details-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 25px;
    border-bottom: 1px solid var(--border-color);
    background-color: var(--content-bg);
    flex-shrink: 0;
  }

  .call-details-title {
    font-size: 18px;
    font-weight: 700;
    color: var(--highlight-color);
    line-height: 1.4;
  }

  .close-details {
    background: none;
    border: none;
    color: var(--text-color);
    cursor: pointer;
    font-size: 24px;
    font-weight: 700;
    width: 32px;
    height: 32px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s ease;
  }

  .close-details:hover {
    background-color: rgba(255, 255, 255, 0.1);
  }

  .call-details-content {
    flex: 1;
    overflow-y: auto;
    overflow-x: hidden;
    padding: 25px;
    display: flex;
    flex-direction: column;
    gap: 18px;
    scrollbar-width: thin;
    scrollbar-color: rgba(255, 255, 255, 0.3) transparent;
  }

  .call-details-content::-webkit-scrollbar {
    width: 8px;
  }

  .call-details-content::-webkit-scrollbar-track {
    background: transparent;
  }

  .call-details-content::-webkit-scrollbar-thumb {
    background-color: rgba(255, 255, 255, 0.3);
    border-radius: 4px;
  }

  .call-details-content::-webkit-scrollbar-thumb:hover {
    background-color: rgba(255, 255, 255, 0.5);
  }

  .detail-item {
    display: flex;
    flex-direction: column;
    gap: 8px;
    background-color: var(--background-color);
    padding: 18px;
    border-radius: 15px;
    transition: all 0.3s ease;
  }

  .detail-item:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }

  .detail-label {
    font-size: 12px;
    font-weight: 700;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  .detail-value {
    font-size: 15px;
    font-weight: 600;
    color: var(--text-color);
    line-height: 1.4;
  }

  /* Modal Styles */
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 2000;
  }

  .modal-content {
    background-color: var(--content-bg);
    border-radius: 20px;
    width: 90%;
    max-width: 500px;
    max-height: 80vh;
    overflow-y: auto;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  }

  .modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px 25px;
    border-bottom: 1px solid var(--border-color);
  }

  .modal-header h3 {
    font-size: 18px;
    font-weight: 700;
    color: var(--text-color);
  }

  .call-timer-header {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 16px;
    font-weight: 700;
    color: var(--success-color);
  }

  .modal-close {
    background: none;
    border: none;
    color: var(--text-color);
    cursor: pointer;
    font-size: 24px;
    font-weight: 700;
    width: 32px;
    height: 32px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s ease;
  }

  .modal-close:hover {
    background-color: rgba(255, 255, 255, 0.1);
  }

  .modal-body {
    padding: 25px;
  }

  .form-group {
    margin-bottom: 20px;
  }

  .form-group label {
    display: block;
    font-size: 14px;
    font-weight: 600;
    color: var(--text-color);
    margin-bottom: 8px;
  }

  .form-group input,
  .form-group select,
  .form-group textarea {
    width: 100%;
    background-color: var(--input-bg);
    color: var(--text-color);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 12px 16px;
    font-size: 14px;
    font-weight: 600;
    transition: all 0.3s ease;
  }

  .form-group input:focus,
  .form-group select:focus,
  .form-group textarea:focus {
    outline: none;
    border-color: var(--accent-color);
  }

  .form-actions {
    display: flex;
    gap: 12px;
    justify-content: flex-end;
    margin-top: 25px;
  }

  .btn-primary {
    background-color: var(--accent-color);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 12px 24px;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .btn-primary:hover {
    background-color: var(--accent-hover);
    transform: translateY(-1px);
  }

  .btn-secondary {
    background-color: var(--border-color);
    color: var(--text-color);
    border: none;
    border-radius: 12px;
    padding: 12px 24px;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
  }

  .btn-secondary:hover {
    background-color: var(--text-secondary);
    transform: translateY(-1px);
  }

  /* Case Options Modal Styles */
  .case-options-modal {
    background-color: var(--content-bg);
    border-radius: 20px;
    width: 90%;
    max-width: 700px;
    max-height: 80vh;
    overflow-y: auto;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    animation: slideUp 0.3s ease-out;
  }

  @keyframes slideUp {
    from {
      opacity: 0;
      transform: translateY(30px);
    }

    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  .case-options-grid {
    display: flex;
    flex-direction: column;
    gap: 20px;
  }

  .case-option-card {
    display: flex;
    align-items: center;
    gap: 20px;
    padding: 25px;
    background-color: var(--background-color);
    border-radius: 15px;
    cursor: pointer;
    transition: all 0.3s ease;
    border: 2px solid var(--border-color);
  }

  .case-option-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
    border-color: var(--accent-color);
  }

  .option-icon {
    width: 70px;
    height: 70px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    flex-shrink: 0;
  }

  .option-icon.new-case {
    background-color: var(--success-color);
  }

  .option-icon.existing-case {
    background-color: var(--accent-color);
  }

  .option-icon.disposition-call {
    background-color: var(--medium-color);
  }

  .option-content {
    flex: 1;
  }

  .option-title {
    font-size: 20px;
    font-weight: 700;
    color: var(--text-color);
    margin-bottom: 8px;
  }

  .option-description {
    font-size: 16px;
    font-weight: 500;
    color: var(--text-secondary);
    line-height: 1.5;
  }

  .option-arrow {
    color: var(--text-secondary);
    transition: all 0.3s ease;
  }

  .case-option-card:hover .option-arrow {
    color: var(--accent-color);
    transform: translateX(5px);
  }

  /* Existing Case Search Modal */
  .existing-case-modal {
    background-color: var(--content-bg);
    border-radius: 20px;
    width: 90%;
    max-width: 800px;
    max-height: 80vh;
    overflow-y: auto;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    animation: slideUp 0.3s ease-out;
  }

  .case-search {
    margin-bottom: 20px;
  }

  .search-input {
    width: 100%;
    background-color: var(--input-bg);
    color: var(--text-color);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 15px 20px;
    font-size: 16px;
    font-weight: 600;
    transition: all 0.3s ease;
  }

  .search-input:focus {
    outline: none;
    border-color: var(--accent-color);
    box-shadow: 0 0 0 3px rgba(150, 75, 0, 0.1);
  }

  .existing-cases-list {
    max-height: 400px;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 15px;
  }

  .existing-case-item {
    display: flex;
    align-items: center;
    gap: 20px;
    padding: 20px;
    background-color: var(--background-color);
    border-radius: 15px;
    cursor: pointer;
    transition: all 0.3s ease;
    border: 2px solid var(--border-color);
  }

  .existing-case-item:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
    border-color: var(--accent-color);
  }

  .case-info {
    flex: 1;
  }

  .case-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
  }

  .case-id {
    font-size: 16px;
    font-weight: 700;
    color: var(--accent-color);
  }

  .case-priority {
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    padding: 4px 8px;
    border-radius: 8px;
    color: white;
  }

  .case-priority.critical {
    background-color: var(--critical-color);
  }

  .case-priority.high {
    background-color: var(--high-color);
  }

  .case-priority.medium {
    background-color: var(--medium-color);
  }

  .case-priority.low {
    background-color: var(--low-color);
  }

  .case-title {
    font-size: 18px;
    font-weight: 600;
    color: var(--text-color);
    margin-bottom: 8px;
    line-height: 1.3;
  }

  .case-meta {
    display: flex;
    gap: 15px;
    font-size: 14px;
    font-weight: 500;
    color: var(--text-secondary);
    margin-bottom: 8px;
  }

  .case-client {
    color: var(--text-color);
  }

  .case-status {
    display: flex;
    align-items: center;
  }

  .case-select-arrow {
    color: var(--text-secondary);
    transition: all 0.3s ease;
  }

  .existing-case-item:hover .case-select-arrow {
    color: var(--accent-color);
    transform: translateX(5px);
  }

  /* Queue Popup Modal */
  .queue-popup {
    background-color: var(--content-bg);
    border-radius: 20px;
    width: 90%;
    max-width: 600px;
    max-height: 80vh;
    overflow-y: auto;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    animation: slideUp 0.3s ease-out;
  }

  .queue-popup-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px 25px;
    border-bottom: 1px solid var(--border-color);
  }

  .queue-popup-header h3 {
    font-size: 18px;
    font-weight: 700;
    color: var(--text-color);
  }

  .queue-members {
    padding: 25px;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 15px;
  }

  .queue-member-card {
    display: flex;
    align-items: center;
    gap: 15px;
    padding: 15px;
    background-color: var(--background-color);
    border-radius: 15px;
    transition: all 0.3s ease;
    cursor: pointer;
  }

  .queue-member-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  }

  .member-avatar {
    position: relative;
    width: 50px;
    height: 50px;
    border-radius: 50%;
    overflow: hidden;
    flex-shrink: 0;
  }

  .member-avatar img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  .status-indicator {
    position: absolute;
    bottom: 2px;
    right: 2px;
    width: 12px;
    height: 12px;
    border-radius: 50%;
    border: 2px solid var(--background-color);
  }

  .status-indicator.available {
    background-color: var(--success-color);
  }

  .status-indicator.busy {
    background-color: var(--danger-color);
  }

  .status-indicator.away {
    background-color: var(--pending-color);
  }

  .member-info {
    flex: 1;
  }

  .member-name {
    font-size: 14px;
    font-weight: 700;
    color: var(--text-color);
    margin-bottom: 2px;
  }

  .member-role {
    font-size: 12px;
    font-weight: 600;
    color: var(--text-secondary);
    margin-bottom: 2px;
  }

  .member-status {
    font-size: 11px;
    font-weight: 600;
    color: var(--accent-color);
  }

  .queue-popup-footer {
    padding: 20px 25px;
    border-top: 1px solid var(--border-color);
    display: flex;
    justify-content: flex-end;
  }

  /* Ringing Call Interface Styles */
  .ringing-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.6);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 3000;
  }

  .ringing-container {
    background-color: var(--content-bg);
    border-radius: 30px;
    width: 90%;
    max-width: 450px;
    padding: 30px;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);
    text-align: center;
  }

  .ringing-header {
    margin-bottom: 20px;
  }

  .call-type-badge {
    font-size: 14px;
    font-weight: 700;
    text-transform: uppercase;
    padding: 8px 16px;
    border-radius: 30px;
    color: white;
    display: inline-block;
  }

  .call-type-badge.critical {
    background-color: var(--critical-color);
  }

  .call-type-badge.high {
    background-color: var(--high-color);
  }

  .call-type-badge.medium {
    background-color: var(--medium-color);
  }

  .call-type-badge.low {
    background-color: var(--low-color);
  }

  .caller-info {
    margin-bottom: 30px;
  }

  .caller-avatar {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    background-color: var(--background-color);
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 15px;
  }

  .caller-avatar svg {
    width: 40px;
    height: 40px;
    stroke: var(--text-color);
  }

  .caller-name {
    font-size: 22px;
    font-weight: 700;
    color: var(--text-color);
    margin-bottom: 8px;
  }

  .caller-number {
    font-size: 16px;
    font-weight: 600;
    color: var(--text-secondary);
    margin-bottom: 12px;
  }

  .call-duration {
    font-size: 15px;
    font-weight: 600;
    color: var(--success-color);
  }

  .ringing-animation {
    position: relative;
    width: 120px;
    height: 120px;
    margin: 0 auto 30px;
  }

  .pulse-ring {
    width: 100%;
    height: 100%;
    border-radius: 50%;
    border: 3px solid var(--medium-color);
    position: absolute;
    top: 0;
    left: 0;
    animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
    opacity: 0;
  }

  .pulse-ring.delay-1 {
    animation-delay: 0.5s;
  }

  .pulse-ring.delay-2 {
    animation-delay: 1s;
  }

  @keyframes pulse {
    0% {
      transform: scale(0);
      opacity: 0;
    }

    50% {
      opacity: 1;
    }

    100% {
      transform: scale(1.2);
      opacity: 0;
    }
  }

  .call-actions {
    display: flex;
    justify-content: center;
    gap: 20px;
  }

  .call-btn {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    border: none;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s ease;
  }

  .call-btn svg {
    width: 28px;
    height: 28px;
    stroke: white;
  }

  .call-btn.decline {
    background-color: var(--danger-color);
  }

  .call-btn.decline:hover {
    background-color: #d32f2f;
    transform: scale(1.1);
  }

  .call-btn.answer {
    background-color: var(--success-color);
  }

  .call-btn.answer:hover {
    background-color: #43a047;
    transform: scale(1.1);
  }

  /* Case Form Styles */
  .case-form-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.4);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 4000;
  }

  .case-form-container {
    background-color: var(--content-bg);
    border-radius: 30px;
    width: 95%;
    max-width: 900px;
    max-height: 90vh;
    overflow: hidden;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);
    display: flex;
    flex-direction: column;
  }

  .case-form-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 25px 30px;
    border-bottom: 1px solid var(--border-color);
    flex-shrink: 0;
  }

  .form-title {
    flex: 1;
    text-align: left;
  }

  .form-title h3 {
    font-size: 20px;
    font-weight: 700;
    color: var(--text-color);
    margin-bottom: 5px;
  }

  .case-id {
    font-size: 14px;
    font-weight: 600;
    color: var(--text-secondary);
  }

  .call-timer {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 16px;
    font-weight: 700;
    color: var(--success-color);
    flex-shrink: 0;
  }

  .minimize-btn {
    background: none;
    border: none;
    color: var(--text-color);
    cursor: pointer;
    font-size: 20px;
    width: 32px;
    height: 32px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s ease;
  }

  .minimize-btn:hover {
    background-color: rgba(255, 255, 255, 0.1);
  }

  .case-form-content {
    flex: 1;
    overflow-y: auto;
    padding: 30px;
  }

  .form-section {
    margin-bottom: 30px;
  }

  .section-title {
    font-size: 18px;
    font-weight: 700;
    color: var(--text-color);
    margin-bottom: 20px;
  }

  .form-row {
    display: flex;
    gap: 20px;
  }

  .form-row .form-group {
    flex: 1;
  }

  .form-control {
    width: 100%;
    background-color: var(--input-bg);
    color: var(--text-color);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 12px 16px;
    font-size: 14px;
    font-weight: 600;
    transition: all 0.3s ease;
  }

  .form-control:focus {
    outline: none;
    border-color: var(--accent-color);
  }

  .form-actions {
    display: flex;
    gap: 15px;
    justify-content: flex-end;
    margin-top: 30px;
  }

  /* Minimized Case Form Styles */
  .minimized-case-form {
    position: fixed;
    bottom: 20px;
    right: 20px;
    background-color: var(--content-bg);
    border-radius: 15px;
    padding: 12px 20px;
    cursor: pointer;
    box-shadow: 0 5px 20px rgba(0, 0, 0, 0.2);
    display: flex;
    align-items: center;
    transition: all 0.3s ease;
    z-index: 4000;
  }

  .minimized-case-form:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
  }

  .minimized-content {
    display: flex;
    align-items: center;
    gap: 10px;
  }

  .minimized-content svg {
    width: 18px;
    height: 18px;
    stroke: var(--text-color);
  }

  .minimized-content span {
    font-size: 15px;
    font-weight: 600;
    color: var(--text-color);
  }

  .minimized-content .timer {
    font-size: 14px;
    font-weight: 600;
    color: var(--success-color);
  }

  /* Enhanced Disposition Modal Styles */
  .disposition-modal {
    background-color: var(--content-bg);
    border-radius: 20px;
    width: 95%;
    max-width: 800px;
    max-height: 90vh;
    overflow-y: auto;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    animation: slideUp 0.3s ease-out;
  }

  .disposition-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
    margin-bottom: 25px;
  }

  .duration-display {
    background-color: var(--background-color) !important;
    color: var(--success-color) !important;
    font-weight: 700 !important;
    text-align: center;
  }

  .disposition-summary {
    background-color: var(--background-color);
    border-radius: 15px;
    padding: 20px;
    margin-top: 25px;
    border: 2px solid var(--border-color);
  }

  .disposition-summary h4 {
    font-size: 16px;
    font-weight: 700;
    color: var(--text-color);
    margin-bottom: 15px;
    text-align: center;
  }

  .summary-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 15px;
  }

  .summary-item {
    display: flex;
    flex-direction: column;
    gap: 5px;
    text-align: center;
  }

  .summary-label {
    font-size: 12px;
    font-weight: 600;
    color: var(--text-secondary);
    text-transform: uppercase;
  }

  .summary-value {
    font-size: 14px;
    font-weight: 700;
    color: var(--text-color);
  }

  .summary-value.priority-indicator {
    padding: 4px 8px;
    border-radius: 8px;
    color: white;
    text-transform: uppercase;
  }

  /* Call Options Modal Styles */
  .call-options-modal {
    max-width: 400px;
  }

  .call-options {
    display: flex;
    flex-direction: column;
    gap: 20px;
  }

  .call-option {
    display: flex;
    align-items: center;
    gap: 15px;
    padding: 20px;
    background-color: var(--background-color);
    border-radius: 15px;
    cursor: pointer;
    transition: all 0.3s ease;
    border: 2px solid var(--border-color);
  }

  .call-option:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
    border-color: var(--accent-color);
  }

  .contacts-modal {
    max-width: 600px;
  }

  .contacts-search {
    margin-bottom: 20px;
  }

  .contacts-list {
    max-height: 300px;
    overflow-y: auto;
  }

  .contact-item {
    display: flex;
    align-items: center;
    gap: 15px;
    padding: 15px;
    background-color: var(--background-color);
    border-radius: 12px;
    transition: all 0.3s ease;
    cursor: pointer;
  }

  .contact-item:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  }

  .contact-avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background-color: var(--content-bg);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }

  .contact-avatar svg {
    width: 20px;
    height: 20px;
    stroke: var(--text-color);
  }

  .contact-info {
    flex: 1;
  }

  .contact-name {
    font-size: 15px;
    font-weight: 700;
    color: var(--text-color);
    margin-bottom: 4px;
  }

  .contact-phone {
    font-size: 14px;
    font-weight: 600;
    color: var(--text-secondary);
    margin-bottom: 6px;
  }

  .contact-meta {
    font-size: 12px;
    font-weight: 500;
    color: var(--text-secondary);
    display: flex;
    gap: 10px;
  }

  .contact-priority {
    width: 20px;
    height: 20px;
    border-radius: 50%;
    flex-shrink: 0;
  }

  .priority-indicator {
    display: block;
    width: 10px;
    height: 10px;
    border-radius: 50%;
  }

  .priority-indicator.critical {
    background-color: var(--critical-color);
  }

  .priority-indicator.high {
    background-color: var(--high-color);
  }

  .priority-indicator.medium {
    background-color: var(--medium-color);
  }

  .priority-indicator.low {
    background-color: var(--low-color);
  }

  .new-call-modal {
    max-width: 450px;
  }

  .phone-input {
    width: 100%;
    background-color: var(--input-bg);
    color: var(--text-color);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 15px 20px;
    font-size: 16px;
    font-weight: 600;
    transition: all 0.3s ease;
  }

  .call-info {
    margin-top: 20px;
    margin-bottom: 20px;
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .info-item {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 14px;
    font-weight: 600;
    color: var(--text-secondary);
  }

  .info-item svg {
    width: 18px;
    height: 18px;
    stroke: var(--text-secondary);
  }

  /* Notification Styles */
  .notification-overlay {
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 5000;
    animation: slideInRight 0.3s ease-out;
  }

  @keyframes slideInRight {
    from {
      opacity: 0;
      transform: translateX(100%);
    }

    to {
      opacity: 1;
      transform: translateX(0);
    }
  }

  .notification-container {
    display: flex;
    align-items: center;
    gap: 12px;
    background-color: var(--content-bg);
    border-radius: 12px;
    padding: 16px 20px;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
    border-left: 4px solid;
    min-width: 300px;
    max-width: 400px;
  }

  .notification-container.success {
    border-left-color: var(--success-color);
  }

  .notification-container.info {
    border-left-color: var(--medium-color);
  }

  .notification-container.error {
    border-left-color: var(--danger-color);
  }

  .notification-icon {
    flex-shrink: 0;
    width: 24px;
    height: 24px;
    color: var(--text-color);
  }

  .notification-container.success .notification-icon {
    color: var(--success-color);
  }

  .notification-container.info .notification-icon {
    color: var(--medium-color);
  }

  .notification-container.error .notification-icon {
    color: var(--danger-color);
  }

  .notification-content {
    flex: 1;
  }

  .notification-message {
    font-size: 14px;
    font-weight: 600;
    color: var(--text-color);
    line-height: 1.4;
  }

  .notification-close {
    background: none;
    border: none;
    color: var(--text-secondary);
    cursor: pointer;
    padding: 4px;
    border-radius: 4px;
    transition: all 0.2s ease;
    flex-shrink: 0;
  }

  .notification-close:hover {
    background-color: rgba(255, 255, 255, 0.1);
    color: var(--text-color);
  }

  /* Responsive Styles */
  @media (max-width: 768px) {
    .header-actions {
      gap: 12px;
    }

    .theme-toggle {
      padding: 6px 12px;
      font-size: 13px;
      min-width: 100px;
    }
  }
</style>