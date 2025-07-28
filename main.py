from MILPModel import MILPModel

#Number of robots and tasks
number_of_robots = 2
number_of_tasks = 16

model = MILPModel(number_of_robots, number_of_tasks)

#Setup -----------------------------------

#Robots
model.get_robot(1).set_start_position(0.6,6.38)
model.get_robot(2).set_start_position(18.43,7.26)


for i in range(16):
    model.get_task(i+1).set_start_position(0, 5.15)
    model.get_task(i+1).set_end_position(0, 0)

#Task 1
model.get_task(1).set_available_time(400)
model.get_task(1).set_duration(201.49)

#Task 2
model.get_task(2).set_available_time(800)
model.get_task(2).set_duration(216.18)

#Task 3
model.get_task(3).set_available_time(1200)
model.get_task(3).set_duration(235.66)

#Task 4
model.get_task(4).set_available_time(1600)
model.get_task(4).set_duration(288.46)

#Task 5
model.get_task(5).set_available_time(2000)
model.get_task(5).set_duration(306.72)

#Task 6
model.get_task(6).set_available_time(2400)
model.get_task(6).set_duration(329.2)

#Task 7
model.get_task(7).set_available_time(800)
model.get_task(7).set_duration(201.49)

#Task 8
model.get_task(8).set_available_time(1600)
model.get_task(8).set_duration(216.18)

#Task 9
model.get_task(9).set_available_time(2400)
model.get_task(9).set_duration(235.66)

#Task 10
model.get_task(10).set_available_time(3200)
model.get_task(10).set_duration(288.46)

#Task 11
model.get_task(11).set_available_time(4000)
model.get_task(11).set_duration(306.72)

#Task 12
model.get_task(12).set_available_time(4800)
model.get_task(12).set_duration(329.2)

#Task 13
model.get_task(13).set_available_time(2800)
model.get_task(13).set_duration(347.38)

#Task 14
model.get_task(14).set_available_time(3200)
model.get_task(14).set_duration(369.64)

#Task 15
model.get_task(15).set_available_time(5600)
model.get_task(15).set_duration(347.38)

#Task 16
model.get_task(16).set_available_time(6400)
model.get_task(16).set_duration(369.64)


model.run()

print(f'Total time: {model.total_time}')
print(f'Total delay: {model.total_delay}')
print(model.results)

print('----------------')
print(f'Total variables: {len(model.variables)}')
print(f'Total constraints: {len(model.constraints)}')