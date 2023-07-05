import asyncio

from parsers.parse_product import gather_data

URL = "http://localhost:8000/api/products/parser"
url_for_parser = "https://www.lamoda.by/c/4170/clothes-maternityclothes/"


def test_get_product_parse(mongo_mock):
    expected_result = 83
    assert len(asyncio.run(gather_data(url_for_parser))) == expected_result



def test_post_products(client, mongo_mock):
    params = {"url": url_for_parser}
    response = client.post(url=URL, params=params)
    assert response.status_code == 201
