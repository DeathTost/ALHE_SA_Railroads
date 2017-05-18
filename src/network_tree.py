from src.math_utils import distance, projection_nearest_point_on_plane
from src.network_segment import NetworkSegment
from random import sample

class NetworkTree:

    def __init__(self):
        self.goal_function = 0
        self.rail_segments = []
        self.power_plant_segments = {}

    def evaluate_goal_function(self, rail_cost, power_cost):
        print("Goal function")

    def add_new_rail_segment(self,rail_segment):
        self.rail_segments.append(rail_segment)

    def connect_power_plant(self, power_plant_coord):
        min_distance = float("inf")
        min_distance_point = None
        min_distance_segment = None

        for segment in self.rail_segments:
            cities = segment.get_segment_points()
            cityA = cities.pop()
            cityB = cities.pop()
            point_between_cities, dist = projection_nearest_point_on_plane(power_plant_coord,cityA,cityB)

            if dist < min_distance:
                min_distance = dist
                min_distance_point = point_between_cities
                min_distance_segment = segment

        if min_distance_point is not None:
            self.link_power_plant_to_segment(min_distance_segment,power_plant_coord,min_distance_point)
        else:
            pass

    def link_power_plant_to_segment(self, segment, power_plant, link_point):
        if link_point:
            connection_segment = NetworkSegment(power_plant,link_point)
            segment.attach_power_plant_to_segment(power_plant,connection_segment,distance(power_plant + (0,),link_point + (0,)))
        else:
            cities = segment.get_segment_points()
            cityA = cities.pop()
            cityB = cities.pop()

        self.power_plant_segments[power_plant] = segment

    def unlink_power_plant_from_segment(self,segment,power_plant):
        segment.detach_power_plant_from_segment(power_plant)
        self.power_plant_segments.pop(power_plant)

    def get_segment_with_given_cities(self,cityA,cityB):
        segment = NetworkSegment(cityA,cityB)
        segment_index = self.rail_segments.index(segment)
        found_segment = self.rail_segments[segment_index]
        return found_segment

    def get_random_rail_segment(self):
        random_rail_segment = sample(self.rail_segments,1)
        return random_rail_segment

    def get_rails_and_electric_traction_length(self):
        rails_length = 0
        electric_tractions_length = 0

        for segment in self.rail_segments:
            rails_length += segment.length()
            if segment.is_power_plant_connected:
                for electric_traction in segment.power_plant_connection_length:
                    electric_tractions_length += electric_traction

        return rails_length,electric_tractions_length
