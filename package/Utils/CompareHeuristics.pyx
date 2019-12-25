import random

from Algorithms.Astar import Astar

from package.Model import Heuristic
from package.Model.Heuristic import get_heuristic_by_name
from package.Utils import Tiles
from package.Utils.Parameters import MIN_DISTANCE, MAX_DISTANCE, GOAL, TIMEOUT

def compare(input_size):
    x = []
    y = []
    input_list = generate_input_list(input_size)
    for name in Heuristic.Name:
        average_expanded_nodes = 0
        average_length = 0
        terminated = 0
        algorithm = Astar(get_heuristic_by_name(name))

        for input in input_list:
            algorithm.solve(input, TIMEOUT)
            average_expanded_nodes += algorithm.expanded_nodes
            if algorithm.terminated:
                terminated += 1
            else:
                average_length += len(algorithm.solution) - 2

        print("Heuristic:", algorithm.heuristic.__class__.__name__)
        print("Terminated:", terminated)
        if terminated < input_size:
            print("Average solution length:", average_length / (input_size - terminated))

        print("Average expanded nodes:", average_expanded_nodes / input_size)
        # print("Solution time", algorithm.solution_time)
        # print("Solution", algorithm.solution)
        x.append(algorithm.heuristic.__class__.__name__)
        y.append(average_expanded_nodes / input_size)
        print()
    return x, y


def generate_input_list(number):
    input_list = []
    i = 0
    while i < number:
        distance_to_goal = random.randint(MIN_DISTANCE, MAX_DISTANCE)
        # distance_to_goal = 15
        print("Distance to goal", distance_to_goal)
        input = Tiles.random_walk(GOAL, distance_to_goal)
        input_list.append(input)
        i += 1

    return input_list