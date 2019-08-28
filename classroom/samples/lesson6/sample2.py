from dataclasses import asdict, dataclass
import json

import faust


#
# TODO: Define a Purchase Record Class
#
# class Purchase(...):


app = faust.App("hello-faust", broker="kafka://localhost:9092")

#
# TODO: Provide the key and value type to the purchase
#
purchases_topic = app.topic("com.udacity.streams.purchases", value_type=Purchase)

#
# TODO: What happens if a field is missing during deserialization? Say, fraud_certainty?
#
@app.agent(purchases_topic)
async def purchase(purchases):
    async for purchase in purchases:
        print(json.dumps(asdict(purchase), indent=2))


if __name__ == "__main__":
    app.main()
