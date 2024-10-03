from flask import Flask, render_template, jsonify, request, redirect, url_for
import random

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pair', methods=['POST'])
def pair():
    # Simulate successful pairing
    return jsonify({'success': True, 'redirect': url_for('collection')})

@app.route('/collection')
def collection():
    return render_template('collection.html')

@app.route('/collect', methods=['POST'])
def collect():
    # Simulate successful data collection
    return jsonify({'success': True})

@app.route('/train', methods=['POST'])
def train():
    # Simulate successful model training
    return jsonify({'success': True})

@app.route('/evaluate', methods=['POST'])
def evaluate():
    # Simulate model evaluation
    result = random.uniform(0.7, 0.99)  # Random accuracy between 70% and 99%
    return jsonify({'result': f"{result:.2%}"})

@app.route('/get_semg_data')
def get_semg_data():
    # Generate dummy sEMG data
    data = [[random.uniform(-1, 1) for _ in range(100)] for _ in range(8)]
    return jsonify({'data': data})

if __name__ == '__main__':
    app.run(debug=True)