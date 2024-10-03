from flask import Flask, render_template, jsonify, request, redirect, url_for
import random
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)

# Set up logging
handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
app.logger.addHandler(handler)
app.logger.setLevel(logging.DEBUG)

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
    result = random.uniform(0.7, 0.99)  # Random accuracy between 70% and 99%
    app.logger.info(f'Model evaluation result: {result:.2%}')
    return jsonify({'result': f"{result:.2%}"})

@app.route('/get_semg_data')
def get_semg_data():
    app.logger.info('Generating sEMG data')
    # Generate dummy sEMG data
    data = [[random.uniform(-1, 1) for _ in range(100)] for _ in range(8)]
    return jsonify({'data': data})

@app.route('/log', methods=['POST'])
def log():
    message = request.json.get('message')
    app.logger.info(f'Client log: {message}')
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True)