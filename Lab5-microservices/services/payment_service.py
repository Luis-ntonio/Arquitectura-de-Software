# simulate payment processing

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/payment', methods=['POST'])
def payment():
    return jsonify({"message": "Payment processed"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)