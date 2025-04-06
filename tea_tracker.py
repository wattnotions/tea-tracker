from flask import Flask, jsonify
import os
import json

app = Flask(__name__)
DATA_FILE = 'tea_count.json'

def load_count():
    if not os.path.exists(DATA_FILE):
        return 0
    with open(DATA_FILE, 'r') as f:
        return json.load(f).get('count', 0)

def save_count(count):
    with open(DATA_FILE, 'w') as f:
        json.dump({'count': count}, f)

@app.route('/tea')
def increment_tea():
    count = load_count() + 1
    save_count(count)
    return jsonify(message="Cup of tea logged!", total_cups=count)

@app.route('/tea/status')
def get_status():
    count = load_count()
    return jsonify(total_cups=count)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
