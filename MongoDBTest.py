import pymongo
from pymongo import MongoClient
import time

# Create mongo client with default host and port
# client = MongoClient()
# Connect host and port
client = MongoClient('localhost', 27017)
# Access database
db = client['test-database']    # Same as warehouse?
collection = db['test-collection']
posts = db.posts

# Message ID
ticks = time.time()
MsgID = "05$" + str(ticks)
print (MsgID)

# Set up a post to send to the database
post = {"Action": "Bob",
        "Place": "My first blog post!",
        "MsgID": ["mongodb", "python", "pymongo"],
        "Subject": "Chairs",
        "Message": str(MsgID)}

# Insert into database
post_id = posts.insert_one(post)

# Retrieve from database
print(posts.find_one({"Action" : "Bob"}))

