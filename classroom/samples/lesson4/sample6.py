from dataclasses import asdict, dataclass, field
import json
import time
import random

import requests
from confluent_kafka import avro, Consumer, Producer
from confluent_kafka.avro import AvroConsumer, AvroProducer, CachedSchemaRegistryClient
from faker import Faker


faker = Faker()
REST_PROXY_URL = "http://localhost:8082"

AVRO_SCHEMA = """{
    "type": "record",
    "name": "purchase",
    "fields": [
        {"name": "username", "type": "string"},
        {"name": "currency", "type": "string"},
        {"name": "amount", "type": "int"}
    ]
}"""


def produce():
    """Produces data using REST Proxy"""

    # TODO: Set the appropriate headers for AVRO
    #       See: https://docs.confluent.io/current/kafka-rest/api.html#content-types
    headers = {"Content-Type": "application/vnd.kafka.avro.v2+json"}
    # TODO: Define the Data
    data = {"value_schema": AVRO_SCHEMA, "records": [{"value": asdict(Purchase())}]}
    resp = requests.post(
        f"{REST_PROXY_URL}/topics/lesson4.sample6.purchases",
        data=json.dumps(data),
        headers=headers,
    )

    try:
        resp.raise_for_status()
    except:
        print(f"Failed to send data to REST Proxy {json.dumps(resp.json(), indent=2)}")

    print(f"Sent data to REST Proxy {json.dumps(resp.json(), indent=2)}")


@dataclass
class Purchase:
    username: str = field(default_factory=faker.user_name)
    currency: str = field(default_factory=faker.currency_code)
    amount: int = field(default_factory=lambda: random.randint(100, 200000))


def main():
    """Runs the simulation against REST Proxy"""
    try:
        while True:
            produce()
            time.sleep(0.5)
    except KeyboardInterrupt as e:
        print("shutting down")


if __name__ == "__main__":
    main()
