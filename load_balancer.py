from flask import Flask, request, jsonify
from consistent_hashing import ConsistentHashMap

app = Flask(__name__)

# Initialize ConsistentHashMap with servers
hash_map = ConsistentHashMap(server_containers=['Server1', 'Server2', 'Server3'])

@app.route('/home', methods=['GET'])
def home():
    return "Welcome to the load balancer!"

@app.route('/forward', methods=['GET'])
def forward():
    request_id = request.args.get('id', default='default_id', type=str)
    server_id = hash_map.get_server(request_id)
    if server_id:
        return jsonify({'message': 'Request forwarded to {}'.format(server_id)})
    else:
        return jsonify({'message': 'Server not found'}), 404

@app.route('/update_servers', methods=['POST'])
def update_servers():
    # Example: Update the server containers list
    global hash_map
    new_servers = request.json.get('servers', [])
    hash_map = ConsistentHashMap(server_containers=new_servers)
    return jsonify({'message': 'Servers updated successfully'})

@app.route('/server_status', methods=['GET'])
def server_status():
    return jsonify({'status': 'All servers are running'})

@app.route('/mark_unhealthy', methods=['POST'])
def mark_unhealthy():
    server_id = request.json.get('server_id', '')
    # Identify physical server from the virtual server ID if needed
    physical_server_id = server_id.split('_')[0]
    
    if physical_server_id in hash_map.server_containers:
        # Mark the server as unhealthy
        hash_map.mark_server_unhealthy(physical_server_id)
        return jsonify({'message': f'{physical_server_id} is marked as unhealthy'})
    else:
        return jsonify({'message': 'Server not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4001)
