import sys 
sys.path.append('.')

from flask import Flask, render_template, jsonify, request, redirect, url_for
import random
import logging
import serial
import os
import time
from threading import Thread
from collections import deque
from logging.handlers import RotatingFileHandler
from Hand.Backend.controller_backend import ControllerBackend
import asyncio

app = Flask(__name__, template_folder='Frontend/templates', static_folder='Frontend/static')
backend = ControllerBackend()

# Set up logging
handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
app.logger.addHandler(handler)
app.logger.setLevel(logging.DEBUG)

# Serial port configuration
SERIAL_PORT = '/dev/ttyUSB1'
BAUD_RATE = 115200

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    app.logger.info(f"Serial port {SERIAL_PORT} opened successfully.")
except serial.SerialException as e:
    ser = None  # Ensure ser is defined even if opening fails
    app.logger.error(f"Error opening serial port {SERIAL_PORT}: {e}")
# Buffer to store the latest data
data_buffers = [deque(maxlen=100) for _ in range(8)]

# Add this at the top of your file
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
    # Logic to find Bluetooth devices
    # This could involve starting the Bluetooth connection process
    try:
        # backend.signal_receiver.connect()  # Start Bluetooth connection
        serial_thread = Thread(target=backend.signal_receiver.connect)
        serial_thread.start()
        
        return jsonify({'success': True})
    except Exception as e:
        app.logger.error(f"Error finding devices: {e}")
        return jsonify({'success': False, 'error': str(e)})
    
# def read_serial_data():
#     try:
#         ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
#         while True:
#             line = ser.readline().decode('utf-8', errors='ignore').strip()
#             if line:
#                 #print(f"Raw data received: {line}")  # Debugging output
#                 values = line.split(',')
#                 if len(values) == 8:
#                     try:
#                         for i, value in enumerate(values):
#                             data_buffers[i].append(float(value))
#                     except ValueError as e:
#                         print(f"Error converting value to float: {value} - {e}")
#                 else:
#                     print(f"Unexpected number of values: {len(values)} - {values}")
#             time.sleep(0.01)  # Small delay to prevent high CPU usage
#     except serial.SerialException as e:
#         print(f"Error reading from serial port: {e}")
#     finally:
#         if 'ser' in locals() and ser.is_open:
#             ser.close()

# Start the background thread to read serial data
# serial_thread = Thread(target=read_serial_data)
# serial_thread.daemon = True
# serial_thread.start()

@app.route('/')
def index():
    app.logger.info('Rendering index page')
    print("Index page rendered")
    return render_template('index.html')

@app.route('/pair', methods=['POST'])
def pair():
    app.logger.info('Attempting to pair armband')
    try:
        asyncio.run(backend.signal_receiver.find_devices())
        asyncio.run(backend.signal_receiver.set_device("MDT UART Service"))
        backend.signal_receiver.start_reception()  # Start Bluetooth connection
        time.sleep(10)
        # print(backend.signal_receiver.get_last_n_signals(2))
        # return jsonify({'success': True})
        return jsonify({'success': True, 'redirect': url_for('collection')})
    except Exception as e:
        print(f"Error finding devices: {e}")
        return jsonify({'success': False, 'error': str(e)})
    # Simulate successful pairing
    
    

@app.route('/collection')
def collection():
    app.logger.info('Rendering collection page')
    return render_template('collection.html')

@app.route('/collect', methods=['POST'])
def collect():
    app.logger.info('Collecting data')
    # Simulate successful data collection
    return jsonify({'success': True})

@app.route('/train', methods=['POST'])
def train():
    app.logger.info('Training model')
    # Simulate successful model training
    return jsonify({'success': True})

@app.route('/evaluate', methods=['POST'])
def evaluate():
    app.logger.info('Evaluating model')
    # Simulate model evaluation
    result = random.uniform(0.7, 0.99)  # Random accuracy between 70% and 99%
    app.logger.info(f'Model evaluation result: {result:.2%}')
    return jsonify({'result': f"{result:.2%}"})

@app.route('/get_semg_data')
def get_semg_data():
    # # Prepare data to send to client
    # data = [list(buffer) for buffer in data_buffers]
    # return jsonify({'data': data})
    signals = backend.signal_receiver.get_last_n_signals(100)
    if signals is not None:
        data = signals.tolist()
        return jsonify({'data': data})
    else:
        return jsonify({'data': []})

