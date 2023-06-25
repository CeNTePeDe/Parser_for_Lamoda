import math
import asyncio
import logging

import aiohttp
from bs4 import BeautifulSoup


from core.constant_variables import MAIN_PAGE
from main import settings

logger = logging.getLogger(__name__)


async def get_page_data(
    session: aiohttp.ClientSession, url: str, page: int
) -> list[dict]:
    url = f"{url}?page={page}"
    logger.info(f"get_page_data function is started on the page={page}, url={url}")
    product_data: list = []
    async with session.get(url=url, headers=settings.HEADERS) as response:
        response_text = await response.text()
        html = BeautifulSoup(response_text, "lxml")
        product_items = html.find_all("div", class_="x-product-card__card")
        for item in product_items:
            name = item.find(
                "div", class_="x-product-card-description__product-name"
            ).text

            picture_link = item.find("img", class_="x-product-card__pic-img")
            if picture_link:
                picture_link = "https:" + picture_link.get("src")

            price = item.find("span", class_="x-product-card-description__price-single")
            if price is None:
                price = item.find(
                    "span", class_="x-product-card-description__price-new"
                )

            scr_link = MAIN_PAGE + item.find("a").get("href")
            product_data.append(
                {
                    "name_product": name,
                    "picture_link": picture_link,
                    "price": price.text,
                    "product_detail_link": scr_link,
                }
            )

        product_data = await get_data_for_each_product(
            product_data=product_data, session=session
        )
        logger.info(f"Parsing date is finished successfully on the page={page}")
        return product_data


async def get_data_for_each_product(
    session: aiohttp.ClientSession, product_data: list[dict]
) -> list[dict]:
    logger.info("get_data_for_each_product is started")
    for product_item in product_data:
        async with session.get(
            url=product_item["link_to_product"], headers=settings.HEADERS
        ) as response:
            response_text = await response.text()
            html_item_product = BeautifulSoup(response_text, "lxml")
            title = html_item_product.find_all(
                "span", class_="x-premium-product-description-attribute__name"
            )
            value = html_item_product.find_all(
                "span", class_="x-premium-product-description-attribute__value"
            )
            description = html_item_product.find(
                "div", class_="x-premium-product-description__text"
            )
            description = (
                description.text.strip("\n").strip() if description else "No content"
            )
            connect_value = zip(title, value)
            characteristic = {}
            for item_title, item_value in connect_value:
                characteristic.update(
                    {item_title.text.strip(): item_value.text.strip()}
                )

            product_item["characteristic"] = characteristic
            product_item["description"] = description
    logger.info("get_data_for_each_product is finished")

    return product_data


async def gather_data(url: str):
    logger.info("gather_data function is started")
    async with aiohttp.ClientSession() as session:
        response = await session.get(url, headers=settings.HEADERS)
        soup = BeautifulSoup(await response.text(), "lxml")
        number_of_products = int(
            soup.find("span", class_="d-catalog-header__product-counter").text.split()[0]
        )
        pages_count = math.ceil(number_of_products / 60)
        logger.info(f"total pages = {pages_count}")
        tasks = []
        for page in range(1, pages_count + 1):
            task = asyncio.create_task(get_page_data(session, url, page=page))
            tasks.append(task)

        await asyncio.gather(*tasks)
    logger.info("gather_data is finished successfully")

