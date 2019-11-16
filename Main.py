import random

import Heuristic
import Tiles
import TrainingData
from Astar import Astar
from Parameters import GOAL, DATA_SIZE, FILE_NAME


def print_solution(heuristic):
    algorithm = Astar(heuristic)
    algorithm.solve(input, GOAL)
    print("Heuristic:", heuristic.__class__.__name__)
    print("Expanded nodes:", algorithm.expanded_nodes)


def best_heuristic(solution_list):
    best_heur = ''
    best_score = 999999999
    for (Astar) in solution_list:
        solution_length = len(Astar.solution)
        if solution_length < best_score:
            best_score = solution_length
            best_heur = Astar

    return TrainingData.TrainingData(best_heur)


def get_training_data(n):
    file_output = open(FILE_NAME, "w+")
    i = 0
    while i < n:
        distance_to_goal = random.randint(15, 40)
        input = Tiles.random_walk(GOAL, distance_to_goal)
        solution_list = []
        for name in Heuristic.Enum:
            algorithm = Astar(Heuristic.Enum.heuristic(name))
            algorithm.solve(input, GOAL)
            if not algorithm.terminated:
                solution_list.append(algorithm)

        if len(solution_list) == 0:
            print("No solution. Distance:", distance_to_goal)
            continue

        best_heur = best_heuristic(solution_list)
        print("Step", i, "Distance:", distance_to_goal)
        file_output.write(str(input))
        file_output.write("\n")
        file_output.write(str(best_heur.solution_length))
        file_output.write("\n")
        file_output.write(str(best_heur.solution_path))
        file_output.write("\n")
        i += 1
    file_output.close()


if __name__ == "__main__":
    get_training_data(DATA_SIZE)
