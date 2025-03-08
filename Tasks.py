#Task

class Task:
    
    def __init__(self, id: int):
        self.id = id
        self.available_time = 0
        self.duration = 1
        self.start_position = (0,0)
        self.end_position = (0,0)
        self.precedents = []
        self.routes = []
        self.n_robots = 1
        self.restrict_robots = []
        self.force_robot = None
        self.tasks_distance = {}
    
    def set_available_time(self, available_time: float):
        self.available_time = available_time

    def set_duration(self, duration: float):
        self.duration = duration

    def set_start_position(self, x: float, y: float):
        self.start_position = (x, y)
    
    def set_end_position(self, x: float, y: float):
        self.end_position = (x, y)
    
    def add_precedent(self, task: int):
        self.precedents.append(task)
    
    def add_navigation_constraint(self, route: int):
        self.routes.append(route)
    
    def set_number_of_robots(self, n_robots: int):
        self.n_robots = n_robots
    
    def add_restrict_robot(self, robot: int):
        self.restrict_robots.append(robot)
    
    def set_force_robot(self, robot: int):
        self.force_robot = robot
    
    def set_distance(self, task: int, distance: float):
        self.tasks_distance[task] = distance