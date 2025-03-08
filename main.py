from MILPModel import MILPModel

#Number of robots and tasks
number_of_robots = 3
number_of_tasks = 7

model = MILPModel(number_of_robots, number_of_tasks)

#Setup -----------------------------------

#Robots
model.get_robot(1).set_start_position(2,0)
model.get_robot(2).set_start_position(4,0)
model.get_robot(3).set_start_position(6,0)
model.get_robot(3).set_navigation('AGV')
model.get_robot(3).set_route(1)

#Task 1
model.get_task(1).set_available_time(100)
model.get_task(1).set_duration(100)
model.get_task(1).set_start_position(1, 5)
model.get_task(1).set_end_position(1, 20)
model.get_task(1).set_force_robot(2)

#Task 2
model.get_task(2).set_available_time(200)
model.get_task(2).set_duration(200)
model.get_task(2).set_start_position(3, 5)
model.get_task(2).set_end_position(3, 20)

#Task 3
model.get_task(3).set_available_time(300)
model.get_task(3).set_duration(200)
model.get_task(3).set_start_position(5, 5)
model.get_task(3).set_end_position(5, 20)
model.get_task(3).add_restrict_robot(1)

#Task 4
model.get_task(4).set_available_time(300)
model.get_task(4).set_duration(100)
model.get_task(4).set_start_position(7, 5)
model.get_task(4).set_end_position(7, 20)
model.get_task(4).add_precedent(3)
model.get_task(4).add_navigation_constraint(1)
model.get_task(4).set_force_robot(2)

#Task 5
model.get_task(5).set_available_time(600)
model.get_task(5).set_duration(50)
model.get_task(5).set_start_position(7, 25)
model.get_task(5).set_end_position(7, 30)
model.get_task(5).add_navigation_constraint(1)
model.get_task(5).add_restrict_robot(1)

#Task 6
model.get_task(6).set_available_time(800)
model.get_task(6).set_duration(400)
model.get_task(6).set_start_position(1, 40)
model.get_task(6).set_end_position(10, 40)
model.get_task(6).add_navigation_constraint(1)
model.get_task(6).set_number_of_robots(2)

#Task 7
model.get_task(7).set_available_time(900)
model.get_task(7).set_duration(600)
model.get_task(7).set_start_position(12, 40)
model.get_task(7).set_end_position(12, 5)
model.get_task(7).add_navigation_constraint(1)

model.run()

print(f'Total time: {model.total_time}')
print(f'Total delay: {model.total_delay}')
print(model.results)