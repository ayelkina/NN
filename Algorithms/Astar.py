import time

from Utils.Parameters import GOAL
from Utils.Tiles import possible_moves


class Astar:
    heuristic = ''
    puzzle_size = ''
    expanded_nodes = 0
    solution = []
    solution_time = ''
    terminated = False

    def __init__(self, heuristic):
        self.heuristic = heuristic

    def solve(self, input, timeout):
        self.expanded_nodes = 0
        expanded = []
        self.terminated = False
        self.solution = []
        self.puzzle_size = len(input[0]) - 1
        open_set = [[0, input]]

        start = time.time()
        while open_set:
            end = time.time()

            # if end - start > timeout:
            if self.expanded_nodes > 10000:
                self.solution = ''
                self.terminated = True
                break

            shortest_solution_index = 0
            for i in range(1, len(open_set)):
                if open_set[shortest_solution_index][0] > open_set[i][0]:
                    shortest_solution_index = i

            self.solution = open_set[shortest_solution_index]
            open_set = open_set[:shortest_solution_index] + open_set[shortest_solution_index + 1:]
            current_path = self.solution[-1]
            if current_path == GOAL:
                break
            if current_path in expanded: continue
            for path in possible_moves(current_path, self.puzzle_size):
                if path in expanded: continue
                cost = self.solution[0] + self.heuristic.compute(path)
                new_path = [cost] + self.solution[1:] + [path]
                open_set.append(new_path)
                expanded.append(current_path)
            self.expanded_nodes += 1
