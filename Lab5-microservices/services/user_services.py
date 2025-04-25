# Login/register users

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    return jsonify({"message": "User logged in (stub)"}), 200

@app.route('/register', methods=['POST'])
def register():
    return jsonify({"message": "User registered (stub)"}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)