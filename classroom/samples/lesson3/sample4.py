import asyncio
from dataclasses import asdict, dataclass, field
import io
import json
import random

from confluent_kafka import avro, Consumer, Producer
from confluent_kafka.avro import (
    AvroConsumer,
    AvroProducer,
    CachedSchemaRegistryClient
)
from faker import Faker


faker = Faker()

SCHEMA_REGISTRY_URL = "http://localhost:8081"
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
    # TODO: Use confluent avro to load the schema
    #
    schema = avro.loads("""{
        "type": "record",
        "name": "purchase",
        "namespace": "com.udacity.lesson3.sample4",
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
                            {"name": "amount", "type": "int"}
                        ]
                    }
                }
            }
        ]
    }""")


async def produce(topic_name):
    """Produces data into the Kafka Topic"""
    #
    # TODO: Create a CachedSchemaRegistryClient
    #
    schema_registry = CachedSchemaRegistryClient({"url": SCHEMA_REGISTRY_URL})

    #
    # TODO: Use the Avro Producer
    #
    p = AvroProducer(
        {"bootstrap.servers": BROKER_URL},
        schema_registry=schema_registry,
    )
    while True:
        #
        # TODO: Update Produce to just send the data
        #
        p.produce(
            topic=topic_name,
            value=asdict(Purchase()),
            value_schema=Purchase.schema
        )
        await asyncio.sleep(1.0)


async def consume(topic_name):
    """Consumes data from the Kafka Topic"""
    #
    # TODO: Create a CachedSchemaRegistryClient
    #
    schema_registry = CachedSchemaRegistryClient({"url": SCHEMA_REGISTRY_URL})

    #
    # TODO: Use the Avro Consumer
    #
    c = AvroConsumer(
        {"bootstrap.servers": BROKER_URL, "group.id": "0"},
        schema_registry=schema_registry
    )
    c.subscribe([topic_name])
    while True:
        message = c.poll(1.0)
        if message is None:
            print("no message received by consumer")
        elif message.error() is not None:
            print(f"error from consumer {message.error()}")
        else:
            try:
                print(message.value())
            except KeyError as e:
                print(f"Failed to unpack message {e}")
        await asyncio.sleep(1.0)



def main():
    """Checks for topic and creates the topic if it does not exist"""
    try:
        asyncio.run(produce_consume("com.udacity.lesson3.sample4.purchases"))
    except KeyboardInterrupt as e:
        print("shutting down")


async def produce_consume(topic_name):
    """Runs the Producer and Consumer tasks"""
    t1 = asyncio.create_task(produce(topic_name))
    t2 = asyncio.create_task(consume(topic_name))
    await t1
    await t2


if __name__ == "__main__":
    main()
