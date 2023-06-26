import logging

from pydantic import AnyUrl
from pymongo import MongoClient
from pymongo.collection import Collection

from schema.schemas import serialize_products_with_url, serialize_list_of_products

logger = logging.getLogger(__name__)


class ProductDAO:
    collection: Collection

    def __init__(self):
        self.client = MongoClient("mongodb://user:1111@mongo:27017")
        self.db = self.client["product_db"]
        self.collection = self.db["products"]

    def create_products(self, url: AnyUrl, products: list[dict]) -> None:
        logger.info("run insert function")
        for product in products:
            self.collection.update_one({'url': url}, {'$push': {'products': product}}, upsert=True)
        logger.info(f"data_structure {products}")


    def get_products(self, url: AnyUrl) -> dict:
        products = self.collection.find({"url": url})
        for item in products:
            logger.info(f"products {item}")
            product_item = serialize_products_with_url(item)
            return product_item

    def get_filter_products(self, url: AnyUrl, min_price: float, max_price: float):
        products = self.collection.find({"url": url})
        for item in products:
            list_products = item.get("products")
            logger.info(f"list of products {list_products}")
            sorted_product_list = []
            for product_item in list_products:
                if min_price < float(product_item["price"].split()[0]) < max_price:
                    sorted_product_list.append(product_item)
                    logger.info(f"{sorted_product_list}")
            return serialize_list_of_products(sorted_product_list)

    def delete_products(self, url: AnyUrl):
        result = self.collection.delete_many({"url": url})
        logger.info(f"Deleted {result.deleted_count} documents")
