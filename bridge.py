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

# Channel initialization
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# MongoDB Initializations: Connect host and port
host = 'localhost'
client = MongoClient(host, 27017)

# Access database
dbName = rmq_params['exchange']
db = client[dbName]  # Same as warehouse?
print("[Checkpoint 01] Connected to database '", dbName, "' on MongoDB server at '", host,"'")
# MongoDB collection
# COLLECION NAME SHOULD BE QUEUES
collectionName = 'test-collection'
collection = db[collectionName]
posts = db.posts
            
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
print("[Checkpoint 03] Created RFCOMM Bluetooth socket on port", port)

# Connect with device
client_sock, client_info = server_sock.accept()
print("[Checkpoint 04] Accepted RFCOMM Bluetooth connection from ", client_info)

# Speak back to bluetooth
client_sock.send("Communicating on Exchange: "+ dbName + '\n')
client_sock.send("Available queues: " + '\n')
for queue in rmq_params['queues']:
    client_sock.send(queue +'\n')
print("[Checkpoint 05] Sending Exchange and Queue names")

try:
    while True:
        # Receive from bluetooth connection
        data = client_sock.recv(1024)
        print("[Checkpoint 06] Received RFCOMM Bluetooth data: ", data)
        # Parse trash from data
        data = str(data).split("'")
        data = data[1].split(':')
        
        # Produce
        if data[0] == 'p':
            command = data[1].split('"')
            queueName = command[0].replace(" ","")
            messageText = command[1]
                        
            # Message ID
            ticks = time.time()
            MsgID = "05$" + str(ticks)
            
            # Set up a post to send to the database
            post = {"Action": data[0],
                    "Place": "My first blog post!",
                    "MsgID": MsgID,
                    "Subject": queueName,
                    "Message": messageText}
            
            # Publish/Produce to status queue
            channel.basic_publish(exchange=rmq_params['exchange'],
                                  routing_key=rmq_params['status_queue'],
                                  body='purple')
            print("[Checkpoint p-01] Published message with routing_key: ", rmq_params['status_queue'])
            print("[Checkpoint p-02] Message: purple")
            
            # Publish/Produce via RabbitMQ to exchange
            channel.basic_publish(exchange=rmq_params['exchange'],
                                  routing_key=queueName,
                                  body=messageText)
            print("[Checkpoint p-01] Published message with routing_key: ", queueName)
            print("[Checkpoint p-02] Message: ", messageText)
            
            # Insert into database
            posts.insert(post)
            print("[Checkpoint m-01] Stored document in collection '", collectionName, "' in MongoDB database '", dbName, "'")
            print("[Checkpoint m-02] Document: ", post)

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

