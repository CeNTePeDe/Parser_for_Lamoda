def product_serializer(product) -> dict:
    return {
        "name_product": product["name_product"],
        "picture_link": product["picture_link"],
        "price": product["price"],
        "product_detail_link": str(product["product_detail_link"]),
        "characteristic": product["characteristic"],
        "description": product["description"],
    }


def list_product_serializer(products) -> list:
    return [product_serializer(product) for product in products]


def serializer_products_by_url(data)->dict:
    return {
        "id": str(data["_id"]),
        "url": data["url"],
        "products": list_product_serializer(data["products"])
    }

