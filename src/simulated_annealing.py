from src.network_tree import NetworkTree
from src.network_segment import NetworkSegment
from random import sample

class SimulatedAnnealing:

    def __init__(self, cities_coords, power_plant_coords, given_max_iteration, rail_cost, electric_cost, given_final_temperature):
        self.history = []

        self.cities_coords = cities_coords
        self.power_plant_coords =power_plant_coords

        self.max_iteration = given_max_iteration
        self.current_iteration = 0
        self.railway_cost = rail_cost
        self.power_cost = electric_cost
        self.final_temperature = given_final_temperature
        self.current_temperature = 0

        self.working_tree = self.generate_starting_tree()
        self.best_tree = self.working_tree


    def run_algorithm(self):
        history = []
        history.append(self.working_tree)
        working_point = self.select_best(history)

        while self.loop_end_condition():
            y = self.select_random(self.generate_neighbours(working_tree))
            if self.q(y) > self.q(working_tree):
                working_point = y
                if self.q(working_tree) > self.q(self.best_tree):
                    self.best_tree = working_tree
            else:
                p_a = self.calculate_pa_parameter(self.q(y), self.q(working_point), temperature)
                if rand() < p_a:
                    working_tree = y
            history.append(y)
        return working_tree

    def generate_starting_tree(self):
        starting_tree = NetworkTree()

        usedCities = set()
        unusedCities = set()

        for city in self.cities_coords:
            unusedCities.add(city)

        while len(unusedCities) != 0:
            new_city = sample(unusedCities,1) #return a list of points (city coord): [(5,4)]
            new_city = new_city.pop(0)        #return a point (city coord): (5,4)
            unusedCities.remove(new_city)

            if len(usedCities) == 0:
                usedCities.add(new_city)
            else:
                old_city = sample(usedCities,1)
                old_city = old_city.pop(0)
                starting_tree.add_new_rail_segment(NetworkSegment(new_city,old_city))
                usedCities.add(new_city)

        for power_plant in self.power_plant_coords:
            starting_tree.connect_power_plant(power_plant)

        starting_tree.evaluate_goal_function(self.railway_cost,self.power_cost)
        return starting_tree



    def select_best(self, history):

    def loop_end_condition(self):

    def select_random(self, neighbours):

    def generate_neighbours(self, working_point):

    def q(self, point):

    def calculate_pa_parameter(q_y, q_working_point, temperature):
