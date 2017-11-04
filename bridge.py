# bridge.py
import pymongo
import pika
import sys
from pymongo import MongoClient
from rmq_params.py import *
from bluetooth import *



# Create mongo client with default host and port
# client = MongoClient()
# Connect host and port
# client = MongoClient('localhost', 27017)
# Access database

# rabbitMQHostName = sys.argv[2]