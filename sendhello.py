#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='Squires',
                         exchange_type='direct')

channel.basic_publish(exchange='Squires',
                      routing_key='wishes',
                      body='I wish I remembered their name')

print(" [x] Sent 'I wish I remembered their name'")
connection.close()