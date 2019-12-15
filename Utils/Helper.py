import random

from Utils import Tiles
from Utils.Parameters import GOAL, MIN_DISTANCE, MAX_DISTANCE


def generate_input_list(number):
    input_list = []
    i = 0
    while i < number:
        distance_to_goal = random.randint(MIN_DISTANCE, MAX_DISTANCE)
        input = Tiles.random_walk(GOAL, distance_to_goal)
        input_list.append(input)
        i += 1

    return input_list
