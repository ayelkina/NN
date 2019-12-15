import random

from Algorithms.Astar import Astar
from Model import Heuristic
from Utils import Tiles
from Utils.Parameters import FILE_NAME, MIN_DISTANCE, MAX_DISTANCE, GOAL, TIMEOUT, TRAIN_SIZE_FACTOR


class TrainingData:
    input = []
    heuristic = ''
    solution_path = []
    solution_length = ''

    def __init__(self, Astar):
        self.input = Astar.input
        self.heuristic = Astar.heuristic
        self.solution_path = Astar.solution[1:]
        self.solution_length = len(self.solution_path)


def generate_training_data(self, n):
    file_output = open(FILE_NAME, "w+")
    i = 0
    while i < n:
        distance_to_goal = random.randint(MIN_DISTANCE, MAX_DISTANCE)
        input = Tiles.random_walk(GOAL, distance_to_goal)
        solution_list = self.get_solution_list(input)

        if len(solution_list) == 0:
            print("No solution. Distance:", distance_to_goal)
            continue

        best_heur = self.heuristic_with_shortest_solution(solution_list)
        print("Step", i, "Distance:", distance_to_goal)
        file_output.write(str(input))
        file_output.write("\n")
        file_output.write(str(best_heur.solution_length))
        file_output.write("\n")
        file_output.write(str(best_heur.solution_path))
        file_output.write("\n")
        i += 1
    file_output.close()


def get_input_list_from_file(file_name):
    input_list = []
    output_list = []

    file = open(file_name, "r")
    training_data = file.read().splitlines()

    line = 0
    while line < len(training_data):
        solution_path = eval(training_data[line + 2])
        solution_length = int(training_data[line + 1])

        i = 1
        for path in solution_path[:-1]:
            input_data = compute_input(path)
            input_list.append(input_data)
            output_list.append(solution_length - i)
            i += 1

        line += 3

    file.close()

    return input_list, output_list


def get_solution_list(input):
    solution_list = []
    for name in Heuristic.Name:
        algorithm = Astar(Heuristic.get_heuristic_by_name(name))
        algorithm.solve(input, TIMEOUT)
        print_solution(algorithm)
        if not algorithm.terminated:
            solution_list.append(algorithm)

    return solution_list


def print_solution(algorithm):
    print("Heuristic:", algorithm.heuristic.__class__.__name__)
    if not algorithm.terminated:
        print("Expanded nodes:", algorithm.expanded_nodes, "Solution length:", len(algorithm.solution))
    else:
        print("Terminated")


def compute_input(input):
    input_data = []
    Manh = Heuristic.Manhattan().compute(input)
    Lin = Heuristic.LinearConflict().compute(input)
    Misp = Heuristic.Misplaced().compute(input)
    Col_Misp = Heuristic.ColumnsMisplaced().compute(input)
    Row_Misp = Heuristic.RowsMisplaced().compute(input)
    Gasch = Heuristic.Gasching().compute(input)

    input_data.append(Manh)
    input_data.append(Lin)
    input_data.append(Misp)
    input_data.append(Col_Misp)
    input_data.append(Row_Misp)
    input_data.append(Gasch)

    return input_data


def get_training_data(training_set):
    input_list = []
    output_list = []

    for line in training_set:
        input_data = compute_input(line[0])
        input_list.append(input_data)
        output_list.append(line[1])

    return input_list, output_list


def split_data(input_list, output_list):
    data_size = len(input_list)
    train_size = int(data_size * TRAIN_SIZE_FACTOR)

    input_train = input_list[:train_size]
    output_train = output_list[:train_size]

    input_test = input_list[train_size:]
    output_test = output_list[train_size:]

    return input_train, output_train, input_test, output_test
