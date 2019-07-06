

class Station:

    def __init__(self):
        pass

    @classmethod
    def from_message(cls, message):
        """Given a Kafka message, creates and returns a station"""
        v = message.value()
        return Station(
                station_id = v.station_id
