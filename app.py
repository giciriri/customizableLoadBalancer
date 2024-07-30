from flask import Flask, jsonify
import os

app = Flask(__name__)

# Get the unique identifier for this server instance from an environment variable
server_id = os.getenv('SERVER_ID', 'default-server-id')

@app.route('/home', methods=['GET'])
def home():
    return jsonify({"server_id": server_id})

@app.route('/heartbeat', methods=['GET'])
def heartbeat():
    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
