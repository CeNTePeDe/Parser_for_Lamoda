import asyncio
import logging

from fastapi import APIRouter, Depends, status
from fastapi_filter import FilterDepends
from pydantic import AnyUrl

from core.filter import UrlProductFilter
from data_base.database import ProductDAO
from parsing_function.parse_product import gather_data

logger = logging.getLogger(__name__)

routers = APIRouter()
product_dao = ProductDAO()


@routers.post("/", status_code=status.HTTP_201_CREATED)
def post_products(url: AnyUrl) -> list[dict]:
    logger.info("get url")
    products = asyncio.run(gather_data(url))
    product_dao.update_products(url, products)
    return product_dao.get_products(url)


@routers.get("/", status_code=status.HTTP_200_OK)
async def get_products(
    product_filter: UrlProductFilter = FilterDepends(UrlProductFilter),
):
    query = product_filter.filter(product_dao.get_collection)
    return query


@routers.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_collection(url: AnyUrl):
    product_dao.delete_products(url)
    return {"message": "Document was deleted"}
