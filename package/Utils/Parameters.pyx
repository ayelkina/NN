FILE_NAME = "short_len.txt"
BATCH_SIZE = 1000
EPOCHS = 500

TRAIN_SIZE_FACTOR = 1
INPUT_DIM = 7

TIMEOUT = 10000
MIN_DISTANCE = 15
MAX_DISTANCE = 35

NN_MODEL_NAME = 'heuristic_2912.model'
RF_MODEL_NAME = 'random_forest_2712.model'

cdef list goal_24 = [[0, 1, 2, 3, 4], [5, 6, 7, 8, 9], [10, 11, 12, 13, 14], [15, 16, 17, 18, 19], [20, 21, 22, 23, 24]]
cdef list goal_15 = [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]]
PUZZLE_SIZE = 4
GOAL = goal_15
