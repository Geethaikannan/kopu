// Mock data
const mockData = {
    dashboard: {
        currentUser: 'John Doe',
        pcStatus: 'Active',
        usbStatus: 'Connected',
        riskLevel: 'Low',
        activities: [
            { time: '10:30 AM', action: 'User logged in' },
            { time: '10:45 AM', action: 'USB device connected' },
            { time: '11:00 AM', action: 'Application started' },
            { time: '11:15 AM', action: 'File accessed' }
        ]
    },
    liveMonitoring: {
        runningApps: ['Chrome', 'VS Code', 'Notepad', 'Calculator'],
        fileAccess: 'Last accessed: document.pdf at 11:20 AM',
        loginTime: 'Logged in at 10:30 AM'
    },
    alerts: [
        { type: 'Unauthorized Access', time: '11:05 AM', severity: 'High' },
        { type: 'USB Device Connected', time: '10:45 AM', severity: 'Medium' },
        { type: 'Application Blocked', time: '10:50 AM', severity: 'Low' }
    ],
    logs: [
        { timestamp: '2023-10-01 10:30:00', activity: 'Login', description: 'User John Doe logged in' },
        { timestamp: '2023-10-01 10:45:00', activity: 'USB', description: 'USB device connected' },
        { timestamp: '2023-10-01 11:00:00', activity: 'Application', description: 'Chrome started' },
        { timestamp: '2023-10-01 11:05:00', activity: 'Alert', description: 'Unauthorized access attempt' },
        { timestamp: '2023-10-01 11:15:00', activity: 'File Access', description: 'document.pdf accessed' }
    ]
};

// Navigation
document.addEventListener('DOMContentLoaded', function() {
    const navLinks = document.querySelectorAll('.sidebar a');
    const pages = document.querySelectorAll('.page');

    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const pageId = this.getAttribute('data-page');

            // Remove active class from all links and pages
            navLinks.forEach(l => l.classList.remove('active'));
            pages.forEach(p => p.classList.remove('active'));

            // Add active class to clicked link and corresponding page
            this.classList.add('active');
            document.getElementById(pageId).classList.add('active');

            // Load page data
            loadPageData(pageId);
        });
    });

    // Load default page (Dashboard)
    loadPageData('dashboard');
    document.querySelector('[data-page="dashboard"]').classList.add('active');

    // Auto-refresh dashboard every 5 seconds
    setInterval(() => {
        if (document.getElementById('dashboard').classList.contains('active')) {
            loadDashboardData();
        }
    }, 5000);

    // Log filtering
    document.getElementById('log-filter').addEventListener('input', filterLogs);
});

function loadPageData(pageId) {
    switch(pageId) {
        case 'dashboard':
            loadDashboardData();
            break;
        case 'live-monitoring':
            loadLiveMonitoringData();
            break;
        case 'alerts':
            loadAlertsData();
            break;
        case 'logs':
            loadLogsData();
            break;
        case 'control-panel':
            // Control panel doesn't need data loading
            break;
    }
}

function loadDashboardData() {
    const data = mockData.dashboard;

    document.getElementById('current-user').textContent = data.currentUser;
    document.getElementById('pc-status').textContent = data.pcStatus;
    document.getElementById('usb-status').textContent = data.usbStatus;

    const riskElement = document.getElementById('risk-level');
    riskElement.textContent = data.riskLevel;
    riskElement.className = data.riskLevel.toLowerCase();

    const timeline = document.getElementById('activity-timeline');
    timeline.innerHTML = '';
    data.activities.forEach(activity => {
        const li = document.createElement('li');
        li.textContent = `${activity.time}: ${activity.action}`;
        timeline.appendChild(li);
    });
}

function loadLiveMonitoringData() {
    const data = mockData.liveMonitoring;

    const appsList = document.getElementById('running-apps');
    appsList.innerHTML = '';
    data.runningApps.forEach(app => {
        const li = document.createElement('li');
        li.textContent = app;
        appsList.appendChild(li);
    });

    document.getElementById('file-access').textContent = data.fileAccess;
    document.getElementById('login-time').textContent = data.loginTime;
}

function loadAlertsData() {
    const alertsList = document.getElementById('alerts-list');
    alertsList.innerHTML = '';

    mockData.alerts.forEach(alert => {
        const alertCard = document.createElement('div');
        alertCard.className = `alert-card ${alert.severity.toLowerCase()}`;
        alertCard.innerHTML = `
            <h4>${alert.type}</h4>
            <p><strong>Time:</strong> ${alert.time}</p>
            <p><strong>Severity:</strong> ${alert.severity}</p>
        `;
        alertsList.appendChild(alertCard);
    });
}

function loadLogsData() {
    const logsBody = document.getElementById('logs-body');
    logsBody.innerHTML = '';

    mockData.logs.forEach(log => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${log.timestamp}</td>
            <td>${log.activity}</td>
            <td>${log.description}</td>
        `;
        logsBody.appendChild(row);
    });
}

function filterLogs() {
    const filterValue = document.getElementById('log-filter').value.toLowerCase();
    const rows = document.querySelectorAll('#logs-body tr');

    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(filterValue) ? '' : 'none';
    });
}

// Control panel actions
document.getElementById('lock-pc').addEventListener('click', () => {
    if (confirm('Are you sure you want to lock the PC?')) {
        alert('PC locked successfully!');
    }
});

document.getElementById('disable-usb').addEventListener('click', () => {
    if (confirm('Are you sure you want to disable USB ports?')) {
        alert('USB ports disabled successfully!');
    }
});

document.getElementById('block-app').addEventListener('click', () => {
    const appName = prompt('Enter the application name to block:');
    if (appName && confirm(`Are you sure you want to block ${appName}?`)) {
        alert(`${appName} blocked successfully!`);
    }
});

document.getElementById('force-logout').addEventListener('click', () => {
    if (confirm('Are you sure you want to force logout?')) {
        alert('User logged out successfully!');
    }
});
