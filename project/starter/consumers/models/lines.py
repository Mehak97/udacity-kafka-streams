"""Contains functionality related to Lines"""
import logging

from models import Line


logger = logging.getLogger(__name__)


class Lines:
    """Contains all train lines"""

    def __init__(self):
        """Creates the Lines object"""
        self.brown_line = Line("brown")
        self.red_line = Line("red")
        self.orange_line = Line("orange")
        self.blue_line = Line("blue")

    def process_message(self, message):
        """Processes a station message"""
        if message.topic() != "org.chicago.cta.stations":
            logger.debug("ignoring non-lines message")

        value = message.value()
        if value["brown"] is True:
            self.brown_line.process_message(message)
        if value["red"] is True:
            self.red_line.process_message(message)
        if value["orange"] is True:
            self.orange_line.process_message(message)
        if value["blue"] is True:
            self.blue_line.process_message(message)
