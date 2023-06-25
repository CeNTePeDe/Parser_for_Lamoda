def serialize_product(product) -> dict:
    return {
        "name_product": product["name_product"],
        "picture_link": product["picture_link"],
        "price": product["price"],
        "product_detail_link": str(product["product_detail_link"]),
        "characteristic": product["characteristic"],
        "description": product["description"],
    }


def serialize_list_of_products(products) -> list:
    return [serialize_product(product) for product in products]


def serialize_products_with_url(data)->dict:
    return {
        "id": str(data["_id"]),
        "url": data["url"],
        "products": serialize_list_of_products(data["products"])
    }

