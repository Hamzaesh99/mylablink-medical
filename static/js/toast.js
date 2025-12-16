(function() {
    'use strict';

    // Toast container
    let container = null;

    function getContainer() {
        if (!container) {
            container = document.createElement('div');
            container.id = 'toast-container';
            container.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                z-index: 9999;
                pointer-events: none;
            `;
            document.body.appendChild(container);
        }
        return container;
    }

    function createToast(message, type = 'info', duration = 5000) {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.style.cssText = `
            background: ${type === 'success' ? '#28a745' : type === 'error' ? '#dc3545' : type === 'warning' ? '#ffc107' : '#17a2b8'};
            color: white;
            padding: 12px 20px;
            border-radius: 4px;
            margin-bottom: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            max-width: 300px;
            word-wrap: break-word;
            opacity: 0;
            transform: translateX(100%);
            transition: all 0.3s ease;
            pointer-events: auto;
            cursor: pointer;
        `;
        toast.innerHTML = message;

        // Add close button
        const closeBtn = document.createElement('span');
        closeBtn.innerHTML = '&times;';
        closeBtn.style.cssText = `
            margin-left: 10px;
            font-size: 16px;
            cursor: pointer;
            opacity: 0.8;
        `;
        closeBtn.onclick = () => removeToast(toast);
        toast.appendChild(closeBtn);

        getContainer().appendChild(toast);

        // Animate in
        setTimeout(() => {
            toast.style.opacity = '1';
            toast.style.transform = 'translateX(0)';
        }, 10);

        // Auto remove
        setTimeout(() => removeToast(toast), duration);

        return toast;
    }

    function removeToast(toast) {
        if (!toast || !toast.parentNode) return;
        
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(100%)';
        
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 300);
    }

    // Global function
    window.showToast = function(message, type = 'info', duration = 5000) {
        return createToast(message, type, duration);
    };

    // Export for module usage
    if (typeof module !== 'undefined' && module.exports) {
        module.exports = { showToast, createToast, removeToast };
    }
})();
