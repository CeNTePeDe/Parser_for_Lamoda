from core.constant_variables import URL_PRODUCTS


def test_get_products(client):
    response = client.get(URL_PRODUCTS)

    assert response.status_code == 200


def test_create_product(client, test_db, product_build, category_build):
    data = product_build()
    category = category_build()
    data_category = {"category": category.category}
    payload = {
        "name_product": data.name_product,
        "picture_link": data.picture_link,
        "price": str(data.price),
        "product_detail_link": data.product_detail_link,
        "characteristic": data.characteristic,
        "description": data.description,
        "category": data_category,
        "product_id": data.product_id,
    }

    response = client.post(url=URL_PRODUCTS, json=payload)

    assert response.status_code == 201
    assert response.json()["product_id"] == payload["product_id"]
    assert response.json()["picture_link"] == payload["picture_link"]
    assert str(response.json()["price"]) == payload["price"]
    assert response.json()["product_detail_link"] == payload["product_detail_link"]
    assert response.json()["description"] == payload["description"]


def test_get_product(client, test_db):
    product_id = "id_0"

    response = client.get(url=URL_PRODUCTS + f"{product_id}")

    assert response.status_code == 200
    assert response.json()["product_id"] == "id_0"
    assert response.json()["name_product"] == "product_0"
    assert response.json()["product_id"] == "id_0"


def test_get_invalid_product(client, test_db):
    product_id = "invalid_product"

    response = client.get(url=URL_PRODUCTS + f"{product_id}")

    assert response.status_code == 404


def test_update_product(client, test_db, category_build, product_build):
    product_id = "id_0"
    data = product_build()
    category = category_build()
    data_category = {"category": category.category}
    payload = {
        "name_product": data.name_product,
        "picture_link": data.picture_link,
        "price": data.price,
        "product_detail_link": data.product_detail_link,
        "characteristic": data.characteristic,
        "description": data.description,
        "category": data_category,
        "product_id": "id_0",
    }

    response = client.put(url=URL_PRODUCTS + f"{product_id}", json=payload)

    assert response.status_code == 200
    assert response.json()["product_id"] == payload["product_id"]
    assert response.json()["product_detail_link"] == payload["product_detail_link"]
    assert response.json()["description"] == payload["description"]
    assert response.json()["name_product"] == payload["name_product"]


def test_delete_product(client, test_db):
    product_id = "id_0"

    response = client.delete(url=URL_PRODUCTS + f"{product_id}")

    assert response.status_code == 204
