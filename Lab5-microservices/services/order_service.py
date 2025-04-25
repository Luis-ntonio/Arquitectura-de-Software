# simulate order processing 

from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/order', methods=['POST'])
def create_order():
    """Handle order creation and forward it to the aggregation service."""
    data = request.get_json()
    provider_id = data.get('provider_id')
    product_id = data.get('product_id')
    quantity = data.get('quantity')

    if not provider_id or not product_id or not quantity:
        return jsonify({"error": "Missing order data"}), 400

    # Forward the order to the aggregation service
    r = requests.post("http://order_aggregation_service:5006/aggregate_order", json={
        "provider_id": provider_id,
        "product_id": product_id,
        "quantity": quantity
    })

    if r.status_code != 200:
        return jsonify({"error": "Failed to aggregate order"}), 500

    return jsonify({"message": "Order created and sent to aggregation service"}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)