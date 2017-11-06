#repository.py
from rmq_params import *
import sys
import pika

# VHost
creds = pika.PlainCredentials(rmq_params['username'],rmq_params['password'])
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost',
                                                               5672,
                                                               rmq_params['vhost'],
                                                               creds))
print("[Checkpoint 01] Connected to vhost '", rmq_params['vhost'], "'on RMQ server at 'localhost' at user '", rmq_params['username'],"'")

# RabbitMQ initializations
channel = connection.channel()

channel.exchange_declare(exchange=rmq_params['exchange'],
                         exchange_type='direct')

# set up loop to iterate through and bind all queues to the exchange
for queue in rmq_params['queues']:
    channel.queue_declare(queue)
    channel.queue_purge(queue)
    channel.queue_unbind(exchange=rmq_params['exchange'],
                         queue=queue)
    channel.queue_bind(exchange=rmq_params['exchange'],
                       queue=queue
                       #routing_key=queue
                       )

#also bind the status queue to the exchange
channel.queue_declare(rmq_params['status_queue'])
channel.queue_purge(rmq_params['status_queue'])
channel.queue_unbind(exchange=rmq_params['exchange'],
                     queue=rmq_params['status_queue'])
channel.queue_bind(exchange=rmq_params['exchange'],
                   queue=rmq_params['status_queue']
                   #routing_key=queue
                   )

#also bind the master queue to the exchange
channel.queue_declare(rmq_params['master_queue'])
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
    #print("%r:%r" % (method.routing_key, body))
    if method.routing_key == rmq_params['status_queue']:
        print("[Checkpoint l-01] Flashing LED to", str(body).split("'")[1])
    else:
        print("[Checkpoint 03] Consumed a message published with routing_key: '", method.routing_key, "'")
        print("[Checkpoint 04] Message:", str(body).split("'")[1])
    
channel.basic_consume(callback,
                      queue=rmq_params['master_queue'],
                      no_ack=True)

print("[Checkpoint 02] Consuming messages from '",rmq_params['master_queue'], "' queue")
channel.start_consuming()


# DO LAST TWO STEPS!