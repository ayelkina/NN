import pyximport
pyximport.install()

from package.Algorithms.Astar import Astar
from package.Model import Heuristic
from package.Utils import Helper

cdef int ins_min = 75
cdef int NODES_MAX = 4000
cdef int nodes_max = NODES_MAX * 8
cdef int rw_ins = 500


cpdef void run(learning_model, goal):
    cdef int nodes_limit = NODES_MAX
    cdef list training_set = []
    cdef list not_solved_list = Helper.generate_random_puzzle_list(rw_ins, goal)
    h_in = Heuristic.Maximizing()
    cdef int solved_number = 0
    cdef int count, solution_length, i
    cdef int not_solved_number = len(not_solved_list)
    cdef list input_list, solution_path, solution

    while not_solved_number >= ins_min and nodes_limit <= nodes_max:
        count = -1
        input_list = not_solved_list
        not_solved_list = []
        for instance in input_list:
            count += 1
            print("Solved number", solved_number, "/", count)
            algorithm = Astar(h_in)
            algorithm.solve(instance, nodes_limit, goal)
            if not algorithm.terminated:
                solved_number += 1
                solution_length = len(algorithm.solution.path) - 1
                solution_path = algorithm.solution.path[:-1]
                i = 1
                for solution in solution_path:
                    training_set.append([solution, solution_length - i])
                    i += 1
            else:
                not_solved_list.append(instance)

        if solved_number >= ins_min:
            print("Solved number:", solved_number)
            solved_number = 0
            not_solved_number = len(not_solved_list)
            learning_model.learn_heuristic(training_set, h_in, goal)
            h_in = learning_model.get_maximizing_heuristic()
            training_set = []
        else:
            print("not solved")
            nodes_limit *= 2
