import copy
import enum
from abc import abstractmethod
from itertools import product

import numpy as np
import tensorflow as tf

import Tiles
from Parameters import GOAL, MODEL_NAME


class Enum(enum.Enum):
    LinearConflict = 1
    Manhattan = 2
    Misplaced = 3
    ColumnsMisplaced = 4
    RowsMisplaced = 5
    Gasching = 6

    def heuristic(self):
        if self == Enum.LinearConflict:
            return LinearConflict()
        elif self == Enum.Manhattan:
            return Manhattan()
        elif self == Enum.Misplaced:
            return Misplaced()
        elif self == Enum.ColumnsMisplaced:
            return ColumnsMisplaced()
        elif self == Enum.RowsMisplaced:
            return RowsMisplaced()
        elif self == Enum.Gasching:
            return Gasching()


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
        return int(distance)


class LinearConflict(Heuristic):
    def solve(self, input, puzzle_size):
        distance = Manhattan().solve(input, puzzle_size)
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
                    else:
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
                        lc += 2

        return lc


class Gasching(Heuristic):
    goal = GOAL

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


class NeuralNetwork(Heuristic):

    def compute_input(self, input):
        input_data = []
        Manh = Manhattan().compute(input)
        Lin = LinearConflict().compute(input)
        Misp = Misplaced().compute(input)
        Col_Misp = ColumnsMisplaced().compute(input)
        Row_Misp = RowsMisplaced().compute(input)
        Gasch = Gasching().compute(input)

        input_data.append(Manh)
        input_data.append(Lin)
        input_data.append(Misp)
        input_data.append(Col_Misp)
        input_data.append(Row_Misp)
        input_data.append(Gasch)

        # for i in input:
        #     for j in i:
        #         input_data.append(j)

        return input_data

    def solve(self, input, puzzle_size):
        model = tf.keras.models.load_model(MODEL_NAME)
        input_data = self.compute_input(input)
        return model.predict(np.array([input_data]))
