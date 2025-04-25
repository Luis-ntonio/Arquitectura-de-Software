# Login/register users

from flask import Flask, request, jsonify

app = Flask(__name__)

# Simulated database
users = {}

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400
    if username in users:
        return jsonify({"error": "User already exists"}), 409
    users[username] = password
    return jsonify({"message": "User registered"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400
    if username not in users or users[username] != password:
        return jsonify({"error": "Invalid credentials"}), 401
    return jsonify({"message": "User logged in"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)