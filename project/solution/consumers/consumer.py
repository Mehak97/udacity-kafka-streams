"""Defines core consumer functionality"""
import logging

import confluent_kafka
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
        offset_earliest=False,
        sleep_secs=1.0,
        consume_timeout=0.1,
        broker_properties=None,
    ):
        """Creates a consumer object for asynchronous use"""
        self.topic_name_pattern = topic_name_pattern
        self.message_handler = message_handler
        self.sleep_secs = sleep_secs
        self.consume_timeout = consume_timeout
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
                "group.id": f"{topic_name_pattern}",
                "default.topic.config": {
                    "auto.offset.reset": "earliest"
                }
            }
        self.offset_earliest = offset_earliest
        self.consumer = AvroConsumer(self.broker_properties)
        self.consumer.subscribe([self.topic_name_pattern], on_assign=self.on_assign)
        self.partitions_assigned = False

    def on_assign(self, consumer, partitions):
        """Callback for when topic assignment takes place"""
        for partition in partitions:
            if self.offset_earliest is True:
                logger.debug("setting partitions to earliest for %s", self.topic_name_pattern)
                logger.debug("before: %s", partition)
                partition.offset = confluent_kafka.OFFSET_BEGINNING
                logger.debug("after: %s", partition)
        logger.info("partitions assigned for %s", self.topic_name_pattern)
        consumer.assign(partitions)

    async def consume(self):
        """Asynchronously consumes data from kafka topic"""
        while True:
            num_results = 1
            while num_results > 0:
                num_results = self._consume()
            await gen.sleep(self.sleep_secs)

    def _consume(self):
        """Polls for a message"""
        logger.debug("consuming from topic pattern %s", self.topic_name_pattern)
        try:
            message = self.consumer.poll(timeout=self.consume_timeout)
        except SerializerError as e:
            logger.error(
                "failed to deserialize message %s: %s", self.topic_name_pattern, e
            )

        if message is None:
            logger.debug("no messages to be consumed")
            return 0
        elif message.error() is not None:
            logger.error(
                "failed to consume message %s: %s",
                self.topic_name_pattern,
                message.error(),
            )
            return 0

        logger.debug(
            "message received: (%s) %s", message.key(), message.value()
        )
        self.message_handler(message)
        return 1


    def close(self):
        """Cleans up any open kafka consumers"""
        logger.debug("closing consumer...")
        self.consumer.close()
