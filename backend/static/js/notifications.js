/* MyLabLink Notifications: Toasts + Alerts (RTL) */
(function(){
  const ICONS = {
    success: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><path d="M9 12l2 2 4-4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" stroke="currentColor" stroke-width="2" fill="none"/></svg>',
    info: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><path d="M12 8h.01M11 12h1v4h1" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="2" fill="none"/></svg>',
    warning: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><path d="M12 9v4m0 4h.01" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M10.29 3.86l-8.48 14.7A2 2 0 0 0 3.52 22h16.96a2 2 0 0 0 1.71-3.44l-8.48-14.7a2 2 0 0 0-3.42 0z" stroke="currentColor" stroke-width="2" fill="none"/></svg>',
    error: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><path d="M15 9l-6 6M9 9l6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" stroke="currentColor" stroke-width="2" fill="none"/></svg>'
  };

  function ensureStack(){
    let stack = document.getElementById('toastStack');
    if(!stack){
      stack = document.createElement('div');
      stack.id = 'toastStack';
      stack.className = 'toast-stack';
      document.body.appendChild(stack);
    }
    return stack;
  }

  function notify({title = 'إشعار', description = '', variant = 'info', timeout = 5000} = {}){
    const stack = ensureStack();
    const toast = document.createElement('div');
    toast.className = `toast ${variant}`;
    toast.setAttribute('role', 'status');
    toast.setAttribute('aria-live', 'polite');

    const icon = document.createElement('div');
    icon.className = 'icon';
    icon.innerHTML = ICONS[variant] || ICONS.info;

    const body = document.createElement('div');
    body.className = 'body';
    const t = document.createElement('div'); t.className = 'title'; t.textContent = title;
    const d = document.createElement('div'); d.className = 'desc'; d.textContent = description;
    body.appendChild(t); if(description) body.appendChild(d);

    const close = document.createElement('button');
    close.className = 'close';
    close.setAttribute('aria-label', 'إغلاق');
    close.innerHTML = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><path d="M15 9l-6 6M9 9l6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>';

    close.addEventListener('click', function(){ dismiss(toast); });

    toast.appendChild(icon);
    toast.appendChild(body);
    toast.appendChild(close);
    stack.appendChild(toast);

    let timer;
    if(timeout > 0){ timer = setTimeout(() => dismiss(toast), timeout); }

    toast.addEventListener('mouseenter', () => { if(timer) clearTimeout(timer); });
    toast.addEventListener('mouseleave', () => { if(timeout > 0) timer = setTimeout(() => dismiss(toast), timeout/2); });

    return { dismiss: () => dismiss(toast) };
  }

  function dismiss(toast){
    if(!toast) return;
    toast.classList.add('out');
    toast.addEventListener('animationend', () => {
      toast.remove();
    }, { once: true });
  }

  // Expose API
  window.MLL = window.MLL || {};
  window.MLL.notify = notify;

  // Bootstrap: read inline data elements if present
  document.addEventListener('DOMContentLoaded', function(){
    var container = document.getElementById('ml-messages');
    if(!container) return;
    var items = container.querySelectorAll('.ml-message');
    items.forEach(function(el){
      notify({
        title: el.getAttribute('data-title') || 'إشعار',
        description: el.getAttribute('data-desc') || '',
        variant: el.getAttribute('data-variant') || 'info'
      });
    });
  });
})();
