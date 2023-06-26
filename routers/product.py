import asyncio
import logging

from fastapi import APIRouter, status
from pydantic import AnyUrl

from data_base.database import ProductDAO
from parsing_function.parse_product import gather_data

logger = logging.getLogger(__name__)

routers = APIRouter()
product_dao = ProductDAO()


@routers.post("/parse", status_code=status.HTTP_200_OK)
def get_products(url: AnyUrl):
    logger.info("get url")
    products = asyncio.run(gather_data(url))
    product_dao.create_products(url, products)
    return product_dao.get_products(url)


@routers.get("/parse/filter", status_code=status.HTTP_200_OK)
def get_filter_products(url: AnyUrl, min_price: float, max_price: float):
    return product_dao.get_filter_products(url, min_price=min_price, max_price=max_price)


@routers.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def delete_collection(url: AnyUrl):
    product_dao.delete_products(url)
    return {"message": "Document was deleted"}
