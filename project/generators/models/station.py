"""Methods pertaining to loading and configuring CTA "L" station data."""
import logging


logger = logging.getLogger(__name__)


class Station:
    """Defines a single station"""

    def __init__(self, name, direction_a=None, direction_b=None):
        self.name = name
        self.dir_a = direction_a
        self.dir_b = direction_b

    def __str__(self):
        return "Station: {}, Direction A: {}, Direction B: {}".format(
            self.name,
            self.dir_a.name if self.dir_a is not None else "---",
            self.dir_b.name if self.dir_b is not None else "---",
        )

    def __repr__(self):
        return str(self)
