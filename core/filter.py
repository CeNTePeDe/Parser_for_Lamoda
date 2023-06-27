from typing import Optional

from fastapi_filter import FilterDepends, with_prefix
from fastapi_filter.contrib.mongoengine import Filter
from pydantic import AnyUrl

from models.product_model import ProductModel, UrlModel


class ProductFilter(Filter):
    price_lt: Optional[float]
    price_gt: Optional[float]

    class Constants(Filter.Constants):
        model = ProductModel


class UrlProductFilter(Filter):
    url: AnyUrl
    products: Optional[ProductFilter] = FilterDepends(
        with_prefix("product", ProductFilter)
    )

    class Constants(Filter.Constants):
        model = UrlModel
