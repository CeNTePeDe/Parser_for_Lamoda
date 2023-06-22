import logging

from fastapi import APIRouter, status
from pydantic import AnyUrl

from data_base.database import ProductDAO

logger = logging.getLogger(__name__)

routers = APIRouter()
product_dao = ProductDAO()


@routers.post("/parse", status_code=status.HTTP_200_OK)
def parse_func(url: AnyUrl):
    logger.info("get url")
    product_dao.insert_many_products(url)
    logger.info("collection is inserted")
    return product_dao.get_all_products(url)


