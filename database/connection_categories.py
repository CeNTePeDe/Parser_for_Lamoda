import logging

from bson import ObjectId
from pymongo.collection import Collection

from core.base_class import AbstractDAO
from core.constant_variables import get_db
from models.product_models import CategoryModel

logger = logging.getLogger(__name__)
db = get_db()


class CategoryDAO(AbstractDAO):
    collection: Collection

    def __init__(self):
        self.collection = db["categories"]
        super().__init__(self.collection)

    def get_item(self, category_id: str) -> CategoryModel:
        cat_id = ObjectId(category_id)
        category = self.collection.find_one({"_id": cat_id})
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
        return self.get_item(category.inserted_id)

    def get_all_items(self) -> list[CategoryModel]:
        collection = self.collection.find()
        list_collection = [CategoryModel(**item) for item in collection]
        return list_collection

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
