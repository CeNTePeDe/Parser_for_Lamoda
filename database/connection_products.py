import logging

from bson import ObjectId
from pymongo import MongoClient
from pymongo.collection import Collection

from core.base_class import AbstractDAO

logger = logging.getLogger(__name__)
CLIENT = MongoClient("mongodb://user:1111@mongo:27017")
DB = CLIENT["product_db"]


class ProductDAO(AbstractDAO):
    collection: Collection

    def __init__(self):
        self.collection = DB["products"]

    def get(self):
        return self.collection.find()

    def create(self, product: dict):
        logger.info("created_method is started")
        self.collection.insert_one(product)
        logger.info("created method is finished")

    def update(self, _id: str, new_price: float) -> dict:
        product_with_old_price = self.collection.find_one({"_id": ObjectId(_id)})
        updated_product = self.collection.update_many(
            product_with_old_price, {"$set": {"price": new_price}}
        )
        if updated_product.modified_count > 0:
            return {"message": "Update document"}
        else:
            return {"message": "Document not found"}

    def delete(self, id: ObjectId):
        deleted_product = self.collection.delete_one({"_id": id})
        if deleted_product.deleted_count == 1:
            return {"message": "Product is deleted"}
        else:
            return {"message": "Document not found"}
