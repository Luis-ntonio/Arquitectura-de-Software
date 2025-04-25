# Sends events/messages

#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='orders')

channel.basic_publish(exchange='', routing_key='orders', body='{"event": "order_created", "order_id": 1}')
print(" [x] Sent 'order_created' event!")
connection.close()