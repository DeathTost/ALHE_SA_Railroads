from math import sqrt

def vector(point1_coords, point2_coords):
    a,b,c = point1_coords
    x,y,z = point2_coords
    return x - a, y - b, z - c

def vector_length(vect):
    x,y,z = vect
    return sqrt((x**2)+(y**2)+(z**2))

def distance(point1,point2):
    return vector_length(vector(point1,point2))

def translate_vector(point1,point2):
    a,b,c = point1
    x,y,z = point2
    return a + x, b + y, c + z

def scale_vector(vect, scale):
    x,y,z = vect
    return x * scale, y * scale, z * scale

def dot_product(vect1 , vect2):
    x,y,z = vect1
    a,b,c = vect2
    return x * a + y * b + z * c

def unit_vector(vect):
    x,y,z = vect
    length = vector_length(vect)
    return x / length, y / length, z / length


def clamp(point_length):
    if point_length > 1.0:
        point_length = 1.0
    elif point_length < 0.0:
        point_length = 0.0
    return point_length

def projection_nearest_point_on_segment_to_power_plant(power_plant,cityA,cityB):
    segment_vector = vector(cityA,cityB)
    power_plant_vector = vector(cityA,power_plant)
    segment_unit_vector = unit_vector(segment_vector)
    segment_vector_length = vector_length(segment_vector)
    scaled_power_plant_vector = scale_vector(power_plant_vector, 1.0 / segment_vector_length)
    point_between_cities_vector = dot_product(segment_unit_vector,scaled_power_plant_vector)
    point_between_cities_vector = clamp(point_between_cities_vector)
    point_between_cities = scale_vector(segment_vector, point_between_cities_vector)
    distance_to_power_plant = distance(point_between_cities, power_plant_vector)
    point_between_cities = translate_vector(point_between_cities, cityA)
    return point_between_cities, distance_to_power_plant

def projection_nearest_point_on_plane(power_plant,cityA,cityB):
    (a,b,c), point_distance = projection_nearest_point_on_segment_to_power_plant(power_plant + (0,),cityA + (0,), cityB + (0,))
    return (a,b), point_distance