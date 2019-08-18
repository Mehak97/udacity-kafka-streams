from dataclasses import asdict, dataclass, field
import random

from faker import Faker


faker = Faker()


@dataclass
class Purchase:
    username: str = field(default_factory=faker.user_name)
    currency: str = field(default_factory=faker.currency_code)
    amount: int = field(default_factory=lambda: random.randint(100, 200000))

    def serialize(self):
        return f"{self.username}, {self.currency}, {self.amount}"


@dataclass
class ClickEvent:
    email: str = field(default_factory=faker.email)
    timestamp: str = field(default_factory=faker.iso8601)
    uri: str = field(default_factory=faker.uri)
    number: int = field(default_factory=lambda: random.randint(0, 999))

    def serialize(self):
        return f"{self.email}, {self.timestamp}, {self.uri}, {self.number}"


with open("clicks.csv", "w") as f:
    f.write("id, email, timestamp, uri, number\n")
    for i in range(1, 500):
        f.write(f"{i}, {ClickEvent().serialize()}\n")


with open("purchases.csv", "w") as f:
    f.write("id, username, currency, amount\n")
    for i in range(1, 200):
        f.write(f"{i}, {Purchase().serialize()}\n")
