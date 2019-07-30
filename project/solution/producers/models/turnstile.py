"""Creates a turnstile data producer"""
import logging
from pathlib import Path

from confluent_kafka import avro

from models.producer import Producer
from models.turnstile_hardware import TurnstileHardware


logger = logging.getLogger(__name__)


class Turnstile(Producer):
    key_schema = avro.load(f"{Path(__file__).parents[0]}/schemas/turnstile_key.json")
    value_schema = avro.load(
        f"{Path(__file__).parents[0]}/schemas/turnstile_value.json"
    )

    def __init__(self, station, create_topic=True):
        """Create the Turnstile"""
        # TODO: Complete the below by deciding on a topic name, number of partitions, and number of
        # replicas
        super().__init__(
            topic_name="org.chicago.cta.station.turnstile.v1",
            key_schema=Turnstile.key_schema,
            value_schema=Turnstile.value_schema,
            num_partitions=5,
            num_replicas=1,
        )
        self.station = station
        self.turnstile_hardware = TurnstileHardware(station)

    def run(self, timestamp, time_step):
        """Simulates riders entering through the turnstile."""
        num_entries = self.turnstile_hardware.get_entries(timestamp, time_step)

        # TODO: Complete this function by emitting a message to the turnstile topic for the number
        # of entries that were calculated
        logger.debug(
            "%s riders have entered station %s at %s",
            num_entries,
            self.station.name,
            timestamp.isoformat(),
        )

        for _ in range(num_entries):
            try:
                self.producer.produce(
                    topic=self.topic_name,
                    key={"timestamp": self.time_millis()},
                    value={
                        "station_id": self.station.station_id,
                        "station_name": self.station.name,
                        "line": self.station.color.name,
                    },
                )
            except Exception as e:
                logger.fatal(e)
                raise e
