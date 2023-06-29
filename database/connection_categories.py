import logging

from pymongo import MongoClient
from pymongo.collection import Collection

from core.base_class import AbstractDAO

logger = logging.getLogger(__name__)
CLIENT = MongoClient("mongodb://user:1111@mongo:27017")
DB = CLIENT["product_db"]


class CategoryDAO(AbstractDAO):
    collection: Collection

    def __init__(self):
        self.collection = DB["category"]

    def create(self, category_dict: dict):
        category = self.collection.find_one({"category": category_dict["category"]})
        if category is not None:
            logger.info(f"category id {category['_id']}")
            return category["_id"]
        else:
            logger.info(f"category look like this {category_dict}")
            category = self.collection.insert_one(category_dict)
            logger.info(f"category inserted {category.inserted_id}")
            return category.inserted_id

    def get(self):
        categories = list(self.collection.find())
        logger.info(f"all categories {categories}")
        return categories

    def update(self, category_old_name, category_new_name):
        category = {"category": category_old_name}
        result = self.collection.update_many(
            category, {"$set": {"category": category_new_name}}
        )
        if result.modified_count > 0:
            return {"message": "Update document"}
        else:
            return {"message": "Document not found"}

    def delete(self, category_name):
        category = {"category": category_name}
        result = self.collection.delete_many(category)
        return {"deleted": result.deleted_count}
