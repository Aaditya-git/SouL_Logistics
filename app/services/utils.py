from geopy.distance import geodesic

def calculate_distance(coord1: str, coord2: str) -> float:
    loc1 = tuple(map(float, coord1.split(',')))
    loc2 = tuple(map(float, coord2.split(',')))
    return geodesic(loc1, loc2).km
