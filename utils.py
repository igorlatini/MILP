import math
from typing import Literal, Sequence


def travel_time_position(p1: Sequence[float], p2: Sequence[float], v: float, type: Literal['EUCLIDEAN', 'MANHATTAN'] = 'EUCLIDEAN'):
    if v <= 0:
        raise ValueError("Invalid speed")
    if type == 'EUCLIDEAN':
        return round(math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)/v, 2)
    elif type == 'MANHATTAN':
        return round((abs(p2[0] - p1[0]) + abs(p2[1] - p1[1])) /v, 2)

def travel_time_distance(d: float, v: float):
    if v <= 0:
        raise ValueError("Invalid speed")
    return round(d/v, 2)