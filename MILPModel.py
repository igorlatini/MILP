# Imports
import pulp
from Robots import Robot
from Tasks import Task
import utils
import matplotlib.pyplot as plt
import time
from itertools import product
import sys

class MILPModel():

    def __init__(self, n_robots, n_tasks):

        if n_robots < 1:
            raise ValueError("Must haveat least one robot")
        
        if n_tasks < 1:
            raise ValueError("Must haveat least one task")

        self.R = range(1, n_robots + 1)  # Set of robots
        self.T = range(1, n_tasks + 1)   # Set of tasks

        #Parameters
        
        self.M = 99999

        self.robots = {}
        self.tasks = {}

        # Create each Robot
        for r in self.R:
            self.robots[r] = Robot(r)

        # Create each Task
        for t in self.T:
            self.tasks[t] = Task(t)
        
        #For results
        self.total_time = 0
        self.results = ''
        self.total_delay = 0


    def get_robot(self, n: int) -> Robot:
        return self.robots[n]

    def get_task(self, n: int) -> Task:
        return self.tasks[n]

    def run(self, generate_graphics = True):

        #For ease of notation
        R = self.R
        T = self.T
        robots = self.robots
        tasks = self.tasks
        M = self.M


        number_of_sequences = 0
        for t in T:
            number_of_sequences += tasks[t].n_robots

        S = range(1, number_of_sequences + 1)   # Set of sequences

        # Problem -----------------------------------------------------------------------------------------
        prob = pulp.LpProblem("Minimize_Delays", pulp.LpMinimize)

        # Variables
        init_time = pulp.LpVariable.dicts("init_time", (S, R, T), lowBound=0, cat='Continuous')
        end_time = pulp.LpVariable.dicts("end_time", (S, R, T), lowBound=0, cat='Continuous')
        allocation = pulp.LpVariable.dicts("allocation", (S, R, T), cat='Binary')
        delay = pulp.LpVariable.dicts("delay", (S, R, T), lowBound=0, cat='Continuous')

        # Objective function
        prob += pulp.lpSum(delay[s][r][t] for s in S for r in R for t in T)

        # Constraints -------------------------------------------------------------------------------------
        # 1 - Each task can be performed a number of times equal to the number of robots necessary to execute it
        for t in T:
            prob += pulp.lpSum(allocation[s][r][t] for s in S for r in R) == tasks[t].n_robots

        # 2 - Each sequence appears only once in all robots and tasks
        for s in S:
            prob += pulp.lpSum(allocation[s][r][t] for r in R for t in T) == 1

        # 3 - Each robot can only execute a task once
        for r in R:
            for t in T:
                prob += pulp.lpSum(allocation[s][r][t] for s in S) <= 1


        # 4 - The end time of each task is equal to its start time plus its duration
        for s in S:
            for r in R:
                for t in T:
                    prob += end_time[s][r][t] == init_time[s][r][t] + tasks[t].duration

        # 5 - Each task must start at least at the time it becomes available
        for s in S:
            for r in R:
                for t in T:
                    prob += init_time[s][r][t] >= tasks[t].available_time

        # 6 - A task can only be started by a robot after the previous one is completed by that robot (including travel time) - Tasks cannot overlap
        for s in S:
            if s > 1:
                for s2 in range(s):
                    if s2 > 0:
                        for r in R:
                            for t1 in T:
                                for t2 in T:
                                    if t1 in tasks[t2].tasks_distance:
                                        prob += init_time[s][r][t1] >= end_time[s2][r][t2] + utils.travel_time_distance(tasks[t2].tasks_distance[t1], robots[r].speed) - M * (1 - allocation[s2][r][t2])
                                    else:
                                        prob += init_time[s][r][t1] >= end_time[s2][r][t2] + utils.travel_time_position(tasks[t2].end_position, tasks[t1].start_position, robots[r].speed) - M * (1 - allocation[s2][r][t2])
            else:
                for r in R:
                    for t in T:
                            prob += init_time[1][r][t] >= utils.travel_time_position(robots[r].start_position, tasks[t].start_position, robots[r].speed) - M * (1 - allocation[1][r][t])

        # 7 - Precedence constraints
        for s1, s2, r1, r2, t1 in product(S, S, R, R, T):
            for t2 in tasks[t1].precedents:
                prob += init_time[s1][r1][t1] >= end_time[s2][r2][t2] - M * (1 - allocation[s2][r2][t2])

        # 8 - Navigation constraints
        for t in T:
            for s in S:
                for r in R:
                    if robots[r].navigation == 'AGV' and robots[r].route not in tasks[t].routes:
                        prob += allocation[s][r][t] == 0

        # 9-  Restrict robots from executing tasks
        for t in T:
            for r in tasks[t].restrict_robots:
                prob += pulp.lpSum(allocation[s][r][t] for s in S) == 0

        # 10 -Force robot to execute specific task
        for t in T:
            if tasks[t].force_robot != None:
                prob += pulp.lpSum(allocation[s][tasks[t].force_robot][t] for s in S) == 1

        # 11 - A task may need more than one robot to be executed
        for s1, s2, r1, r2, t in product(S, S, R, R, T):
            if r1 != r2 and s1 != s2:
                if tasks[t].n_robots > 1:
                    prob += init_time[s1][r1][t] >= init_time[s2][r2][t] - M * (1 - allocation[s2][r2][t])
                    prob += init_time[s2][r2][t] >= init_time[s1][r1][t] - M * (1 - allocation[s1][r1][t])

        # The delay of each task is the start time minus the time it became availables
        for s in S:
            for r in R:
                for t in T:
                    prob += delay[s][r][t] >= (init_time[s][r][t] - tasks[t].available_time - M * (1 - allocation[s][r][t]))/tasks[t].n_robots
                    prob += delay[s][r][t] <= M * allocation[s][r][t]

        # Solve the problem -------------------------------------------------------------------------------
        time_begin = time.time()
        prob.solve()

        
        #print(f'Total time: {time.time() - time_begin}')
        self.total_time = time.time() - time_begin


        if pulp.LpStatus[prob.status] == "Infeasible":
            #print("The problem is infeasible.")
            self.results = 'The problem is infeasible'
            return 

        # Print the results
        for s in S:
            for r in R:
                for t in T:
                    if pulp.value(allocation[s][r][t]) == 1:
                        #print(f"Seq {s} | Robot {r} | Task {t} | Start {pulp.value(init_time[s][r][t])} | End {pulp.value(end_time[s][r][t])}")
                        #print(f"Delay seq {s}: {pulp.value(delay[s][r][t])}")
                        self.results += f"Seq {s} | Robot {r} | Task {t} | Start {pulp.value(init_time[s][r][t])} | End {pulp.value(end_time[s][r][t])} \n"
                        self.results += f"Delay seq {s}: {pulp.value(delay[s][r][t])} \n"

        total_delay = pulp.value(pulp.lpSum(delay[s][r][t] for s in S for r in R for t in T))
        self.total_delay = total_delay
        #print(f"Total delay: {total_delay}")

        # Plotting - Timeline ------------------------------------------------------------------------------
        if generate_graphics:
            tasks_data = []
            colors = plt.get_cmap('tab20', len(T) + 1)  # Get a colormap with enough colors for each task
            for s in S:
                for r in R:
                    for t in T:
                        if pulp.value(allocation[s][r][t]) == 1:
                            start_time_value = pulp.value(init_time[s][r][t])
                            end_time_value = pulp.value(end_time[s][r][t])
                            tasks_data.append((r, t, start_time_value, end_time_value))

            # Create a figure and axis
            fig, ax = plt.subplots(figsize=(10, 6))

            available_time_plotted = []
            # Plot each task for each robot with different colors
            for r, t, start, end in tasks_data:
                ax.barh(r, end - start, left=start, label=f'Task {t}', color=colors(t))
                # Mark where each task starts to be available
                ax.plot([tasks[t].available_time, tasks[t].available_time], [r - 0.4, r + 0.4], color='red', linestyle='--')
                # Annotate the task with its available time
                if tasks[t].available_time not in available_time_plotted:
                    ax.text(tasks[t].available_time, r+0.45, f'Task {t}', ha='center', va='top', color='black', fontsize=9)
                else:
                    offset = available_time_plotted.count(tasks[t].available_time)
                    ax.text(tasks[t].available_time, r+0.45+0.1*offset, f'Task {t}', ha='center', va='top', color='black', fontsize=9)
                available_time_plotted.append(tasks[t].available_time)

            # Print total delay on the plot
            ax.text(0.5, -0.1, f'Total Delay: {total_delay} s', ha='center', va='top', transform=ax.transAxes, fontsize=12, color='blue')

            # Formatting the timeline
            ax.set_xlabel('Time (s)')
            ax.set_ylabel('Robots')
            ax.set_title('Robot Task Timeline')
            ax.set_yticks(range(1, len(R) + 1))  # Set Y axis to integers only
            ax.set_yticklabels(range(1, len(R) + 1))  # Ensure Y axis labels are integers

            # Sort both labels and handles by labels
            handles, labels = ax.get_legend_handles_labels()
            unique_labels = dict(zip(labels, handles))  # Remove duplicates
            sorted_labels = sorted(unique_labels.keys(), key=lambda x: int(x.split()[1]))
            sorted_handles = [unique_labels[label] for label in sorted_labels]
            ax.legend(sorted_handles, sorted_labels)

            # Adjust margin
            ax.use_sticky_edges = False
            ax.set_xmargin(0.1)

            # Show the plot
            plt.show()

            # Plotting - Positioning  --------------------------------------------------------------------------
            # Create a new figure for the start and end positions of tasks and robot initial positions
            fig2, ax2 = plt.subplots(figsize=(10, 6))

            # Plot the initial positions of each robot
            for r in R:
                init_pos = robots[r].start_position
                ax2.plot(init_pos[0], init_pos[1], 'bo')  # Blue dot for robot initial position
                ax2.text(init_pos[0], init_pos[1], f'Robot {r}', fontsize=12, ha='right')

            # Plot the start and end positions of each task
            for t in T:
                start_pos = tasks[t].start_position
                end_pos = tasks[t].end_position
                ax2.plot(start_pos[0], start_pos[1], 'go')  # Green dot for start position
                ax2.plot(end_pos[0], end_pos[1], 'ro')  # Red dot for end position
                ax2.text(start_pos[0], start_pos[1], f'Start {t}', fontsize=12, ha='right')
                ax2.text(end_pos[0], end_pos[1], f'End {t}', fontsize=12, ha='right')
                # Draw an arrow from start to end position
                ax2.annotate('', xy=end_pos, xytext=start_pos, arrowprops=dict(arrowstyle='->', color='blue', lw=1.5))

            # Formatting the plot
            ax2.set_xlabel('X Position')
            ax2.set_ylabel('Y Position')
            ax2.set_title('Start and End Positions of Tasks and Robots Initial Positions')
            ax2.legend()
            ax2.grid()

            # Show the plot
            plt.show()

