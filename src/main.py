#from file_reader import FileReader

#data = FileReader().read_power_stations_coordinates("testData.txt")
#print(data)

from report_generator import ReportGenerator
report = ReportGenerator('graf')

report.add_graph_points([2, 3, 7, 16])
report.set_params(333, 333, 333, 333, 333, 333)

report.generate_graph()