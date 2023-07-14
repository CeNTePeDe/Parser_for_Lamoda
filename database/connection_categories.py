import logging
from typing import Optional

from pymongo.collection import Collection

from config.settings import db
from core.base_class import AbstractDAO
from models.product_models import CategoryModel

logger = logging.getLogger(__name__)



class CategoryDAO(AbstractDAO):
    collection: Collection

    def __init__(self, collection: str):
        self.collection: Collection = db[collection]
        super().__init__(self.collection)

    def get_item(self, category: str) -> Optional[CategoryModel]:
        category = self.collection.find_one({"category": category})
        if category is None:
            return None
        return CategoryModel(**category)

    def create_item(self, category: CategoryModel) -> CategoryModel:
        category_dict = category.dict()
        category = self.collection.find_one({"category": category_dict["category"]})
        if category is not None:
            logger.info(f"category id {category['_id']}")
            return CategoryModel(**category)

        logger.info(f"category look like this {category_dict}")
        category = self.collection.insert_one(category_dict)
        logger.info(f"category inserted {category.inserted_id}")
        category_model = self.collection.find_one({"_id": category.inserted_id})
        return CategoryModel(**category_model)

    def get_all_items(self) -> list[CategoryModel]:
        collection = self.collection.find()
        list_collection = [CategoryModel(**item) for item in collection]
        return list_collection

    def update_item(self, category_name: str, category: CategoryModel) -> Optional[int]:
        category_updated = self.collection.update_one(
            {"category": category_name}, {"$set": category.dict()}
        )
        if category_updated is None:
            return None
        return category_updated.modified_count

    def delete_item(self, category: str) -> int:
        result = self.collection.delete_one({"category": {"$eq": category}})
        return result.deleted_count
