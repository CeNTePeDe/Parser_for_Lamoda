import logging

from fastapi import APIRouter, HTTPException, status

from database import CategoryDAO
from models.product_models import CategoryModel

logger = logging.getLogger(__name__)

category_routers = APIRouter()
category_dao = CategoryDAO(collection="categories")


@category_routers.get("/", status_code=status.HTTP_200_OK)
async def get_categories() -> list[CategoryModel]:
    return category_dao.get_all_items()


@category_routers.get("/{category}", status_code=status.HTTP_200_OK)
async def get_category(category: str) -> CategoryModel:
    if category_dao.get_item(category) is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category_dao.get_item(category)


@category_routers.put("/{category_name}", status_code=status.HTTP_200_OK)
async def update_category(category_name: str, category: CategoryModel) -> dict:
    if category_dao.update_item(category_name, category) == 0:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"message": "category is updated"}


@category_routers.post("/", status_code=status.HTTP_201_CREATED)
async def create_category(category: CategoryModel) -> CategoryModel:
    return category_dao.create_item(category)


@category_routers.delete("/{category}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(category: str) -> None:
    logger.info("category is deleted")
    if category_dao.delete_item(category) == 0:
        raise HTTPException(status_code=404, detail="Category not found")
