import random

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
