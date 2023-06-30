from pymongo import MongoClient

MAIN_PAGE: str = "https://www.lamoda.by"

NUMBER_OF_PRODUCT_PER_PAGE = 60

MAIN_PAGE_MEN: str = "https://www.lamoda.by/men-home/"

HEADERS: dict = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
                    Chrome/114.0.0.0 Safari/537.36"
}

client: MongoClient = MongoClient("mongodb://user:1111@mongo:27017")
db = client["product_db"]
