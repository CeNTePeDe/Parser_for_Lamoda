from pymongo import MongoClient

from settings import environment

client = MongoClient(environment.settings.MONGO_URL)

db = client[environment.settings.MONGODB_DB]

collection = db.get_collection(environment.settings.PRODUCT_COLLECTION)

