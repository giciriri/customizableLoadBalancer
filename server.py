from flask import Flask, jsonify
import os

app = Flask(__name__)

# Get the unique identifier from an environment variable
unique_id = os.getenv('UNIQUE_ID', 'unknown')

@app.route('/home', methods=['GET'])
def home():
    return f"Server ID: {unique_id}"

@app.route('/heartbeat', methods=['GET'])
def heartbeat():
    return jsonify({"status": "alive"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
