class FlightData:
    def __init__(self, day_of_month, day_of_week, carrier, origin, destination, dep_time_blk, distance):
        self.data = {
            'DAY_OF_MONTH': [day_of_month],
            'DAY_OF_WEEK': [day_of_week],
            'OP_UNIQUE_CARRIER': [carrier],
            'ORIGIN': [origin],
            'DEST': [destination],
            'DEP_TIME_BLK': [dep_time_blk],
            'DISTANCE': [distance]
        }

    def get_data(self):
        return self.data
