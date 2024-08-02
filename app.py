import os
import random
from flask import Flask, jsonify

# Initialize Flask app
app = Flask(__name__)

# Set a unique server ID for each instance
server_id = os.getenv('SERVER_ID', 'default-server-id')

@app.route('/home', methods=['GET'])
def home():
    request_id = random.randint(1, 100000)
    return jsonify({"message": f"Server {server_id} is responding with request ID {request_id}"}), 200

@app.route('/rep', methods=['GET'])
def get_replicas():
    # For demonstration purposes, return the server ID
    return jsonify({"message": {"replicas": [server_id]}})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
