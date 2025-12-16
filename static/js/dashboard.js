// dashboard.js: chart examples and PDF generation & notifications
document.addEventListener('DOMContentLoaded', () => {
    // Patient chart
    const ctx = document.getElementById('chartResults');
    if (ctx) {
        new Chart(ctx, {
            type: 'doughnut',
            data: { labels: ['هيموجلوبين', 'صفائح', 'WBC'], datasets: [{ data: [13.5, 210, 6.2], backgroundColor: ['#EF4444', '#0B3D91', '#60A5FA'] }] },
            options: { plugins: { legend: { position: 'bottom' } } }
        });
    }

    // Doctor chart
    const dctx = document.getElementById('doctorChart');
    if (dctx) {
        new Chart(dctx, { type: 'bar', data: { labels: ['أكتوبر', 'سبتمبر', 'أغسطس', 'يوليو'], datasets: [{ label: 'عدد التحاليل', data: [120, 98, 85, 110], backgroundColor: '#0B3D91' }] }, options: { scales: { y: { beginAtZero: true } } } });
    }

    // Admin chart
    const actx = document.getElementById('adminChart');
    if (actx) {
        new Chart(actx, { type: 'line', data: { labels: ['يناير', 'فبراير', 'مارس', 'أبريل', 'مايو', 'يونيو'], datasets: [{ label: 'تحاليل', data: [400, 380, 420, 500, 450, 480], borderColor: '#EF4444', backgroundColor: 'rgba(239,68,68,0.08)', fill: true }] }, options: { interaction: { mode: 'index', intersect: false } } });
    }

    // PDF download for patient
    const downloadBtn = document.getElementById('downloadPdf');
    if (downloadBtn) {
        downloadBtn.addEventListener('click', () => {
            const element = document.querySelector('.card');
            const opt = { margin: 0.5, filename: 'Result.pdf', image: { type: 'jpeg', quality: 0.98 }, html2canvas: { scale: 2 }, jsPDF: { unit: 'in', format: 'a4', orientation: 'portrait' } };
            html2pdf().set(opt).from(element).save();
        });
    }

    // Notifications demo
    const notifyBtn = document.getElementById('notifyBtn');
    if (notifyBtn) {
        notifyBtn.addEventListener('click', () => {
            alert('إشعار: نتيجة تحاليلك الطبية جاهزة. تفضل بمراجعتها في حسابك.');
        });
    }

    const alertCritical = document.getElementById('alertCritical');
    if (alertCritical) {
        alertCritical.addEventListener('click', () => {
            alert('تنبيه: اكتشاف نتيجة حرجة! سيتم إخطار المريض والطبيب المعني.');
        });
    }
});
