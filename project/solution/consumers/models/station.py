"""Contains functionality related to Stations"""
import logging


logger = logging.getLogger(__name__)


class Station:
    """Defines the Station Model"""

    def __init__(self, station_id, station_name):
        """Creates a Station Model"""
        self.station_id = station_id
        self.station_name = station_name
        self.dir_a = None
        self.dir_b = None
        self.num_turnstile_entries = 0

    @classmethod
    def from_message(cls, message):
        """Given a Kafka Station message, creates and returns a station"""
        value = message.value()
        return Station(value["station_id"], value["station_name"])

    def handle_departure(self, direction):
        """Removes a train from the station"""
        if direction == "a":
            self.dir_a = None
        else:
            self.dir_b = None

    def handle_arrival(self, direction, train_id, train_status):
        """Unpacks arrival data"""
        status_dict = {"train_id": train_id, "status": train_status.replace("_", " ")}
        if direction == "a":
            self.dir_a = status_dict
        else:
            self.dir_b = status_dict

    def _handle_turnstile(self):
        """Handles turnstile messages"""
        self.num_turnstile_entries += 1

    def process_message(self, message):
        """Handles arrival and turnstile messages"""
        # TODO: Check if the message is a turnstile event, and if it is, call
        # `self._handle_turnstile()
        try:
            logger.debug("processing station message from topic %s", message.topic())
            value = message.value()
            if "turnstile" in message.topic():
                logger.debug("handling turnstile message for station")
                self._handle_turnstile()
        except Exception as e:
            logger.fatal("encountered an exception in station! %s", e)
