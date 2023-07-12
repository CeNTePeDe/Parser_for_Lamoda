import asyncio
import logging

from fastapi import APIRouter, HTTPException, status
from pydantic import AnyUrl

from database import CategoryDAO, ProductDAO
from models.product_models import CategoryModel, ProductModel
from parsers.parse_product import gather_data

logger = logging.getLogger(__name__)

product_routers = APIRouter()
product_dao = ProductDAO()
category_dao = CategoryDAO(collection="categories")


@product_routers.post("/parser", status_code=status.HTTP_201_CREATED)
def post_products(url: AnyUrl) -> dict:
    logger.info("get url")
    products = asyncio.run(gather_data(url))
    category = CategoryModel(category=url.split("/")[-2])
    for product in products:
        product_id = product["product_detail_link"].split("/")[-3]
        category_item = category_dao.create_item(category)
        product_dao.create_item(
            ProductModel(**product, category=category_item, product_id=product_id)
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
