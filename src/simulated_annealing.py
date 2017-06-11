from src.network_tree import NetworkTree
from src.network_segment import NetworkSegment
from random import sample, random
from math import exp, fabs
import copy

class SimulatedAnnealing:

    def __init__(self, cities_coords, power_plant_coords, given_max_iteration,
                 rail_cost, electric_cost, given_final_temperature, given_starting_temperature, alpha):
        self.history = []

        self.cities_coords = cities_coords
        self.power_plant_coords =power_plant_coords

        self.max_iteration = given_max_iteration
        self.current_iteration = 0
        self.railway_cost = rail_cost
        self.power_cost = electric_cost
        self.final_temperature = given_final_temperature
        self.current_temperature = given_starting_temperature
        self.alpha = alpha

        self.working_tree = self.generate_starting_tree()
        self.best_tree = self.working_tree

    def run_algorithm(self):
        history = []
        history.append(self.working_tree)
        goal_per_iteration = []
        goal_per_iteration.append(self.working_tree.goal_function)

        while not self.is_end_condition():
            y = self.generate_random_neighbour()
            if self.q(y) > self.q(self.working_tree):
                self.working_tree = y
                if self.q(self.working_tree) > self.q(self.best_tree):
                    self.best_tree = self.working_tree
            else:
                p_a = self.calculate_pa_parameter(self.q(y), self.q(self.working_tree), self.current_temperature)
                if random() < p_a:
                    self.working_tree = y
            history.append(y)
            self.current_iteration += 1
            self.current_temperature = self.current_temperature * self.alpha

            self.working_tree.evaluate_goal_function(self.railway_cost,self.power_cost)
            goal_per_iteration.append(self.working_tree.goal_function)

        return goal_per_iteration

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

    def is_end_condition(self):
        if self.current_iteration == self.max_iteration:
            print('Finished iterations')
            print(self.current_iteration)
            return True
        if self.current_temperature < self.final_temperature:
            print('Finished temperature')
            print(self.current_iteration)
            return True
        return False

    def q(self, point):
        return point.evaluate_goal_function(self.railway_cost,self.power_cost )

    def calculate_pa_parameter(self, q_y, q_working_tree, temperature):
        difference = fabs(q_y - q_working_tree)
        return exp(-1*difference/temperature)

    def generate_random_neighbour(self):
        random_neighbour = NetworkTree()

        rails_count = len(self.working_tree.rail_segments)

        for segment_number in range(rails_count):
            random_neighbour.add_new_rail_segment(copy.deepcopy(self.working_tree.rail_segments[segment_number]))

        random_neighbour.generate_neighbour()
        return random_neighbour