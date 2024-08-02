from flask import Flask, jsonify
import requests
import random
from consistent_hashing import ConsistentHashMap

app = Flask(__name__)

# Define the server ID mappings for 3 physical servers
server_name_map = {
    'S1_0': 'flask-server1:5000',
    'S1_1': 'flask-server1:5000',
    'S1_2': 'flask-server1:5000',
    'S2_0': 'flask-server2:5000',
    'S2_1': 'flask-server2:5000',
    'S2_2': 'flask-server2:5000',
    'S3_0': 'flask-server3:5000',
    'S3_1': 'flask-server3:5000',
    'S3_2': 'flask-server3:5000',
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
        app.logger.error(f"Server ID '{server_id}' not found in name map")
        return jsonify({"error": "Server not found"}), 500
    
    server_url = f"http://{server_name_map[server_id]}/home"
    
    try:
        response = requests.get(server_url)
        return jsonify(response.json())
    except requests.RequestException as e:
        app.logger.error(f"Error forwarding request to {server_url}: {e}")
        return jsonify({"error": "Failed to connect to server"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4001)
