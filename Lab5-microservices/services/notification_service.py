# simulate notification processing

import pika
import time

def connect_to_rabbitmq():
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
            return connection
        except pika.exceptions.AMQPConnectionError:
            print(" [!] RabbitMQ not ready, retrying in 3 seconds...")
            time.sleep(3)

def main():
    connection = connect_to_rabbitmq()
    channel = connection.channel()
    channel.queue_declare(queue='orders')

    def callback(ch, method, properties, body):
        print(f" [x] Received event: {body}")

    channel.basic_consume(queue='orders', on_message_callback=callback, auto_ack=True)
    print(' [*] Waiting for events. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    main()
    