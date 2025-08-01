import { ref } from 'vue';

// Helper functions
const randomId = () => Math.floor(Math.random() * 1000000).toString().padStart(6, '0');
const randomDate = (days = 30) => {
    const date = new Date();
    date.setDate(date.getDate() - Math.floor(Math.random() * days));
    return date.toISOString();
};
const randomFutureDate = (days = 30) => {
    const date = new Date();
    date.setDate(date.getDate() + Math.floor(Math.random() * days));
    return date.toISOString();
};

// Mock data for relationships
const caseTypes = [
    { id: 1, name: 'GBV', code: 'GBV', default_sla_hours: 24 },
    { id: 2, name: 'Assault', code: 'ASLT', default_sla_hours: 48 },
    { id: 3, name: 'Medical', code: 'MED', default_sla_hours: 12 },
    { id: 4, name: 'Transport', code: 'TRNS', default_sla_hours: 72 }
];

const caseStatuses = [
    { id: 1, name: 'Open', is_closed: false },
    { id: 2, name: 'In Progress', is_closed: false },
    { id: 3, name: 'Pending Review', is_closed: false },
    { id: 4, name: 'Resolved', is_closed: true },
    { id: 5, name: 'Closed', is_closed: true }
];

const users = [
    { id: 1, name: 'Robert Jackson' },
    { id: 2, name: 'Sarah Mitchell' },
    { id: 3, name: 'Michael Lee' },
    { id: 4, name: 'Ntaate Kimani' },
    { id: 5, name: 'Emergency Director' }
];

// Generate a single case
const generateCase = () => {
    const caseType = caseTypes[Math.floor(Math.random() * caseTypes.length)];
    const status = caseStatuses[Math.floor(Math.random() * caseStatuses.length)];
    const assignedUser = Math.random() > 0.3 ? users[Math.floor(Math.random() * users.length)] : null;
    const isResolved = status.is_closed;
    const createdDate = randomDate(60);
    const dueDate = randomFutureDate(30);

    const timestamp = new Date(createdDate).toISOString().split('T')[0].replace(/-/g, '');
    const caseNumber = `${caseType.code}-${timestamp}-${randomId().slice(0, 4)}`;

    return {
        id: randomId(),
        case_type: caseType,
        case_number: caseNumber,
        title: `Case #${caseNumber} - ${caseType.name} ${['Request', 'Incident', 'Support', 'Emergency'][Math.floor(Math.random() * 4)]}`,
        description: `This is a ${caseType.name.toLowerCase()} case requiring attention. ${['Urgent action needed.', 'Please review details.', 'Needs follow up.', 'Critical situation.'][Math.floor(Math.random() * 4)]}`,
        status: status,
        priority: Math.floor(Math.random() * 3) + 1, // 1-3
        assigned_to: assignedUser,
        due_date: dueDate,
        resolved_at: isResolved ? randomDate(10) : null,
        resolved_by: isResolved ? users[Math.floor(Math.random() * users.length)] : null,
        sla_expires_at: randomFutureDate(7),
        is_high_priority: Math.random() > 0.7,
        is_confidential: Math.random() > 0.8,
        source_channel: ['Email', 'Web', 'Phone', 'In-Person', 'Referral'][Math.floor(Math.random() * 5)],
        reference_id: `EXT-${randomId()}`,
        custom_fields: {},
        tags: [caseType.name.toLowerCase(), status.name.toLowerCase().replace(' ', '-')],
        created_at: createdDate,
        updated_at: randomDate(10),
        audit_logs: [],
        // Additional computed properties
        is_overdue: new Date(dueDate) < new Date(),
        time_to_resolution: isResolved ?
            `${Math.floor(Math.random() * 10) + 1} days` : null
    };
};

// Generate multiple cases
export const generateCases = (count = 10) => {
    return Array.from({ length: count }, () => generateCase());
};

// Utility functions for the generator
export const getCaseTypes = () => caseTypes;
export const getCaseStatuses = () => caseStatuses;
export const getUsers = () => users;

// Default export
export default {
    generateCases,
    getCaseTypes,
    getCaseStatuses,
    getUsers
};