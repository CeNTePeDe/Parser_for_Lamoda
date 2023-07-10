import logging
from typing import Optional

from fastapi import HTTPException
from pymongo.collection import Collection

from core.base_class import AbstractDAO
from core.constant_variables import db
from models.product_models import ProductModel

logger = logging.getLogger(__name__)


class ProductDAO(AbstractDAO):
    collection: Collection

    def __init__(self):
        self.collection: Collection = db["products"]
        super().__init__(self.collection)

    def get_all_items(self) -> list[ProductModel]:
        collection = self.collection.find()
        list_collection = []
        for item in collection:
            product = ProductModel(**item)
            list_collection.append(product)

        return list_collection

    def get_item(self, product_id: str) -> Optional[ProductModel]:
        product = self.collection.find_one({"product_id": product_id})
        if product is None:
            return None
        return ProductModel(**product)

    def create_item(self, product: ProductModel) -> ProductModel:
        logger.info("created_product method is started")
        product_dict = product.dict()
        logger.info(f"product dict is {product_dict}")
        price_old = str(product_dict.pop("price"))
        product_dict["price"] = str(price_old)
        logger.info(f"the second product dict is {product_dict}")
        product = self.collection.insert_one(product_dict)
        return product.inserted_id

    def update_item(self, product_id: str, product: ProductModel) -> int:
        product_update = self.collection.update_one(
            {"product_id": product_id}, {"$set": product.dict()}
        )
        return product_update.modified_count

    def delete_item(self, product_id: str) -> int:
        deleted_product = self.collection.delete_one(
            {"product_id": {"$eq": product_id}}
        )
        return deleted_product.deleted_count
