import pyximport

pyximport.install()

from package.Algorithms.Astar import Astar
from package.Model import Heuristic
from package.Utils import Helper

cdef int ins_min = 75
cdef int NODES_MAX = 2000
cdef int nodes_max = NODES_MAX * 64
cdef int rw_ins = 500

cdef class BLHF:

    learning_model = ''
    cdef list goal
    cdef int nodes_limit

    def __init__(self, learning_model, goal):
        self.learning_model = learning_model
        self.goal = goal

    cpdef void execute(self):
        cdef int nodes_limit = NODES_MAX
        cdef list not_solved_list = Helper.generate_random_puzzle_list(rw_ins, self.goal)
        h_in = Heuristic.Maximizing()
        self.__bootstrap(not_solved_list, h_in)

    cpdef void __bootstrap(self, ins, h_in):
        cdef list training_set = []
        cdef int solved_number = 0
        cdef int count, solution_length, i
        cdef int not_solved_number = len(ins)
        cdef list input_list, solution_path, solution

        while not_solved_number >= ins_min and self.nodes_limit <= nodes_max:
            count = -1
            input_list = not_solved_list
            not_solved_list = []
            for instance in input_list:
                count += 1
                print("Solved number", solved_number, "/", count)
                algorithm = Astar(h_in)
                algorithm.solve(instance, self.nodes_limit, self.goal)
                if not algorithm.terminated:
                    solved_number += 1
                    solution_length = len(algorithm.solution.path)
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
                self.learning_model.learn_heuristic(training_set, h_in, self.goal)
                h_in = self.learning_model.get_maximizing_heuristic()
                training_set = []
                self.nodes_limit *= 2
            else:
                print("not solved")
                self.nodes_limit *= 2
