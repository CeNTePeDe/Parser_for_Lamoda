import asyncio
import json
import logging

from kafka import KafkaProducer
from parsers.parse_product import gather_data

logger = logging.getLogger(__name__)


def send_data_to_kafka(url):
    producer = KafkaProducer(bootstrap_servers="localhost:29092")
    logger.info(f"{producer}")
    parse_record = asyncio.run(gather_data(url))
    topic_name = "product_parser"
    for product in parse_record:
        logger.info("add product to producer")
        product_str = json.dumps(product)
        product_bytes = product_str.encode("utf-8")
        logger.info("connect to producer")
        producer.send(topic_name, value=product_bytes)
