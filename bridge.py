# bridge.py
import pymongo
import pika
import sys
import time
from pymongo import MongoClient
from rmq_params.py import *
from bluetooth import *

# rabbitMQHostName = sys.argv[2]

server_sock = BluetoothSocket(RFCOMM)
server_sock.bind(("", PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

advertise_service(server_sock, "SampleServer",
                  service_id=uuid,
                  service_classes=[uuid, SERIAL_PORT_CLASS],
                  profiles=[SERIAL_PORT_PROFILE],
#                 protocols = [ OBEX_UUID ]
                  )

print("Waiting for connection on RFCOMM channel %d" % port)

client_sock, client_info = server_sock.accept()
print("Accepted connection from ", client_info)

# Connect host and port
client = MongoClient('localhost', 27017)

# Access database
db = client['test-database']  # Same as warehouse?
collection = db['test-collection']
posts = db.posts

try:
    while True:
        data = client_sock.recv(1024)


        # Message ID
        ticks = time.time()
        MsgID = "05$" + str(ticks)
        print(MsgID)

        # Set up a post to send to the database
        post = {"Action": "Bob",
                "Place": "My first blog post!",
                "MsgID": ["mongodb", "python", "pymongo"],
                "Subject": "Chairs",
                "Message": str(MsgID)}

        # Insert into database
        post_id = posts.insert_one(post)

        # Retrieve from database
        print(posts.find_one({"Action": "Bob"}))

except IOError:
    pass

print("disconnected")

client_sock.close()
server_sock.close()
print("all done")

