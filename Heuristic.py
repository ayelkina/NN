import copy
from abc import abstractmethod
from itertools import product

import Tiles


class Heuristic:
    puzzle_size = ''

    def compute(self, input):
        puzzle_size = len(input[0])
        return self.solve(input, puzzle_size)

    @abstractmethod
    def solve(self, input, puzzle_size):
        ...


class Misplaced(Heuristic):

    def solve(self, input, puzzle_size):
        misplaced = 0
        compare = 0
        for row in range(puzzle_size):
            for col in range(puzzle_size):
                if input[row][col] != compare:
                    misplaced += 1
                compare += 1
        return misplaced


class ColumnsMisplaced(Heuristic):
    def solve(self, input, puzzle_size):
        misplaced = 0
        for row in range(puzzle_size):
            for col in range(puzzle_size):
                col_goal = input[row][col] % puzzle_size
                if col != col_goal:
                    misplaced += 1
        return misplaced


class RowsMisplaced(Heuristic):
    def solve(self, input, puzzle_size):
        misplaced = 0
        for row in range(puzzle_size):
            for col in range(puzzle_size):
                col_goal = input[row][col] % puzzle_size
                row_goal = (input[row][col] - col_goal) / puzzle_size
                if row != row_goal:
                    misplaced += 1
        return misplaced


class Manhattan(Heuristic):
    def solve(self, input, puzzle_size):
        distance = 0
        for row in range(puzzle_size):
            for col in range(puzzle_size):
                col_goal = input[row][col] % puzzle_size
                row_goal = (input[row][col] - col_goal) / puzzle_size
                distance += abs(col - col_goal) + abs(row - row_goal)
        return distance


class LinearConflict(Heuristic):
    def solve(self, input, puzzle_size):
        distance = Manhattan().solve(input, puzzle_size)
        # Two tiles tj and tk are in a linear conflict if tj and tk are in the same line, the goal positions of tj and tk are both in that line,
        # tj is to the right of tk and goal position of tj is to the left of the goal position of tk
        distance += self.linear_vertical_conflict(input, puzzle_size)
        distance += self.linear_horizontal_conflict(input, puzzle_size)
        return distance

    @staticmethod
    def linear_vertical_conflict(input, puzzle_size):
        lc = 0
        for row in range(puzzle_size):
            max = -1
            for col in range(puzzle_size):
                cellvalue = input[row][col]
                if cellvalue != 0 and (cellvalue - 1) / puzzle_size == row:
                    if cellvalue > max:
                        max = cellvalue
                    else:  # linear conflict, one tile must move up or down to allow the other to pass brow and then back up
                        # add two moves to the manhattan distance
                        lc += 2
        return lc

    @staticmethod
    def linear_horizontal_conflict(input, puzzle_size):
        lc = 0
        for col in range(puzzle_size):
            max = -1
            for row in range(puzzle_size):
                cellvalue = input[row][col]
                if cellvalue != 0 and cellvalue % puzzle_size == col + 1:
                    if cellvalue > max:
                        max = cellvalue
                    else:
                        # linear conflict, one tile must move left or right to allow the other to pass brow and then back up
                        # add two moves to the manhattan distance
                        lc += 2

        return lc


class Gasching(Heuristic):
    goal = []

    def __init__(self, goal):
        self.goal = goal

    def solve(self, input, puzzle_size):
        tiles = copy.deepcopy(input)
        distance = 0
        zero_col, zero_row = Tiles.get_zero_position(tiles)
        goal_value = zero_row * puzzle_size + zero_col

        if tiles == self.goal:
            return 0

        if goal_value == 0:
            goal_value = 1
            for row, col in product(range(puzzle_size), range(puzzle_size)):
                if tiles[row][col] != goal_value:
                    tiles[row][col], tiles[zero_row][zero_col] = tiles[zero_row][zero_col], tiles[row][col]
                    break
                goal_value += 1

        while tiles[0][0] != 0:
            goal_value = zero_row * puzzle_size + zero_col
            for row, col in product(range(puzzle_size), range(puzzle_size)):
                if tiles[row][col] == goal_value:
                    tiles[row][col], tiles[zero_row][zero_col] = tiles[zero_row][zero_col], tiles[row][col]
                    zero_row, zero_col = row, col
                    distance += 1
                    break

        return distance
