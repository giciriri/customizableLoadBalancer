from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/home', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to Server Home", "id": "unique_identifier"})

@app.route('/heartbeat', methods=['GET'])
def heartbeat():
    return jsonify({"status": "alive"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
