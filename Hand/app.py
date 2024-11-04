import sys
import logging
import serial
import time
import csv
import threading
from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_socketio import SocketIO, emit
from threading import Lock

# Add the Backend directory to the system path
sys.path.append('/Users/travisallabon/Documents/senior_design/ArmSense/Hand/Backend')
from Backend.controller_backend import ControllerBackend

# Initialize Flask app
app = Flask(__name__, template_folder='Frontend/templates', static_folder='Frontend/static')
socketio = SocketIO(app, cors_allowed_origins="*")
controller_backend = ControllerBackend()

# Initialize serial communication
ser = serial.Serial('/dev/tty.usbserial-0001', 115200)

# SignalReceiver should use the serial port
controller_backend.signal_receiver.serial_port = ser
data_collection_thread = None
collecting_data = False

def collect_serial_data():
    """Function to collect serial data and send it via WebSocket."""
    while collecting_data:
        data = controller_backend.signal_receiver.get_last_n_signals(1)  # Ensure get_latest_data is implemented
        if data and len(data) == 1:
            socketio.emit('semg_data', {'data': data})
        time.sleep(0.1)  # Adjust based on real-time needs

@app.route('/start_data_collection', methods=['POST'])
def start_data_collection():
    global collecting_data, data_collection_thread
    gesture_label = request.json.get('gesture_label', 0)
    controller_backend.data_collector.start_collection(gesture_label, 100, 0.2, 0.05)
    collecting_data = True
    data_collection_thread = threading.Thread(target=collect_serial_data)
    data_collection_thread.start()
    return jsonify({"success": True})

@app.route('/stop_data_collection', methods=['POST'])
def stop_data_collection():
    global collecting_data
    controller_backend.data_collector.stop_collection("/Users/travisallabon/Documents/senior_design/ArmSense/Hand/Backend/Resources/data.csv")
    collecting_data = False
    return jsonify({"success": True})

@socketio.on('connect')
def handle_connect():
    emit('connection_response', {'status': 'Connected'})

def decode_with_fallback(raw_line):
    try:
        return raw_line.decode('utf-8')
    except UnicodeDecodeError:
        return raw_line.decode('utf-8', 'replace')

def read_serial_data(signal_receiver):
    while True:
        if ser.in_waiting > 0:
            raw_line = ser.readline()
            decoded_line = raw_line.decode('utf-8', errors='ignore').strip()
            if decoded_line:
                try:
                    data_values = list(map(int, decoded_line.split(',')))
                    if len(data_values) == 8:
                        with signal_receiver.buffer_lock:
                            signal_receiver.signal_buffer.append(data_values)
                        print(f"Appended signal: {data_values}")
                except ValueError:
                    print(f"Invalid data received: {decoded_line}")
        time.sleep(0.01)

# Flask routes
@app.route('/')
def index():
    app.logger.info('Rendering index page')
    return render_template('index.html')

@app.route('/pair', methods=['POST'])
def pair():
    app.logger.info('Attempting to pair armband')
    return jsonify({'success': True, 'redirect': url_for('collection')})

@app.route('/collection')
def collection():
    app.logger.info('Rendering collection page')
    return render_template('collection.html')

@app.route('/collect', methods=['POST'])
def collect():
    app.logger.info('Collecting data')
    return jsonify({'success': True})

@app.route('/train', methods=['POST'])
def train():
    app.logger.info('Training model')
    return jsonify({'success': True})

@app.route('/evaluate', methods=['POST'])
def evaluate():
    app.logger.info('Evaluating model')
    return jsonify({'success': True})

@app.route('/get_semg_data')
def get_semg_data():
    app.logger.info('Generating sEMG data')
    return jsonify({'data': 'dummy sEMG data'})

@app.route('/log', methods=['POST'])
def log():
    message = request.json.get('message')
    app.logger.info(f'Client log: {message}')
    return jsonify({'success': True})

@app.route('/data_collection', methods=['GET', 'POST'])
def data_collection():
    app.logger.info('Rendering data_collection page')
    controller_backend.data_collector.start_collection(0, 100, 0.2, 0.05)
    if request.method == 'POST':
        return redirect(url_for('peace_sign'))
    return render_template('data_collection.html')

@app.route('/peace_sign', methods=['GET', 'POST'])
def peace_sign():
    app.logger.info('Rendering peace_sign page')
    controller_backend.data_collector.start_collection(1, 100, 0.2, 0.05)  # Assume 1 is for 'peace sign'
    if request.method == 'POST':
        return redirect(url_for('pointing'))
    return render_template('peace_sign.html')

@app.route('/pointing', methods=['GET', 'POST'])
def pointing():
    app.logger.info('Rendering pointing page')
    if request.method == 'POST':
        return redirect(url_for('thumbs_up'))
    return render_template('pointing.html')

@app.route('/thumbs_up')
def thumbs_up():
    return render_template('thumbs_up.html')

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

if __name__ == '__main__':
    # Start the serial reading in a background thread
    socketio.start_background_task(read_serial_data, controller_backend.signal_receiver)
    socketio.run(app, host='0.0.0.0', port=5000)