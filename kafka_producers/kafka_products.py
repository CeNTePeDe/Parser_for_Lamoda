import asyncio
import json
import logging

from core.constant_variables import (AUTO_OFFSET_RESET, CONSUMER_TIMEOUT_MS,
                                     KAFKA_URL, TOPIC_PRODUCT)
from kafka import KafkaConsumer, KafkaProducer
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


def kafka_consumer_for_products():
    return KafkaConsumer(
        TOPIC_PRODUCT,
        bootstrap_servers=KAFKA_URL,
        auto_offset_reset=AUTO_OFFSET_RESET,
        consumer_timeout_ms=CONSUMER_TIMEOUT_MS,
    )
