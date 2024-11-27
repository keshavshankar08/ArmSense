from flask import Flask, render_template, jsonify, request, redirect, url_for
import random
import serial
import time
from threading import Thread, Lock
from collections import deque
from Backend.controller_backend import ControllerBackend
import asyncio
import bleak
from statistics import mode
import os

app = Flask(__name__, template_folder='Frontend/templates', static_folder='Frontend/static')
backend = ControllerBackend()

# Serial port configuration
SERIAL_PORT = '/dev/ttyUSB1'
BAUD_RATE = 115200

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
except serial.SerialException as e:
    ser = None  # Ensure ser is defined even if opening fails
data_buffers = [deque(maxlen=1000) for _ in range(8)]
found_devices = []
found_devices_lock = Lock()

latest_prediction = None

gesture_labels = {
    0: 'Resting',
    1: 'Fist',
    2: 'Peace Sign',
    3: 'Pointing',
    4: 'Thumbs Up'
}

command_map = {
    0: 0,
    1: 1,
    2: 2,
    3: 3,
    4: 4
}


@app.route('/find_devices', methods=['POST'])
def find_devices():
    global found_devices  # Declare as global to modify the global variable
    try:
        # Run the asynchronous find_devices method
        asyncio.run(backend.signal_receiver.find_devices())
        # Store the devices in the global list
        with found_devices_lock:
            found_devices = backend.signal_receiver.devices  # This should be a list of (name, address) tuples
        devices_list = []
        for name, address in found_devices:
            devices_list.append({'name': name, 'address': address})
        return jsonify(devices_list)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/set_device', methods=['POST'])
def set_device():
    global found_devices
    try:
        data = request.json
        device_name = data.get('device_name')
        if not device_name:
            return jsonify({'success': False, 'error': 'Device name is required.'}), 400

        with found_devices_lock:
            # Use the global found_devices to find the device address
            device_address = next((address for name, address in found_devices if name == device_name), None)

        if not device_address:
            error_message = f'Device "{device_name}" not found in the list of discovered devices.'
            return jsonify({'success': False, 'error': error_message}), 404

        # Set the device address in signal_receiver
        backend.signal_receiver.bt_address = device_address
        backend.signal_receiver.selected_device = (device_name, device_address)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/pair', methods=['POST'])
def pair():
    try:
        if not hasattr(backend.signal_receiver, 'selected_device') or not backend.signal_receiver.selected_device:
            error_message = 'Device not set. Please select a device first.'
            return jsonify({'success': False, 'error': error_message}), 400

        # Start the Bluetooth connection
        backend.signal_receiver.start_reception()

        time.sleep(2)  # Adjust the sleep time as needed

        redirect_url = url_for('collection')
        return jsonify({'success': True, 'redirect': redirect_url})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/collection')
def collection():
    return render_template('collection.html')

@app.route('/collect', methods=['POST'])
def collect():
    return jsonify({'success': True})

@app.route('/train', methods=['POST'])
def train():
    return jsonify({'success': True})

# @app.route('/evaluate', methods=['POST'])
# def evaluate():
#     result = random.uniform(0.7, 0.99)  # Random accuracy between 70% and 99%
#     return jsonify({'result': f"{result:.2%}"})

@app.route('/get_semg_data')
def get_semg_data():
    signals = backend.signal_receiver.get_last_n_signals(100)
    if signals is not None and len(signals) > 0:
        data = signals.tolist()
        if len(data) < 100:
            num_missing = 100 - len(data)
            zero_padding = [[0] * 8 for _ in range(num_missing)]
            data = data + zero_padding
        return jsonify({'data': data})
    else:
        return jsonify({'data': []})

@app.route('/log', methods=['POST'])
def log():
    message = request.json.get('message')
    return jsonify({'success': True})

@app.route('/data_collection', methods=['GET', 'POST'])
def data_collection():
    if request.method == 'POST':
        return redirect(url_for('peace_sign'))
    return render_template('data_collection.html')

@app.route('/peace_sign', methods=['GET', 'POST'])
def peace_sign():
    if request.method == 'POST':
        return redirect(url_for('pointing'))
    return render_template('peace_sign.html')

@app.route('/pointing', methods=['GET', 'POST'])
def pointing():
    if request.method == 'POST':
        return redirect(url_for('thumbs_up'))
    return render_template('pointing.html')

@app.route('/thumbs_up', methods=['GET', 'POST'])
def thumbs_up():
    if request.method == 'POST':
        return redirect(url_for('collection'))
    return render_template('thumbs_up.html')

@app.route('/start_collection', methods=['POST'])
def start_collection():
    gesture_class = int(request.json.get('gesture_class'))
    backend.data_collector.start_collection(gesture_class)
    return jsonify({'success': True})

@app.route('/stop_collection', methods=['POST'])
def stop_collection():
    backend.data_collector.stop_collection()
    return jsonify({'success': True})

@app.route('/train_model', methods=['POST'])
def train_model():
    try:
        backend.trainer.process_data()
        time.sleep(1)

        backend.trainer.train_model()
        time.sleep(1)
        return jsonify({'success': True})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    
@app.route('/evaluate_model', methods=['POST'])
def evaluate_model():
    try:
        prediction_thread = Thread(target=continuous_prediction)
        prediction_thread.daemon = True
        prediction_thread.start()

        return jsonify({'success': True, 'redirect': url_for('gesture_prediction')})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/get_gesture_prediction', methods=['GET'])
def gesture_prediction():
    global latest_prediction
    return render_template('gesture_prediction.html', predicted_gesture=latest_prediction)

def send_serial_command(prediction_index):
    if ser and ser.is_open:
        command_value = command_map.get(prediction_index)
        if command_value is not None:
            ser.write(f"{command_value}".encode())
            ser.flush()

def continuous_prediction():
    global latest_prediction
    try:
        # Perform model evaluation
        backend.predictor.start_prediction()
        
        while True:
            # Check for errors in the predictor thread
            error = backend.predictor.get_error()
            if error:
                raise error  # This will be caught by the except block

            # Get the prediction
            prediction_index = backend.predictor.get_prediction()
            if prediction_index is not None:
                # Map the prediction index to the gesture label
                latest_prediction = gesture_labels.get(prediction_index, 'Unknown')

                # Send the predicted gesture over serial
                send_serial_command(prediction_index)
            else:
                latest_prediction = 'No prediction made.'
            time.sleep(1)  # Adjust sleep time as needed

    except Exception as e:
        backend.predictor.stop_prediction()

@app.route('/get_latest_prediction', methods=['GET'])
def get_latest_prediction():
    global latest_prediction
    return jsonify({'predicted_gesture': latest_prediction})

@app.route('/stop_prediction', methods=['POST'])
def stop_prediction():
    try:
        backend.predictor.running = False
        if backend.predictor.thread is not None and backend.predictor.thread.is_alive():
            backend.predictor.thread.join(timeout=5)
        else:
            return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/resting', methods=['GET', 'POST'])
def resting():
    return render_template('resting.html')

@app.route('/check_model', methods=['GET'])
def check_model():
    model_exists = os.path.exists('Hand/Backend/Resources/model.h5')
    return jsonify({'modelAvailable': model_exists})

if __name__ == '__main__':
    print(app.url_map)
    app.run(debug=True)