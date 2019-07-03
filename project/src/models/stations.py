"""Methods pertaining to loading and configuring CTA "L" station data."""
import collections
import json
import logging
import os

import pandas as pd


logger = logging.getLogger(__name__)


class Stations:
    """Contains Chicago Transit Authority (CTA) Elevated Loop Train ("L") Station Data"""

    def __init__(self):
        self.raw_df = pd.read_csv(
            f"{os.path.dirname(os.path.abspath(__file__))}/data/cta_stations.csv"
        ).sort_values("STOP_ID")
        self.blue_line = self._build_line_data(self.raw_df[self.raw_df["BLUE"]])
        self.red_line = self._build_line_data(self.raw_df[self.raw_df["RED"]])
        self.brown_line = self._build_line_data(self.raw_df[self.raw_df["BRN"]])
        self.green_line = self._build_line_data(self.raw_df[self.raw_df["G"]])
        self.purple_line = self._build_line_data(self.raw_df[self.raw_df["P"]])
        self.yellow_line = self._build_line_data(self.raw_df[self.raw_df["Y"]])
        self.pink_line = self._build_line_data(self.raw_df[self.raw_df["Pnk"]])
        self.orange_line = self._build_line_data(self.raw_df[self.raw_df["O"]])


    def _build_linked_list(self, stations):
        """Transforms a list of stations into a linked list of stations with ordering"""
        # TODO
        return stations

    def _build_line_data(self, station_df):
        line = {
            "stations": {},
            "directions": collections.defaultdict(list)
        }
        stations = station_df["STATION_NAME"].unique()
        for station in stations:
            stops = station_df[station_df["STATION_NAME"] == station]
            stop_data = collections.defaultdict(list)
            for _, stop in stops.iterrows():
                stop_info = {
                    "name": stop["STOP_NAME"],
                    "station": station,
                    "direction": stop["DIRECTION_ID"],
                    "id": stop["STOP_ID"]
                }
                stop_data[stop["DIRECTION_ID"]].append(stop_info)
                line["directions"][stop["DIRECTION_ID"]].append(stop_info)
            line["stations"][station] = stop_data
        return line


if __name__ == "__main__":
    print(json.dumps(Stations().blue_line, indent=2))
