/**
 * MyLabLink - API Integration
 * ربط الصفحات ببيانات حقيقية من قاعدة البيانات
 */

// تكوين API
const API_CONFIG = {
    baseURL: window.API_BASE || 'http://127.0.0.1:8000',
    endpoints: {
        // المستخدمين
        login: '/api/accounts/login/',
        register: '/api/accounts/register/',
        logout: '/api/accounts/logout/',
        profile: '/api/accounts/profile/',

        // التحاليل
        tests: '/api/tests/',
        testDetail: '/api/tests/:id/',
        patientTests: '/api/tests/patient/:patientId/',

        // المرضى (للأطباء)
        patients: '/api/patients/',
        patientDetail: '/api/patients/:id/',

        // الأطباء
        doctors: '/api/doctors/',
        doctorDetail: '/api/doctors/:id/',

        // الإحصائيات
        stats: '/api/stats/',
        dashboardStats: '/api/stats/dashboard/',

        // الأرشيف
        archive: '/api/archive/',
        archiveSearch: '/api/archive/search/',
    }
};

// دالة مساعدة لإرسال الطلبات
async function apiRequest(endpoint, options = {}) {
    const url = `${API_CONFIG.baseURL}${endpoint}`;
    const token = localStorage.getItem('authToken');

    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
            ...(token && { 'Authorization': `Bearer ${token}` })
        }
    };

    const config = { ...defaultOptions, ...options };

    try {
        const response = await fetch(url, config);
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || data.message || 'حدث خطأ في الاتصال');
        }

        return { success: true, data };
    } catch (error) {
        console.error('API Error:', error);
        return { success: false, error: error.message };
    }
}

// ===== دوال تسجيل الدخول والتسجيل =====

async function login(email, password, userType) {
    const result = await apiRequest(API_CONFIG.endpoints.login, {
        method: 'POST',
        body: JSON.stringify({ email, password, user_type: userType })
    });

    if (result.success && result.data.token) {
        localStorage.setItem('authToken', result.data.token);
        localStorage.setItem('userType', userType);
        localStorage.setItem('userId', result.data.user.id);
        localStorage.setItem('userName', result.data.user.name);
    }

    return result;
}

async function register(userData) {
    const result = await apiRequest(API_CONFIG.endpoints.register, {
        method: 'POST',
        body: JSON.stringify(userData)
    });

    return result;
}

async function logout() {
    await apiRequest(API_CONFIG.endpoints.logout, { method: 'POST' });
    localStorage.clear();
    window.location.href = '/';
}

// ===== دوال جلب البيانات =====

async function fetchDashboardStats() {
    return await apiRequest(API_CONFIG.endpoints.dashboardStats);
}

async function fetchPatientTests(patientId) {
    const endpoint = API_CONFIG.endpoints.patientTests.replace(':patientId', patientId);
    return await apiRequest(endpoint);
}

async function fetchPatients(filters = {}) {
    const queryString = new URLSearchParams(filters).toString();
    const endpoint = `${API_CONFIG.endpoints.patients}${queryString ? '?' + queryString : ''}`;
    return await apiRequest(endpoint);
}

async function fetchTestDetail(testId) {
    const endpoint = API_CONFIG.endpoints.testDetail.replace(':id', testId);
    return await apiRequest(endpoint);
}

async function fetchArchiveData(filters = {}) {
    const queryString = new URLSearchParams(filters).toString();
    const endpoint = `${API_CONFIG.endpoints.archive}${queryString ? '?' + queryString : ''}`;
    return await apiRequest(endpoint);
}

// ===== دوال عرض البيانات =====

function displayDashboardStats(stats) {
    // تحديث الإحصائيات في لوحة التحكم
    const statElements = document.querySelectorAll('[data-stat]');
    statElements.forEach(el => {
        const statName = el.dataset.stat;
        if (stats[statName] !== undefined) {
            animateCounter(el, stats[statName]);
        }
    });
}

