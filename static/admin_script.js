// Flash animation for updates
function flashCard(id) {
    const card = document.getElementById(id);
    if(card) {
        card.classList.add('flash-card');
        setTimeout(() => card.classList.remove('flash-card'), 800);
    }
}

// Example: toggle dark mode (optional)
const toggleBtn = document.getElementById('toggleTheme');
if(toggleBtn){
    toggleBtn.addEventListener('click', ()=>{
        document.body.classList.toggle('bg-dark');
        document.body.classList.toggle('text-light');
    });
}
// static/js/admin_dashboard.js

document.addEventListener("DOMContentLoaded", function() {
    // Fetch data from HTML dataset
    const chartElement = document.getElementById('solvesChart');
    if (!chartElement) return;

    const dates = JSON.parse(chartElement.dataset.dates);
    const counts = JSON.parse(chartElement.dataset.counts);

    new Chart(chartElement, {
        type: 'line',
        data: {
            labels: dates,
            datasets: [{
                label: 'Flags Solved Over Time',
                data: counts,
                borderColor: 'rgba(75, 192, 192, 1)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: true }
            },
            scales: {
                y: { beginAtZero: true }
            }
        }
    });
});
document.addEventListener("DOMContentLoaded", function() {
    const chartElement = document.getElementById('solvesChart');
    if (!chartElement) return;

    const dates = JSON.parse(chartElement.dataset.dates);
    const counts = JSON.parse(chartElement.dataset.counts);

    new Chart(chartElement, {
        type: 'line',
        data: {
            labels: dates,
            datasets: [{
                label: 'Flags Solved Over Time',
                data: counts,
                borderColor: '#0d6efd',
                backgroundColor: 'rgba(13,110,253,0.2)',
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: true }
            },
            scales: {
                y: { beginAtZero: true }
            }
        }
    });
});
