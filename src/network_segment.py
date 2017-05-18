
class NetworkSegment:

    def __init__(self,city_point1, city_point2):
        self.cities = []
        self.cities.append(city_point1)
        self.cities.append(city_point2)
        self.is_power_plant_connected = False
        self.power_plant_connection = []
        self.power_plant_connection_length = []
        self.power_plant_coords = []


    def get_segment_points(self):
        points = self.cities.copy()
        return points

