from flask import Flask, request, jsonify
import pika
import threading

app = Flask(__name__)

# In-memory storage for order aggregation
order_buffer = {}

# Lock for thread safety
lock = threading.Lock()

# Threshold for triggering a bulk purchase
ORDER_THRESHOLD = 10

def send_bulk_purchase_event(provider_id, orders):
    """Send a bulk purchase event to the provider service via RabbitMQ."""
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='bulk_purchases')
    event = {
        "event": "bulk_purchase",
        "provider_id": provider_id,
        "orders": orders
    }
    channel.basic_publish(exchange='', routing_key='bulk_purchases', body=str(event))
    connection.close()

@app.route('/aggregate_order', methods=['POST'])
def aggregate_order():
    """Handle incoming orders and aggregate them by provider."""
    data = request.get_json()
    provider_id = data.get('provider_id')
    product_id = data.get('product_id')
    quantity = data.get('quantity')

    if not provider_id or not product_id or not quantity:
        return jsonify({"error": "Missing order data"}), 400

    with lock:
        # Initialize the buffer for the provider if not present
        if provider_id not in order_buffer:
            order_buffer[provider_id] = []

        # Add the order to the buffer
        order_buffer[provider_id].append({"product_id": product_id, "quantity": quantity})

        # Check if the threshold is reached
        if len(order_buffer[provider_id]) >= ORDER_THRESHOLD:
            send_bulk_purchase_event(provider_id, order_buffer[provider_id])
            order_buffer[provider_id] = []  # Reset the buffer after triggering the event

    return jsonify({"message": "Order aggregated", "provider_id": provider_id}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5006)