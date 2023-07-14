import asyncio
import json
import logging

from config.settings import settings
from kafka import KafkaConsumer, KafkaProducer
from parsers.parse_product import gather_data

logger = logging.getLogger(__name__)


def send_data_to_kafka_products(url):
    producer = KafkaProducer(bootstrap_servers=settings.KAFKA_URL)
    logger.info(f"{producer}")
    parse_record = asyncio.run(gather_data(url))
    for product in parse_record:
        logger.info("add product to producer")
        product_str = json.dumps(product)
        product_bytes = product_str.encode("utf-8")
        logger.info("connect to producer")
        producer.send(topic=settings.TOPIC_PRODUCT, value=product_bytes)


consumer_products =  KafkaConsumer(
        settings.TOPIC_PRODUCT,
        bootstrap_servers=settings.KAFKA_URL,
        auto_offset_reset=settings.AUTO_OFFSET_RESET,
        consumer_timeout_ms=settings.CONSUMER_TIMEOUT_MS,
    )
