# simulate notification processing

import pika

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='orders')

    def callback(ch, method, properties, body):
        print(f" [Notification] Sending notification for event: {body}")

    channel.basic_consume(queue='orders', on_message_callback=callback, auto_ack=True)
    print(' [*] Notification Service waiting for order events...')
    channel.start_consuming()

if __name__ == '__main__':
    main()