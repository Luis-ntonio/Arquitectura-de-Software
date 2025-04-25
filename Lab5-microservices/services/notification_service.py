import pika
import time
import json

def connect_to_rabbitmq():
    """
    Intenta conectarse a RabbitMQ con reintentos en caso de fallo.
    """
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
            return connection
        except pika.exceptions.AMQPConnectionError:
            print(" [!] RabbitMQ not ready, retrying in 3 seconds...")
            time.sleep(3)

def consume_bulk_purchases():
    """
    Consume mensajes de la cola 'bulk_purchases' y procesa cada evento.
    """
    connection = connect_to_rabbitmq()
    channel = connection.channel()
    channel.queue_declare(queue='bulk_purchases')

    def callback(ch, method, properties, body):
        print(f" [x] Received event: {body}")
        try:
            # Procesar el mensaje recibido
            event = json.loads(body)
            order_id = event.get("order_id")
            if order_id:
                notification_producer(order_id)
            else:
                print(" [!] Event does not contain 'order_id'")
        except json.JSONDecodeError:
            print(" [!] Failed to decode message as JSON")

    channel.basic_consume(queue='bulk_purchases', on_message_callback=callback, auto_ack=True)
    print(" [*] Waiting for messages in 'bulk_purchases' queue...")
    channel.start_consuming()

def notification_producer(order_id):
    """
    Produce un mensaje en la cola 'reports' indicando que la notificación ha llegado.
    """
    connection = connect_to_rabbitmq()
    channel = connection.channel()
    channel.queue_declare(queue='reports')

    event = {
        "event": "notification_arrived",
        "order_id": order_id
    }

    channel.basic_publish(exchange='', routing_key='reports', body=json.dumps(event))
    print(f" [x] Notification sent for order {order_id}")

    connection.close()

if __name__ == '__main__':
    consume_bulk_purchases()