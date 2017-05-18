class FileReader:

    def read_railway_unit_cost(self, file_name):
        f = open(file_name, "r")
        line = f.readline().split();
        f.close()
        return int(line[4])

    def read_electric_traction_unit_cost(self, file_name):
        f = open(file_name, "r")
        line = f.readlines()[1].split()
        f.close()
        return int(line[4])

    def read_coordinates(self, name, file_name):
        f = open(file_name, "r")
        coordinates = []
        startedLocations = False
        for line in f:
            l = line.rstrip()
            if l:
                word = line.split()
                if startedLocations is True:
                    if len(word) != 2:
                        return coordinates
                    coordinates.append(word)
                    # print(word)
                if word[0] == name:
                    startedLocations = True
                    #print(word)


        f.close()
        return coordinates

    def read_cities_coordinates(self, file_name):
        return FileReader().read_coordinates("Miasta:", "testData.txt")

    def read_power_stations_coordinates(self, file_name):
        return FileReader().read_coordinates("Elektrownie:", "testData.txt")
