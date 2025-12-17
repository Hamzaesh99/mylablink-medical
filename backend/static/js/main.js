// main.js: handles auth role toggle and basic interactions
document.addEventListener('DOMContentLoaded', () => {
    const accountRadios = document.querySelectorAll('input[name="role"]');
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    const switchToRegister = document.getElementById('switchToRegister');
    const switchToLogin = document.getElementById('switchToLogin');
    const showLogin = document.getElementById('showLogin');
    const showRegister = document.getElementById('showRegister');
    const doctorFields = document.getElementById('doctorFields');
    const panelTitle = document.getElementById('panelTitle');
    const panelSubtitle = document.getElementById('panelSubtitle');

    function applyRoleStyles(role) {
        // change primary button color slightly based on role and toggle doctor-specific fields
        const primaryButtons = document.querySelectorAll('.btn-primary');
        if (role === 'doctor') {
            primaryButtons.forEach(b => { b.style.background = 'linear-gradient(90deg, var(--navy), #153b8f)'; });
            doctorFields && (doctorFields.style.display = 'block');
        } else {
            primaryButtons.forEach(b => { b.style.background = 'var(--primary-red)'; });
            doctorFields && (doctorFields.style.display = 'none');
        }
    }

    // wire role change to style & fields
    accountRadios.forEach(r => r.addEventListener('change', e => applyRoleStyles(e.target.value)));
    // initial apply
    const initialRole = document.querySelector('input[name="role"]:checked').value;
    applyRoleStyles(initialRole);

    // toggle views
    function showLoginView() {
        loginForm.style.display = 'block';
        registerForm.style.display = 'none';
        panelTitle.textContent = 'تسجيل الدخول';
        panelSubtitle.textContent = 'سجّل دخولك بحسابك للوصول إلى النتائج.';
        showLogin.classList.remove('btn-outline-secondary');
        showLogin.classList.add('btn-outline-secondary');
        showRegister.classList.remove('btn-primary');
        showRegister.classList.add('btn-primary');
    }

    function showRegisterView() {
        loginForm.style.display = 'none';
        registerForm.style.display = 'block';
        panelTitle.textContent = 'إنشاء حساب جديد';
        panelSubtitle.textContent = 'أنشئ حساب مريض أو طبيب للوصول إلى الخدمات.';
        showRegister.classList.remove('btn-primary');
        showRegister.classList.add('btn-primary');
        showLogin.classList.remove('btn-outline-secondary');
        showLogin.classList.add('btn-outline-secondary');
    }

    // attach toggles
    switchToRegister && switchToRegister.addEventListener('click', showRegisterView);
    switchToLogin && switchToLogin.addEventListener('click', showLoginView);
    showLogin && showLogin.addEventListener('click', showLoginView);
    showRegister && showRegister.addEventListener('click', showRegisterView);

    // login (calls backend via window.Auth if available)
    loginForm && loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const role = document.querySelector('input[name="role"]:checked').value;
        const email = document.getElementById('loginEmail').value.trim();
        const password = document.getElementById('loginPassword').value;

        try {
            if (window.Auth && typeof window.Auth.login === 'function') {
                // backend expects 'username' field by default; use email as username if that's how users are registered
                await window.Auth.login(email, password);
            } else {
                // fallback to previous demo behavior
                console.warn('Auth helper not available; falling back to demo redirect');
            }

            if (role === 'doctor') window.location.href = 'doctor/dashboard.html';
            else window.location.href = 'patient/dashboard.html';
        } catch (err) {
            console.error('Login error', err);
            const message = (err && err.detail) ? err.detail : 'فشل تسجيل الدخول، الرجاء المحاولة';
            alert(message);
        }
    });

    // register (calls backend register endpoint)
    registerForm && registerForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const role = document.querySelector('input[name="role"]:checked').value;
        const name = document.getElementById('regName').value.trim();
        const email = document.getElementById('regEmail').value.trim();
        const phone = document.getElementById('regPhone').value.trim();
        const pass = document.getElementById('regPassword').value;
        const passConfirm = document.getElementById('regPasswordConfirm').value;
        if (pass !== passConfirm) {
            alert('كلمتا المرور غير متطابقتين.');
            return;
        }
        try {
            if (window.Auth && typeof window.Auth.register === 'function') {
                // backend RegisterSerializer expects username; we'll use email as username by default
                const payload = {
                    username: email,
                    email: email,
                    first_name: name,
                    password: pass,
                    password2: passConfirm,
                    role: role,
                    phone: phone
                }
                await window.Auth.register(payload)
            } else {
                console.warn('Auth.register not available; falling back to demo');
            }
            alert('تم إنشاء الحساب بنجاح. سيتم توجيهك الآن.');
            if (role === 'doctor') window.location.href = 'doctor/dashboard.html';
            else window.location.href = 'patient/dashboard.html';
        } catch (err) {
            console.error('Register error', err);
            const message = (err && err.detail) ? err.detail : 'فشل إنشاء الحساب، الرجاء المحاولة';
            alert(message);
        }
    });
});
