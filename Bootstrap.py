import Heuristic
from Astar import Astar
from Helper import Helper
from Parameters import GOAL

ins_min = 75
t_max = 1
t_inf = 512
rw_ins = 200


def bootstrap():
    training_set = []
    input_list = Helper.get_input_list(rw_ins)
    h_in = Heuristic.Maximizing()

    for i in input_list:
        algorithm = Astar(h_in)
        algorithm.solve(i, GOAL)
        if not algorithm.terminated:
            solution_length = len(algorithm.solution) - 1
            solution_path = algorithm.solution[1:]
            i = 1
            for solution in solution_path[:-1]:
                training_set.append([solution, solution_length - i])
                i += 1

            print()


bootstrap()
