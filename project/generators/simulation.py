"""Defines a time simulation responsible for executing any registered
generators
"""
import datetime
import time
from enum import IntEnum
import logging
import logging.config
import os

import pandas as pd

# Import logging before models to ensure configuration is picked up
logging.config.fileConfig(f"{os.path.dirname(os.path.abspath(__file__))}/logging.ini")

from models import Line


logger = logging.getLogger(__name__)


class TimeSimulation:
    weekdays = IntEnum('weekdays', 'mon tue wed thu fri sat sun', start=0)
    ten_min_frequency = datetime.timedelta(minutes=10)

    def __init__(self, schedule=None):
        """Initializes the time simulation"""
        # Read data from disk
        self.raw_df = pd.read_csv(
            f"{os.path.dirname(os.path.abspath(__file__))}/data/cta_stations.csv"
        ).sort_values("MAP_ID")

        # Define the train schedule (same for all trains)
        self.schedule = schedule
        if schedule is None:
            self.schedule = {
                TimeSimulation.weekdays.mon: {0: TimeSimulation.ten_min_frequency},
                TimeSimulation.weekdays.tue: {0: TimeSimulation.ten_min_frequency},
                TimeSimulation.weekdays.wed: {0: TimeSimulation.ten_min_frequency},
                TimeSimulation.weekdays.thu: {0: TimeSimulation.ten_min_frequency},
                TimeSimulation.weekdays.fri: {0: TimeSimulation.ten_min_frequency},
                TimeSimulation.weekdays.sat: {0: TimeSimulation.ten_min_frequency},
                TimeSimulation.weekdays.sun: {0: TimeSimulation.ten_min_frequency}
            }

        self.blue_line = Line(Line.colors.blue, self.raw_df[self.raw_df["BLUE"]])
        #self.red_line = self._build_line_data(self.raw_df[self.raw_df["RED"]])
        #self.brown_line = self._build_line_data(self.raw_df[self.raw_df["BRN"]])
        #self.green_line = self._build_line_data(self.raw_df[self.raw_df["G"]])
        #self.purple_line = self._build_line_data(self.raw_df[self.raw_df["P"]])
        #self.yellow_line = self._build_line_data(self.raw_df[self.raw_df["Y"]])
        #self.pink_line = self._build_line_data(self.raw_df[self.raw_df["Pnk"]])
        #self.orange_line = self._build_line_data(self.raw_df[self.raw_df["O"]])

    def run(self):
        curr_time = datetime.datetime.utcnow().replace(hour=0, minute=0, second=0,
                microsecond=0)
        logger.info("Beginning simulation, press Ctrl+C to exit at any time")
        try:
            while True:
                dow = curr_time.weekday()
                logger.debug(f"simulation running.. {curr_time.isoformat()}, hour: {curr_time.hour}")
                logger.debug(self.blue_line)
                curr_time = curr_time + datetime.timedelta(minutes=3)
                time.sleep(1)
                self.blue_line.advance()
        except KeyboardInterrupt as e:
            logger.info("Shutting down")


if __name__ == "__main__":
    TimeSimulation().run()
