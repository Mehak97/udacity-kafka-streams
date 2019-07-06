"""Contains functionality related to Lines"""
import logging

from models import Station


logger = logging.getLogger(__name__)


class Line:
    """Defines the Line Model"""

    def __init__(self, color):
        """Creates a line"""
        self.color = color
        self.stations = {}

    def _handle_station(self, message):
        """Adds the station to this Line's data model"""
        value = message.value()
        if value[self.color] is not True:
            return

        self.stations[value["station_id"]] = Station.from_message(message)

    def process_message(self, message):
        """Given a kafka message, extract data"""
        if message.topic() == "org.chicago.cta.stations":
            self._handle_station(message)
            return

        station_id = message.value().get("station_id")
        if station_id is not None:
            station = self.stations.get(station_id)
            if station is None:
                logger.error("unable to handle message due to missing station %s", station_id)
                return
            self.stations[station_id].process_message(message)
