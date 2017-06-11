from src.file_reader import FileReader
from src.simulated_annealing import SimulatedAnnealing
from src.report_generator import ReportGenerator

test_file_name = "testData.txt"
arg_file_name = "args.txt"

args = FileReader().read_arguments(arg_file_name)
print(args)
for arg in args:
    max_iteration = arg[0]
    starting_temp = arg[1]
    final_temp = arg[2]
    alpha = arg[3]

rail_cost = FileReader().read_railway_unit_cost(test_file_name)
traction_cost = FileReader().read_electric_traction_unit_cost(test_file_name)
power_plant_coords = FileReader().read_power_stations_coordinates("testData.txt")
print("POWER PLANT")
print(power_plant_coords)

cities_coords = FileReader().read_cities_coordinates("testData.txt")
print("CITIES")
print(cities_coords)



print("RUN ALGORITHM")
#cities_coords, power_plant_coords, given_max_iteration,rail_cost, electric_cost, given_final_temperature, given_starting_temperature, alpha
heuristic = SimulatedAnnealing(cities_coords,power_plant_coords,max_iteration,rail_cost,traction_cost,final_temp,starting_temp,alpha)
heuristic.run_algorithm()




report = ReportGenerator()

#report.generate_best_railroad(heuristic.best_tree, cities_coords, power_plant_coords, rail_cost, traction_cost, "asd")

costs = [1, 2, 3, 8]
#report.generate_diagram(costs, "asd")

report.generate_average_diagram([1,2,3],[4,4,4],[5,6,7], "asd")




'''
print("\n\n\nBEST TREE")
for segment in heuristic.best_tree.rail_segments:
    print("CONNECTED CITIES")
    print(segment.cities)
   # print("SEGMENT LENGTH")
   # print(segment.length())

print("\n\n\nPOWER PLANTS")
for segment in heuristic.best_tree.rail_segments:
    if segment.is_power_plant_connected:
        for power_plant_connection in segment.power_plant_connection:
            print("COORDS:")
            print(segment.power_plant_coords)
            print("CONNECTION")
            print(power_plant_connection)
            print("LENGTH")
            print(segment.power_plant_connection_length)

heuristic.best_tree.evaluate_goal_function(4,2)
print("FINAL NETWORK SIZE")
lengths = heuristic.best_tree.get_rails_and_electric_traction_length()
print(lengths[1]*heuristic.power_cost + lengths[0]*heuristic.railway_cost)
print("Q FUNCTION")
print(heuristic.q(heuristic.best_tree))
print("GOAL")
print(heuristic.best_tree.goal_function)


report = ReportGenerator("asd")

report.generate_best_railroad(heuristic.best_tree)

'''
'''
report = ReportGenerator()
costs = [1, 2, 3, 8]
report.generate_diagram(costs, "asd")
'''


