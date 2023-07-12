import asyncio

from core.constant_variables import (
    EXPECTED_RESULT_OF_PRODUCTS,
    URL_FOR_PARSER,
    URL_PARSER_FUNCTION,
)
from parsers.parse_product import gather_data


def test_get_product_parse(mongo_mock):
    assert len(asyncio.run(gather_data(URL_FOR_PARSER))) == EXPECTED_RESULT_OF_PRODUCTS


def test_post_products(client, mongo_mock):
    params = {"url": URL_FOR_PARSER}
    response = client.post(url=URL_PARSER_FUNCTION, params=params)
    assert response.status_code == 201
