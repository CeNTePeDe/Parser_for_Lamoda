import math
import asyncio
import logging

import aiohttp
import requests
from bs4 import BeautifulSoup

from core.constant_variables import MAIN_PAGE, HEADERS

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler("parser.log")
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


async def get_page_data(session: aiohttp.ClientSession, url: str, page: int) -> list[dict]:
    url = f"{url}?page={page}"
    logger.info(f"get_page_data function is started on the page={page}, url={url}")
    product_data: list = []
    async with session.get(url=url, headers=HEADERS) as response:

        response_text = await response.text()
        html = BeautifulSoup(response_text, "lxml")
        product_items = html.find_all("div", class_="x-product-card__card")
        for item in product_items:
            name = item.find("div", class_="x-product-card-description__product-name").text

            picture_link = item.find("img", class_="x-product-card__pic-img")
            if picture_link is None:
                picture_link = url
            else:
                picture_link = MAIN_PAGE + picture_link.get("src")

            price = item.find("span", class_="x-product-card-description__price-single")
            if price is None:
                price = item.find("span", class_="x-product-card-description__price-new").text
            else:
                price = price.text

            scr_link = MAIN_PAGE + item.find("a").get("href")
            product_data.append({
                "name": name,
                "picture": picture_link,
                "price": price,
                "link_to_product": scr_link,
            })
        product_data = get_data_for_each_product(product_data=product_data)
        logger.debug(f"Parsing date is finished successfully on the page={page}")
        return product_data


def get_data_for_each_product(product_data: list[dict]) -> list[dict]:
    logger.info(f"get_data_for_each_product function is started")
    for product_item in product_data:
        req = requests.get(product_item["link_to_product"])
        html_item_product = BeautifulSoup(req.text, "lxml")
        title = html_item_product.find_all("span", class_="x-premium-product-description-attribute__name")
        value = html_item_product.find_all("span", class_="x-premium-product-description-attribute__value")
        description = html_item_product.find("div", class_="x-premium-product-description__text")
        if description is None:
            description = "No Content"
        else:
            description = description.text.strip("\n").strip()

        connect_value = zip(title, value)
        characteristic_product_item = {}
        for item_title, item_value in connect_value:
            characteristic_product_item.update({item_title.text.strip(): item_value.text.strip()})
        product_item["characteristic"] = characteristic_product_item
        product_item["description"] = description
    logger.debug("Parsing date for each product is finished successfully")
    return product_data


async def gather_data(url: str):
    logger.info("gather_data function is started")
    async with aiohttp.ClientSession() as session:
        response = await session.get(url, headers=HEADERS)
        soup = BeautifulSoup(await response.text(), "lxml")
        number_of_products = int(soup.find("span", class_="d-catalog-header__product-counter").text.split()[0])
        pages_count = math.ceil(number_of_products / 60)
        logger.info(f"total pages = {pages_count}")
        tasks = []
        for page in range(1, pages_count + 1):
            task = asyncio.create_task(get_page_data(session, url, page=page))
            tasks.append(task)

        await asyncio.gather(*tasks)
    logger.debug("gather_data is finished successfully")
