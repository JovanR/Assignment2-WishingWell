# bridge.py
import pymongo
import pika
import sys
import time
import bluetooth
from pymongo import MongoClient
from rmq_params import *
from bluetooth import *



# rabbitMQHostName = sys.argv[2]

# Bluetooth initialization
server_sock = bluetooth.BluetoothSocket(RFCOMM)
server_sock.bind(("", PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

# wait for a connection
advertise_service(server_sock, "SampleServer",
                  service_id=uuid,
                  service_classes=[uuid, SERIAL_PORT_CLASS],
                  profiles=[SERIAL_PORT_PROFILE],
#                 protocols = [ OBEX_UUID ]
                  )
print("Waiting for connection on RFCOMM channel %d" % port)

# Connect with device
client_sock, client_info = server_sock.accept()
print("Accepted connection from ", client_info)

# MongoDB Initializations: Connect host and port
client = MongoClient('localhost', 27017)

# Access database
dbName = 'test-database'
db = client[dbName]  # Same as warehouse?
collectionName = 'test-collection'
collection = db[collectionName]
posts = db.posts

# Speak back to bluetooth
client_sock.send("Available queues: " + '\n')
for queue in rmq_params['queues']:
    client_sock.send(queue +'\n')

try:
    while True:
        # Receive from bluetooth connection
        data = client_sock.recv(1024)
        # Parse trash from data
        data = str(data).split("'")
        data = data[1].split(':')
        
        # Produce
        if data[0] == 'p':
            command = data[1].split('"')
            queueName = command[0].replace(" ","")
            messageText = command[1]
            print("queueName p:", queueName)
            # Message ID
            ticks = time.time()
            MsgID = "05$" + str(ticks)
            
            # Set up a post to send to the database
            post = {"Action": data[0],
                    "Place": "My first blog post!",
                    "MsgID": MsgID,
                    "Subject": queueName,
                    "Message": messageText}
        
            # Insert into database
            posts.insert(post)
            
            """""
            channel.basic_publish(exchange='Squires',
                                  routing_key='wishes',
                                  body='I wish I remembered their name')
            """
        # Consume
        elif data[0] == 'c':
            queueName = data[1]
            # Parse trash from queueName
            queueName = queueName.split("\\")
            queueName = queueName[0]
            queueName = queueName.replace(" ","")
            print("queueName: ", queueName)
            # Retrieve from database
            print(posts.find_one({"Subject": "food"}))
        
        # History
        elif data[0] == 'h':
            queueName = data[1]
        

except IOError:
    pass

print("disconnected")

client_sock.close()
server_sock.close()
print("all done")

