import json
import logging

from kafka import KafkaProducer
from parsers.parse_streamer import get_data_streams

logger = logging.getLogger(__name__)


def send_data_to_kafka_streamers(url):
    from main import settings

    producer = KafkaProducer(bootstrap_servers=settings.KAFKA_URL)
    logger.info(f"{producer}")
    streamers = get_data_streams()
    for stream in streamers:
        streamer_str = json.dumps(stream)
        streamer_bytes = streamer_str.encode("utf-8")
        producer.send(topic=settings.TOPIC_STREAMER, value=streamer_bytes)
