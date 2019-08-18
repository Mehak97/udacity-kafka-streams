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
class LineItem:
    description: str = field(default_factory=faker.bs)
    amount: int = field(default_factory=lambda: random.randint(100, 200000))

    @classmethod
    def line_items(self):
        return [LineItem() for _ in range(random.randint(1, 10))]


@dataclass
class Purchase:
    username: str = field(default_factory=faker.user_name)
    currency: str = field(default_factory=faker.currency_code)
    amount: int = field(default_factory=lambda: random.randint(100, 200000))
    line_items: list = field(default_factory=LineItem.line_items)

    #
    # TODO: Update the schema to incorporate line items
    #
    schema = parse_schema(
        {
            "type": "record",
            "name": "purchase",
            "namespace": "com.udacity.lesson3.sample3",
            "fields": [
                {"name": "username", "type": "string"},
                {"name": "currency", "type": "string"},
                {"name": "amount", "type": "int"},
                {
                    "name": "line_items",
                    "type": {
                        "type": "array",
                        "items": {
                            "type": "record",
                            "name": "line_item",
                            "fields": [
                                {"name": "description", "type": "string"},
                                {"name": "amount", "type": "int"},
                            ],
                        },
                    },
                },
            ],
        }
    )

    def serialize(self):
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
        asyncio.run(produce_consume("com.udacity.lesson3.sample3.purchases"))
    except KeyboardInterrupt as e:
        print("shutting down")


async def produce_consume(topic_name):
    """Runs the Producer and Consumer tasks"""
    await asyncio.create_task(produce(topic_name))


if __name__ == "__main__":
    main()
