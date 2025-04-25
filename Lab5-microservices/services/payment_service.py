from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

payments = []

@app.route('/payment', methods=['POST'])
def payment():
    data = request.get_json()
    user = data.get('user')
    order_id = data.get('order_id')
    amount = data.get('amount')
    if not user or not order_id or not amount:
        return jsonify({"error": "Missing payment data"}), 400
    if amount <= 0:
        return jsonify({"error": "Amount must be positive"}), 400
    payments.append({"user": user, "order_id": order_id, "amount": amount})

    # Llama al servicio de recibos
    receipt_resp = requests.post(
        "http://receipt_service:5011/receipt",
        json={"user": user, "order_id": order_id, "amount": amount}
    )
    receipt = receipt_resp.json()
    return jsonify({"message": "Payment processed", "receipt": receipt}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)