import logging

from fastapi import APIRouter, status

from database import CategoryDAO
from models.product_models import CategoryModel
from schemas.schemas import serialize_list_of_category

logger = logging.getLogger(__name__)

category_routers = APIRouter()
category_dao = CategoryDAO()


@category_routers.get("/", status_code=status.HTTP_200_OK)
async def get_categories() -> list[dict]:
    categories = category_dao.get_categories()
    return serialize_list_of_category(categories)


@category_routers.post("/", status_code=status.HTTP_201_CREATED)
async def create_category(category: CategoryModel) -> dict:
    category_dict = category.dict()
    category_dao.create_category(category_dict)
    return {"message": "category is created"}


@category_routers.put("/", status_code=status.HTTP_201_CREATED)
async def update_category(category_old: str, category_new: str) -> dict:
    category_dao.update_category(category_old, category_new)
    logger.info("category is updated")
    return {"message": "category is updated"}


@category_routers.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(category_name: str) -> None:
    category_dao.delete_category(category_name)
    logger.info("category is deleted")
