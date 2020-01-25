import unittest

from package.Utils.Helper import generate_goal


class MyTestCase(unittest.TestCase):
    goal_3 = [[0, 1, 2],
              [3, 4, 5],
              [6, 7, 8]]
    goal_4 = [[0, 1, 2, 3],
              [4, 5, 6, 7],
              [8, 9, 10, 11],
              [12, 13, 14, 15]]
    goal_5 = [[0, 1, 2, 3, 4],
              [5, 6, 7, 8, 9],
              [10, 11, 12, 13, 14],
              [15, 16, 17, 18, 19],
              [20, 21, 22, 23, 24]]
    goal_6 = [[0, 1, 2, 3, 4, 5],
              [6, 7, 8, 9, 10, 11],
              [12, 13, 14, 15, 16, 17],
              [18, 19, 20, 21, 22, 23],
              [24, 25, 26, 27, 28, 29],
              [30, 31, 32, 33, 34, 35]]

    def test_generate_goal_3(self):
        test_goal = generate_goal(3)
        self.assertEqual(test_goal, self.goal_3)

    def test_generate_goal_4(self):
        test_goal = generate_goal(4)
        self.assertEqual(test_goal, self.goal_4)

    def test_generate_goal_5(self):
        test_goal = generate_goal(5)
        self.assertEqual(test_goal, self.goal_5)

    def test_generate_goal_6(self):
        test_goal = generate_goal(6)
        self.assertEqual(test_goal, self.goal_6)


if __name__ == '__main__':
    unittest.main()
