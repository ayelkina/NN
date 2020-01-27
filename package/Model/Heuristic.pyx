import copy
import pickle
from abc import abstractmethod
from enum import Enum
from itertools import product

import numpy as np
import tensorflow as tf

from package.Utils import Tiles


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

    def compute(self, input, goal):
        self.puzzle_size = len(input[0])
        return self.solve(input, self.puzzle_size, goal)

    @abstractmethod
    def solve(self, list input, int puzzle_size, goal):
        ...

    @staticmethod
    def get_predicted_values_with_maximum(predicted_values, goal):
        ...


class Misplaced(AbstractHeuristic):

    def solve(self, list input, int puzzle_size, goal):
        cdef int misplaced = 0
        cdef int goal_value = 0
        cdef int row, col, value

        for row in range(puzzle_size):
            for col in range(puzzle_size):
                value = input[row][col]
                if value == 0:
                    goal_value += 1
                    continue

                if value != goal_value:
                    misplaced += 1
                goal_value += 1

        return misplaced


class ColumnsMisplaced(AbstractHeuristic):
    def solve(self, list input, int puzzle_size, goal):
        if input == goal:
            return 0

        cdef int misplaced = 0
        cdef int goal_value = 0
        cdef int row, col, col_goal, value
        for row in range(puzzle_size):
            for col in range(puzzle_size):
                value = input[row][col]
                if value == 0:
                    continue

                col_goal = value % puzzle_size
                if col != col_goal:
                    misplaced += 1

        return misplaced


class RowsMisplaced(AbstractHeuristic):
    def solve(self, list input, int puzzle_size, goal):
        if input == goal:
            return 0

        cdef int misplaced = 0
        cdef int col_goal, row_goal, row, col, value
        for row in range(puzzle_size):
            for col in range(puzzle_size):
                value = input[row][col]
                if value == 0:
                    continue

                col_goal = value % puzzle_size
                row_goal = (value - col_goal) / puzzle_size
                if row != row_goal:
                    misplaced += 1

        return misplaced


class Manhattan(AbstractHeuristic):
    def solve(self, list input, int puzzle_size, goal):
        cdef int distance = 0
        cdef int col_goal, row_goal, row, col, value

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
    def solve(self, list input, int puzzle_size, goal):
        cdef int distance = Manhattan().solve(input, puzzle_size, goal)
        # distance += self.linear_vertical_conflict(input, puzzle_size)
        distance += self.linear_horizontal_conflict(input, puzzle_size)
        return distance

    @staticmethod
    def linear_vertical_conflict(input, puzzle_size):
        cdef int distance = 0
        cdef int max, cellvalue, row, col
        for row in range(puzzle_size):
            max = -1
            for col in range(puzzle_size):
                cellvalue = input[row][col]
                if cellvalue != 0 and (cellvalue - 1) / puzzle_size == row:
                    if cellvalue > max:
                        max = cellvalue
                    else:
                        distance += 2
        return distance

    @staticmethod
    def linear_horizontal_conflict(input, puzzle_size):
        cdef int distance = 0
        cdef int max, cellvalue, row, col
        for col in range(puzzle_size):
            max = -1
            for row in range(puzzle_size):
                cellvalue = input[row][col]
                if cellvalue != 0 and cellvalue % puzzle_size == col + 1:
                    if cellvalue > max:
                        max = cellvalue
                    else:
                        distance += 2

        return distance


class Gasching(AbstractHeuristic):
    def solve(self, list input, int puzzle_size, goal):
        cdef list tiles = copy.deepcopy(input)
        cdef int distance = 0
        cdef int goal_value, cellvalue, row, col, zero_col, zero_row
        zero_col, zero_row = Tiles.get_zero_position(tiles)

        while tiles != goal:
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

    def __init__(self, model_name):
        try:
            self.model = tf.keras.models.load_model(model_name)
        except IOError:
            return

    def solve(self, list input, int puzzle_size, goal):
        cdef list input_data = get_predicted_values_from_heuristics(input, goal)
        return int(self.model.predict(np.array([input_data])))

class RandomForest(AbstractHeuristic):
    model = ''

    def __init__(self, model_name):
        try:
            self.model = pickle.load(open(model_name, 'rb'))
        except IOError:
            return

    def solve(self, list input, int puzzle_size, goal):
        cdef list input_data = get_predicted_values_from_heuristics(input, goal)
        return int(self.model.predict(np.array([input_data])))


class Maximizing(AbstractHeuristic):
    def solve(self, list input, int puzzle_size, goal):
        if input == goal:
            return 0

        cdef int maximum = 0
        cdef int predicted_value
        cdef list heur = [LinearConflict(), Gasching()]
        for h in heur:
            predicted_value = h.compute(input, goal)

            if predicted_value > maximum:
                maximum = predicted_value

        return maximum

    @staticmethod
    def get_predicted_values_with_maximum(input, goal):
        return get_predicted_values_from_heuristics(input, goal)


class MaximizingWithNN(AbstractHeuristic):
    model = ''

    def __init__(self, model_name):
        try:
            self.model = tf.keras.models.load_model(model_name)
        except IOError:
            return

    def solve(self, list input, int puzzle_size, goal):
        if input == goal:
            return 0

        return self.get_maximum_value(input, goal)

    def get_maximum_value(self, input, goal):
        predicted_values = self.get_predicted_values_with_maximum(input, goal)
        return predicted_values[-1]

    def get_predicted_values_with_maximum(self, input, goal):
        cdef list predicted_values = get_predicted_values_from_heuristics(input, goal)
        cdef int maximum_value = predicted_values[-1]

        cdef int distance = int(self.model.predict(np.array([predicted_values])))
        if distance > maximum_value:
            predicted_values[-1] = distance

        return predicted_values


class MaximizingWithRF(AbstractHeuristic):
    model = ''

    def __init__(self, model_name):
        try:
            self.model = pickle.load(open(model_name, 'rb'))
        except IOError:
            return

    def solve(self, list input, int puzzle_size, goal):
        if input == goal:
            return 0

        return self.get_maximum_value(input, goal)


    def get_maximum_value(self, input, goal):
        predicted_values = self.get_predicted_values_with_maximum(input, goal)
        return predicted_values[-1]

    def get_predicted_values_with_maximum(self, input, goal):
        cdef list predicted_values = get_predicted_values_from_heuristics(input, goal)
        cdef int maximum_value = predicted_values[-1]

        cdef int distance = int(self.model.predict(np.array([predicted_values])))
        if distance > maximum_value:
            predicted_values[-1] = distance

        return predicted_values


def get_predicted_values_from_heuristics(input, goal):
    cdef list predicted_values = []
    cdef int maximum_value = 0
    cdef int index, predicted_value

    for index in range(1, 7):
        predicted_value = get_heuristic_by_name(Name(index)).compute(input, goal)
        predicted_values.append(predicted_value)

        if predicted_value > maximum_value:
            maximum_value = predicted_value

    predicted_values.append(maximum_value)

    return predicted_values
