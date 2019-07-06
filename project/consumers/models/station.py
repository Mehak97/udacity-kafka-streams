"""Contains functionality related to Stations"""
import logging


logger = logging.getLogger(__name__)


class Station:
    """Defines the Station Model"""

    def __init__(self, station_id, station_name):
        """Creates a Station Model"""
        self.station_id = station_id
        self.station_name = station_name

    @classmethod
    def from_message(cls, message):
        """Given a Kafka Station message, creates and returns a station"""
        value = message.value()
        return Station(value["station_id"], value["stop_name"])

    def process_message(self, message):
        """Handles arrival and turnstile messages"""
        logger.debug("processing station message from topic %s", message.topic())
