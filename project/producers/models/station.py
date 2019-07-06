"""Methods pertaining to loading and configuring CTA "L" station data."""
import logging
from pathlib import Path

from confluent_kafka import avro

from models import Turnstile
from models.producer import Producer


logger = logging.getLogger(__name__)


class Station(Producer):
    """Defines a single station"""

    key_schema = avro.load(f"{Path(__file__).parents[0]}/schemas/arrival_key.json")
    value_schema = avro.load(f"{Path(__file__).parents[0]}/schemas/arrival_value.json")

    def __init__(self, station_id, name, color, direction_a=None, direction_b=None):
        self.name = name
        st_name = (
            self.name.lower()
            .replace("/", "_and_")
            .replace(" ", "_")
            .replace("-", "_")
            .replace("'", "")
        )
        topic_name = f"org.chicago.cta.{color.name}.station.{st_name}.arrivals.v1"
        super().__init__(
            topic_name,
            key_schema=Station.key_schema,
            value_schema=Station.value_schema,
            num_partitions=5,
            num_replicas=2,
        )
        self.station_id = int(station_id)
        self.color = color
        self.dir_a = direction_a
        self.dir_b = direction_b
        self.a_train = None
        self.b_train = None
        self.turnstile = Turnstile(self)

    def __str__(self):
        return "Station | {:^5} | {:<30} | Direction A: | {:^5} | departing to {:<30} | Direction B: | {:^5} | departing to {:<30} | ".format(
            self.station_id,
            self.name,
            self.a_train.train_id if self.a_train is not None else "---",
            self.dir_a.name if self.dir_a is not None else "---",
            self.b_train.train_id if self.b_train is not None else "---",
            self.dir_b.name if self.dir_b is not None else "---",
        )

    def __repr__(self):
        return str(self)

    def arrive_a(self, train):
        """Denotes a train arrival at this station in the 'a' direction"""
        self.a_train = train
        # TODO: Use real name here
        self.run(train, "a")

    def arrive_b(self, train):
        """Denotes a train arrival at this station in the 'b' direction"""
        self.b_train = train
        # TODO: Use real name here
        self.run(train, "b")

    def run(self, train, direction):
        """Simulates train arrivals at this station"""
        try:
            self.producer.produce(
                topic=self.topic_name,
                key={"timestamp": self.time_millis()},
                value={
                    "station_id": self.station_id,
                    "train_id": train.train_id,
                    "direction": direction,
                    "line": self.color.name,
                    "train_status": train.status.name,
                },
            )
        except Exception as e:
            logger.fatal(e)
            raise e

    def close(self):
        """Prepares the producer for exit by cleaning up the producer"""
        self.turnstile.close()
        super(Station, self).close()
