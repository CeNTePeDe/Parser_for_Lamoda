import asyncio
import json
import logging

from kafka import KafkaProducer
from parsers.parse_product import gather_data

logger = logging.getLogger(__name__)


def send_data_to_kafka_products(url):
    from main import settings

    producer = KafkaProducer(bootstrap_servers=settings.KAFKA_URL)
    logger.info(f"{producer}")
    parse_record = asyncio.run(gather_data(url))
    for product in parse_record:
        logger.info("add product to producer")
        product_str = json.dumps(product)
        product_bytes = product_str.encode("utf-8")
        logger.info("connect to producer")
        producer.send(topic=settings.TOPIC_PRODUCT, value=product_bytes)
