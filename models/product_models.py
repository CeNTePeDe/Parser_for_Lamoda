from decimal import Decimal
from typing import Optional

from pydantic import AnyUrl, BaseModel


class CategoryModel(BaseModel):
    category: str


class ProductModel(BaseModel):
    name_product: str
    picture_link: Optional[AnyUrl] = None
    price: Decimal
    product_detail_link: AnyUrl
    characteristic: dict
    description: str
    category: CategoryModel
