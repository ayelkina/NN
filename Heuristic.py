import enum


class Heuristic(enum.Enum):
    Manhattan = 0
    Misplaced = 1

    def compute(self, input):
        if self == Heuristic.Manhattan:
            return manhattan_distance(input)
        if self == Heuristic.Misplaced:
            return misplaced_tiles(input)


def misplaced_tiles(input):
    misplaced = 0
    compare = 0
    for i in range(4):
        for j in range(4):
            if input[i][j] != compare:
                misplaced += 1
            compare += 1
    return misplaced


def manhattan_distance(input):
    distance = 0
    for i in range(4):
        for j in range(4):
            if input[i][j] == 0: continue
            distance += abs(i - (input[i][j] / 4)) + abs(j - (input[i][j] % 4))
    return distance
