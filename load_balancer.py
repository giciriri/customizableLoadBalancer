import logging
import requests
from flask import Flask, request, jsonify
from consistent_hashing import ConsistentHashMap, hash_function, virtual_server_hash_function

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Parameters
num_servers = 3
num_slots = 512
num_virtual_servers = 9

# Initialize consistent hash map
consistent_hash_map = ConsistentHashMap(num_servers, num_slots, num_virtual_servers, hash_function, virtual_server_hash_function)

# Add initial servers
servers = [
    'flask-server1',
    'flask-server2',
    'flask-server3'
]

for server in servers:
    consistent_hash_map.add_server(server)

@app.route('/rep', methods=['GET'])
def get_replicas():
    replicas = consistent_hash_map.servers
    return jsonify({"N": len(replicas), "replicas": replicas})

@app.route('/add', methods=['POST'])
def add_servers():
    data = request.get_json()
    new_servers = data.get("hostnames", [])
    for server in new_servers:
        consistent_hash_map.add_server(server)
    return jsonify({"message": {"N": len(consistent_hash_map.servers), "replicas": consistent_hash_map.servers}, "status": "successful"})

@app.route('/rm', methods=['DELETE'])
def remove_servers():
    data = request.get_json()
    remove_servers = data.get("hostnames", [])
    for server in remove_servers:
        consistent_hash_map.remove_server(server)
    return jsonify({"message": {"N": len(consistent_hash_map.servers), "replicas": consistent_hash_map.servers}, "status": "successful"})

@app.route('/<path>', methods=['GET', 'POST'])
def route_request(path):
    server_id = consistent_hash_map.get_server(path)
    
    # Map server IDs to container names
    server_name_map = {
        'flask-server1': 'flask-server1:5000',
        'flask-server2': 'flask-server2:5000',
        'flask-server3': 'flask-server3:5000'
    }
    
    server_name = server_name_map.get(server_id)
    
    if not server_name:
        logger.error(f"Server ID '{server_id}' not found in name map")
        return "Server not found", 500
    
    server_url = f"http://{server_name}/{path}"
    
    # Log request details
    logger.info(f"Routing request for path '{path}' to server '{server_id}'")
    
    try:
        response = requests.request(
            method=request.method,
            url=server_url,
            headers={k: v for k, v in request.headers if k != 'Host'},
            data=request.get_data(),
            cookies=request.cookies
        )
        return response.content, response.status_code
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}")
        return str(e), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4001)
