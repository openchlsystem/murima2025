export const sampleCases = [
    {
        id: '123456',
        title: 'Case #123456-GBV request',
        priority: 'High',
        assignedTo: 'Robert Jackson',
        caseTitle: 'Emergency call',
        caseFiler: 'Nelson Adega',
        caseer: 'Mitch Ngugi',
        jurisdiction: 'Judge- in Court',
        disposition: 'Abusive Call',
        date: '15th Aug 2025',
        escalatedTo: 'Ntaate Kimani'
    },
    {
        id: '789012',
        title: 'Case #789012 - Assault',
        priority: 'Medium',
        assignedTo: 'Sarah Mitchell',
        caseTitle: 'Assault Case',
        caseFiler: 'Jane Doe',
        caseer: 'John Smith',
        jurisdiction: 'District Court',
        disposition: 'Under Investigation',
        date: '14th Aug 2025',
        escalatedTo: 'Senior Detective'
    },
    {
        id: '345678-1',
        title: 'Case #345678-In-transit medical support',
        priority: 'Low',
        assignedTo: null,
        caseTitle: 'Medical Support',
        caseFiler: 'Medical Team',
        caseer: 'Emergency Services',
        jurisdiction: 'Emergency Response',
        disposition: 'Resolved',
        date: '13th Aug 2025',
        escalatedTo: 'Hospital Administration'
    },
    {
        id: '901234-1',
        title: 'Case #901234-battery coordination',
        priority: 'High',
        assignedTo: 'Michael Lee',
        caseTitle: 'Battery Case',
        caseFiler: 'Police Department',
        caseer: 'Detective Brown',
        jurisdiction: 'Criminal Court',
        disposition: 'Active Investigation',
        date: '16th Aug 2025',
        escalatedTo: 'District Attorney'
    },
    {
        id: '345678-2',
        title: 'Case #345678-In-transit medical support',
        priority: 'High',
        assignedTo: 'Michael Lee',
        caseTitle: 'Medical Emergency',
        caseFiler: 'Paramedic Team',
        caseer: 'Emergency Coordinator',
        jurisdiction: 'Emergency Response',
        disposition: 'In Progress',
        date: '16th Aug 2025',
        escalatedTo: 'Medical Director'
    },
    {
        id: '901234-2',
        title: 'Case #901234-Transport coordination',
        priority: 'High',
        assignedTo: 'Michael Lee',
        caseTitle: 'Transport Coordination',
        caseFiler: 'Transport Authority',
        caseer: 'Logistics Team',
        jurisdiction: 'Transport Commission',
        disposition: 'Pending Review',
        date: '12th Aug 2025',
        escalatedTo: 'Operations Manager'
    },
    {
        id: '901234-3',
        title: 'Case #901234-Transport coordination',
        priority: 'High',
        assignedTo: 'Michael Lee',
        caseTitle: 'Transport Emergency',
        caseFiler: 'Emergency Services',
        caseer: 'Transport Coordinator',
        jurisdiction: 'Emergency Response',
        disposition: 'Active',
        date: '16th Aug 2025',
        escalatedTo: 'Emergency Director'
    }
];

// Optional: Export additional utility functions
export const generateSampleCases = (count = 5) => {
    // If you need to generate more cases dynamically
    const newCases = [];
    for (let i = 0; i < count; i++) {
        newCases.push({
            id: `auto-${Math.floor(Math.random() * 1000000)}`,
            title: `Case #auto-${i + 1} - Generated case`,
            priority: ['Low', 'Medium', 'High'][Math.floor(Math.random() * 3)],
            assignedTo: Math.random() > 0.3 ? 'Generated User' : null,
            caseTitle: ['Emergency', 'Routine', 'Investigation'][Math.floor(Math.random() * 3)],
            caseFiler: 'System Generated',
            caseer: 'Auto Caseer',
            jurisdiction: 'Generated Jurisdiction',
            disposition: ['Open', 'In Progress', 'Resolved'][Math.floor(Math.random() * 3)],
            date: new Date(Date.now() - Math.random() * 30 * 24 * 60 * 60 * 1000).toLocaleDateString('en-US', { day: 'numeric', month: 'short', year: 'numeric' }),
            escalatedTo: 'System Admin'
        });
    }
    return [...sampleCases, ...newCases];
};

// Default export
export default sampleCases;