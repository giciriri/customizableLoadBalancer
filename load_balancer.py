from flask import Flask, jsonify, request
import requests
import random
from consistent_hashing import ConsistentHashMap

app = Flask(__name__)

# Define the server ID mappings for virtual servers to physical servers
server_name_map = {
    'S1': 'flask-server1:5000',
    'S2': 'flask-server2:5000',
    'S3': 'flask-server3:5000',
}

# Initialize the consistent hash map with 3 real servers and 9 virtual servers
hash_map = ConsistentHashMap(
    N=3,  # Number of server containers (3 real servers)
    M=512,  # Number of slots in the consistent hash map
    K=3  # Number of virtual servers (3 virtual servers per real server)
)

@app.route('/home', methods=['GET'])
def home():
    return jsonify({"message": "Load balancer is responding"})

@app.route('/forward', methods=['GET'])
def forward():
    request_id = random.randint(1, 100000)
    server_id = hash_map.get_server(request_id)
    
    if server_id not in server_name_map:
        app.logger.error(f"Unexpected server_id received: {server_id}")
        return jsonify({"error": "Server not found"}), 500
    
    server_url = f"http://{server_name_map[server_id]}/home"
    
    try:
        response = requests.get(server_url)
        response.raise_for_status()  # Ensure we notice bad responses
        
        # Return the response along with the server ID
        return jsonify({
            "server_id": server_id,
            "message": response.json().get('message', 'No message in response')
        })
    except requests.RequestException as e:
        app.logger.error(f"Error forwarding request to {server_url}: {e}")
        return handle_forward_error()

def handle_forward_error():
    available_servers = [f"http://{server}" for server in server_name_map.values() if is_server_healthy(f"http://{server}")]
    if not available_servers:
        app.logger.error("All servers are down")
        return jsonify({"error": "All servers are down"}), 502

    server_url = random.choice(available_servers) + '/home'
    try:
        response = requests.get(server_url)
        response.raise_for_status()
        return jsonify({
            "server_id": "BackupServer",
            "message": response.json().get('message', 'No message in response')
        })
    except requests.RequestException as e:
        app.logger.error(f"Error forwarding request to backup server {server_url}: {e}")
        return jsonify({"error": "Failed to connect to any server"}), 502

def is_server_healthy(server_url):
    try:
        response = requests.get(server_url)
        return response.status_code == 200
    except requests.RequestException:
        return False

@app.route('/update_servers', methods=['POST'])
def update_servers():
    server_list = request.json.get('servers', [])
    hash_map.update_servers(server_list)
    
    # Update server_name_map based on the new server list
    global server_name_map
    server_name_map = {server: f'flask-server{server[1]}:5000' for server in server_list}
    
    return jsonify({"message": "Server list updated"}), 200

@app.route('/server_status/<server_id>', methods=['POST'])
def update_server_status(server_id):
    status = request.json.get('status', 'down')
    if status == 'up':
        if server_id not in server_name_map:
            server_name_map[server_id] = f'flask-server{server_id[1]}:5000'
        hash_map.add_server(server_id)
    else:
        if server_id in server_name_map:
            del server_name_map[server_id]
        hash_map.remove_server(server_id)
    return jsonify({"message": "Server status updated"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4001)

