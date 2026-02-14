/**
 * Dashboard Module
 * Handles dashboard functionality, API polling, and real-time updates
 */

const POLLING_INTERVAL = 10000; // 10 seconds

// State
let currentPage = 'dashboard';
let pollingTimer = null;

// Initialize dashboard
function initDashboard() {
    if (!requireAuth()) return;

    // Setup navigation
    setupNavigation();

    // Setup logout
    document.getElementById('logout-btn').addEventListener('click', logout);

    // Setup refresh buttons
    document.getElementById('refresh-alerts-btn')?.addEventListener('click', loadAlerts);
    document.getElementById('refresh-logs-btn')?.addEventListener('click', loadLogs);
    document.getElementById('risk-filter')?.addEventListener('change', loadLogs);

    // Initial data load
    loadDashboardData();
    loadAlerts();
    loadLogs();

    // Start polling
    startPolling();

    // Update connection status
    updateConnectionStatus(true);
}

// Setup navigation
function setupNavigation() {
    const navItems = document.querySelectorAll('.nav-item');
    
    navItems.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            const page = item.getAttribute('data-page');
            switchPage(page);
            
            // Update active state
            navItems.forEach(nav => nav.classList.remove('active'));
            item.classList.add('active');
        });
    });
}

// Switch page
function switchPage(page) {
    // Hide all pages
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
    
    // Show selected page
    const selectedPage = document.getElementById(`${page}-page`);
    if (selectedPage) {
        selectedPage.classList.add('active');
    }
    
    // Update title
    const titles = {
        'dashboard': 'Dashboard',
        'alerts': 'Alerts',
        'logs': 'Activity Logs'
    };
    document.getElementById('page-title').textContent = titles[page] || 'Dashboard';
    
    currentPage = page;
    
    // Refresh data for the page
    if (page === 'dashboard') {
        loadDashboardData();
    } else if (page === 'alerts') {
        loadAlerts();
    } else if (page === 'logs') {
        loadLogs();
    }
}

// Start polling for updates
function startPolling() {
    if (pollingTimer) {
        clearInterval(pollingTimer);
    }
    
    pollingTimer = setInterval(() => {
        if (currentPage === 'dashboard') {
            loadDashboardData();
        }
        loadAlertsCount();
    }, POLLING_INTERVAL);
}

// Update connection status
function updateConnectionStatus(online) {
    const statusEl = document.getElementById('connection-status');
    if (online) {
        statusEl.textContent = '● Online';
        statusEl.className = 'status-badge status-online';
    } else {
        statusEl.textContent = '● Offline';
        statusEl.className = 'status-badge status-offline';
    }
}

// Update last updated time
function updateLastUpdated() {
    const now = new Date();
    document.getElementById('last-updated').textContent = 
        `Last updated: ${now.toLocaleTimeString()}`;
}

// Load dashboard data
async function loadDashboardData() {
    try {
        // Load activity stats
        const statsResponse = await apiRequest('/api/activity/stats?hours=24');
        if (statsResponse && statsResponse.ok) {
            const stats = await statsResponse.json();
            updateDashboardStats(stats);
        }

        // Load recent activities
        const activitiesResponse = await apiRequest('/api/activity/?limit=10');
        if (activitiesResponse && activitiesResponse.ok) {
            const activities = await activitiesResponse.json();
            updateRecentActivity(activities);
        }

        // Load alert stats
        const alertStatsResponse = await apiRequest('/api/alerts/stats');
        if (alertStatsResponse && alertStatsResponse.ok) {
            const alertStats = await alertStatsResponse.json();
            updateAlertStats(alertStats);
        }

        updateConnectionStatus(true);
        updateLastUpdated();
    } catch (error) {
        console.error('Failed to load dashboard data:', error);
        updateConnectionStatus(false);
    }
}

// Update dashboard stats
function updateDashboardStats(stats) {
    document.getElementById('total-activities').textContent = stats.total_activities || 0;
    document.getElementById('avg-risk-score').textContent = stats.average_risk_score?.toFixed(1) || '0.0';

    // Update risk distribution bars
    const total = stats.total_activities || 1;
    const distribution = stats.risk_distribution || {};

    // Update counts
    document.getElementById('risk-low-count').textContent = distribution.low || 0;
    document.getElementById('risk-medium-count').textContent = distribution.medium || 0;
    document.getElementById('risk-high-count').textContent = distribution.high || 0;
    document.getElementById('risk-critical-count').textContent = distribution.critical || 0;

    // Update bar widths
    document.getElementById('risk-low-bar').style.width = `${((distribution.low || 0) / total) * 100}%`;
    document.getElementById('risk-medium-bar').style.width = `${((distribution.medium || 0) / total) * 100}%`;
    document.getElementById('risk-high-bar').style.width = `${((distribution.high || 0) / total) * 100}%`;
    document.getElementById('risk-critical-bar').style.width = `${((distribution.critical || 0) / total) * 100}%`;
}

