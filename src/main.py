from file_reader import FileReader
from simulated_annealing import SimulatedAnnealing
from report_generator import ReportGenerator

power_plant_coords = FileReader().read_power_stations_coordinates("testData.txt")
print("POWER PLANT")
print(power_plant_coords)

cities_coords = FileReader().read_cities_coordinates("testData.txt")
print("CITIES")
print(cities_coords)



print("RUN ALGORITHM")

heuristic = SimulatedAnnealing(cities_coords,power_plant_coords,10,4,2,10,100,0.8)
heuristic.run_algorithm()

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
print("GOAL")
print(heuristic.best_tree.goal_function)


report = ReportGenerator("asd")

report.generate_best_railroad(heuristic.best_tree)