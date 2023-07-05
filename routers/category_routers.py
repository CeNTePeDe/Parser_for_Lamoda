import logging

from fastapi import APIRouter, status

from database import CategoryDAO
from models.product_models import CategoryModel

logger = logging.getLogger(__name__)

category_routers = APIRouter()
category_dao = CategoryDAO(collection="categories")


@category_routers.get("/", status_code=status.HTTP_200_OK)
async def get_categories() -> list[CategoryModel]:
    return category_dao.get_all_item()


@category_routers.get("/{category}", status_code=status.HTTP_200_OK)
async def get_category(category: str) -> CategoryModel:
    return category_dao.get_item(category)


@category_routers.put("/{category_name}", status_code=status.HTTP_200_OK)
async def update_category(category_name: str, category: CategoryModel) -> int:
    new_category = category_dao.update_item(category_name, category)
    return new_category


@category_routers.post("/", status_code=status.HTTP_201_CREATED)
async def create_category(category: CategoryModel) -> CategoryModel:
    return category_dao.create_item(category)


@category_routers.delete("/{category}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(category: str) -> None:
    category_dao.delete_item(category)
    logger.info("category is deleted")
