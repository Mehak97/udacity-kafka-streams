"""Defines a time simulation responsible for executing any registered
generators
"""
import datetime
import time
from enum import IntEnum


class TimeSimulation:
    weekdays = IntEnum('weekdays', 'mon tue wed thu fri sat sun', start=0)

    def __init__(self, schedule=None):
        """Initializes the time simulation"""
        self.schedule = schedule
        if schedule is None:
            self.schedule = {
                TimeSimulation.weekdays.mon: {},
                TimeSimulation.weekdays.tue: {},
                TimeSimulation.weekdays.wed: {},
                TimeSimulation.weekdays.thu: {},
                TimeSimulation.weekdays.fri: {},
                TimeSimulation.weekdays.sat: {},
                TimeSimulation.weekdays.sun: {}
            }


    def run(self):
        try:
            curr_time = datetime.datetime.utcnow().replace(hour=0, minute=0, second=0,
                    microsecond=0)
            while True:
                print(f"simulation running.. {curr_time.isoformat()}")
                curr_time = curr_time + datetime.timedelta(minutes=3)
                time.sleep(1)
        except KeyboardInterrupt as e:
            print("Shutting down")


if __name__ == "__main__":
    TimeSimulation().run()
