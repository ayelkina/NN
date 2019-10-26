import copy
import enum
import random


class Directions(enum.Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


def random_walk(goal, moves_from_goal):
    tiles = copy.deepcopy(goal)
    puzzle_size = len(goal[0]) - 1
    directions = [Directions.UP, Directions.DOWN, Directions.LEFT, Directions.RIGHT]
    opposite_previous = ''
    x, y = 0, 0

    for i in range(0, moves_from_goal):
        new_dir = directions[:]
        if x == 0:
            new_dir.remove(Directions.LEFT)
        if y == 0:
            new_dir.remove(Directions.UP)
        if x == puzzle_size:
            new_dir.remove(Directions.RIGHT)
        if y == puzzle_size:
            new_dir.remove(Directions.DOWN)
        if opposite_previous in new_dir:
            new_dir.remove(opposite_previous)

        direction = random.choice(new_dir)
        if direction == Directions.UP:
            move_up(tiles, x, y)
            y -= 1
            opposite_previous = Directions.DOWN
        elif direction == Directions.DOWN:
            move_down(tiles, x, y)
            y += 1
            opposite_previous = Directions.UP
        elif direction == Directions.RIGHT:
            move_right(tiles, x, y)
            x += 1
            opposite_previous = Directions.LEFT
        elif direction == Directions.LEFT:
            move_left(tiles, x, y)
            x -= 1
            opposite_previous = Directions.RIGHT

    return tiles


def possible_moves(tiles, puzzle_size):
    output = []
    x, y = get_zero_position(tiles)

    if y > 0:
        new_list = copy.deepcopy(tiles)
        new_list = move_up(new_list, x, y)
        output.append(new_list)

    if y < puzzle_size:
        new_list = copy.deepcopy(tiles)
        new_list = move_down(new_list, x, y)
        output.append(new_list)

    if x > 0:
        new_list = copy.deepcopy(tiles)
        new_list = move_left(new_list, x, y)
        output.append(new_list)

    if x < puzzle_size:
        new_list = copy.deepcopy(tiles)
        new_list = move_right(new_list, x, y)
        output.append(new_list)

    return output


def get_zero_position(tiles):
    y = 0
    while 0 not in tiles[y]: y += 1
    x = tiles[y].index(0)  # blank space (zero)
    return x, y


def move_up(new_list, x, y):
    new_list[y][x], new_list[y - 1][x] = new_list[y - 1][x], new_list[y][x]
    return new_list


def move_down(new_list, x, y):
    new_list[y][x], new_list[y + 1][x] = new_list[y + 1][x], new_list[y][x]
    return new_list


def move_left(new_list, x, y):
    new_list[y][x], new_list[y][x - 1] = new_list[y][x - 1], new_list[y][x]
    return new_list


def move_right(new_list, x, y):
    new_list[y][x], new_list[y][x + 1] = new_list[y][x + 1], new_list[y][x]
    return new_list
