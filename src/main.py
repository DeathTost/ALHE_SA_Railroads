from src.file_reader import FileReader
from src.simulated_annealing import SimulatedAnnealing
from src.report_generator import ReportGenerator
import os.path

#files and paths
test_file_name = "data_groups_2"
arg_file_name = "args"
folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'res'))
arg_file_path = folder_path + "\\" + arg_file_name+".txt"
test_file_path = folder_path + "\\" + test_file_name+".txt"

#loading arguments
args = FileReader().read_arguments(arg_file_path)
for arg in args:
    max_iteration = arg[0]
    starting_temp = arg[1]
    final_temp = arg[2]
    alpha = arg[3]

rail_cost = FileReader().read_railway_unit_cost(test_file_path)
traction_cost = FileReader().read_electric_traction_unit_cost(test_file_path)
power_plant_coords = FileReader().read_power_stations_coordinates(test_file_path)
cities_coords = FileReader().read_cities_coordinates(test_file_path)


#heursitic results
results = []
for i in range(20):
    heuristic = SimulatedAnnealing(cities_coords, power_plant_coords, max_iteration, rail_cost, traction_cost,
                                   final_temp, starting_temp, alpha)
    result = heuristic.run_algorithm()
    heuristic.best_tree.evaluate_goal_function(rail_cost,traction_cost)
    report = ReportGenerator()
    report.generate_best_railroad(heuristic.best_tree,cities_coords,power_plant_coords,rail_cost,traction_cost,test_file_name,i)
    results.append(result)

#process all results
values_per_iteration = {}

for result in results:
    for i, goal in enumerate(result):
        values_per_iteration.setdefault(i,[]).append(goal)

min_per_iteration = []
avg_per_iteration = []
max_per_iteration = []
step = int(len(values_per_iteration)/10)

for i, iteration in enumerate(values_per_iteration.keys()):
    values = values_per_iteration[iteration]
    avg_value = sum(values)/len(values)
    min_value = 0 if not (i % step == 1) else avg_value - min(values)
    max_value = 0 if not (i % step == 1) else max(values) - avg_value
    min_per_iteration.append(min_value)
    avg_per_iteration.append(avg_value)
    max_per_iteration.append(max_value)

#average diagram
final_report = ReportGenerator()
final_report.generate_average_diagram(min_per_iteration,max_per_iteration,avg_per_iteration,starting_temp,alpha,test_file_name)

print('DONE')
