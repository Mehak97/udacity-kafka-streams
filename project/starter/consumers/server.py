"""Defines a Tornado Server that consumes Kafka Event data for display"""
import logging
import logging.config
from pathlib import Path

import tornado.ioloop
import tornado.template
import tornado.web


# Import logging before models to ensure configuration is picked up
logging.config.fileConfig(f"{Path(__file__).parents[0]}/logging.ini")


from consumer import Consumer
from models import Lines, Weather


logger = logging.getLogger(__name__)


class MainHandler(tornado.web.RequestHandler):
    """Defines a web request handler class"""
    template_dir = tornado.template.Loader(f"{Path(__file__).parents[0]}/templates")
    template = template_dir.load("status.html")

    def initialize(self, weather, lines):
        """Initializes the handler with required configuration"""
        self.weather = weather
        self.lines = lines

    def get(self):
        """Responds to get requests"""
        logging.debug("rendering and writing handler template")
        self.write(MainHandler.template.generate(weather=self.weather, lines=self.lines))


def run_server():
    """Runs the Tornado Server and begins Kafka consumption"""
    weather_model = Weather()
    lines = Lines()

    application = tornado.web.Application([(r"/", MainHandler, {"weather": weather_model, "lines": lines})])
    application.listen(8888)

    # Build kafka consumers
    consumers = [
        Consumer("org.chicago.cta.weather.v1", weather_model.process_message),
        Consumer("org.chicago.cta.stations", lines.process_message, offset_earliest=True),
        Consumer("^org.chicago.cta.blue.station.*", lines.blue_line.process_message),
        Consumer("^org.chicago.cta.orange.station.*", lines.orange_line.process_message),
        Consumer("^org.chicago.cta.red.station.*", lines.red_line.process_message),
        Consumer("^org.chicago.cta.brown.station.*", lines.brown_line.process_message),
    ]

    try:
        logger.info("Open a web browser to http://localhost:8888 to see the Transit Status Page")
        for consumer in consumers:
            tornado.ioloop.IOLoop.current().spawn_callback(consumer.consume)

        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt as e:
        logger.info("shutting down server")
        tornado.ioloop.IOLoop.current().stop()
        for consumer in consumers:
            consumer.close()


if __name__ == "__main__":
    run_server()
