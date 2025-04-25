# simulate order processing 

from flask import Flask, request, jsonify
import pika

app = Flask(__name__)

@app.route('/order', methods=['POST'])
def create_order():
    # Here you would save the order to DB, etc.
    # For demo, just send event to event bus
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='orders')
    channel.basic_publish(exchange='', routing_key='orders', body='{"event": "order_created", "order_id": 1}')
    connection.close()
    return jsonify({"message": "Order created and event sent"}), 201

if __name__ == '__main__':
    app.run(port=5003)