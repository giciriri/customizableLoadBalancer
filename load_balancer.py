from flask import Flask, request, jsonify
from consistent_hashing import ConsistentHashMap

app = Flask(__name__)

# Initialize ConsistentHashMap with servers
hash_map = ConsistentHashMap(
    server_containers=['Server1', 'Server2', 'Server3'],  # Initial servers
    N=5,  # Number of replicas
    K=10,  # Number of virtual servers per physical server
    M=1024  # Size of the hash map
)

@app.route('/home', methods=['GET'])
def home():
    return "Welcome to the load balancer!"

@app.route('/forward', methods=['GET'])
def forward():
    request_id = request.args.get('id', default='default_id', type=str)
    server_id = hash_map.get_server(request_id)
    if server_id:
        return jsonify({'message': f'Request forwarded to {server_id}'})
    else:
        return jsonify({'message': 'Server not found'}), 404

@app.route('/update_servers', methods=['POST'])
def update_servers():
    new_servers = request.json.get('servers', [])
    global hash_map
    hash_map = ConsistentHashMap(
        server_containers=new_servers,
        N=hash_map.N,
        K=hash_map.K,
        M=hash_map.M
    )
    return jsonify({'message': 'Servers updated successfully'})

@app.route('/add_server', methods=['POST'])
def add_server():
    server_id = request.json.get('server_id', '')
    if server_id not in hash_map.server_containers:
        hash_map.add_server(server_id)
        return jsonify({'message': f'{server_id} added successfully'})
    else:
        return jsonify({'message': f'Server {server_id} already exists'}), 400

@app.route('/remove_server', methods=['POST'])
def remove_server():
    server_id = request.json.get('server_id', '')
    if server_id in hash_map.server_containers:
        hash_map.remove_server(server_id)
        return jsonify({'message': f'{server_id} removed successfully'})
    else:
        return jsonify({'message': f'Server {server_id} not found'}), 404

@app.route('/server_status', methods=['GET'])
def server_status():
    return jsonify({'status': 'All servers are running'})

@app.route('/mark_unhealthy', methods=['POST'])
def mark_unhealthy():
    server_id = request.json.get('server_id', '')
    if server_id in hash_map.server_containers:
        hash_map.mark_server_unhealthy(server_id)
        return jsonify({'message': f'{server_id} is marked as unhealthy'})
    else:
        return jsonify({'message': 'Server not found'}), 404

@app.route('/list_servers', methods=['GET'])
def list_servers():
    return jsonify({'servers': hash_map.server_containers})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4001)
