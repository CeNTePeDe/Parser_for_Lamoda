import math

from bs4 import BeautifulSoup
import asyncio
import aiohttp
import requests

from core.constant_variables import MAIN_PAGE

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}

product_data = []


async def get_page_data(session, url: str, page: int):
    url = f"{url}?page={page}"

    async with session.get(url=url, headers=headers) as response:
        response_text = await response.text()
        html = BeautifulSoup(response_text, "lxml")
        product_items = html.find_all("div", class_="x-product-card__card")
        for item in product_items:
            name = item.find("div", class_="x-product-card-description__product-name").text
            picture_link = MAIN_PAGE + item.find("img", class_="x-product-card__pic-img").get("src")
            try:
                price = item.find("span",
                                  class_="x-product-card-description__price-single").text
            except AttributeError:
                price = item.find("span",
                                  class_="x-product-card-description__price-new").text
            scr_link = MAIN_PAGE + item.find("a").get("href")
            product_data.append({
                "name": name,
                "picture": picture_link,
                "price": price,
                "link_to_product": scr_link,
            })
            for product_item in product_data:
                req = requests.get(product_item["link_to_product"])
                html_item_product = BeautifulSoup(req.text, "lxml")
                title = html_item_product.find_all("span", class_="x-premium-product-description-attribute__name")
                value = html_item_product.find_all("span", class_="x-premium-product-description-attribute__value")
                description = html_item_product.find("div", class_="x-premium-product-description__text").text.strip(
                    "\n").strip()
                connect_value = zip(title, value)
                characteristic_product_item = {}
                for item_title, item_value in connect_value:
                    characteristic_product_item.update({item_title.text.strip(): item_value.text.strip()})
                product_item["characteristic"] = characteristic_product_item
                product_item["description"] = description


async def gather_data(url: str):
    async with aiohttp.ClientSession() as session:
        response = await session.get(url, headers=headers)
        soup = BeautifulSoup(await response.text(), "lxml")
        number_of_products = int(soup.find("span", class_="d-catalog-header__product-counter").text.split(' ')[0])
        pages_count = math.ceil(number_of_products / 60)

        tasks = []
        for page in range(1, pages_count + 1):
            task = asyncio.create_task(get_page_data(session, url, page=page))
            tasks.append(task)

        await asyncio.gather(*tasks)
