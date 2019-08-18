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
# TODO: Define an output topic for purchases dollars
#


@app.agent(purchases_topic)
async def order(purchases):
    async for purchase in purchases:
        #
        # TODO: Modify the incoming purchase to be in dollars, then send the data on a new topic
        #       with key and value
        #
        pass


if __name__ == "__main__":
    app.main()
