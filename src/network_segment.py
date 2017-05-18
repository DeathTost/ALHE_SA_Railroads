from src.math_utils import distance

class NetworkSegment:
    def __init__(self, city_point1, city_point2):
        self.cities = set()
        self.cities.add(city_point1)
        self.cities.add(city_point2)
        self.is_power_plant_connected = False
        self.power_plant_connection = []
        self.power_plant_connection_length = []
        self.power_plant_coords = []

    def attach_power_plant_to_segment(self, power_plant_coords, connection_segment, connection_length):
        if not self.power_plant_coords:
            self.is_power_plant_connected = True
        self.power_plant_coords.append(power_plant_coords)
        self.power_plant_connection.append(connection_segment)
        self.power_plant_connection_length.append(connection_length)

    def detach_power_plant_from_segment(self,power_plant_coords):
        if power_plant_coords in self.power_plant_coords:
            power_plant_index = self.power_plant_coords.index(power_plant_coords)
            self.power_plant_coords.pop(power_plant_index)
            self.power_plant_connection.pop(power_plant_index)
            self.power_plant_connection_length.pop(power_plant_index)
            if not self.power_plant_coords:
                self.is_power_plant_connected = False

    def get_segment_points(self):
        points = self.cities.copy()
        return points

    def length(self):
        points = self.cities.copy()
        return distance(points.pop() + (0,),points.pop() + (0,))

    def distance_to_power_plant(self,power_plant):
        if power_plant in self.power_plant_coords:
            power_plant_index = self.power_plant_coords.index(power_plant)
            return self.power_plant_connection_length[power_plant_index]
        else:
            return None