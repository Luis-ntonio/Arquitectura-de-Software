from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/products', methods=['GET'])
def get_products():
    # Llama al servicio de proveedores para obtener productos
    resp = requests.get("http://provider_service:5010/provider_products")
    return jsonify(resp.json())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)