@app.route('/log', methods=['POST'])
def log():
    message = request.json.get('message')
    app.logger.info(f'Client log: {message}')
    return jsonify({'success': True})

@app.route('/data_collection', methods=['GET', 'POST'])
def data_collection():
    app.logger.info('Rendering data_collection page')
    if request.method == 'POST':
        # Redirect to the next page in the sequence
        return redirect(url_for('peace_sign'))
    return render_template('data_collection.html')

@app.route('/peace_sign', methods=['GET', 'POST'])
def peace_sign():
    app.logger.info('Rendering peace_sign page')
    if request.method == 'POST':
        # Redirect to the next page in the sequence
        return redirect(url_for('pointing'))
    return render_template('peace_sign.html')

@app.route('/pointing', methods=['GET', 'POST'])
def pointing():
    app.logger.info('Rendering pointing page')
    if request.method == 'POST':
        # Redirect to the next page in the sequence
        return redirect(url_for('thumbs_up'))
    return render_template('pointing.html')

@app.route('/thumbs_up', methods=['GET', 'POST'])
def thumbs_up():
    app.logger.info('Rendering thumbs_up page')
    if request.method == 'POST':
        # Redirect back to collection page
        return redirect(url_for('collection'))
    return render_template('thumbs_up.html')

@app.route('/start_collection', methods=['POST'])
def start_collection():
    gesture_class = int(request.json.get('gesture_class'))
    # Start data collection
    backend.data_collector.start_collection(gesture_class)
    return jsonify({'success': True})

@app.route('/stop_collection', methods=['POST'])
def stop_collection():
    backend.data_collector.stop_collection()
    #backend.data_collector.stop_collection("Hand/Backend/Resources/data.csv")
    return jsonify({'success': True})

@app.route('/train_model', methods=['POST'])
def train_model():
    try:
        # Data cleaning and normalization logic
        backend.trainer.process_data()
        time.sleep(1)

        # Send training signal    
        backend.trainer.train_model()
        time.sleep(1)
        return jsonify({'success': True})

    except Exception as e:
        app.logger.error(f"Error during model training: {e}")
        return jsonify({'success': False, 'error': str(e)})
    
@app.route('/evaluate_model', methods=['POST'])
def evaluate_model():
    try:
        # Start the continuous prediction in a background thread
        prediction_thread = Thread(target=continuous_prediction)
        prediction_thread.daemon = True
        prediction_thread.start()

        # Redirect to the gesture prediction page
        return jsonify({'success': True, 'redirect': url_for('gesture_prediction')})

    except Exception as e:
        app.logger.error(f"Error starting evaluation: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/get_gesture_prediction', methods=['GET'])
def gesture_prediction():
    # Example: Pass a dummy prediction for demonstrations
    global latest_prediction
    return render_template('gesture_prediction.html', predicted_gesture=latest_prediction)

def send_serial_command(prediction_index):
    if ser and ser.is_open:
        try:
            # Map the prediction index to the command value
            command_value = command_map.get(prediction_index)
            print(f"Command value: {command_value}")
            if command_value is not None:
                # data_to_send = f"{command_value}"
                ser.write(f"{command_value}".encode())
                ser.flush()
            else:
                app.logger.error(f"Unrecognized prediction index: {prediction_index}")
        except serial.SerialException as e:
            app.logger.error(f"Error sending serial command: {e}")
    else:
        app.logger.error("Serial port is not open.")

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
                app.logger.info(f"Latest prediction: {latest_prediction}")

                # Send the predicted gesture over serial
                send_serial_command(prediction_index)
            else:
                latest_prediction = 'No prediction made.'
                app.logger.info(latest_prediction)

            time.sleep(1)  # Adjust sleep time as needed

    except Exception as e:
        app.logger.error(f"Error during continuous prediction: {e}")
        backend.predictor.stop_prediction()

@app.route('/get_latest_prediction', methods=['GET'])
def get_latest_prediction():
    global latest_prediction
    return jsonify({'predicted_gesture': latest_prediction})

if __name__ == '__main__':
    print(app.url_map)
    app.run(debug=True)