import time

from Utils.Parameters import GOAL
from Utils.Tiles import possible_moves


class Astar:
    heuristic = ''
    puzzle_size = ''
    expanded_nodes = 0
    input = []
    solution = []
    solution_time = ''
    terminated = False

    def __init__(self, heuristic):
        self.heuristic = heuristic

    def solve(self, input, timeout):
        self.expanded_nodes = 0
        expanded = []
        self.terminated = False
        self.input = input
        self.solution = []
        self.puzzle_size = len(input[0]) - 1
        open_set = [[self.heuristic.compute(input), input]]

        start = time.time()
        break_loop = False
        while open_set and not break_loop:
            end = time.time()

            # if end - start > timeout:
            if self.expanded_nodes > 5000:
                self.solution = ''
                self.terminated = True
                break_loop = True
                break
            i = 0
            for j in range(1, len(open_set)):
                if open_set[i][0] > open_set[j][0]:
                    i = j

            self.solution = open_set[i]
            open_set = open_set[:i] + open_set[i + 1:]
            current_path = self.solution[-1]
            if current_path == GOAL:
                break
            if current_path in expanded: continue
            for k in possible_moves(current_path, self.puzzle_size):
                if k in expanded: continue
                cost = self.solution[0] + self.heuristic.compute(k) - self.heuristic.compute(current_path)
                new_path = [cost] + self.solution[1:] + [k]
                open_set.append(new_path)
                expanded.append(current_path)
            self.expanded_nodes += 1

        self.solution_time = time.time() - start
