import random
import matplotlib.pyplot as plt
import numpy as np

import pyximport
pyximport.install()

from package.Utils import Tiles
from package.Utils.Parameters import MIN_DISTANCE, MAX_DISTANCE


def generate_random_puzzle_list(number, goal):
    input_list = []
    i = 0
    while i < number:
        distance_to_goal = random.randint(MIN_DISTANCE, MAX_DISTANCE)
        input = Tiles.random_walk(goal, distance_to_goal)
        input_list.append(input)
        i += 1

    return input_list

def draw_bar_spot(x, y, goal):
    x_pos = np.arange(len(x))
    plt.barh(x_pos, y, align='center', alpha=1)
    plt.yticks(x_pos, x)
    plt.xlabel('Expanded nodes')
    size = len(goal[0])
    puzzle_type = str(size * size - 1)
    title = puzzle_type + '-puzzle'
    plt.title(title)

    plt.savefig(puzzle_type + '.png')
    plt.show()

def generate_goal(size):
    goal = []
    i = 0
    for row in range(size):
        row_list = []
        for column in range(size):
            row_list.append(i)
            i += 1
        goal.append(row_list)

    return goal
