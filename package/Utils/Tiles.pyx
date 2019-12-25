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
    col, row = 0, 0

    for i in range(0, moves_from_goal):
        new_dir = directions[:]
        if col == 0:
            new_dir.remove(Directions.LEFT)
        if row == 0:
            new_dir.remove(Directions.UP)
        if col == puzzle_size:
            new_dir.remove(Directions.RIGHT)
        if row == puzzle_size:
            new_dir.remove(Directions.DOWN)
        if opposite_previous in new_dir:
            new_dir.remove(opposite_previous)

        direction = random.choice(new_dir)
        if direction == Directions.UP:
            move_up(tiles, col, row)
            row -= 1
            opposite_previous = Directions.DOWN
        elif direction == Directions.DOWN:
            move_down(tiles, col, row)
            row += 1
            opposite_previous = Directions.UP
        elif direction == Directions.RIGHT:
            move_right(tiles, col, row)
            col += 1
            opposite_previous = Directions.LEFT
        elif direction == Directions.LEFT:
            move_left(tiles, col, row)
            col -= 1
            opposite_previous = Directions.RIGHT

    return tiles

cpdef list possible_moves(list tiles, int puzzle_size):
    cdef list output = []
    cdef list new_list
    cdef int col, row
    col, row = get_zero_position(tiles)

    if row > 0:
        new_list = copy.deepcopy(tiles)
        new_list = move_up(new_list, col, row)
        output.append(new_list)

    if row < puzzle_size:
        new_list = copy.deepcopy(tiles)
        new_list = move_down(new_list, col, row)
        output.append(new_list)

    if col > 0:
        new_list = copy.deepcopy(tiles)
        new_list = move_left(new_list, col, row)
        output.append(new_list)

    if col < puzzle_size:
        new_list = copy.deepcopy(tiles)
        new_list = move_right(new_list, col, row)
        output.append(new_list)

    return output


def get_zero_position(tiles):
    cdef int row = 0
    cdef int col
    while 0 not in tiles[row]: row += 1
    col = tiles[row].index(0)
    return col, row

cpdef list move_up(list new_list, int col, int row):
    new_list[row][col], new_list[row - 1][col] = new_list[row - 1][col], new_list[row][col]
    return new_list

cpdef list move_down(list new_list, int col, int row):
    new_list[row][col], new_list[row + 1][col] = new_list[row + 1][col], new_list[row][col]
    return new_list

cpdef list move_left(list new_list, int col, int row):
    new_list[row][col], new_list[row][col - 1] = new_list[row][col - 1], new_list[row][col]
    return new_list

cpdef list move_right(list new_list, int col, int row):
    new_list[row][col], new_list[row][col + 1] = new_list[row][col + 1], new_list[row][col]
    return new_list
