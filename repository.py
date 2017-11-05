#repository.py
import rmq_params.py
import sys
import pika

# 10 for GPIO.BOARD or 11 for GPIO.BCM
gpioMode = sys.argv[2]
redPin = sys.argv[4]
greenPin = sys.argv[6]
bluePin = sys.argv[8]


# RabbitMQ initializations
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='Squires',
                         exchange_type='direct')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

# set up loop to iterate through and bind all queues to one routing key
while queue in queues:
    channel.queue_bind(exchange= rmq_params['exchange'],
                   queue=rmq_params['master_queue'],
                   routing_key='wishes')


def callback(ch, method, properties, body):
    print("%r:%r" % (method.routing_key, body))
channel.basic_consume(callback,
                      queue=rmq_params['master_queue'],
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming() # CONSUME FROM MASTER