import faust

#
# TODO: Create the faust app with a name and broker
#
# app = faust.App(...)

#
# TODO: Connect Faust to a topic
#
# topic = app.topic(...)

#
# TODO: Provide an app agent to execute this function on topic event retrieval
#
# app.agent(...)
async def purchase(purchases):
    async for purchase in purchases:
        print(purchase)


if __name__ == "__main__":
    app.main()
