import logging

logger = logging.getLogger(__name__)


def serialize_category(category) -> dict:
    return {"id": str(category["_id"]), "category": category["category"]}


def serialize_list_of_category(categories) -> list[dict]:
    return [serialize_category(category) for category in categories]


def serialize_product(product) -> dict:
    return {
        "id": str(product["_id"]),
        "name_product": product["name_product"],
        "picture_link": product["picture_link"],
        "price": product["price"],
        "product_detail_link": product["product_detail_link"],
        "characteristic": product["characteristic"],
        "description": product["description"],
        "category": str(product["category"]),
    }


def serialize_list_of_products(products) -> list:
    return [serialize_product(product) for product in products]
