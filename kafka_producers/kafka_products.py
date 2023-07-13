import asyncio
import json
import logging

from core.constant_variables import KAFKA_URL, TOPIC_PRODUCT
from kafka import KafkaProducer
from parsers.parse_product import gather_data

logger = logging.getLogger(__name__)


def send_data_to_kafka_products(url):
    producer = KafkaProducer(bootstrap_servers=KAFKA_URL)
    logger.info(f"{producer}")
    parse_record = asyncio.run(gather_data(url))
    for product in parse_record:
        logger.info("add product to producer")
        product_str = json.dumps(product)
        product_bytes = product_str.encode("utf-8")
        logger.info("connect to producer")
        producer.send(topic=TOPIC_PRODUCT, value=product_bytes)
