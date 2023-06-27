import logging

from pydantic import AnyUrl
from pymongo import MongoClient
from pymongo.collection import Collection

from schema.schemas import (serialize_list_of_products,
                            serialize_products_with_url)

logger = logging.getLogger(__name__)


class ProductDAO:
    collection: Collection

    def __init__(self):
        self.client = MongoClient("mongodb://user:1111@mongo:27017")
        self.db = self.client["product_db"]
        self.collection = self.db["products"]

    def update_products(self, url: AnyUrl, products: list[dict]) -> None:
        logger.info("run insert function")
        for product in products:
            self.collection.update_one(
                {"url": url}, {"$push": {"products": product}}, upsert=True
            )
        logger.info(f"data_structure {products}")

    def get_products(self, url: AnyUrl) -> list[dict]:
        products_collection = self.collection.find({"url": url})[0]
        list_of_products = products_collection["products"]
        return list_of_products

    def get_collection(self):
        collection = self.collection.objects.all()
        logger.info(f"this is collection {collection}, type {type(collection)}")
        return collection

    def delete_products(self, url: AnyUrl) -> None:
        result = self.collection.delete_many({"url": url})
        logger.info(f"Deleted {result.deleted_count} documents")
