from pymongo import MongoClient

from config.dev import settings


client = MongoClient(settings.MONGO_URL)

db = client[settings.MONGODB_DB]

collection = db[settings.PRODUCT_COLLECTION]
