"""Creates a turnstile data producer"""
import logging
import os

from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer

from generator import Generator


logger = logging.getLogger(__name__)


class TurnstileGenerator(Generator):
    key_schema = avro.load(
        f"{os.path.dirname(os.path.abspath(__file__))}/schemas/turnstile_key.json"
    )
    value_schema = avro.load(
        f"{os.path.dirname(os.path.abspath(__file__))}/schemas/turnstile_value.json"
    )

    def __init__(self, create_topic=True):
        """Create the TurnstileGenerator"""
        super().__init__("org.chicago.cta.turnstile.v1", num_partitions=5, num_replicas=3)

    def run(self):
        """Begin producing turnstile records"""
        producer = AvroProducer(
            self.broker_properties,
            default_key_schema=TurnstileGenerator.key_schema,
            default_value_schema=TurnstileGenerator.value_schema,
        )

        # TODO: Production loop. Actually, this ought to just go into Generator.
        producer.produce(
                topic=self.topic_name,
                key={"timestamp": self.time_millis()},
                value={
                    "stop_id": 0,
                    "stop_name": "Jefferson Park",
                    "line": "blue"
                }
        )
        # TODO: End loop here

        producer.flush()


if __name__ == "__main__":
    TurnstileGenerator().run()
