import random
import time

from package.Algorithms.Astar import Astar
from package.Utils import Tiles
from package.Model import Heuristic
from package.Utils.Parameters import MIN_DISTANCE, MAX_DISTANCE, TIMEOUT


class Result:
    heuristic = ''
    expanded_nodes = 0
    solution_length = 0
    subopt = 0
    duration = 0

    def __init__(self, heuristic):
        self.heuristic = heuristic


def compare(input_size, learning_models, goal):
    output = []
    number = 0
    input_list = generate_input_list(input_size, goal)
    heuristics = [Heuristic.Maximizing()]
    output.append(Result("Maximizing"))
    for learning_model in learning_models:
        heuristics.append(learning_model.get_base_heuristic())
        output.append(Result(learning_model.model_name))

    for input in input_list:
        print(number)
        number += 1
        for index in range(len(heuristics)):
            print(heuristics[index].__class__.__name__)

            algorithm = Astar(heuristics[index])
            start_time = time.time()
            algorithm.solve(input, TIMEOUT, goal)
            end_time = time.time()

            output[index].expanded_nodes += algorithm.expanded_nodes
            solution_length = len(algorithm.solution.path)
            output[index].solution_length += solution_length
            output[index].duration += end_time - start_time

            if index == 0:
                optimal_length = len(algorithm.solution.path)
            else:
                subopt = solution_length - optimal_length
                output[index].subopt += subopt / 100

    calculate_average(output, input_list)

    return output


def calculate_average(output, input_list):
    input_size = len(input_list)
    for result in output:
        result.expanded_nodes /= input_size
        result.solution_length /= input_size
        result.subopt /= input_size
        result.duration /= input_size


def generate_input_list(number, goal):
    input_list = []
    i = 0
    while i < number:
        distance_to_goal = random.randint(MIN_DISTANCE, MAX_DISTANCE)
        input = Tiles.random_walk(goal, distance_to_goal)

        input_list.append(input)
        i += 1

    return input_list
