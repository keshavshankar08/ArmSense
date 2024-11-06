function log(functionName, purpose, error = null) {
    const message = `${functionName}: ${purpose}${error ? `, ERROR: ${error.message}` : ''}`;
    console.log(message);
    // You can also send this log to the server if needed
    fetch('/log', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message })
    }).catch(err => console.error('Failed to send log to server:', err));
}

document.addEventListener('DOMContentLoaded', () => {
    try {
        const pairButton = document.getElementById('pairButton');
        const findDevicesButton = document.getElementById('findDevicesButton');

        if (pairButton) {
            pairButton.addEventListener('click', pairArmband);
        }

        if (findDevicesButton) {
            findDevicesButton.addEventListener('click', findDevices);
        }

        if (window.location.pathname === '/collection') {
            initializeCharts();
            updateCharts();
        }
        log('DOMContentLoaded', 'Event listener setup complete');
    } catch (error) {
        log('DOMContentLoaded', 'Error in setup', error);
    }
});

function pairArmband() {
    log('pairArmband', 'Attempting to pair armband');
    try {
        fetch('/pair', { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    log('pairArmband', 'Pairing successful, redirecting');
                    window.location.href = data.redirect;
                } else {
                    log('pairArmband', 'Pairing failed');
                    alert('Pairing failed. Please try again.');
                }
            })
            .catch(error => {
                log('pairArmband', 'Error during pairing', error);
                alert('An error occurred during pairing. Please try again.');
            });
    } catch (error) {
        log('pairArmband', 'Unexpected error', error);
    }
}

function trainModel() {
    log('trainModel', 'Training model');
    try {
        fetch('/train', { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    log('trainModel', 'Model trained successfully');
                    alert('Model trained successfully.');
                } else {
                    log('trainModel', 'Model training failed');
                    alert('Model training failed. Please try again.');
                }
            })
            .catch(error => {
                log('trainModel', 'Error during model training', error);
            });
    } catch (error) {
        log('trainModel', 'Unexpected error', error);
    }
}

function evaluateModel() {
    log('evaluateModel', 'Evaluating model');
    try {
        fetch('/evaluate', { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                log('evaluateModel', `Model evaluation result: ${data.result}`);
                alert(`Model evaluation result: ${data.result}`);
            })
            .catch(error => {
                log('evaluateModel', 'Error during model evaluation', error);
            });
    } catch (error) {
        log('evaluateModel', 'Unexpected error', error);
    }
}

let charts = [];

function initializeCharts() {
    log('initializeCharts', 'Initializing charts');
    try {
        for (let i = 0; i < 8; i++) { // Initialize 8 charts (0-7)
            const canvasId = `semgChart${i}`;
            const canvas = document.getElementById(canvasId);
            if (!canvas) {
                log('initializeCharts', `Canvas with ID ${canvasId} not found.`);
                continue;
            }
            const ctx = canvas.getContext('2d');
            charts.push(new Chart(ctx, {
                type: 'line',
                data: {
                    labels: [],
                    datasets: [{
                        label: `Channel ${i + 1}`,
                        data: [],
                        borderColor: `hsl(${45 * i}, 100%, 50%)`, // Distinct color for each channel
                        tension: 0.1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: false
                        },
                        title: {
                            display: true,
                            text: `Channel ${i + 1}`
                        }
                    },
                    scales: {
                        x: { 
                            display: true,
                            title: {
                                display: true,
                                text: 'Sample'
                            },
                            grid: {
                                color: 'rgba(171,171,171,0.2)', // Optional: Customize grid color
                                lineWidth: 1
                            }
                        },
                        y: { 
                            beginAtZero: true,
                            display: true,
                            title: {
                                display: true,
                                text: 'Amplitude'
                            },
                            grid: {
                                color: 'rgba(171,171,171,0.2)', // Optional: Customize grid color
                                lineWidth: 0.5
                            }
                        }
                    }
                }
            }));
        }
        log('initializeCharts', 'Charts initialized successfully');
    } catch (error) {
        log('initializeCharts', 'Error initializing charts', error);
    }
}

function updateCharts() {
    log('updateCharts', 'Updating charts');
    try {
        fetch('/get_semg_data')
            .then(response => response.json())
            .then(data => {
                if (!data.data || !Array.isArray(data.data)) {
                    log('updateCharts', 'Invalid data format received.');
                    return;
                }
                charts.forEach((chart, index) => {
                    const channelData = data.data[index] || [];
                    chart.data.labels = channelData.map((_, i) => i);
                    chart.data.datasets[0].data = channelData;
                    chart.update();
                });
                log('updateCharts', 'Charts updated successfully');
            })
            .catch(error => {
                log('updateCharts', 'Error fetching sEMG data', error);
            });
        setTimeout(updateCharts, 1000); // Update every second
    } catch (error) {
        log('updateCharts', 'Unexpected error', error);
    }
}

function collectData() {
    log('collectData', 'Collecting data');
    try {
        fetch('/collect', { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    log('collectData', 'Data collected successfully');
                    alert('Data collected successfully.');
                } else {
                    log('collectData', 'Data collection failed');
                    alert('Data collection failed. Please try again.');
                }
            })
            .catch(error => {
                log('collectData', 'Error during data collection', error);
            });
    } catch (error) {
        log('collectData', 'Unexpected error', error);
    }
}

function findDevices() {
    log('findDevices', 'Finding Bluetooth devices');
    // Implement Bluetooth device discovery logic here
    // This might involve calling a backend endpoint to start the Bluetooth scan
    fetch('/find_devices', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                log('findDevices', 'Devices found successfully');
                alert('Devices found successfully.');
            } else {
                log('findDevices', 'Failed to find devices');
                alert('Failed to find devices. Please try again.');
            }
        })
        .catch(error => {
            log('findDevices', 'Error finding devices', error);
        });
}