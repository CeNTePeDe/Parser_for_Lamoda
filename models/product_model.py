from pydantic import AnyUrl, BaseModel


class ProductModel(BaseModel):
    name_product: str
    picture_link: AnyUrl
    price: float
    product_detail_link: AnyUrl
    characteristic: dict
    description: str


class UrlModel(BaseModel):
    url: AnyUrl
    products: list[ProductModel]
