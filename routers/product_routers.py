import asyncio
import logging

from fastapi import APIRouter, status
from pydantic import AnyUrl

from database import CategoryDAO, ProductDAO
from models.product_models import ProductModel
from parsers.parse_product import gather_data
from schemas.schemas import serialize_list_of_products

logger = logging.getLogger(__name__)

product_routers = APIRouter()
product_dao = ProductDAO()
category_dao = CategoryDAO()


@product_routers.post("/parser", status_code=status.HTTP_201_CREATED)
def post_products(url: AnyUrl):
    logger.info("get url")
    products = asyncio.run(gather_data(url))
    category_dict = {"category": url.split("/")[-2]}
    logger.info(f"id look like {id}")
    for product in products:
        product["category"] = category_dao.create_category(category_dict)
        product_dao.create_product(product)
        logger.info(f"product is {product}")


@product_routers.get("/", status_code=status.HTTP_200_OK)
async def get_products():
    products = product_dao.get_products()
    return serialize_list_of_products(products)


@product_routers.post("/", status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductModel):
    product_dict = dict(product)
    category_dict = dict(product_dict.pop("category"))
    id_category = category_dao.create_category(category_dict)
    product_dict["category"] = id_category
    product_dao.create_product(product_dict)
    logger.info("products created")


@product_routers.put("/", status_code=status.HTTP_200_OK)
async def update_product_price(_id: str, new_price: float):
    product_dao.update_product(_id, new_price)
    return {"message": "product is updated"}


@product_routers.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_products(_id) -> None:
    product_dao.delete_products(_id)
