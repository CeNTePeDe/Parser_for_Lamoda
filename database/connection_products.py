import logging
from typing import Any, Mapping

from bson import ObjectId
from pymongo.collection import Collection
from pymongo.cursor import Cursor

from core.base_class import AbstractDAO
from core.constant_variables import db
from models.product_models import ProductModel

logger = logging.getLogger(__name__)


class ProductDAO(AbstractDAO):
    collection: Collection
    name_collection = "products"

    def __init__(self):
        self.collection = db["products"]
        super().__init__(self.collection)

    def get_all_item(self) -> Cursor:
        return self.collection.find()

    def get_item(self, product_id: str) -> Mapping[str, Any]:
        prod_id = ObjectId(product_id)
        product = self.collection.find_one({"_id": {"$eq": prod_id}})
        return product

    def create_item(self, product: Any) -> ObjectId:
        logger.info("created_product method is started")
        price_old = str(product.pop("price"))
        product["price"] = str(price_old)
        product = self.collection.insert_one(product)
        return product.inserted_id

    def update_item(self, product_id: str, product: ProductModel) -> int:
        prod_id = ObjectId(product_id)
        product_update = self.collection.update_one(
            {"_id": prod_id}, {"$set": product.dict()}
        )
        return product_update.modified_count

    def delete_item(self, product_id: str) -> int:
        prod_id = ObjectId(product_id)
        deleted_product = self.collection.delete_one({"_id": {"$eq": prod_id}})
        return deleted_product.deleted_count
