"""Defines functionality relating to train lines"""
import collections
from enum import IntEnum
import logging

from models import Station, Train


logger = logging.getLogger(__name__)


class Line:
    """Contains Chicago Transit Authority (CTA) Elevated Loop Train ("L") Station Data"""

    colors = IntEnum("colors", "blue", start=0)

    def __init__(self, color, station_data, num_trains=10):
        self.color = color
        self.num_trains = num_trains
        self.stops = self._build_line_data(station_data)
        self.trains = self._build_trains()

    def _build_line_data(self, station_df):
        """Constructs all stations on the line"""
        stations = station_df["STATION_NAME"].unique()
        line = [Station(stations[0])]
        prev_station = line[0]
        for station in stations[1:]:
            new_station = Station(station, prev_station)
            prev_station.dir_b = new_station
            prev_station = new_station
            line.append(new_station)
        return line

    def _build_trains(self):
        """Constructs and assigns train objects to stations"""
        trains = []
        for trainID in range(self.num_trains):
            trains.append(Train(f"BL{trainID}", Train.status.in_service))
        import pprint
        pprint.pprint(trains)
        return trains
