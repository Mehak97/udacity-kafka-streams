import asyncio
from dataclasses import asdict, dataclass, field
import io
import json
import random

from confluent_kafka import Producer
from faker import Faker
from fastavro import parse_schema, writer


faker = Faker()

BROKER_URL = "PLAINTEXT://localhost:9092"


@dataclass
class Purchase:
    username: str = field(default_factory=faker.user_name)
    currency: str = field(default_factory=faker.currency_code)
    amount: int = field(default_factory=lambda: random.randint(100, 200000))

    schema = parse_schema(
        {
            "type": "record",
            "name": "purchase",
            "namespace": "com.udacity.lesson3.sample2",
            "fields": [
                {"name": "username", "type": "string"},
                {"name": "currency", "type": "string"},
                {"name": "amount", "type": "int"},
            ],
        }
    )

    def serialize(self):
        #
        # TODO: Modify the following sample to use Avro instead of JSON
        #
        out = io.BytesIO()
        writer(out, Purchase.schema, [asdict(self)])
        return out.getvalue()


async def produce(topic_name):
    """Produces data into the Kafka Topic"""
    p = Producer({"bootstrap.servers": BROKER_URL})
    while True:
        p.produce(topic_name, Purchase().serialize())
        await asyncio.sleep(1.0)


def main():
    """Checks for topic and creates the topic if it does not exist"""
    try:
        asyncio.run(produce_consume("com.udacity.lesson3.sample2.purchases"))
    except KeyboardInterrupt as e:
        print("shutting down")


async def produce_consume(topic_name):
    """Runs the Producer and Consumer tasks"""
    await asyncio.create_task(produce(topic_name))


if __name__ == "__main__":
    main()
