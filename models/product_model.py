from pydantic import BaseModel, Field, HttpUrl


class Product(BaseModel):
    name_product: str = Field()
    picture_link: HttpUrl
    price: float = Field()
    product_detail_link: HttpUrl
    description: dict


    class Config:
        schema_extra = {
            "example": {
                "name_product": "example",
                "picture_link": "https://www.example.by",
                "price": 12345.0,
                "product_detail_link": "https://www.example.by",
                "description": {}
            }
        }
