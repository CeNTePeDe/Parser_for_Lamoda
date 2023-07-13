from pymongo import MongoClient

MAIN_PAGE: str = "https://www.lamoda.by"

NUMBER_OF_PRODUCT_PER_PAGE: int = 60

MAIN_PAGE_MEN: str = "https://www.lamoda.by/men-home/"

HEADERS: dict = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
                    Chrome/114.0.0.0 Safari/537.36"
}

client: MongoClient = MongoClient("mongodb://user:1111@mongo:27017")
db = client["product_db"]


BASE_URL: str = "https://api.twitch.tv/helix/streams"
KAFKA_URL: str = "kafka:9092"
TOPIC_PRODUCT: str = "product_parser"
TOPIC_STREAMER: str = "streamer_parser"
AUTO_OFFSET_RESET: str = "earliest"
CONSUMER_TIMEOUT_MS: int = 1000
# test constant
URL_CATEGORIES: str = "http://localhost:8000/api/categories/"
URL_PRODUCTS: str = "http://localhost:8000/api/products/"

URL_PARSER_FUNCTION: str = "http://localhost:8000/api/products/parser"
URL_FOR_PARSER: str = "https://www.lamoda.by/c/4170/clothes-maternityclothes/"
EXPECTED_RESULT_OF_PRODUCTS: int = 83
