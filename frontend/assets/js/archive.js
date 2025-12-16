// Archive Management System
// API Configuration
const API_BASE = window.API_BASE || 'http://127.0.0.1:8000';

class ArchiveManager {
    constructor() {
        this.tests = [];
        this.filteredTests = [];
        this.currentPage = 1;
        this.itemsPerPage = 10;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadTests();
    }

    setupEventListeners() {
        // Search input
        const searchInput = document.getElementById('searchInput');
        if (searchInput) {
            searchInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    this.loadTests();
                }
            });
        }

        // Filter buttons
        const filterBtn = document.getElementById('filterBtn');
        if (filterBtn) {
            filterBtn.addEventListener('click', () => this.loadTests());
        }

        const resetBtn = document.getElementById('resetBtn');
        if (resetBtn) {
            resetBtn.addEventListener('click', () => this.resetFilters());
        }
    }

    async loadTests() {
        this.showLoading();

        try {
            // Get filter values
            const searchTerm = document.getElementById('searchInput')?.value || '';
            const dateFrom = document.getElementById('dateFrom')?.value || '';
            const dateTo = document.getElementById('dateTo')?.value || '';

            // Build query parameters
            let queryParams = new URLSearchParams();
            if (searchTerm) queryParams.append('search', searchTerm);
            if (dateFrom) queryParams.append('date_from', dateFrom);
            if (dateTo) queryParams.append('date_to', dateTo);

            // Get auth token
            const token = localStorage.getItem('access_token');

            // Fetch data from backend
            const response = await fetch(`${API_BASE}/api/tests/?${queryParams.toString()}`, {
                headers: {
                    'Authorization': token ? `Bearer ${token}` : '',
                    'Content-Type': 'application/json'
                }
            });

            if (response.ok) {
                const data = await response.json();
                this.tests = data.results || data;
                this.filteredTests = [...this.tests];
                this.renderTests();
                this.updateStatistics();
            } else {
                throw new Error('Failed to fetch tests');
            }

        } catch (error) {
            console.error('Error loading tests:', error);
            // Load sample data as fallback
            this.loadSampleData();
        }
    }

    loadSampleData() {
        this.tests = [
            {
                id: 'ML000001',
                patient_name: 'أحمد محمد علي',
                test_type: 'تحليل الدم الشامل',
                created_at: '2025-10-25',
                doctor_name: 'د. فاطمة حسن',
                status: 'completed'
            },
            {
                id: 'ML000002',
                patient_name: 'فاطمة أحمد حسن',
                test_type: 'الهرمونات',
                created_at: '2025-08-09',
                doctor_name: 'د. سارة أحمد',
                status: 'pending'
            },
            {
                id: 'ML000003',
                patient_name: 'محمد حسن علي',
                test_type: 'تحاليل الكبد',
                created_at: '2025-05-02',
                doctor_name: 'د. نورا إبراهيم',
                status: 'completed'
            },
            {
                id: 'ML000004',
                patient_name: 'سارة علي محمد',
                test_type: 'تحليل البول',
                created_at: '2025-03-15',
                doctor_name: 'د. أحمد محمد',
                status: 'reviewed'
            },
            {
                id: 'ML000005',
                patient_name: 'خالد محمود أحمد',
                test_type: 'الكيمياء الحيوية',
                created_at: '2025-02-20',
                doctor_name: 'د. فاطمة حسن',
                status: 'completed'
            },
            {
                id: 'ML000006',
                patient_name: 'نورا إبراهيم',
                test_type: 'تحليل الغدة الدرقية',
                created_at: '2025-01-18',
                doctor_name: 'د. خالد محمود',
                status: 'completed'
            },
            {
                id: 'ML000007',
                patient_name: 'عمر حسن',
                test_type: 'تحليل السكر',
                created_at: '2024-12-10',
                doctor_name: 'د. أحمد محمد',
                status: 'completed'
            },
            {
                id: 'ML000008',
                patient_name: 'ليلى أحمد',
                test_type: 'تحليل الكوليسترول',
                created_at: '2024-11-05',
                doctor_name: 'د. فاطمة حسن',
                status: 'reviewed'
            }
        ];

        this.filteredTests = [...this.tests];
        this.renderTests();
        this.updateStatistics();
    }

    renderTests() {
        const tbody = document.getElementById('testsTableBody');
        const tableContainer = document.getElementById('tableContainer');
        const emptyState = document.getElementById('emptyState');
        const loadingState = document.getElementById('loadingState');

        // Hide loading
        if (loadingState) loadingState.style.display = 'none';

        if (this.filteredTests.length === 0) {
            if (tableContainer) tableContainer.style.display = 'none';
            if (emptyState) emptyState.style.display = 'block';
            return;
        }

        if (tableContainer) tableContainer.style.display = 'block';
        if (emptyState) emptyState.style.display = 'none';

        if (!tbody) return;

        // Calculate pagination
        const startIndex = (this.currentPage - 1) * this.itemsPerPage;
        const endIndex = startIndex + this.itemsPerPage;
        const pageTests = this.filteredTests.slice(startIndex, endIndex);

        // Render table rows
        tbody.innerHTML = pageTests.map(test => `
            <tr>
                <td><strong>${test.id}</strong></td>
                <td>${test.patient_name || test.patient?.full_name || 'غير محدد'}</td>
                <td>${test.test_type || test.type || 'تحليل عام'}</td>
                <td>${this.formatDate(test.created_at || test.date)}</td>
                <td>${test.doctor_name || test.doctor?.full_name || 'غير محدد'}</td>
                <td>${this.getStatusBadge(test.status)}</td>
                <td>
                    <div class="d-flex gap-2">
                        <button class="btn btn-sm btn-outline-primary" onclick="archiveManager.viewTest('${test.id}')">
                            <i class="bi bi-eye"></i>
                        </button>
                        <button class="btn btn-sm btn-secondary" onclick="archiveManager.downloadTest('${test.id}')">
                            <i class="bi bi-download"></i>
                        </button>
                    </div>
                </td>
            </tr>
        `).join('');

        // Update record info
        this.updateRecordInfo();
    }

    updateStatistics() {
        const totalTests = this.tests.length;

        // Update total tests
        const totalTestsEl = document.getElementById('totalTests');
        if (totalTestsEl) {
            this.animateCounter(totalTestsEl, totalTests);
        }

        // Calculate this month's tests
        const thisMonth = this.tests.filter(test => {
            const testDate = new Date(test.created_at || test.date);
            const now = new Date();
            return testDate.getMonth() === now.getMonth() &&
                testDate.getFullYear() === now.getFullYear();
        }).length;

        const thisMonthEl = document.getElementById('thisMonth');
        if (thisMonthEl) {
            this.animateCounter(thisMonthEl, thisMonth);
        }

        // Calculate pending tests
        const pending = this.tests.filter(test => test.status === 'pending').length;
        const pendingEl = document.getElementById('pendingTests');
        if (pendingEl) {
            this.animateCounter(pendingEl, pending);
        }

        // Count unique patients
        const uniquePatients = new Set(
            this.tests.map(test => test.patient_name || test.patient?.id)
        ).size;

        const patientsEl = document.getElementById('totalPatients');
        if (patientsEl) {
            this.animateCounter(patientsEl, uniquePatients);
        }

        // Update total records
        const totalRecordsEl = document.getElementById('totalRecords');
        if (totalRecordsEl) {
            totalRecordsEl.textContent = totalTests.toLocaleString();
        }
    }

    updateRecordInfo() {
        const recordInfoEl = document.getElementById('recordInfo');
        if (recordInfoEl) {
            const startIndex = (this.currentPage - 1) * this.itemsPerPage + 1;
            const endIndex = Math.min(this.currentPage * this.itemsPerPage, this.filteredTests.length);
            recordInfoEl.textContent = `${startIndex}-${endIndex}`;
        }
    }

    animateCounter(element, target) {
        let current = 0;
        const increment = target / 50;
        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            element.textContent = Math.floor(current).toLocaleString();
        }, 20);
    }

    formatDate(dateString) {
        if (!dateString) return 'غير محدد';
        const date = new Date(dateString);
        return date.toLocaleDateString('ar-LY', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    }

    getStatusBadge(status) {
        const statusMap = {
            'completed': { label: 'مكتمل', class: 'badge-success' },
            'pending': { label: 'قيد الانتظار', class: 'badge-warning' },
            'reviewed': { label: 'تمت المراجعة', class: 'badge-info' },
            'cancelled': { label: 'ملغي', class: 'badge-danger' }
        };

        const statusInfo = statusMap[status] || { label: status, class: 'badge-info' };
        return `<span class="badge ${statusInfo.class}">${statusInfo.label}</span>`;
    }

    showLoading() {
        const loadingState = document.getElementById('loadingState');
        const tableContainer = document.getElementById('tableContainer');
        const emptyState = document.getElementById('emptyState');

        if (loadingState) loadingState.style.display = 'block';
        if (tableContainer) tableContainer.style.display = 'none';
        if (emptyState) emptyState.style.display = 'none';
    }

    resetFilters() {
        const searchInput = document.getElementById('searchInput');
        const dateFrom = document.getElementById('dateFrom');
        const dateTo = document.getElementById('dateTo');

        if (searchInput) searchInput.value = '';
        if (dateFrom) dateFrom.value = '';
        if (dateTo) dateTo.value = '';

        this.loadTests();
    }

    viewTest(testId) {
        const test = this.tests.find(t => t.id === testId);
        if (test) {
            alert(`عرض تفاصيل التحليل: ${testId}\n\nالمريض: ${test.patient_name}\nالنوع: ${test.test_type}\nالتاريخ: ${this.formatDate(test.created_at)}`);
            // TODO: Implement modal or redirect to test details page
        }
    }

    downloadTest(testId) {
        alert(`جاري تحميل تقرير التحليل: ${testId}`);
        // TODO: Implement PDF download from backend
        // window.location.href = `${API_BASE}/api/tests/${testId}/download/`;
    }

    exportToExcel() {
        alert('جاري تصدير البيانات إلى Excel...');
        // TODO: Implement Excel export
        // window.location.href = `${API_BASE}/api/tests/export/excel/`;
    }
}

// Initialize archive manager
let archiveManager;
document.addEventListener('DOMContentLoaded', () => {
    archiveManager = new ArchiveManager();
});

// Global functions for inline onclick handlers
function loadTests() {
    if (archiveManager) archiveManager.loadTests();
}

function exportToExcel() {
    if (archiveManager) archiveManager.exportToExcel();
}

function viewTest(testId) {
    if (archiveManager) archiveManager.viewTest(testId);
}

function downloadTest(testId) {
    if (archiveManager) archiveManager.downloadTest(testId);
}
