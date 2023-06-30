import asyncio
import logging

from bson import ObjectId
from fastapi import APIRouter, HTTPException, status
from pydantic import AnyUrl

from database import CategoryDAO, ProductDAO
from models.product_models import CategoryModel, ProductModel
from parsers.parse_product import gather_data
from schemas.schemas import serialize_list_of_products, serialize_product

logger = logging.getLogger(__name__)

product_routers = APIRouter()
product_dao = ProductDAO()
category_dao = CategoryDAO()


@product_routers.post("/parser", status_code=status.HTTP_201_CREATED)
def post_products(url: AnyUrl):
    logger.info("get url")
    products = asyncio.run(gather_data(url))
    category = CategoryModel(category=url.split("/")[-2])
    logger.info(f"id look like {id}")
    for product in products:
        product["category"] = category_dao.create_item(category)
        product_dao.create_item(product)
        logger.info(f"product is {product}")


@product_routers.get("/", status_code=status.HTTP_200_OK)
async def get_products():
    products = product_dao.get_all_item()
    return serialize_list_of_products(products)


@product_routers.get("/product", status_code=status.HTTP_200_OK)
async def get_product(product_id: str) -> dict:
    product = product_dao.get_item(product_id)
    return serialize_product(product)


@product_routers.post("/", status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductModel):
    logger.info("product create is started")
    category = product.category
    category_dao.create_item(category)
    product = product_dao.create_item(product.dict())
    logger.info("product is created")
    return product


@product_routers.put("/", status_code=status.HTTP_200_OK)
async def update_product(product_id: str, product: ProductModel):
    if not ObjectId.is_valid(product_id):
        raise HTTPException(status_code=400, detail="Invalid category id")
    new_product = product_dao.update_item(product_id, product)
    return new_product


@product_routers.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: str) -> None:
    product_dao.delete_item(product_id)
    logger.info("product is deleted")
