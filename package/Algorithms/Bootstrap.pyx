import pyximport

pyximport.install()

from package.Algorithms import NeuralNetwork
from package.Algorithms.Astar import Astar
from package.Model import Heuristic
from package.Utils import Helper

cdef int ins_min = 75
cdef int NODES_MAX = 10000
cdef int nodes_max = NODES_MAX * 27
cdef int rw_ins = 300

cpdef void run():
    cdef int nodes_limit = NODES_MAX
    cdef list training_set = []
    # file_output = open("generated_list", "w+")
    # file_solved = open("solved_10000", "w+")
    # file_not_solved = open("not_solved_10000", "w+")
    cdef list not_solved_list = Helper.generate_input_list(rw_ins)
    # file_output.write(str(not_solved_list))
    # file_output.close()
    h_in = Heuristic.Maximizing()
    cdef int solved_number = 0
    cdef int count, solution_length, i
    cdef list input_list, solution_path, solution

    while len(not_solved_list) >= ins_min and nodes_limit < nodes_max:
        count = -1
        input_list = not_solved_list
        not_solved_list = []
        for instance in input_list:
            count += 1
            print("Solved number", solved_number, "/", count)
            algorithm = Astar(h_in)
            algorithm.solve(instance, nodes_limit)
            if not algorithm.terminated:
                solved_number += 1
                solution_length = len(algorithm.solution) - 1
                solution_path = algorithm.solution[1:]
                i = 1
                for solution in solution_path[:-1]:
                    training_set.append([solution, solution_length - i])
                    i += 1
                    # file_solved.write(str([solution, solution_length - i]))
            else:
                not_solved_list.append(instance)
                # file_not_solved.write(str(instance))

        if solved_number >= ins_min:
            print("Solved number:", solved_number)
            solved_number = 0
            NeuralNetwork.learn_heuristic(training_set, h_in)
            # RandomForest.learn_heuristic(training_set)
            h_in = Heuristic.MaximizingWithNN()
            training_set = []
        else:
            print("not solved")
            # not_solved_list = input_list

        nodes_limit *= 3

    # file_solved.close()
    # file_not_solved.close()
