# Listen for events/messages

#!/usr/bin/env python
import pika, sys, os

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='orders')

    def callback(ch, method, properties, body):
        print(f" [x] Received event: {body}")

    channel.basic_consume(queue='orders', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for events. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)