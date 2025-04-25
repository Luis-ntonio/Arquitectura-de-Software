from flask import Flask, request, jsonify

app = Flask(__name__)

receipts = []

@app.route('/receipt', methods=['POST'])
def create_receipt():
    data = request.get_json()
    user = data.get('user')
    order_id = data.get('order_id')
    amount = data.get('amount')
    receipt = {
        "receipt_id": len(receipts) + 1,
        "user": user,
        "order_id": order_id,
        "amount": amount
    }
    receipts.append(receipt)
    return jsonify(receipt), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5011)