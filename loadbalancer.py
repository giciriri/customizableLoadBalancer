from flask import Flask, request, jsonify
import requests
from consistent_hash_map import ConsistentHashMap  # Import the consistent hash map from Task 2

app = Flask(__name__)

# Initialize the consistent hash map for load balancing
N = 3  # Initial number of server containers
M = 512  # Total number of slots in the consistent hash map
K = 5  # Number of virtual servers for each server container
chm = ConsistentHashMap(N, M, K)

# List to keep track of active server replicas
active_replicas = {f'S{i}': f'http://server{i}:5000' for i in range(1, N + 1)}

@app.route('/rep', methods=['GET'])
def get_replicas():
    return jsonify(active_replicas)

@app.route('/add', methods=['POST'])
def add_server():
    global N
    N += 1
    new_server_id = f'S{N}'
    active_replicas[new_server_id] = f'http://server{N}:5000'
    chm.add_server(N)
    return jsonify({"message": f"Server {new_server_id} added.", "servers": active_replicas})

@app.route('/rm', methods=['POST'])
def remove_server():
    if len(active_replicas) == 0:
        return jsonify({"message": "No servers to remove."}), 400

    server_id = request.json.get('server_id')
    if server_id not in active_replicas:
        return jsonify({"message": f"Server {server_id} not found."}), 404

    chm.remove_server(int(server_id[1:]))  # Extract the server number from the ID
    del active_replicas[server_id]
    return jsonify({"message": f"Server {server_id} removed.", "servers": active_replicas})

@app.route('/<path:path>', methods=['GET', 'POST'])
def route_request(path):
    request_id = hash(path)
    server = chm.map_request(request_id)
    server_url = active_replicas[server.split('_')[0]]
    
    # Forward the request to the appropriate server replica
    if request.method == 'POST':
        resp = requests.post(f"{server_url}/{path}", json=request.json)
    else:
        resp = requests.get(f"{server_url}/{path}")
    
    return (resp.content, resp.status_code, resp.headers.items())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
