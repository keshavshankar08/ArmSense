from flask import Flask, render_template, jsonify, request, redirect, url_for
from ArmSense.controller_backend import ControllerBackend

app = Flask(__name__)
controller = ControllerBackend()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pair', methods=['POST'])
def pair():
    #success = controller.pair_armband()
    #if success:
    return jsonify({'success': True, 'redirect': url_for('collection')})
    #return jsonify({'success': False})

@app.route('/collection')
def collection():
    return render_template('collection.html')

@app.route('/collection', methods=['POST'])
def collect():
    success = controller.collect_data()
    return jsonify({'success': success})

@app.route('/train', methods=['POST'])
def train():
    success = controller.train_model()
    return jsonify({'success': success})

@app.route('/evaluate', methods=['POST'])
def evaluate():
    result = controller.evaluate_model()
    return jsonify({'result': result})

@app.route('/get_semg_data')
def get_semg_data():
    data = controller.get_semg_data()
    return jsonify({'data': data})

if __name__ == '__main__':
    app.run(debug=True)
