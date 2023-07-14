import json
import logging

from core.constant_variables import (AUTO_OFFSET_RESET, CONSUMER_TIMEOUT_MS,
                                     KAFKA_URL, TOPIC_STREAMER)
from kafka import KafkaConsumer, KafkaProducer
from parsers.parse_streamer import get_data_streams

logger = logging.getLogger(__name__)


def send_data_to_kafka_streamers(url):
    producer = KafkaProducer(bootstrap_servers=KAFKA_URL)
    logger.info(f"{producer}")
    streamers = get_data_streams()
    for stream in streamers:
        streamer_str = json.dumps(stream)
        streamer_bytes = streamer_str.encode("utf-8")
        producer.send(topic=TOPIC_STREAMER, value=streamer_bytes)


def kafka_consumer_for_streamers():
    return KafkaConsumer(
        TOPIC_STREAMER,
        auto_offset_reset=AUTO_OFFSET_RESET,
        bootstrap_servers=KAFKA_URL,
        consumer_timeout_ms=CONSUMER_TIMEOUT_MS,
    )
