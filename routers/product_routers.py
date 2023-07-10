import asyncio
import logging

from bson import ObjectId
from fastapi import APIRouter, HTTPException, status
from pydantic import AnyUrl

from database import CategoryDAO, ProductDAO
from models.product_models import CategoryModel, ProductModel
from parsers.parse_product import gather_data

logger = logging.getLogger(__name__)

product_routers = APIRouter()
product_dao = ProductDAO()
category_dao = CategoryDAO()


@product_routers.post("/parser", status_code=status.HTTP_201_CREATED)
def post_products(url: AnyUrl) -> None:
    logger.info("get url")
    products = asyncio.run(gather_data(url))
    category = CategoryModel(category=url.split("/")[-2])
    for product in products:
        category_item = category_dao.create_item(category)
        product_dao.create_item(ProductModel(**product, category=category_item))
        logger.info(f"product is {product}")


@product_routers.get("/", status_code=status.HTTP_200_OK)
async def get_products() -> list[ProductModel]:
    return product_dao.get_all_items()


@product_routers.get("/product", status_code=status.HTTP_200_OK)
async def get_product(product_id: str) -> ProductModel:
    if not ObjectId.is_valid(product_id):
        raise HTTPException(status_code=400, detail="Invalid product_id")
    return product_dao.get_item(product_id)


@product_routers.post("/", status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductModel) -> ProductModel:
    logger.info("product create is started")
    category = product.category
    category_dao.create_item(category)
    product = product_dao.create_item(product)
    logger.info("product is created")
    return product


@product_routers.put("/", status_code=status.HTTP_200_OK)
async def update_product(product_id: str, product: ProductModel) -> int:
    if not ObjectId.is_valid(product_id):
        raise HTTPException(status_code=400, detail="Invalid product id")
    new_product = product_dao.update_item(product_id, product)
    return new_product


@product_routers.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: str) -> None:
    if not ObjectId.is_valid(product_id):
        raise HTTPException(status_code=400, detail="Invalid product id")
    product_dao.delete_item(product_id)
    logger.info("product is deleted")
