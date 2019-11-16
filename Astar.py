import time

from Tiles import possible_moves


class Astar:
    heuristic = ''
    puzzle_size = ''
    expanded_nodes = 0
    input = []
    solution = []
    terminated = False

    def __init__(self, heuristic):
        self.heuristic = heuristic

    def solve(self, input, goal):
        expanded = []
        self.input = input
        self.puzzle_size = len(input[0]) - 1
        open_set = [[self.heuristic.compute(input), input]]

        start = time.time()
        break_loop = False
        while open_set and not break_loop:
            end = time.time()

            if end - start > 5:
                self.solution = ''
                self.terminated = True
                break_loop = True
            i = 0
            for j in range(1, len(open_set)):
                if open_set[i][0] > open_set[j][0]:
                    i = j
            self.solution = open_set[i]
            open_set = open_set[:i] + open_set[i + 1:]
            current_path = self.solution[-1]
            if current_path == goal:
                break
            if current_path in expanded: continue
            for k in possible_moves(current_path, self.puzzle_size):
                if k in expanded: continue
                cost = self.solution[0] + self.heuristic.compute(k) - self.heuristic.compute(current_path)
                new_path = [cost] + self.solution[1:] + [k]
                open_set.append(new_path)
                expanded.append(current_path)
            self.expanded_nodes += 1

