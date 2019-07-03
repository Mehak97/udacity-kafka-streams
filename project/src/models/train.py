"""Defines the train type used in the simulation"""

from enum import IntEnum

class Train:
    """Contains information pertaining to a CTA train"""
    status = IntEnum("status", "out_of_service in_service mechanical_failure", start=0)

    def __init__(self, train_number):
        self.train_number = train_number
        self.station = None
        self.status = Train.status.out_of_service
