import json
import logging

from core.constant_variables import KAFKA_URL, TOPIC_STREAMER
from kafka import KafkaProducer
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
