import copy
import pickle
from abc import abstractmethod
from enum import Enum
from itertools import product

import numpy as np
import tensorflow as tf

from Utils import Tiles, TrainingData
from Utils.Parameters import GOAL, NN_MODEL_NAME, RF_MODEL_NAME


class Name(Enum):
    LinearConflict = 1
    Manhattan = 2
    NeuralNetwork = 7
    Maximizing = 8
    MaximizingWithNN = 9
    Gasching = 6
    Misplaced = 3
    ColumnsMisplaced = 4
    RowsMisplaced = 5
    # RandomForest = 10


def get_heuristic_by_name(name):
    if name == Name.LinearConflict:
        return LinearConflict()
    elif name == Name.Manhattan:
        return Manhattan()
    elif name == Name.Misplaced:
        return Misplaced()
    elif name == Name.ColumnsMisplaced:
        return ColumnsMisplaced()
    elif name == Name.RowsMisplaced:
        return RowsMisplaced()
    elif name == Name.Gasching:
        return Gasching()
    if name == Name.NeuralNetwork:
        return NeuralNetwork()
    elif name == Name.Maximizing:
        return Maximizing()
    elif name == Name.MaximizingWithNN:
        return MaximizingWithNN()
    elif name == Name.RandomForest:
        return RandomForest()


class AbstractHeuristic:
    puzzle_size = ''

    def compute(self, input):
        puzzle_size = len(input[0])
        return self.solve(input, puzzle_size)

    @abstractmethod
    def solve(self, input, puzzle_size):
        ...


class Misplaced(AbstractHeuristic):

    def solve(self, input, puzzle_size):
        misplaced = 0
        goal_value = 0
        for row in range(puzzle_size):
            for col in range(puzzle_size):
                if input[row][col] != goal_value and input[row][col] != 0:
                    misplaced += 1
                goal_value += 1
        return misplaced


class ColumnsMisplaced(AbstractHeuristic):
    def solve(self, input, puzzle_size):
        if input == GOAL:
            return 0

        misplaced = 0
        for row in range(puzzle_size):
            for col in range(puzzle_size):
                col_goal = input[row][col] % puzzle_size
                if input[row][col] == 0:
                    continue
                if col != col_goal:
                    misplaced += 1

        if misplaced == 0:
            misplaced += 1
        return misplaced


class RowsMisplaced(AbstractHeuristic):
    def solve(self, input, puzzle_size):
        if input == GOAL:
            return 0

        misplaced = 0
        for row in range(puzzle_size):
            for col in range(puzzle_size):
                value = input[row][col]
                if value == 0:
                    continue

                col_goal = value % puzzle_size
                row_goal = (value - col_goal) / puzzle_size
                if row != row_goal:
                    misplaced += 1

        if misplaced == 0:
            misplaced += 1

        return misplaced


class Manhattan(AbstractHeuristic):
    def solve(self, input, puzzle_size):
        distance = 0
        for row in range(puzzle_size):
            for col in range(puzzle_size):
                value = input[row][col]
                if value == 0:
                    continue
                col_goal = value % puzzle_size
                row_goal = (value - col_goal) / puzzle_size
                distance += abs(col - col_goal) + abs(row - row_goal)
        return int(distance)


class LinearConflict(AbstractHeuristic):
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


class Gasching(AbstractHeuristic):
    goal = GOAL

    def solve(self, input, puzzle_size):
        tiles = copy.deepcopy(input)
        distance = 0
        zero_col, zero_row = Tiles.get_zero_position(tiles)

        while tiles != self.goal:
            goal_value = zero_row * puzzle_size + zero_col
            if goal_value == 0:
                for row, col in product(range(puzzle_size), range(puzzle_size)):
                    if tiles[row][col] != goal_value:
                        tiles[row][col], tiles[zero_row][zero_col] = tiles[zero_row][zero_col], tiles[row][col]
                        zero_row, zero_col = row, col
                        distance += 1
                        break
                    goal_value += 1

            for row, col in product(range(puzzle_size), range(puzzle_size)):
                if tiles[row][col] == goal_value:
                    tiles[row][col], tiles[zero_row][zero_col] = tiles[zero_row][zero_col], tiles[row][col]
                    zero_row, zero_col = row, col
                    distance += 1
                    break

        return distance


class NeuralNetwork(AbstractHeuristic):
    model = ''

    def __init__(self):
        try:
            self.model = tf.keras.models.load_model(NN_MODEL_NAME)
        except IOError:
            return

    def solve(self, input, puzzle_size):
        input_data, maximum_value = TrainingData.compute_input(input)
        return int(self.model.predict(np.array([input_data])))


class RandomForest(AbstractHeuristic):
    model = ''

    def __init__(self):
        try:
            self.model = pickle.load(open(RF_MODEL_NAME, 'rb'))
        except IOError:
            return

    def solve(self, input, puzzle_size):
        input_data, maximum = TrainingData.compute_input(input)
        return int(self.model.predict(np.array([input_data])))


class Maximizing(AbstractHeuristic):
    def solve(self, input, puzzle_size):
        if input == GOAL:
            return 0

        maximum = 0
        for index in range(1, 6):
            predicted_value = get_heuristic_by_name(Name(index)).compute(input)

            if predicted_value > maximum:
                maximum = predicted_value

        return maximum


class MaximizingWithNN(AbstractHeuristic):
    model = ''

    def __init__(self):
        try:
            self.model = tf.keras.models.load_model(NN_MODEL_NAME)
        except IOError:
            return

    def solve(self, input, puzzle_size):
        if input == GOAL:
            return 0

        return self.get_maximum_value(input)

    def get_maximum_value(self, input):
        input_data, maximum_value = TrainingData.compute_input(input)
        distance = int(self.model.predict(np.array([input_data])))
        if distance > maximum_value:
            maximum_value = distance

        return maximum_value
