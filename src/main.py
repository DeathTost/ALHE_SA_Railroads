from file_reader import FileReader

data = FileReader().read_power_stations_coordinates("testData.txt")
print(data)