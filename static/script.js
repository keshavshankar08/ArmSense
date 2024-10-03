document.addEventListener('DOMContentLoaded', () => {
    const pairButton = document.getElementById('pairButton');
    if (pairButton) {
        pairButton.addEventListener('click', pairArmband);
    }

    if (window.location.pathname === '/collection') {
        initializeChart();
        updateChart();
    }
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
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred during pairing. Please try again.');
        });
}

let chart;

function initializeChart() {
    const ctx = document.getElementById('semgChart0').getContext('2d');
    chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: `Channel 1`,
                data: [],
                borderColor: `hsl(45, 100%, 50%)`,
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                x: { 
                    display: true
                },
                y: { 
                    beginAtZero: true,
                    ticks: {
                        display: false
                    }
                }
            }
        }
    });
}

function updateChart() {
    fetch('/get_semg_data')
        .then(response => response.json())
        .then(data => {
            chart.clear();  // Clear the chart
            const channelData = data.data[0];
            chart.data.labels = channelData.map((_, index) => index);
            chart.data.datasets[0].data = channelData;
            chart.update();
        })
        .catch(error => {
            console.error('Error fetching sEMG data:', error);
        });
    setTimeout(updateChart, 1000);
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