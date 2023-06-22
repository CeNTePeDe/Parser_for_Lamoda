from pymongo import MongoClient

from main import settings

client = MongoClient(settings.MONGO_URL)

db = client[settings.MONGODB_DB]

collection = db.get_collection(settings.PRODUCT_COLLECTION)

