"""Contains functionality related to Lines"""
import logging

from models import Station


logger = logging.getLogger(__name__)


class Line:
    """Defines the Line Model"""

    def __init__(self, color):
        """Creates a line"""
        self.color = color
        self.color_code = "0xFFFFFF"
        if self.color == "blue":
            self.color_code = "#1E90FF"
        elif self.color == "red":
            self.color_code = "#DC143C"
        elif self.color == "green":
            self.color_code = "#32CD32"
        self.stations = {}

    def _handle_station(self, message):
        """Adds the station to this Line's data model"""
        value = message.value()
        if value[self.color] is not True:
            return
        self.stations[value["station_id"]] = Station.from_message(message)

    def _handle_arrival(self, message):
        """Updates train locations"""
        value = message.value()
        prev_station_id = value.get("prev_station_id")
        prev_dir = value.get("prev_direction")
        if prev_dir is not None and prev_station_id is not None:
            prev_station = self.stations.get(prev_station_id)
            if prev_station is not None:
                prev_station.handle_departure(prev_dir)
            else:
                logger.debug("unable to handle previous station due to missing station")
        else:
            logger.debug("unable to handle previous station due to missing previous info")

        station_id = value.get("station_id")
        station = self.stations.get(station_id)
        if station is None:
            logger.debug("unable to handle message due to missing station")
            return
        station.handle_arrival(
            value.get("direction"), value.get("train_id"), value.get("train_status")
        )

    def process_message(self, message):
        """Given a kafka message, extract data"""
        # TODO: Based on the message topic, call the appropriate handler.
        if message.topic() == "org.chicago.cta.stations":
            self._handle_station(message)
        elif "arrivals" in message.topic():
            self._handle_arrival(message)
        elif "turnstile" in message.topic():
            station_id = message.value().get("station_id")
            station = self.stations.get(station_id)
            if station is None:
                logger.debug("unable to handle message due to missing station")
                return
            station.process_message(message)
        else:
            logger.debug("unable to find handler for message from topic %s", message.topic)
