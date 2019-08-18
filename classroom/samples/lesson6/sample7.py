from datetime import timedelta
from dataclasses import asdict, dataclass
import json

import faust


@dataclass
class Purchase(faust.Record):
    username: str
    currency: str
    amount: int


app = faust.App("hello-faust", broker="kafka://localhost:9092")
purchases_topic = app.topic("com.udacity.streams.purchases", value_type=Purchase)
#
# TODO: Define a tumbling window with a 30 second timedelta and a 10 minute expires
#
currency_summary_table = app.Table("currency_summary_tumbling", default=int).tumbling(
    timedelta(seconds=30), expires=timedelta(minutes=10)
)


@app.agent(purchases_topic)
async def purchase(purchases):
    async for purchase in purchases.group_by(Purchase.currency):
        currency_summary_table[purchase.currency] += purchase.amount
        #
        # TODO: Play with printing value by: now(), current(), value()
        #       See: https://faust.readthedocs.io/en/latest/userguide/tables.html#how-to
        #
        print(
            f"{purchase.currency}: {currency_summary_table[purchase.currency].current()}"
        )


if __name__ == "__main__":
    app.main()
