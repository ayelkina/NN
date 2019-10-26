import pprint

import Tiles
from Astar import Astar
from Heuristic import Heuristic

pp = pprint.PrettyPrinter(indent=4)

goal = [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]]
input = Tiles.random_walk(goal, 20)

algorithm = Astar(Heuristic.Manhattan)
pp.pprint(input)
expanded_nodes, solution_path = algorithm.solve(input, goal)

print("Expanded nodes:", expanded_nodes)
print("Solution:")
pp.pprint(solution_path)
