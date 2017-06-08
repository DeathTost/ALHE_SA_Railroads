class FileReader:

    def read_railway_unit_cost(self, file_name):
        f = open(file_name, "r")
        line = f.readline().split()
        f.close()
        return int(line[4])

    def read_electric_traction_unit_cost(self, file_name):
        f = open(file_name, "r")
        line = f.readlines()[1].split()
        f.close()
        return int(line[4])

    def read_arguments(self, file_name):
        file = open(file_name, "r")
        args = []

        for line in file:
            row = ("".join(line.split())).split(",")
            args.append(
                (int(row[0]), float(row[1]), float(row[2]), float(row[3])))

        file.close()
        return args

    def read_coordinates(self, name, file_name):
        f = open(file_name, "r")
        coordinates = set()
        startedLocations = False
        for line in f:
            l = line.rstrip()
            if l:
                word = line.split()
                if startedLocations is True:
                    if len(word) != 2:
                        return coordinates
                    coordinates.add((float(word[0]),(float(word[1]))))
                    # print(word)
                if word[0] == name:
                    startedLocations = True
                    #print(word)


        f.close()
        return coordinates

    def read_cities_coordinates(self, file_name):
        return self.read_coordinates("Miasta:", file_name)

    def read_power_stations_coordinates(self, file_name):
        return self.read_coordinates("Elektrownie:", file_name)
