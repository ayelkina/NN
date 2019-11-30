import pprint
import random

import Heuristic
import Tiles
import TrainingData
from Astar import Astar
from Parameters import GOAL, FILE_NAME

pp = pprint.PrettyPrinter(indent=4)


class Helper:
    count = 0

    @staticmethod
    def get_solution_list(input):
        solution_list = []
        for name in Heuristic.Enum:
            algorithm = Astar(Heuristic.Enum.heuristic(name))
            algorithm.solve(input, GOAL)
            Helper.print_solution(algorithm)
            if not algorithm.terminated:
                solution_list.append(algorithm)

        return solution_list

    @staticmethod
    def print_solution(algorithm):
        print("Heuristic:", algorithm.heuristic.__class__.__name__)
        if not algorithm.terminated:
            print("Expanded nodes:", algorithm.expanded_nodes, "Solution length:", len(algorithm.solution))
        else:
            print("Terminated")

    @staticmethod
    def heristic_with_shortest_solution(solution_list):
        best_heur = ''
        best_score = 999999999
        for (Astar) in solution_list:
            solution_length = len(Astar.solution)
            if solution_length < best_score:
                best_score = solution_length
                best_heur = Astar

        return TrainingData.TrainingData(best_heur)

    def get_training_data(self, n):
        file_output = open(FILE_NAME, "w+")
        i = 0
        while i < n:
            distance_to_goal = random.randint(15, 40)
            input = Tiles.random_walk(GOAL, distance_to_goal)
            solution_list = self.get_solution_list(input)

            if len(solution_list) == 0:
                print("No solution. Distance:", distance_to_goal)
                continue

            best_heur = self.heristic_with_shortest_solution(solution_list)
            print("Step", i, "Distance:", distance_to_goal)
            file_output.write(str(input))
            file_output.write("\n")
            file_output.write(str(best_heur.solution_length))
            file_output.write("\n")
            file_output.write(str(best_heur.solution_path))
            file_output.write("\n")
            i += 1
        file_output.close()

    def heuristic_with_less_expanded_nodes(self, solution_list):
        best_heur = ''
        best_score = 999999999
        for (Astar) in solution_list:
            if Astar.expanded_nodes < best_score:
                best_score = Astar.expanded_nodes
                best_heur = Astar.heuristic

        if best_heur.__class__ == Heuristic.NeuralNetwork:
            self.count += 1

        return best_heur

    @staticmethod
    def get_input_list(number):
        input_list = []
        i = 0
        while i < number:
            distance_to_goal = random.randint(15, 25)
            input = Tiles.random_walk(GOAL, distance_to_goal)
            input_list.append(input)
            i += 1

        return input_list

    @staticmethod
    def compare_heuristics(input_size):
        input_list = Helper.get_input_list(input_size)
        for name in Heuristic.Enum:
            average_expanded_nodes = 0
            average_length = 0
            terminated = 0
            algorithm = Astar(Heuristic.Enum.heuristic(name))

            for input in input_list:
                algorithm.solve(input, GOAL)
                average_expanded_nodes += algorithm.expanded_nodes
                if algorithm.terminated:
                    terminated += 1
                else:
                    average_length += len(algorithm.solution)

            print("Heuristic:", algorithm.heuristic.__class__.__name__)
            print("Terminated:", terminated)
            if terminated < input_size:
                print("Average expanded nodes:", average_expanded_nodes / input_size)
                print("Average solution length:", average_length / (input_size - terminated))
            print()

    @staticmethod
    def show_best_heuristic_for_tasks(input_size):
        helper = Helper()
        for i in range(input_size):
            distance_to_goal = random.randint(15, 40)
            input = Tiles.random_walk(GOAL, distance_to_goal)
            print("Input with distance to goal:", distance_to_goal)
            pp.pprint(input)
            solution_list = Helper.get_solution_list(input)
            print("Best heuristic", helper.heuristic_with_less_expanded_nodes(solution_list).__class__.__name__)
            print("Iteration:", i, "NeuralNetwork won:", Helper.count)
