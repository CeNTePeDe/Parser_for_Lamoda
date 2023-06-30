import logging
from typing import Any, Mapping

from bson import ObjectId
from pymongo.collection import Collection

from core.base_class import AbstractDAO
from core.constant_variables import db
from models.product_models import CategoryModel

logger = logging.getLogger(__name__)


class CategoryDAO(AbstractDAO):
    collection: Collection

    def __init__(self):
        self.collection = db["categories"]
        super().__init__(self.collection)

    def create_item(self, category: CategoryModel) -> ObjectId:
        category_dict = category.dict()
        category = self.collection.find_one({"category": category_dict["category"]})
        if category is not None:
            logger.info(f"category id {category['_id']}")
            return category["_id"]
        else:
            logger.info(f"category look like this {category_dict}")
            category = self.collection.insert_one(category_dict)
            logger.info(f"category inserted {category.inserted_id}")
            return category.inserted_id

    def get_all_item(self) -> Any:
        categories = self.collection.find()
        return categories

    def get_item(self, category_id: str) -> Mapping[str, Any]:
        cat_id = ObjectId(category_id)
        category = self.collection.find_one({"_id": {"$eq": cat_id}})
        return category

    def update_item(self, category_id: str, category: CategoryModel) -> int:
        cat_id = ObjectId(category_id)
        category_updated = self.collection.update_one(
            {"_id": cat_id}, {"$set": category.dict()}
        )
        return category_updated.modified_count

    def delete_item(self, category_id: str) -> int:
        category_id = ObjectId(category_id)
        result = self.collection.delete_one({"_id": {"$eq": category_id}})
        return result.deleted_count
