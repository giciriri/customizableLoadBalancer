from flask import Flask, request, jsonify
from load_balancer import LoadBalancer

app = Flask(__name__)
N = 3  # Number of server containers
M = 512  # Total number of slots in the consistent hash map
K = 1  # Number of virtual servers for each server container
lb = LoadBalancer(N, M, K)

for i in range(1, N + 1):
    lb.add_server(i)

@app.route('/route', methods=['POST'])
def route_request():
    data = request.json
    Rid = data['Rid']
    server = lb.route_request(Rid)
    return jsonify({"server": server})

@app.route('/add_server/<int:Sid>', methods=['POST'])
def add_server(Sid):
    lb.add_server(Sid)
    return "Server added", 200

@app.route('/remove_server/<int:Sid>', methods=['DELETE'])
def remove_server(Sid):
    lb.remove_server(Sid)
    return "Server removed", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4001)
