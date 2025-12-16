// Toast Notification System
// Usage: showToast('رسالتك هنا', 'success|error|warning|info')

function showToast(message, type = 'info', title = '') {
    const container = document.getElementById('toast-container');
    if (!container) {
        console.error('Toast container not found');
        return;
    }

    // Auto-generate title if not provided
    if (!title) {
        const titles = {
            success: 'نجح!',
            error: 'خطأ!',
            warning: 'تحذير!',
            info: 'معلومة'
        };
        title = titles[type] || 'إشعار';
    }

    // Create toast element
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;

    // Icon mapping
    const icons = {
        success: 'bi-check-circle-fill',
        error: 'bi-x-circle-fill',
        warning: 'bi-exclamation-triangle-fill',
        info: 'bi-info-circle-fill'
    };

    toast.innerHTML = `
        <div class="toast-icon">
            <i class="bi ${icons[type] || icons.info}"></i>
        </div>
        <div class="toast-content">
            <div class="toast-title">${title}</div>
            <div class="toast-message">${message}</div>
        </div>
        <button class="toast-close" aria-label="Close">
            <i class="bi bi-x"></i>
        </button>
        <div class="toast-progress"></div>
    `;

    // Add to container
    container.appendChild(toast);

    // Close button functionality
    const closeBtn = toast.querySelector('.toast-close');
    closeBtn.addEventListener('click', () => closeToast(toast));

    // Auto-close after 5 seconds
    const autoCloseTimer = setTimeout(() => closeToast(toast), 5000);

    // Clear timer on hover
    toast.addEventListener('mouseenter', () => clearTimeout(autoCloseTimer));
    toast.addEventListener('mouseleave', () => {
        setTimeout(() => closeToast(toast), 2000);
    });

    return toast;
}

function closeToast(toast) {
    if (!toast || !toast.parentElement) return;

    toast.classList.add('toast-hiding');
    setTimeout(() => {
        if (toast.parentElement) {
            toast.parentElement.removeChild(toast);
        }
    }, 300);
}

// Expose functions globally
window.showToast = showToast;
window.closeToast = closeToast;

// Export for module usage
export { showToast, closeToast };
