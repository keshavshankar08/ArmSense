function log(functionName, purpose, error = null) {
    const message = `${functionName}: ${purpose}${error ? `, ERROR: ${error.message}` : ''}`;
    console.log(message);
    fetch('/log', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message }),
    }).catch(err => console.error('Failed to send log to server:', err));
}

document.addEventListener('DOMContentLoaded', () => {
    const findDevicesButton = document.getElementById('findDevicesButton');
    const deviceDropdown = document.getElementById('deviceDropdown');
    const pairDeviceButton = document.getElementById('pairDeviceButton');
    const homeButton = document.getElementById('homeButton');
    const evaluateButton = document.getElementById('evaluateButton');
    const disconnectButton = document.getElementById('disconnectButton');
    const trainModel = document.getElementById('trainModel');

    if (findDevicesButton) {
        findDevicesButton.addEventListener('click', async () => {
            try {
                const response = await fetch('/find_devices', { method: 'POST' });
                const devices = await response.json();

                if (devices.error) {
                    console.error('Error finding devices:', devices.error);
                    alert('Error finding devices.');
                    return;
                }

                deviceDropdown.innerHTML = ''; // Clear previous options
                devices.forEach(device => {
                    const option = document.createElement('option');
                    option.value = device.name; // Use device name
                    option.textContent = `${device.name} (${device.address})`;
                    deviceDropdown.appendChild(option);
                });

                deviceDropdown.style.display = 'block';
                pairDeviceButton.style.display = 'inline-block';

            } catch (error) {
                console.error('Error finding devices:', error);
                alert('Error finding devices.');
            }
        });
    }
    if (pairDeviceButton) {
        pairDeviceButton.addEventListener('click', async () => {
            try {
                const selectedDevice = deviceDropdown.value;
                if (!selectedDevice) {
                    alert('Please select a device.');
                    return;
                }

                const setResponse = await fetch('/set_device', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ device_name: selectedDevice }),
                });
                const setResult = await setResponse.json();

                if (setResult.success) {
                    const pairResponse = await fetch('/pair', { method: 'POST' });
                    const pairResult = await pairResponse.json();

                    if (pairResult.success) {
                        updateCharts();
                        window.location.href = pairResult.redirect;
                    } else {
                        alert(`Pairing failed: ${pairResult.error}`);
                    }
                } else {
                    alert(`Setting device failed: ${setResult.error}`);
                }
            } catch (error) {
                alert('Error pairing device.');
                console.error('Pairing error:', error);
            }
        });
    }
    if (window.location.pathname === '/collection') {
        initializeCharts();
        updateCharts();
        setInterval(updateCharts, 50);
    }
    if (homeButton) {
        homeButton.addEventListener('click', () => {
            // Stop the model prediction
            fetch('/stop_prediction', { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Redirect to the collection page
                        window.location.href = '/collection';
                    } else {
                        console.error('Error stopping prediction:', data.error);
                        alert('Error stopping prediction. Please try again.');
                    }
                })
                .catch(error => {
                    console.error('Error stopping prediction:', error);
                    alert('An error occurred while stopping prediction. Please try again.');
                });
        });
    }
    if (disconnectButton) {
        disconnectButton.addEventListener('click', () => {
            fetch('/disconnect', { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        window.location.href = '/';
                    } else {
                        console.error('Error disconnecting:', data.error);
                        alert('Error disconnecting. Please try again.');
                    }
                })
                .catch(error => {
                    console.error('Error disconnecting:', error);
                    alert('An error occurred while disconnecting. Please try again.');
                });
        });
    }
    if (trainModel) {
        trainModel.addEventListener('click', () => {
            const buttons = document.querySelectorAll('button');
            buttons.forEach(button => button.disabled = true);

            fetch('/train_model', { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Model training started successfully.');
                } else {
                    alert('Error during model training: ' + data.error);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred during model training. Please try again.');
            })
            .finally(() => {
                buttons.forEach(button => button.disabled = false);
            });
        });
    }

    fetch('check_model')
        .then(response => response.json())
        .then(data => {
            if (data.modelAvailable) {
                evaluateButton.disabled = false;
            }
            else {
                evaluateButton.disabled = true;
            }
        })
        .catch(error => console.error('Error checking model:', error));
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

