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

