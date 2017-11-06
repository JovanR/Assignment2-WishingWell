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
rabbitMQHostName = '172.29.81.26'

# MongoDB Initializations: Connect host and port
host = 'localhost'
client = MongoClient(host, 27017)

# Access database
dbName = rmq_params['exchange']
db = client[dbName]  # Same as warehouse?
print("[Checkpoint 01] Connected to database '", dbName, "' on MongoDB server at '", host,"'")
for collection in rmq_params['queues']:
    db[collection].drop()
#Vhost
creds= pika.PlainCredentials(rmq_params['username'],rmq_params['password'])
connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitMQHostName,
                                                               port=5672,
                                                               virtual_host=rmq_params['vhost'],
                                                               credentials=creds))
# Channel initialization
channel = connection.channel()

print("[Checkpoint 02] Connected to vhost '", rmq_params['vhost'], "'on RMQ server at '", host, "' at user '", rmq_params['username'],"'")
# MongoDB collection
# COLLECION NAME SHOULD BE QUEUES
##for queue in rmq_params['queues']:
##    collectionName = queue
##    collection = db[collectionName]
##posts = db.posts
            
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
# Publish/Produce to status queue
channel.basic_publish(exchange=rmq_params['exchange'],
                               routing_key=rmq_params['status_queue'],
                               body="green")
print("[Checkpoint p-01] Published message with routing_key: ", rmq_params['status_queue'])
print("[Checkpoint p-02] Message: green")

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
            if queueName not in rmq_params['queues']:
                print("ERROR: ", queueName," is not in list of queues")
                sys.exit(1)
            # Message ID
            ticks = time.time()
            MsgID = "05$" + str(ticks)
            
            # Set up a post to send to the database
            post = {"Action": data[0],
                    "Place": dbName,
                    "MsgID": MsgID,
                    "Subject": queueName,
                    "Message": messageText}
            
            # Publish/Produce to status queue
            channel.basic_publish(exchange=rmq_params['exchange'],
                                  routing_key=rmq_params['status_queue'],
                                  body="purple")
            print("[Checkpoint p-01] Published message with routing_key: ", rmq_params['status_queue'])
            print("[Checkpoint p-02] Message: purple")
            
            # Publish/Produce via RabbitMQ to exchange
            channel.basic_publish(exchange=rmq_params['exchange'],
                                  routing_key=queueName,
                                  body=messageText)
            print("[Checkpoint p-01] Published message with routing_key: ", queueName)
            print("[Checkpoint p-02] Message: ", messageText)
##            
            # Insert into database
            db[queueName].insert(post)
            print("[Checkpoint m-01] Stored document in collection '", queueName, "' in MongoDB database '", dbName, "'")
            print("[Checkpoint m-02] Document: ", post)

        # Consume
        elif data[0] == 'c':
            queueName = data[1]
            # Parse trash from queueName
            queueName = queueName.split("\\")
            queueName = queueName[0]
            queueName = queueName.replace(" ","")
            messageText = ""
            
            if queueName not in rmq_params['queues']:
                print("ERROR: ", queueName," is not in list of queues")
                sys.exit(1)
            
            # Message ID
            ticks = time.time()
            MsgID = "05$" + str(ticks)
            
            # Set up a post to send to the database
            post = {"Action": data[0],
                    "Place": dbName,
                    "MsgID": MsgID,
                    "Subject": queueName,
                    "Message": messageText}
            
            db[queueName].insert(post)
            # Publish/Produce to status queue
            channel.basic_publish(exchange=rmq_params['exchange'],
                                  routing_key=rmq_params['status_queue'],
                                  body="yellow")
            print("[Checkpoint p-01] Published message with routing_key: ", rmq_params['status_queue'])
            print("[Checkpoint p-02] Message: yellow")
            

            method1, header1, messageText = channel.basic_get(queueName)
            if method1:
                channel.basic_ack(method1.delivery_tag)
            else:
                print("Error: ", queueName, " is empty")
                sys.exit(1)
            messageText = str(messageText).split("'")[1]

            print("[Checkpoint c-01] Consumed a message published with routing_key: '",queueName, "'")
            print("[Checkpoint c-02] Message:",messageText)
            print("[Checkpoint c-03] Sending to RFCOMM Bluetooth Client")
            
            print("[Checkpoint m-01] Stored document in collection '", queueName, "' in MongoDB database '", dbName, "'")
            print("[Checkpoint m-02] Document: ", post)
            # Retrieve from database
            client_sock.send(str(messageText) + '\n')
        
        # History
        elif data[0] == 'h':
            count = 0
            queueName = data[1]
            # Parse trash from queueName
            queueName = queueName.split("\\")
            queueName = queueName[0]
            queueName = queueName.replace(" ","")
            
            if queueName not in rmq_params['queues']:
                print("ERROR: ", queueName," is not in list of queues")
                sys.exit(1)
            
            # Publish/Produce to status queue
            channel.basic_publish(exchange=rmq_params['exchange'],
                                  routing_key=rmq_params['status_queue'],
                                  body="blue")
            print("[Checkpoint p-01] Published message with routing_key: ", rmq_params['status_queue'])
            print("[Checkpoint p-02] Message: blue")
            
            # Print history
            print("[Checkpoint h-01] Printing history of Collection '" + queueName +"'in MongoDB database '" + dbName + "'")
            print("[Checkpoint h-02] Collection: ", queueName)
            for x in db[queueName].find():
                print("Document"+str(count)+":"+str(x))
                count = count + 1
        

except IOError:
    pass

# Publish/Produce to status queue
channel.basic_publish(exchange=rmq_params['exchange'],
                      routing_key=rmq_params['status_queue'],
                      body="red")
print("[Checkpoint p-01] Published message with routing_key: ", rmq_params['status_queue'])
print("[Checkpoint p-02] Message: red")
client_sock.close


