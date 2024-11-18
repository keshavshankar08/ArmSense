// script.js

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

// Global variables
let charts = [];
const maxDataPoints = 50; // Number of data points to display
const channelDataArrays = []; // Array to store data arrays for each channel
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

            // Initialize data array for each channel
            channelDataArrays.push([]);

            charts.push(new Chart(ctx, {
                type: 'line',
                data: {
                    labels: [], // Start with empty labels
                    datasets: [{
                        label: `Channel ${i + 1}`,
                        data: [],
                        borderColor: `hsl(${45 * i}, 100%, 50%)`, // Distinct color for each channel
                        tension: 0.1
                    }]
                },
                options: {
                    animation: false, // Disable animations for better performance
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: { 
                            type: 'linear',
                            display: true,
                            title: {
                                display: true,
                                text: 'Sample'
                            },
                            grid: {
                                color: 'rgba(171,171,171,0.2)',
                                lineWidth: 1
                            },
                            ticks: {
                                minRotation: 0,
                                maxRotation: 0,
                                autoSkip: true,
                                maxTicksLimit: 10
                            }
                        },
                        y: { 
                            beginAtZero: true,
                            display: true,
                            min: 0,       // Set the minimum value of the y-axis to 0
                            max: 2000,    // Set the maximum value of the y-axis to 2000
                            title: {
                                display: true,
                                text: 'Amplitude'
                            },
                            grid: {
                                color: 'rgba(171,171,171,0.2)',
                                lineWidth: 0.5
                            }
                        }
                    },
                    plugins: {
                        legend: {
                            display: false
                        },
                        title: {
                            display: true,
                            text: `Channel ${i + 1}`
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
    fetch('/get_semg_data')
        .then(response => response.json())
        .then(data => {
            console.log('Data received:', data); // Debugging line
            if (!data.data || !Array.isArray(data.data)) {
                log('updateCharts', 'Invalid data format received.');
                // Schedule the next update
                setTimeout(updateCharts, 50);
                return;
            }
            for (let channelIndex = 0; channelIndex < 8; channelIndex++) {
                const dataArray = channelDataArrays[channelIndex];

                // Extract all the values for the current channel
                const channelValues = data.data.map(reading => parseFloat(reading[channelIndex]) || 0);

                // Append the new values to the channel's data array
                dataArray.push(...channelValues);

                // Keep only the latest maxDataPoints
                while (dataArray.length > maxDataPoints) {
                    dataArray.shift();
                }

                // Update the chart
                const chart = charts[channelIndex];
                chart.data.labels = dataArray.map((_, i) => i);
                chart.data.datasets[0].data = dataArray;
                chart.update('none');
            }

            log('updateCharts', 'Charts updated successfully');
            // Schedule the next update
            setTimeout(updateCharts, 50);
        })
        .catch(error => {
            log('updateCharts', 'Error fetching sEMG data', error);
            console.error('Fetch error:', error); // Debugging line
            // Schedule the next update even if an error occurs
            setTimeout(updateCharts, 50);
        });
}