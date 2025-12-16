/**
 * Toast Notification System
 * Beautiful, modern notifications for MyLabLink
 * 
 * Usage:
 *   showToast('success', 'تم بنجاح!', 'تم إنشاء الحساب بنجاح');
 *   showToast('error', 'خطأ!', 'فشل تسجيل الدخول');
 *   showToast('warning', 'تحذير!', 'يرجى التحقق من البيانات');
 *   showToast('info', 'معلومة', 'تم إرسال رابط التحقق إلى بريدك');
 */

// Create toast container if it doesn't exist
function ensureToastContainer() {
    let container = document.querySelector('.toast-container');
    if (!container) {
        container = document.createElement('div');
        container.className = 'toast-container';
        document.body.appendChild(container);
    }
    return container;
}

// Icon mapping for different toast types
const toastIcons = {
    success: '✓',
    error: '✕',
    warning: '⚠',
    info: 'ℹ'
};

/**
 * Show a toast notification
 * @param {string} type - Type of toast: 'success', 'error', 'warning', 'info'
 * @param {string} title - Toast title
 * @param {string} message - Toast message (optional)
 * @param {number} duration - Duration in milliseconds (default: 5000)
 */
export function showToast(type = 'info', title = '', message = '', duration = 5000) {
    const container = ensureToastContainer();

    // Create toast element
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;

    // Create icon
    const icon = document.createElement('div');
    icon.className = 'toast-icon';
    icon.textContent = toastIcons[type] || 'ℹ';

    // Create content
    const content = document.createElement('div');
    content.className = 'toast-content';

    const titleEl = document.createElement('div');
    titleEl.className = 'toast-title';
    titleEl.textContent = title;
    content.appendChild(titleEl);

    if (message) {
        const messageEl = document.createElement('div');
        messageEl.className = 'toast-message';
        messageEl.textContent = message;
        content.appendChild(messageEl);
    }

    // Create close button
    const closeBtn = document.createElement('button');
    closeBtn.className = 'toast-close';
    closeBtn.innerHTML = '×';
    closeBtn.onclick = () => removeToast(toast);

    // Assemble toast
    toast.appendChild(icon);
    toast.appendChild(content);
    toast.appendChild(closeBtn);

    // Add to container
    container.appendChild(toast);

    // Auto remove after duration
    setTimeout(() => {
        removeToast(toast);
    }, duration);

    return toast;
}

/**
 * Remove a toast with animation
 * @param {HTMLElement} toast - Toast element to remove
 */
function removeToast(toast) {
    if (!toast || !toast.parentElement) return;

    toast.classList.add('toast-hiding');

    // Remove from DOM after animation
    setTimeout(() => {
        if (toast.parentElement) {
            toast.parentElement.removeChild(toast);
        }
    }, 400);
}

/**
 * Convenience functions for specific toast types
 */
export function showSuccess(title, message = '', duration) {
    return showToast('success', title, message, duration);
}

export function showError(title, message = '', duration) {
    return showToast('error', title, message, duration);
}

export function showWarning(title, message = '', duration) {
    return showToast('warning', title, message, duration);
}

export function showInfo(title, message = '', duration) {
    return showToast('info', title, message, duration);
}

// Global exposure for non-module usage
if (typeof window !== 'undefined') {
    window.showToast = showToast;
    window.showSuccess = showSuccess;
    window.showError = showError;
    window.showWarning = showWarning;
    window.showInfo = showInfo;
}

export default {
    showToast,
    showSuccess,
    showError,
    showWarning,
    showInfo
};
