"""Defines functionality relating to train lines"""
from enum import IntEnum

class Line:
    """Represents a line on the CTA "EL" Train, eg Blue, Red, Brown, etc."""

    colors = IntEnum("colors", "blue", start=0)
    def __init__(self, color, stations, num_trains, schedule=None):
        self.color = color
        self.stations = stations
        self.num_trains = num_trains
        self.schedule = schedule
        if self.schedule == None:
            self.schedule = {}
