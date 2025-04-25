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

def consume_reports():
    """
    Consume mensajes de la cola 'reports' y procesa cada evento.
    """
    connection = connect_to_rabbitmq()
    channel = connection.channel()
    channel.queue_declare(queue='reports')

    def callback(ch, method, properties, body):
        try:
            # Decodificar el mensaje recibido
            event = json.loads(body.decode('utf-8'))
            event_type = event.get("event")
            order_id = event.get("order_id")

            # Verificar si el evento es "notification_arrived"
            if event_type == "notification_arrived":
                print(f"Llegó tu pedido con el ID {order_id}")
            else:
                print(f" [!] Evento desconocido: {event_type}")
        except json.JSONDecodeError:
            print(" [!] Error al decodificar el mensaje como JSON")

    channel.basic_consume(queue='reports', on_message_callback=callback, auto_ack=True)
    print(" [*] Waiting for messages in 'reports' queue...")
    channel.start_consuming()

if __name__ == '__main__':
    consume_reports()