// Update alert stats
function updateAlertStats(stats) {
    const activeAlerts = stats.active || 0;
    document.getElementById('active-alerts').textContent = activeAlerts;
    
    // Update badge
    const badge = document.getElementById('alert-badge');
    if (activeAlerts > 0) {
        badge.textContent = activeAlerts;
        badge.style.display = 'inline';
    } else {
        badge.style.display = 'none';
    }

    // Update high/critical count
    const highCritical = (stats.by_severity?.high || 0) + (stats.by_severity?.critical || 0);
    document.getElementById('high-risk-count').textContent = highCritical;
}

// Update recent activity table
function updateRecentActivity(activities) {
    const tbody = document.getElementById('recent-activity-table');
    
    if (!activities || activities.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" class="text-center">No recent activity</td></tr>';
        return;
    }

    tbody.innerHTML = activities.map(activity => `
        <tr>
            <td>${formatDate(activity.timestamp)}</td>
            <td>${activity.agent_id || 'Unknown'}</td>
            <td>${activity.activity_type}</td>
            <td>${activity.app_name || '-'}</td>
            <td>${getRiskBadge(activity.risk_level)}</td>
            <td>${activity.risk_score?.toFixed(2) || '0.00'}</td>
        </tr>
    `).join('');
}

// Load alerts
async function loadAlerts() {
    try {
        const response = await apiRequest('/api/alerts/active');
        if (response && response.ok) {
            const alerts = await response.json();
            updateAlertsList(alerts);
        }
    } catch (error) {
        console.error('Failed to load alerts:', error);
    }
}

// Load alerts count (for badge)
async function loadAlertsCount() {
    try {
        const response = await apiRequest('/api/alerts/stats');
        if (response && response.ok) {
            const stats = await response.json();
            updateAlertStats(stats);
        }
    } catch (error) {
        console.error('Failed to load alert stats:', error);
    }
}

// Update alerts list
function updateAlertsList(alerts) {
    const container = document.getElementById('alerts-container');
    
    if (!alerts || alerts.length === 0) {
        container.innerHTML = '<p class="text-center">No active alerts</p>';
        return;
    }

    container.innerHTML = alerts.map(alert => `
        <div class="alert-item alert-${alert.severity}">
            <div class="alert-header">
                <span class="alert-title">${alert.alert_type}</span>
                <span class="alert-time">${formatDate(alert.created_at)}</span>
            </div>
            <p class="alert-message">${alert.message}</p>
            <div class="alert-actions">
                <button class="btn btn-success btn-sm" onclick="resolveAlert(${alert.id})">
                    Resolve
                </button>
                <span class="risk-badge risk-badge-${alert.severity}">${alert.severity}</span>
            </div>
        </div>
    `).join('');
}

// Resolve alert
async function resolveAlert(alertId) {
    try {
        const response = await apiRequest(`/api/alerts/${alertId}/resolve`, {
            method: 'PUT'
        });
        
        if (response && response.ok) {
            // Refresh alerts
            loadAlerts();
            loadAlertsCount();
        }
    } catch (error) {
        console.error('Failed to resolve alert:', error);
        alert('Failed to resolve alert. Please try again.');
    }
}

// Load logs
async function loadLogs() {
    try {
        const riskFilter = document.getElementById('risk-filter')?.value;
        let url = '/api/activity/?limit=50';
        if (riskFilter) {
            url += `&risk_level=${riskFilter}`;
        }
        
        const response = await apiRequest(url);
        if (response && response.ok) {
            const logs = await response.json();
            updateLogsTable(logs);
        }
    } catch (error) {
        console.error('Failed to load logs:', error);
    }
}

// Update logs table
function updateLogsTable(logs) {
    const tbody = document.getElementById('logs-table');
    
    if (!logs || logs.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="text-center">No logs found</td></tr>';
        return;
    }

    tbody.innerHTML = logs.map(log => `
        <tr>
            <td>${log.id}</td>
            <td>${formatDate(log.timestamp)}</td>
            <td>${log.agent_id || 'Unknown'}</td>
            <td>${log.activity_type}</td>
            <td>${log.app_name || '-'}</td>
            <td>${getRiskBadge(log.risk_level)}</td>
            <td>${log.risk_score?.toFixed(2) || '0.00'}</td>
        </tr>
    `).join('');
}

// Helper: Format date
function formatDate(dateString) {
    if (!dateString) return '-';
    const date = new Date(dateString);
    return date.toLocaleString();
}

// Helper: Get risk badge HTML
function getRiskBadge(level) {
    const classes = {
        'low': 'risk-badge-low',
        'medium': 'risk-badge-medium',
        'high': 'risk-badge-high',
        'critical': 'risk-badge-critical'
    };
    return `<span class="risk-badge ${classes[level] || 'risk-badge-low'}">${level || 'low'}</span>`;
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    const currentPage = window.location.pathname.split('/').pop();
    
    if (currentPage === 'dashboard.html') {
        initDashboard();
    }
});
