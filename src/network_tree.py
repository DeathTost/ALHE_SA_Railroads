from src.math_utils import distance, projection_nearest_point_on_plane
from src.network_segment import NetworkSegment
from random import sample

class NetworkTree:

    def __init__(self):
        self.goal_function = 0
        self.rail_segments = []
        self.power_plant_segments = {}

    def evaluate_goal_function(self, rail_cost, power_cost):
        self.goal_function = 0
        for rail_segment in self.rail_segments:
            self.goal_function += rail_segment.length() * rail_cost

            if rail_segment.is_power_plant_connected:
                for power_line_length in rail_segment.power_plant_connection_length:
                    self.goal_function += power_line_length * power_cost

        self.goal_function = 1.0 / self.goal_function
        return self.goal_function

    def generate_neighbour(self):
        new_segment = self.add_random_rail_segment()
        new_segment_city = new_segment.cities.copy().pop()
        network_cycle = self.find_cycle(new_segment_city)
        network_cycle.remove(new_segment)   #we want a tree with a new segment so we need to remove it from the search
        segment_to_remove = sample(network_cycle,1).pop()
        self.rail_segments.remove(segment_to_remove)

        if segment_to_remove.is_power_plant_connected:
            for power_plant_coord in segment_to_remove.power_plant_coords:
                self.connect_power_plant(power_plant_coord)

        new_segment_cities = new_segment.get_segment_points()
        new_cityA = new_segment_cities.pop()
        new_cityB = new_segment_cities.pop()

        for power_plant in self.power_plant_segments:
            connection_point_between_cities, power_plant_distance = projection_nearest_point_on_plane(power_plant,new_cityA,new_cityB)
            current_rail_segment = self.power_plant_segments[power_plant]

            if power_plant_distance < current_rail_segment.distance_to_power_plant(power_plant):
                self.unlink_power_plant_from_segment(current_rail_segment,power_plant)
                self.link_power_plant_to_segment(new_segment,power_plant,connection_point_between_cities)


    def add_new_rail_segment(self,rail_segment):
        self.rail_segments.append(rail_segment)

    def add_random_rail_segment(self):
        adjacency_list = self.get_adjacency_list()
        all_city_points = set(adjacency_list.keys())
        unchecked_points = all_city_points.copy()
        random_city = None
        not_neighbour_cities = None
        new_segment = None

        while unchecked_points:
            random_city = sample(unchecked_points,1).pop()
            unchecked_points.remove(random_city)
            city_neighbours = adjacency_list[random_city]
            not_neighbour_cities = (all_city_points - city_neighbours)
            not_neighbour_cities.remove(random_city)
            if not_neighbour_cities:
                break

        if not_neighbour_cities:
            new_neighbour_city = sample(not_neighbour_cities,1).pop()
            new_segment = NetworkSegment(random_city,new_neighbour_city)
            self.add_new_rail_segment(new_segment)
        else:
            pass

        return new_segment

    def get_adjacency_list(self):
        adjacency_list = {}
        for segment in self.rail_segments:
            cities = segment.cities.copy()
            cityA = cities.pop()
            cityB = cities.pop()
            if cityA not in adjacency_list:
                adjacency_list[cityA] = set()
            if cityB not in adjacency_list:
                adjacency_list[cityB] = set()
            adjacency_list[cityA].add(cityB)
            adjacency_list[cityB].add(cityA)
        return adjacency_list

    def find_cycle(self,starting_city_point):
        queue_list = [starting_city_point]
        adjacency_list =self.get_adjacency_list()
        visited_cities = set()
        visited_cities.add(starting_city_point)
        history_parents = dict()
        history_parents[starting_city_point] = None
        found_cycle = None

        while queue_list and not found_cycle: #queue is not empty and we havent found it yet

            parent = queue_list.pop()
            for child in adjacency_list[parent]:    #search all children of current node
                if child in visited_cities and child != history_parents[parent]:    #we previously viisted that city and it isnt our parent
                    found_cycle = list()
                    found_cycle.append(self.get_segment_with_given_cities(parent,child))
                    previously_visited_child = child
                    child = parent
                    parent = history_parents[parent]
                    while parent is not previously_visited_child:
                        found_cycle.append(self.get_segment_with_given_cities(parent,child))
                        child = parent
                        if not history_parents[parent]: #we found starting point because he has no parents
                            break
                        parent = history_parents[parent]

                    if parent is not previously_visited_child:  #we need to connect our starting point and previously visited child
                        child = parent
                        parent = previously_visited_child
                        found_cycle.append(self.get_segment_with_given_cities(parent,child))
                        break

                elif child not in visited_cities:
                    visited_cities.add(child)
                    history_parents[child] = parent
                    queue_list.append(child)

        return found_cycle

    def connect_power_plant(self, power_plant_coord):
        min_distance = float("inf")
        min_distance_point = None
        min_distance_segment = None

        for segment in self.rail_segments:
            cities = segment.get_segment_points()
            cityA = cities.pop()
            cityB = cities.pop()
            connection_point_between_cities, dist = projection_nearest_point_on_plane(power_plant_coord,cityA,cityB)

            if dist < min_distance:
                min_distance = dist
                min_distance_point = connection_point_between_cities
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
            connection_point_between_cities, power_plant_distance = projection_nearest_point_on_plane(power_plant,cityA,cityB)
            traction_segment = NetworkSegment(power_plant,connection_point_between_cities)
            segment.attach_power_plant_to_segment(power_plant,traction_segment,power_plant_distance)

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
