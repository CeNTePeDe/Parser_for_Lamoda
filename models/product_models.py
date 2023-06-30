from decimal import Decimal

from pydantic import AnyUrl, BaseModel


class CategoryModel(BaseModel):
    category: str


class ProductModel(BaseModel):
    name_product: str
    picture_link: AnyUrl
    price: Decimal
    product_detail_link: AnyUrl
    characteristic: dict
    description: str
    category: CategoryModel
