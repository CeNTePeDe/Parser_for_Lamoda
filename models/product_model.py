from pydantic import BaseModel, AnyUrl


class ProductModel(BaseModel):
    name_product: str
    picture_link: AnyUrl
    price: str
    product_detail_link: AnyUrl
    characteristic: dict
    description: str


