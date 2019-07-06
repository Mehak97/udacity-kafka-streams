"""Producer base-class providing common utilites and functionality"""
import logging
import time


from confluent_kafka import avro
from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka.avro import AvroProducer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Producer:
    """Defines and provides common functionality amongst Producers"""

    def __init__(
        self, topic_name, key_schema, value_schema, num_partitions=1, num_replicas=1,
        broker_properties=None
    ):
        """Initializes a Producer object with basic settings"""
        self.topic_name = topic_name
        self.key_schema = key_schema
        self.value_schema = value_schema
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
        self.producer = AvroProducer(
            self.broker_properties,
            default_key_schema=key_schema,
            default_value_schema=value_schema,
        )

    def create_topic(self):
        """Creates the producer topic if it does not already exist"""
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

    def close(self):
        """Prepares the producer for exit by cleaning up the producer"""
        if self.producer is not None:
            logger.debug("flushing producer...")
            self.producer.flush()
