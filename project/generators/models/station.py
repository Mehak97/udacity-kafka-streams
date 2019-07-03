"""Methods pertaining to loading and configuring CTA "L" station data."""
import logging


logger = logging.getLogger(__name__)


class Station:
    """Defines a single station"""

    def __init__(self, name, direction_a=None, direction_b=None):
        self.name = name
        self.dir_a = direction_a
        self.dir_b = direction_b
        self.a_train = None
        self.b_train = None

    def __str__(self):
        return "Station | {:<30} | Direction A: | {:^5} | departing to {:<30} | Direction B: | {:^5} | departing to {:<30} | ".format(
            self.name,
            self.a_train.train_id if self.a_train is not None else "---",
            self.dir_a.name if self.dir_a is not None else "---",
            self.b_train.train_id if self.b_train is not None else "---",
            self.dir_b.name if self.dir_b is not None else "---",
        )

    def __repr__(self):
        return str(self)

    def arrive_a(self, train):
        self.a_train = train
        self.a_train.arrive(self)

    def arrive_b(self, train):
        self.b_train = train
        self.b_train.arrive(self)
