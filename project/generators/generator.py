"""Generator base-class providing common utilites and functionality"""
import logging
import time

from confluent_kafka.admin import AdminClient, NewTopic

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Generator:
    """Defines and provides common functionality amongst Generators"""

    def __init__(
        self, topic_name, num_partitions=1, num_replicas=1, broker_properties=None
    ):
        """Initializes a Generator object with basic settings"""
        self.topic_name = topic_name
        self.num_partitions = num_partitions
        self.num_replicas = num_replicas
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
            }
        self.create_topic()

    def create_topic(self):
        """Creates the generator topic if it does not already exist"""
        logger.info("beginning topic creation for %s", self.topic_name)
        client = AdminClient(
            {"bootstrap.servers": self.broker_properties["bootstrap.servers"]}
        )
        topic_metadata = client.list_topics(timeout=5)
        if self.topic_name in set(t.topic for t in iter(topic_metadata.topics.values())):
            logger.info("not recreating existing topic %s", self.topic_name)
            return
        logger.info("creating topic %s", self.topic_name)
        futures = client.create_topics(
            [NewTopic(self.topic_name, self.num_partitions, self.num_replicas)]
        )

        for topic, future in futures.items():
            try:
                future.result()
                logger.info("topic created")
            except Exception as e:
                logger.fatal("failed to create topic %s: %s", topic, e)

    def time_millis(self):
        return int(round(time.time() * 1000))
