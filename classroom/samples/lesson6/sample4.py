from dataclasses import asdict, dataclass
import json

import faust


@dataclass
class Purchase(faust.Record):
    username: str
    currency: str
    amount: int


@dataclass
class PurchaseDollars(faust.Record):
    username: str
    currency: str
    amount: float


app = faust.App("hello-faust", broker="kafka://localhost:9092")
purchases_topic = app.topic("com.udacity.streams.purchases", value_type=Purchase)
purchase_dollars_topic = app.topic(
    "com.udacity.streams.purchases.dollars",
    value_type=Purchase,
    key_type=str,
    serializer="json",
)


@app.agent(purchases_topic)
async def order(purchases):
    async for purchase in purchases:
        dollar_purchase = PurchaseDollars(
            username=purchase.username,
            currency=purchase.currency,
            amount=purchase.amount / 100.0,
        )
        await purchase_dollars_topic.send(key=purchase.username, value=dollar_purchase)


if __name__ == "__main__":
    app.main()
