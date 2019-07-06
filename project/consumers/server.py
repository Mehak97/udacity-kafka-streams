"""Defines a Tornado Server that consumes Kafka Event data for display"""
import logging
import logging.config
from pathlib import Path

import tornado.ioloop
import tornado.template
import tornado.web


# Import logging before models to ensure configuration is picked up
logging.config.fileConfig(f"{Path(__file__).parents[1]}/logging.ini")


from . import Consumer


logger = logging.getLogger(__name__)


class MainHandler(tornado.web.RequestHandler):
    """Defines a web request handler class"""

    template_dir = tornado.template.Loader(f"{Path(__file__).parents[0]}/templates")
    template = template_dir.load("status.html")

    def get(self):
        """Responds to get requests"""
        logging.debug("rendering and writing handler template")
        # TODO: Add values
        self.write(MainHandler.template.generate())


def run_server():
    """Runs the Tornado Server and begins Kafka consumption"""
    application = tornado.web.Application([(r"/", MainHandler)])
    application.listen(8888)
    c = Consumer("org.chicago.cta.weather.v1")
    try:
        logger.info("listening on :8888")
        tornado.ioloop.IOLoop.current().spawn_callback(c.consume)
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt as e:
        logger.info("shutting down server")
        tornado.ioloop.IOLoop.current().stop()
        c.close()



if __name__ == "__main__":
    run_server()
