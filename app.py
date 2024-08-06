import os
import random
from flask import Flask, jsonify, request, send_file
import matplotlib.pyplot as plt
from io import BytesIO
from consistent_hashing import ConsistentHashMap

# Initialize Flask app
app = Flask(__name__)

# Set a unique server ID for each instance
server_id = os.getenv('SERVER_ID', 'default-server-id')

# Initialize ConsistentHashMap with some dummy servers
hash_map = ConsistentHashMap(server_containers=['Server1', 'Server2', 'Server3'])

@app.route('/home', methods=['GET'])
def home():
    request_id = random.randint(1, 100000)
    server = hash_map.get_server(request_id)
    return jsonify({"message": f"Server {server_id} (actual server: {server}) is responding with request ID {request_id}"}), 200

@app.route('/rep', methods=['GET'])
def get_replicas():
    return jsonify({"message": {"replicas": [server_id]}})

@app.route('/visualize', methods=['GET'])
def visualize():
    img = BytesIO()
    hash_map.visualize_hash_map()
    plt.savefig(img, format='png')
    img.seek(0)
    return send_file(img, mimetype='image/png')

@app.route('/add_server', methods=['POST'])
def add_server():
    data = request.json
    server_id = data.get('server_id')
    if not server_id:
        return jsonify({"error": "server_id is required"}), 400
    
    hash_map.add_server(server_id)
    return jsonify({"message": f"Server {server_id} added successfully"}), 200

@app.route('/remove_server', methods=['POST'])
def remove_server():
    data = request.json
    server_id = data.get('server_id')
    if not server_id:
        return jsonify({"error": "server_id is required"}), 400

    hash_map.remove_server(server_id)
    return jsonify({"message": f"Server {server_id} removed successfully"}), 200

@app.route('/list_servers', methods=['GET'])
def list_servers():
    servers = hash_map.get_all_servers()
    return jsonify({"servers": servers}), 200

@app.route('/mark_unhealthy', methods=['POST'])
def mark_unhealthy():
    data = request.json
    server_id = data.get('server_id')
    if not server_id:
        return jsonify({"error": "server_id is required"}), 400
    
    hash_map.mark_server_unhealthy(server_id)
    return jsonify({"message": f"Server {server_id} marked as unhealthy"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
