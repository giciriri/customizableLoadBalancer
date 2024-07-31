from flask import Flask, request, jsonify
import requests
import random
from consistent_hashing import ConsistentHashMap  # Ensure you import correctly

app = Flask(__name__)

# Define the server ID mappings here
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
    # Add servers for S4, S5, and S6 (these are not actually used in this example)
    'S4_0': 'flask-server4:5000', 
    'S4_1': 'flask-server4:5000',
    'S4_2': 'flask-server4:5000',
    'S5_0': 'flask-server5:5000', 
    'S5_1': 'flask-server5:5000',
    'S5_2': 'flask-server5:5000',
    'S6_0': 'flask-server6:5000', 
    'S6_1': 'flask-server6:5000',
    'S6_2': 'flask-server6:5000' 
}

# Initialize the consistent hash map with 3 real servers (N=3) and 9 virtual servers (K=9)
hash_map = ConsistentHashMap(
    N=3,  # Number of server containers (3 real servers)
    M=512,  # Number of slots in the consistent hash map
    K=9  # Number of virtual servers (9 virtual servers)
)

@app.route('/home', methods=['GET'])
def home():
    return jsonify({"message": "Load balancer is responding"})

@app.route('/forward', methods=['GET'])
def forward():
    # Map request to a server ID using consistent hashing
    request_id = random.randint(1, 100000)  # You can use a more specific ID based on request attributes
    server_id = hash_map.get_server(request_id)
    
    # Check if server ID is in the name map
    if server_id not in server_name_map:
        app.logger.error(f"Server ID '{server_id}' not found in name map")
        return jsonify({"error": "Server not found"}), 500
    
    server_url = f"http://{server_name_map[server_id]}/home"
    
    # Forward request to the selected server
    try:
        response = requests.get(server_url)
        return jsonify(response.json())
    except requests.RequestException as e:
        app.logger.error(f"Error forwarding request to {server_url}: {e}")
        return jsonify({"error": "Failed to connect to server"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4001) 