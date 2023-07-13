import json
import logging
from decimal import Decimal

from fastapi import APIRouter, HTTPException, status
from pydantic import AnyUrl

from database import CategoryDAO, ProductDAO
from kafka import KafkaConsumer
from kafka_producers.kafka_products import send_data_to_kafka_products
from models.product_models import CategoryModel, ProductModel

logger = logging.getLogger(__name__)

product_routers = APIRouter()
product_dao = ProductDAO()
category_dao = CategoryDAO(collection="categories")


@product_routers.post("/parser", status_code=status.HTTP_201_CREATED)
def post_products(url: AnyUrl) -> dict:
    from main import settings

    logger.info("get url")
    send_data_to_kafka_products(url)
    logger.info("retrieve data from kafka")
    products = KafkaConsumer(
        settings.TOPIC_PRODUCT,
        bootstrap_servers=settings.KAFKA_URL,
        auto_offset_reset=settings.AUTO_OFFSET_RESET,
        consumer_timeout_ms=settings.CONSUMER_TIMEOUT_MS,
    )
    category = CategoryModel(category=url.split("/")[-2])
    for product in products:
        product = json.loads(product.value)
        logger.info(f"product {type(product)}")
        product_id = product["product_detail_link"].split("/")[-3]
        price = product.pop("price")
        price = Decimal(price)
        category_item = category_dao.create_item(category)
        product_dao.create_item(
            ProductModel(
                **product, price=price, category=category_item, product_id=product_id
            )
        )
        logger.info(f"product is {product}")
    return {"message": "products are created"}


@product_routers.get("/", status_code=status.HTTP_200_OK)
async def get_products() -> list[ProductModel]:
    return product_dao.get_all_items()


@product_routers.get("/{product_id}", status_code=status.HTTP_200_OK)
async def get_product(product_id: str) -> ProductModel:
    product = product_dao.get_item(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@product_routers.post("/", status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductModel) -> dict:
    logger.info("product create is started")
    category = product.category
    category_dao.create_item(category)
    product = product_dao.create_item(product)
    logger.info("product is created")
    return {"message": "product is created"}


@product_routers.put("/{product_id}", status_code=status.HTTP_200_OK)
async def update_product(product_id: str, product: ProductModel) -> int:
    new_product = product_dao.update_item(product_id, product)
    if new_product == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return new_product


@product_routers.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: str) -> None:
    if product_dao.delete_item(product_id) == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    logger.info("product is deleted")
