"""Creates a turnstile data producer"""
import logging
import math
from pathlib import Path
import random

from confluent_kafka import avro
import pandas as pd

from models.producer import Producer


logger = logging.getLogger(__name__)


class Turnstile(Producer):
    curve_df = None
    seed_df = None

    key_schema = avro.load(
        f"{Path(__file__).parents[0]}/schemas/turnstile_key.json"
    )
    value_schema = avro.load(
        f"{Path(__file__).parents[0]}/schemas/turnstile_value.json"
    )

    def __init__(self, station, create_topic=True):
        """Create the Turnstile"""
        st_name = station.name.lower().replace("/", "_and_").replace(" ", "_").replace("-", "_").replace("'", "")
        topic_name = f"org.chicago.cta.station.{st_name}.turnstile.v1"
        super().__init__(
                topic_name,
                key_schema=Turnstile.key_schema,
                value_schema=Turnstile.value_schema,
                num_partitions=25,
                num_replicas=2,
        )
        self.station = station
        Turnstile._load_data()
        self.metrics_df = Turnstile.seed_df[Turnstile.seed_df["station_id"] == station.station_id]
        self.weekday_ridership = int(round(self.metrics_df.iloc[0]["avg_weekday_rides"]))
        self.saturday_ridership = int(round(self.metrics_df.iloc[0]["avg_saturday_rides"]))
        self.sunday_ridership = int(round(self.metrics_df.iloc[0]["avg_sunday-holiday_rides"]))

    @classmethod
    def _load_data(cls):
        if cls.curve_df is None:
            cls.curve_df = pd.read_csv(f"{Path(__file__).parents[1]}/data/ridership_curve.csv")
        if cls.seed_df is None:
            cls.seed_df = pd.read_csv(f"{Path(__file__).parents[1]}/data/ridership_seed.csv")

    def run(self, timestamp, time_step):
        """Simulates riders entering through the turnstile."""
        hour_curve = Turnstile.curve_df[Turnstile.curve_df["hour"] == timestamp.hour]
        ratio = hour_curve.iloc[0]["ridership_ratio"]
        total_steps = int(60 / (60 / time_step.total_seconds()))

        num_riders = 0
        dow = timestamp.weekday()
        if dow >= 0 or dow < 5:
            num_riders = self.weekday_ridership
        elif dow == 6:
            num_riders = self.saturday_ridership
        else:
            num_riders = self.sunday_ridership

        # Calculate approximation of number of entries for this simulation step
        num_entries = int(math.floor(num_riders * ratio / total_steps))
        # Introduce some randomness in the data
        num_entries = max(num_entries + random.choice(range(-5,5)), 0)
        logger.debug(
                "%s riders have entered station %s at %s",
                num_entries,
                self.station.name,
                timestamp.isoformat())

        for _ in range(num_entries):
            try:
                self.producer.produce(
                        topic=self.topic_name,
                        key={"timestamp": self.time_millis()},
                        value={
                            "station_id": self.station.station_id,
                            "station_name": self.station.name,
                            "line": self.station.color.name,
                        }
                )
            except Exception as e:
                logger.fatal(e)
                raise e
