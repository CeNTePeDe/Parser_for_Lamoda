from pymongo import MongoClient

MAIN_PAGE: str = "https://www.lamoda.by"

NUMBER_OF_PRODUCT_PER_PAGE: int = 60

HEADERS: dict = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
                    Chrome/114.0.0.0 Safari/537.36"
}

def get_db(db_name="product_db"):
    client = MongoClient("mongodb://user:1111@mongo:27017")
    db = client.get_database(db_name)
    return db


BASE_URL: str = "https://api.twitch.tv/helix/streams"

# test_constant

URL_STREAMERS: str = "http://localhost:8000/api/streamers/"

URL_STREAMERS_PARSE: str = "http://localhost:8000/api/streamers/parsing_streamers/"
