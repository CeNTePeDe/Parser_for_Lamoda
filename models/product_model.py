from pydantic import BaseModel, Field, HttpUrl


class Product(BaseModel):
    name: str = Field()
    link: HttpUrl
    price: float = Field()
    discription: dict = Field()

    class Config:
        schema_extra = {
            "example": {
                "name": "product_name",
                "link": "",
                "price": 12345.0,
                "description": {},
            }
        }
