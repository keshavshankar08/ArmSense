from flask import Flask, render_template, jsonify, request, redirect, url_for
import logging
import sys
import threading
import serial
import time
from flask_socketio import *

sys.path.append('.')
from Backend.controller_backend import ControllerBackend

app = Flask(__name__, template_folder='Frontend/templates', static_folder='Frontend/static')
socketio = SocketIO(app, cors_allowed_origins="*")
controller_backend = ControllerBackend()

# Initialize serial communication
ser = serial.Serial('/dev/tty.usbserial-0001', 115200)

def decode_with_fallback(raw_line):
    """
    Attempt to decode a raw byte line into a UTF-8 string. If any character fails to decode,
    it will be replaced with '0'.
    """
    decoded_chars = []
    for byte in raw_line:
        try:
            decoded_chars.append(chr(byte).encode('utf-8').decode('utf-8'))
        except UnicodeDecodeError:
            decoded_chars.append('0')  # Replace invalid byte with '0'
    return ''.join(decoded_chars)

def read_serial_data():
    while True:
        try:
            raw_line = ser.readline()  # Read raw bytes from serial
            line = decode_with_fallback(raw_line).strip()  # Use fallback decoding
            print(f"Raw data from serial: {line}")
            if line.endswith('.'):
                data_str = line[:-1]  # Remove trailing period
                data = data_str.split(',')
                if len(data) == 8:
                    try:
                        data = [int(value) for value in data]  # Convert each element to an integer
                        print(f"Parsed data: {data}")
                        socketio.emit('semg_data', {'data': data})  # Emit parsed data to frontend
                    except ValueError:
                        print(f"Error converting data to integers: {data}")
        except serial.SerialException as e:
            print(f"Serial port error: {e}")
            time.sleep(1)  # Wait and retry
        except Exception as e:
            print(f"Unexpected error: {e}")
            
# SocketIO event handlers
@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')


@socketio.on('start_data_collection')
def handle_start_data_collection(data):
    gesture_id = data.get('gesture_id')
    controller_backend.data_collector.start_collection(gesture_id)
    emit('collection_started', {'success': True})

@socketio.on('stop_data_collection')
def handle_stop_data_collection():
    controller_backend.data_collector.stop_collection()
    emit('collection_stopped', {'success': True})



# Set up logging
# handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
# handler.setLevel(logging.INFO)
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# handler.setFormatter(formatter)
# app.logger.addHandler(handler)
# app.logger.setLevel(logging.DEBUG)

@app.route('/')
def index():
    app.logger.info('Rendering index page')
    return render_template('index.html')

@app.route('/pair', methods=['POST'])
def pair():
    app.logger.info('Attempting to pair armband')
    # Simulate successful pairing
    return jsonify({'success': True, 'redirect': url_for('collection')})

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

@app.route('/get_semg_data')
def get_semg_data():
    app.logger.info('Generating sEMG data')
    # Generate dummy sEMG data

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
    controller_backend.data_collector.start_collection(1) # say 1 is fist
    #controller_backend.data_collector.stop_collection()
    if request.method == 'POST':
        # Redirect to the next page in the sequence
        return redirect(url_for('pointing'))
    return render_template('peace_sign.html')

@app.route('/pointing', methods=['GET', 'POST'])
def pointing():
    app.logger.info('Rendering pointing page')
    controller_backend.data_collector.stop_collection()
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

# Function to emit sEMG data
if __name__ == '__main__':
    # Start the serial reading in a background thread
    socketio.start_background_task(target=read_serial_data)
    socketio.run(app, host='0.0.0.0', port=5001)
    # threading.Thread(target=read_serial_data, daemon=True).start()
    # socketio.run(app, debug=True)
    # Remove or comment out app.run(debug=True)
    # app.run(debug=True)

