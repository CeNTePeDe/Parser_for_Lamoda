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
def parse_func(url: AnyUrl):
    logger.info("get url")
    products = asyncio.run(gather_data(url))
    product_dao.insert_products(url, products)
    return product_dao.get_products(url)

