import pprint

import Heuristic
import Tiles
import TrainingData
from Astar import Astar

pp = pprint.PrettyPrinter(indent=4)

goal_24 = [[0, 1, 2, 3, 4], [5, 6, 7, 8, 9], [10, 11, 12, 13, 14], [15, 16, 17, 18, 19], [20, 21, 22, 23, 24]]
goal_15 = [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]]
goal = goal_15


# input = Tiles.random_walk(goal, 20)
# input = [[1, 8, 2, 3], [4, 5, 0, 6], [9, 10, 11, 7], [12, 13, 14, 15]]
# print("Input")
# pp.pprint(input)


def print_solution(heuristic):
    algorithm = Astar(heuristic)
    algorithm.solve(input, goal)
    print("Heuristic:", heuristic.__class__.__name__)
    print("Expanded nodes:", algorithm.expanded_nodes)
    # pp.pprint(solution_path)


def best_heuristic(solution_list):
    best_heur = ''
    best_score = 999999999
    for (Astar) in solution_list:
        if Astar.expanded_nodes < best_score:
            best_score = Astar.expanded_nodes
            best_heur = Astar

    return TrainingData.TrainingData(best_heur)


def get_training_data(n):
    file = open("training_data_2.txt", "w+")
    training_list = []
    for i in range(n):
        input = Tiles.random_walk(goal, 20)
        solution_list = []
        for name in Heuristic.Enum:
            algorithm = Astar(Heuristic.Enum.heuristic(name))
            algorithm.solve(input, goal)
            solution_list.append(algorithm)

        best_heur = best_heuristic(solution_list)
        training_list.append(best_heur)
        file.write(str(best_heur.input))
        file.write("\n")
        file.write(str(best_heur.solution_length))
        file.write("\n")
        file.write(best_heur.heuristic.__class__.__name__)
        file.write("\n")
        file.write(str(best_heur.solution_path))
        file.write("\n")
    file.close()
    return training_list


# print_solution(Heuristic.LinearConflict())
# print_solution(Heuristic.Manhattan())
# print_solution(Heuristic.Misplaced())
# print_solution(Heuristic.ColumnsMisplaced())
# print_solution(Heuristic.RowsMisplaced())
# print_solution(Heuristic.Gasching(goal))

# print("Best heuristic", best_heuristic().__class__.__name__)

if __name__ == "__main__":
    # input = Tiles.random_walk(goal, 20)
    # print("Input")
    # pp.pprint(input)
    # print_solution(Heuristic.LinearConflict())
    # print_solution(Heuristic.Manhattan())
    # print_solution(Heuristic.Misplaced())
    # print_solution(Heuristic.ColumnsMisplaced())
    # print_solution(Heuristic.RowsMisplaced())
    # print_solution(Heuristic.Gasching())
    training_data = get_training_data(500)
