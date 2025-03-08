from typing import Literal

class Robot:

    def __init__(self, id: int):
        self.id = id
        self.navigation = 'AMR'
        self.route = 0
        self.speed = 1
        self.start_position = (0,0)

    def set_navigation(self, type: Literal['AGV', 'AMR']):
        self.navigation = type

    def set_speed(self, speed: float):
        if speed < 0:
            raise ValueError("Speed cannot be negative")
        self.speed = speed
    
    def set_route(self, route: int):
        self.route = route
    
    def set_start_position(self, x: float, y: float):
        self.start_position = (x,y)