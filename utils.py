import math

def travel_time_position(p1: float, p2: float, v: float):
    if v <= 0:
        raise ValueError("Invalid speed")
    return round(math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)/v, 2)

def travel_time_distance(d: float, v: float):
    if v <= 0:
        raise ValueError("Invalid speed")
    return round(d/v, 2)