function displayPatientTests(tests) {
    const container = document.getElementById('testsContainer');
    if (!container) return;

    container.innerHTML = tests.map(test => `
        <tr>
            <td>${test.test_date}</td>
            <td>${test.test_type}</td>
            <td>${test.doctor_name}</td>
            <td><span class="badge-custom-${test.status}">${test.status_display}</span></td>
            <td>
                <button class="btn btn-primary-custom btn-sm" onclick="viewTestDetail(${test.id})">
                    <i class="bi bi-eye"></i> عرض
                </button>
                <button class="btn btn-secondary-custom btn-sm" onclick="downloadTestPDF(${test.id})">
                    <i class="bi bi-download"></i>
                </button>
            </td>
        </tr>
    `).join('');
}

function displayPatients(patients) {
    const container = document.getElementById('patientsContainer');
    if (!container) return;

    container.innerHTML = patients.map(patient => `
        <tr>
            <td>
                <div class="d-flex align-items-center">
                    <div class="avatar me-3">${patient.name.charAt(0)}</div>
                    <div>
                        <div class="fw-bold">${patient.name}</div>
                        <div class="text-muted small">ID: ${patient.id}</div>
                    </div>
                </div>
            </td>
            <td>${patient.age} سنة</td>
            <td>${patient.last_test}</td>
            <td>${patient.last_visit}</td>
            <td><span class="badge-custom-${patient.status}">${patient.status_display}</span></td>
            <td>
                <button class="btn btn-primary-custom btn-sm" onclick="viewPatientDetail(${patient.id})">
                    <i class="bi bi-eye"></i> عرض
                </button>
            </td>
        </tr>
    `).join('');
}

// ===== دوال مساعدة =====

function animateCounter(element, target) {
    let current = 0;
    const increment = target / 100;
    const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
            current = target;
            clearInterval(timer);
        }
        element.textContent = Math.floor(current).toLocaleString('ar-EG');
    }, 20);
}

function showNotification(message, type = 'info') {
    // إنشاء إشعار
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} notification-toast`;
    notification.innerHTML = `
        <i class="bi bi-${type === 'success' ? 'check-circle' : 'exclamation-circle'}"></i>
        ${message}
    `;

    document.body.appendChild(notification);

    setTimeout(() => {
        notification.classList.add('show');
    }, 100);

    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('ar-EG', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

function formatTime(dateString) {
    const date = new Date(dateString);
    return date.toLocaleTimeString('ar-EG', {
        hour: '2-digit',
        minute: '2-digit'
    });
}

// ===== التهيئة عند تحميل الصفحة =====

document.addEventListener('DOMContentLoaded', async function () {
    // التحقق من تسجيل الدخول
    const authToken = localStorage.getItem('authToken');
    const currentPage = window.location.pathname;

    // إذا كان المستخدم في صفحة لوحة التحكم وليس مسجل دخول
    if (currentPage.includes('dashboard') && !authToken) {
        window.location.href = '/auth.html';
        return;
    }

    // تحميل البيانات حسب الصفحة
    if (currentPage.includes('dashboard_patient')) {
        const userId = localStorage.getItem('userId');
        const statsResult = await fetchDashboardStats();
        if (statsResult.success) {
            displayDashboardStats(statsResult.data);
        }

        const testsResult = await fetchPatientTests(userId);
        if (testsResult.success) {
            displayPatientTests(testsResult.data);
        }
    }

    if (currentPage.includes('dashboard_doctor')) {
        const statsResult = await fetchDashboardStats();
        if (statsResult.success) {
            displayDashboardStats(statsResult.data);
        }

        const patientsResult = await fetchPatients();
        if (patientsResult.success) {
            displayPatients(patientsResult.data);
        }
    }

    if (currentPage.includes('archive')) {
        const archiveResult = await fetchArchiveData();
        if (archiveResult.success) {
            displayArchiveData(archiveResult.data);
        }
    }

    // تحديث اسم المستخدم في الواجهة
    const userName = localStorage.getItem('userName');
    if (userName) {
        const userNameElements = document.querySelectorAll('[data-user-name]');
        userNameElements.forEach(el => {
            el.textContent = userName;
        });
    }
});

// تصدير الدوال للاستخدام العام
window.MyLabAPI = {
    login,
    register,
    logout,
    fetchDashboardStats,
    fetchPatientTests,
    fetchPatients,
    fetchTestDetail,
    fetchArchiveData,
    showNotification,
    formatDate,
    formatTime
};
