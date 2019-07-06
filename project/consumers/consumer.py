"""Defines core consumer functionality"""
import logging

from confluent_kafka.avro import AvroConsumer
from confluent_kafka.avro.serializer import SerializerError
from tornado import gen


logger = logging.getLogger(__name__)


class Consumer:
    """Defines the base kafka consumer class"""

    def __init__(
        self,
        topic_name_pattern,
        message_handler,
        sleep_secs=0.1,
        poll_timeout=0.1,
        broker_properties=None,
    ):
        """Creates a consumer object for asynchronous use"""
        self.topic_name_pattern = topic_name_pattern
        self.message_handler = message_handler
        self.sleep_secs = sleep_secs
        self.poll_timeout = poll_timeout
        self.broker_properties = broker_properties
        if self.broker_properties is None:
            self.broker_properties = {
                "bootstrap.servers": ",".join(
                    [
                        "PLAINTEXT://localhost:9092",
                        "PLAINTEXT://localhost:9093",
                        "PLAINTEXT://localhost:9094",
                    ]
                ),
                "schema.registry.url": "http://localhost:8081",
                "group.id": "cta.consumer.1",
            }
        self.consumer = AvroConsumer(self.broker_properties)

    async def consume(self):
        """Asynchronously consumes data from kafka topic"""
        self.consumer.subscribe([self.topic_name_pattern])
        while True:
            logger.debug("consuming from topic pattern %s", self.topic_name_pattern)
            try:
                message = self.consumer.poll(self.poll_timeout)
            except SerializerError as e:
                logger.error(
                    "failed to deserialize message %s: %s", self.topic_name_pattern, e
                )

            if message is not None and message.error():
                logger.error(
                    "failed to consume message %s: %s",
                    self.topic_name_pattern,
                    message.error(),
                )
            elif message is not None:
                logger.debug(
                    "message received: (%s) %s", message.key(), message.value()
                )
                self.message(handler(message))
            else:
                logger.debug("no message received on consume poll")

            await gen.sleep(self.sleep_secs)

    def close(self):
        """Cleans up any open kafka consumers"""
        logger.debug("closing consumer...")
        self.consumer.close()
