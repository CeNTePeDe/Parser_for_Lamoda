from pydantic import AnyUrl, BaseModel


class CategoryModel(BaseModel):
    category: str


class ProductModel(BaseModel):
    name_product: str
    picture_link: AnyUrl
    price: float
    product_detail_link: AnyUrl
    characteristic: dict
    description: str
    category: CategoryModel
