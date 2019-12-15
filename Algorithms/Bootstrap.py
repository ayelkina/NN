from Algorithms import NeuralNetwork
from Algorithms.Astar import Astar
from Model import Heuristic
from Utils import Helper

ins_min = 75
t_inf = 512
rw_ins = 500


def run():
    t_max = 1
    training_set = []
    not_solved_list = Helper.generate_input_list(rw_ins)
    h_in = Heuristic.Maximizing()
    count = -1

    while len(not_solved_list) >= ins_min and t_max < t_inf:
        input_list = not_solved_list
        not_solved_list = []
        solved_number = 0
        for instance in input_list:
            count += 1
            print("Solved number", solved_number, "/", count)
            algorithm = Astar(h_in)
            algorithm.solve(instance, t_max)
            if not algorithm.terminated:
                # print("Solve")
                solved_number += 1
                solution_length = len(algorithm.solution) - 1
                solution_path = algorithm.solution[1:]
                i = 1
                for solution in solution_path[:-1]:
                    training_set.append([solution, solution_length - i])
                    i += 1
            else:
                # print("Terminated")
                not_solved_list.append(instance)

        if solved_number > ins_min:
            print("Solved number:", solved_number)
            NeuralNetwork.learn_heuristic(training_set)
            # RandomForest.learn_heuristic(training_set)
            h_in = Heuristic.MaximizingWithNN()
            training_set = []
        else:
            print("not solved")
            not_solved_list = input_list
            t_max *= 2
