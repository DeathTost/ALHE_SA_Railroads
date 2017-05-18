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

    def get_random_rail_segment(self):
        random_rail_segment = sample(self.rail_segments,1)
        return random_rail_segment
