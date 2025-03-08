# MILP
MILP Model for Robot Task Allocation

1 - Objective: minimize delay to start tasks
2 - One robot can only do one task at a time
3 - One task should be done by one or more robots
4 - Each task can only be completed once
5 - Some tasks can only be done after another is completed - Precedence
6 - Possibility to force a robot to complete a task
7 - Possibility to restrict a robot from completing a task
8 - Constraint for navigation type (route-based)
9 - Tasks may need more than one robot to be executed
10 - Distance between tasks can be calculated via position or direct input

Configuration is done at main: to change it, change the main file