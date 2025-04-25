from flask import Flask, jsonify

app = Flask(__name__)

# Simula productos del proveedor (empresa USA)
provider_products = [
    {"id": 1, "name": "Laptop", "price": 1200},
    {"id": 2, "name": "Smartphone", "price": 800},
    {"id": 3, "name": "Tablet", "price": 500}
]

@app.route('/provider_products', methods=['GET'])
def get_provider_products():
    return jsonify(provider_products)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5010)