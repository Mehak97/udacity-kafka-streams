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
currency_summary_table = app.Table("currency_summary", default=int)


@app.agent(purchases_topic)
async def purchase(purchases):
    #
    # TODO: Group by currency
    #
    async for purchase in purchases:
        #
        # TODO: Update the table by currency, print updated value
        #
        pass


if __name__ == "__main__":
    app.main()
