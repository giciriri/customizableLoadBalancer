import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# Set a unique server ID for each instance
server_id = os.getenv('SERVER_ID', 'default-server-id')

@app.route('/home', methods=['GET'])
def home():
    return jsonify({"message": f"Server {server_id} is responding"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)