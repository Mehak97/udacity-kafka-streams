from dataclasses import asdict, dataclass
import json

import faust


@dataclass
class Purchase(faust.Record):
    username: str
    currency: str
    amount: int
    fraud_score: float = 0.0


#
# TODO: Define a function which adds a fraud score to incoming records
#
def add_fraud_score(value):
    value.fraud_score = random.random()
    return value


app = faust.App("hello-faust", broker="kafka://localhost:9092")
purchases_topic = app.topic("com.udacity.streams.purchases", value_type=Purchase)
#
# TODO: Define a stream
# TODO: Assign processors to incoming records
#
purchases_stream = app.stream(...)


#
# TODO: Enumerate the purchases stream
#
async for purchase in purchases_stream:
    print(json.dumps(asdict(purchase), indent=2))


if __name__ == "__main__":
    app.main()
