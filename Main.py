import pprint

import Heuristic
import Tiles
from Astar import Astar

pp = pprint.PrettyPrinter(indent=4)

goal = [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]]
input = Tiles.random_walk(goal, 5)
print("Input")
pp.pprint(input)


def print_solution(heuristic):
    algorithm = Astar(heuristic)
    expanded_nodes, solution_path = algorithm.solve(input, goal)
    print("Heuristic:", heuristic.__class__.__name__)
    print("Expanded nodes:", expanded_nodes)


# print_solution(Heuristic.LinearConflict())
# print_solution(Heuristic.Manhattan())
# print_solution(Heuristic.Misplaced())
# print_solution(Heuristic.ColumnsMisplaced())
# print_solution(Heuristic.RowsMisplaced())
print_solution(Heuristic.Gasching(goal))
