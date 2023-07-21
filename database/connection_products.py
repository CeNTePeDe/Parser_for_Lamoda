import logging
from typing import Optional

from pymongo.collection import Collection

from config.settings import db
from core.base_class import AbstractDAO
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

    def get_items_by_category(self, category_name: str) -> Optional[list[ProductModel]]:
        products = self.collection.find({"category": {"category": category_name}})
        if products is None:
            return None
        return [ProductModel(**product) for product in products]

    def create_item(self, product: ProductModel) -> ProductModel:
        logger.info("created_product method is started")
        product_dict = product.dict()
        price_old = str(product_dict.pop("price"))
        product_dict["price"] = str(price_old)
        check_product = self.collection.find_one(
            {"product_id": product_dict["product_id"]}
        )
        if check_product is None:
            logger.info(f"the second product dict is {product_dict}")
            product = self.collection.insert_one(product_dict)
            logger.info("created product")
            new_product = self.collection.find_one({"_id": product.inserted_id})
            return ProductModel(**new_product)
        logger.info("updated product")
        self.collection.update_one(
            {"product_id": product_dict["product_id"]}, {"$set": product_dict}
        )
        updated_product = self.collection.find_one(
            {"product_id": product_dict["product_id"]}
        )
        return ProductModel(**updated_product)

    def update_item(self, product_id: str, product: ProductModel) -> ProductModel:
        self.collection.update_one({"product_id": product_id}, {"$set": product.dict()})
        product_updated = self.collection.find_one(
            {"product_id": product.dict()["product_id"]}
        )
        return ProductModel(**product_updated)

    def delete_item(self, product_id: str) -> int:
        deleted_product = self.collection.delete_one(
            {"product_id": {"$eq": product_id}}
        )
        return deleted_product.deleted_count
