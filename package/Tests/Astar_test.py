import unittest
import pyximport
pyximport.install()

from package.Algorithms.Astar import Astar
from package.Model import Heuristic
from package.Utils.Parameters import TIMEOUT


class Puzzle15(unittest.TestCase):
    input = [[1, 2, 3, 7], [4, 5, 10, 6], [12, 0, 8, 11], [13, 14, 9, 15]]
    goal_15 = [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]]

    def test_manhattan(self):
        algorithm = Astar(Heuristic.Manhattan())
        algorithm.solve(self.input, TIMEOUT, self.goal_15)
        self.assertEqual(len(algorithm.solution.path) - 1, 13)

    def test_linear(self):
        algorithm = Astar(Heuristic.LinearConflict())
        algorithm.solve(self.input, TIMEOUT, self.goal_15)
        self.assertEqual(len(algorithm.solution.path) - 1, 13)

    def test_rows(self):
        algorithm = Astar(Heuristic.RowsMisplaced())
        algorithm.solve(self.input, TIMEOUT, self.goal_15)
        self.assertEqual(len(algorithm.solution.path) - 1, 13)

    def test_columns(self):
        algorithm = Astar(Heuristic.ColumnsMisplaced())
        algorithm.solve(self.input, TIMEOUT, self.goal_15)
        self.assertEqual(len(algorithm.solution.path) - 1, 13)

    def test_misplaced(self):
        algorithm = Astar(Heuristic.Misplaced())
        algorithm.solve(self.input, TIMEOUT, self.goal_15)
        self.assertEqual(len(algorithm.solution.path) - 1, 13)

    def test_gasching(self):
        algorithm = Astar(Heuristic.Gasching())
        algorithm.solve(self.input, TIMEOUT, self.goal_15)
        self.assertEqual(len(algorithm.solution.path) - 1, 13)

    def test_maximizing(self):
        algorithm = Astar(Heuristic.Maximizing())
        algorithm.solve(self.input, TIMEOUT, self.goal_15)
        self.assertEqual(len(algorithm.solution.path) - 1, 13)


if __name__ == '__main__':
    unittest.main()
