import logging

from bson import ObjectId
from pymongo.collection import Collection

from core.base_class import AbstractDAO
from core.constant_variables import db
from models.product_models import ProductModel

logger = logging.getLogger(__name__)


class ProductDAO(AbstractDAO):
    collection: Collection

    def __init__(self):
        self.collection = db["products"]
        super().__init__(self.collection)

    def get_all_item(self) -> list[ProductModel]:
        collection = self.collection.find()
        list_collection = []
        for item in collection:
            logger.info(f"item look like this {item}")
            product = ProductModel(**item)
            list_collection.append(product)

        return list_collection

    def get_item(self, product_id: str) -> ProductModel:
        prod_id = ObjectId(product_id)
        product = self.collection.find_one({"_id": {"$eq": prod_id}})
        return ProductModel(**product)

    def create_item(self, product: ProductModel) -> ProductModel:
        logger.info("created_product method is started")
        product_dict = product.dict()
        price_old = str(product_dict.pop("price"))
        product_dict["price"] = str(price_old)
        product = self.collection.insert_one(product_dict)
        return self.get_item(product.inserted_id)

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
