import logging

from bson import ObjectId
from fastapi import APIRouter, HTTPException, status

from database import CategoryDAO
from models.product_models import CategoryModel

logger = logging.getLogger(__name__)

category_routers = APIRouter()
category_dao = CategoryDAO()


@category_routers.get("/", status_code=status.HTTP_200_OK)
async def get_categories() -> list[CategoryModel]:
    return category_dao.get_all_item()


@category_routers.get("/category", status_code=status.HTTP_200_OK)
async def get_category(category_id: str) -> CategoryModel:
    if not ObjectId.is_valid(category_id):
        raise HTTPException(status_code=400, detail="Invalid category id")
    return category_dao.get_item(category_id)


@category_routers.put("/{category_id}", status_code=status.HTTP_200_OK)
async def update_category(category_id: str, category: CategoryModel) -> int:
    if not ObjectId.is_valid(category_id):
        raise HTTPException(status_code=400, detail="Invalid category id")
    new_category = category_dao.update_item(category_id, category)
    return new_category


@category_routers.post("/", status_code=status.HTTP_201_CREATED)
async def create_category(category: CategoryModel) -> CategoryModel:
    return category_dao.create_item(category)


@category_routers.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(category_id: str) -> None:
    if not ObjectId.is_valid(category_id):
        raise HTTPException(status_code=400, detail="Invalid category id")
    category_dao.delete_item(category_id)
    logger.info("category is deleted")