function evaluateModel() {
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
    try {
        fetch('/collect', { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Data collected successfully.');
                } else {
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
                    animation: false,
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
                            max: 5000,    // Set the maximum value of the y-axis to 2000
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
        })
        .catch(error => {
            log('updateCharts', 'Error fetching sEMG data', error);
            console.error('Fetch error:', error); // Debugging line
        });
}

document.getElementById('findDevicesButton').addEventListener('click', async () => {
    try {
        const response = await fetch('/find_devices', { method: 'POST' });
        const devices = await response.json();

        if (devices.success === false) {
            console.error('Error finding devices:', devices.error);
            alert(`Error finding devices: ${devices.error}`);
            return;
        }

        const dropdown = document.getElementById('deviceDropdown');
        dropdown.innerHTML = ''; // Clear existing options

        if (Array.isArray(devices) && devices.length > 0) {
            devices.forEach(device => {
                const option = document.createElement('option');
                option.value = device.name; // Set value to device name
                option.textContent = `${device.name} (${device.address})`;
                dropdown.appendChild(option);
            });

            dropdown.style.display = 'block';
            document.getElementById('pairDeviceButton').style.display = 'block';
            console.log('Devices found and dropdown populated');
        } else {
            console.log('No devices found.');
            alert('No devices found.');
        }
    } catch (error) {
        console.error('Error finding devices:', error);
        alert('Error finding devices.');
    }
});

document.getElementById('pairDeviceButton').addEventListener('click', async () => {
    const dropdown = document.getElementById('deviceDropdown');
    const selectedDevice = dropdown.options[dropdown.selectedIndex].text; // Ensure correct device name

    console.log('Selected device:', selectedDevice);

    try {
        const response = await fetch('/set_device', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ device_name: selectedDevice })
        });

        const result = await response.json();
        if (result.success) {
            console.log('Device set successfully');
        } else {
            console.error('Error setting device:', result.error);
        }
    } catch (error) {
        console.error('Error pairing device:', error);
    }
});

// Function to find devices
function findDevices() {
    fetch('/find_devices', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.devices && data.devices.length > 0) {
            const deviceDropdown = document.getElementById('deviceDropdown');
            deviceDropdown.style.display = 'block';
            deviceDropdown.innerHTML = ''; // Clear existing options

            data.devices.forEach(device => {
                const option = document.createElement('option');
                option.value = device.address;
                option.text = device.name;
                deviceDropdown.add(option);
            });

            // Show the 'Pair Device' button now that devices are listed
            document.getElementById('pairDeviceButton').style.display = 'block';
        } else {
            console.error('No devices found');
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function setDevice() {
    const deviceDropdown = document.getElementById('deviceDropdown');
    const selectedDeviceName = deviceDropdown.value;

    fetch('/set_device', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ device_name: selectedDeviceName })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('Device set successfully');
            // Enable the Pair Device button now that the device is set
            document.getElementById('pairDeviceButton').disabled = false;
        } else {
            console.error('Failed to set device:', data.error);
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}
document.getElementById('deviceDropdown').addEventListener('change', setDevice);


function populateDeviceDropdown(devices) {
    deviceDropdown.innerHTML = '';
    devices.forEach(device => {
        const option = document.createElement('option');
        option.value = device.name; // Use device name as value
        option.textContent = `${device.name} (${device.address})`;
        deviceDropdown.appendChild(option);
    });
    deviceDropdown.style.display = 'block';
    pairDeviceButton.style.display = 'inline-block';
}
