import asyncio
import logging

from pydantic import AnyUrl
from pymongo import MongoClient
from pymongo.collection import Collection

from parsing_function.parse_product import gather_data
from schema.schemas import serializer_products_by_url

logger = logging.getLogger(__name__)


class ProductDAO:
    collection: Collection

    def __init__(self):
        self.client = MongoClient("mongodb://user:1111@mongo:27017")
        self.db = self.client["product_db"]
        self.collection = self.db["products"]

    def insert_many_products(self, url: AnyUrl) -> None:
        logger.info("run insert function")
        products = asyncio.run(gather_data(url))
        for product in products:
            self.collection.update_one({'url': url}, {'$push': {'products': product}}, upsert=True)
        logger.info(f"data_structure {products}")

    def get_all_products(self, url: AnyUrl) -> dict:
        products = self.collection.find({"url": url})
        for item in products:
            logger.info(f"products {item}")
            product_item = serializer_products_by_url(item)
            return product_item

