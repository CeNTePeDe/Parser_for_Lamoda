from typing import Optional

from pydantic import BaseModel, AnyUrl


class ProductModel(BaseModel):
    name_product: str
    picture_link: AnyUrl
    price: str
    product_detail_link: AnyUrl
    description: str
    characteristic: Optional[dict]


class UrlSchema(BaseModel):
    url: AnyUrl

