import os

from pymongo import MongoClient

client = MongoClient(os.environ["MONGODB_URL"])

db = client["product_db"]

collection = db["collection"]