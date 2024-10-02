let charts = [];

document.addEventListener('DOMContentLoaded', () => {
    const pairButton = document.getElementById('pairButton');
    pairButton.addEventListener('click', pairArmband);
});

function pairArmband() {
    fetch('/pair', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.href = data.redirect;
            } else {
                alert('Pairing failed. Please try again.');
            }
        });
}

function collectData() {
    fetch('/collect', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Data collected successfully.');
            } else {
                alert('Data collection failed. Please try again.');
            }
        });
}

function trainModel() {
    fetch('/train', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Model trained successfully.');
            } else {
                alert('Model training failed. Please try again.');
            }
        });
}

function evaluateModel() {
    fetch('/evaluate', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            alert(`Model evaluation result: ${data.result}`);
        });
}

function initializeCharts() {
    for (let i = 0; i < 8; i++) {
        const ctx = document.getElementById(`semgChart${i}`).getContext('2d');
        charts.push(new Chart(ctx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: `Channel ${i + 1}`,
                    data: [],
                    borderColor: `hsl(${i * 45}, 100%, 50%)`,
                    tension: 0.1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: { type: 'linear', position: 'bottom' },
                    y: { beginAtZero: true }
                }
            }
        }));
    }
}

function updateCharts() {
    fetch('/get_semg_data')
        .then(response => response.json())
        .then(data => {
            for (let i = 0; i < 8; i++) {
                charts[i].data.labels = data.data[i].map((_, index) => index);
                charts[i].data.datasets[0].data = data.data[i];
                charts[i].update();
            }
        });
    setTimeout(updateCharts, 1000); // Update every second
}
