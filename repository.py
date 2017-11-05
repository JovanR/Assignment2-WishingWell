#repository.py
from rmq_params import *
import sys
import pika

# 10 for GPIO.BOARD or 11 for GPIO.BCM
##gpioMode = sys.argv[2]
##redPin = sys.argv[4]
##greenPin = sys.argv[6]
##bluePin = sys.argv[8]

# RabbitMQ initializations
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange=rmq_params['exchange'],
                         exchange_type='direct')

# set up loop to iterate through and bind all queues to the exchange
for queue in rmq_params['queues']:
    channel.queue_declare(queue, exclusive=True)
    channel.queue_purge(queue)
    channel.queue_unbind(exchange=rmq_params['exchange'],
                         queue=queue)
    channel.queue_bind(exchange=rmq_params['exchange'],
                       queue=queue
                       #routing_key=queue
                       )

#also bind the status queue to the exchange
channel.queue_declare(rmq_params['status_queue'], exclusive=True)
channel.queue_purge(rmq_params['status_queue'])
channel.queue_unbind(exchange=rmq_params['exchange'],
                     queue=rmq_params['status_queue'])
channel.queue_bind(exchange=rmq_params['exchange'],
                   queue=rmq_params['status_queue']
                   #routing_key=queue
                   )

#also bind the master queue to the exchange
channel.queue_declare(rmq_params['master_queue'], exclusive=True)
channel.queue_purge(rmq_params['master_queue'])
channel.queue_unbind(exchange=rmq_params['exchange'],
                     queue=rmq_params['master_queue'])
channel.queue_bind(exchange=rmq_params['exchange'],
                   queue=rmq_params['master_queue']
                   #routing_key=queue
                   )
    
# set up loop to iterate through and bind all queues to the master queue as well
for queue in rmq_params['queues']:
    channel.queue_unbind(exchange=rmq_params['exchange'],
                         queue=rmq_params['master_queue'],
                         routing_key=queue)
    channel.queue_bind(exchange=rmq_params['exchange'],
                       queue=rmq_params['master_queue'],
                       routing_key=queue)
    
#also bind the status queue to the master queue
channel.queue_unbind(exchange=rmq_params['exchange'],
                     queue=rmq_params['master_queue'],
                     routing_key=rmq_params['status_queue'])
channel.queue_bind(exchange=rmq_params['exchange'],
                   queue=rmq_params['master_queue'],
                   routing_key=rmq_params['status_queue'])

# CHECK THIS IF PRINTING RIGHT!
def callback(ch, method, properties, body):
    print("%r:%r" % (method.routing_key, body))
    # JOVAN DO STUFF HERE
    
channel.basic_consume(callback,
                      queue=rmq_params['master_queue'],
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
print("[Checkpoint 02] Consuming messages from", rmq_params['master_queue'], " queue")

# DO LAST TWO STEPS!