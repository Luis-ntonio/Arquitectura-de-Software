# simulate product listing

from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/products', methods=['GET'])
def products():
    return jsonify([
        {"id": 1, "name": "Laptop"},
        {"id": 2, "name": "Smartphone"}
    ])

if __name__ == '__main__':
    app.run(port=5002)