// Dashboard JavaScript
// General dashboard functionality

document.addEventListener('DOMContentLoaded', function () {
    console.log('Dashboard loaded successfully');

    // Animate counters
    const counters = document.querySelectorAll('.stat-number');
    counters.forEach(counter => {
        const target = parseInt(counter.getAttribute('data-count') || counter.textContent);
        animateCounterElement(counter, target);
    });
});

// Animate counter function
function animateCounterElement(element, target) {
    if (!element || !target) return;

    let current = 0;
    const increment = target / 50;
    const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
            element.textContent = target;
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(current);
        }
    }, 20);
}
