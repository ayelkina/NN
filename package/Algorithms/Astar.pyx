from package.Utils.Parameters import GOAL
from package.Utils.Tiles import possible_moves

cdef class Astar:
    cdef public:
        object heuristic
        cdef int puzzle_size
        cdef int expanded_nodes
        cdef list solution
        terminated

    def __init__(self, heuristic):
        self.heuristic = heuristic

    cpdef void solve(self, input, int nodes_limit):
        self.expanded_nodes = 0
        self.terminated = False
        self.solution = []
        self.puzzle_size = len(input[0]) - 1
        cdef list expanded = []
        cdef list open_set = [[0, input]]
        cdef int shortest_solution_index = 0
        cdef int i, cost
        cdef list current_path = []
        cdef list path, new_path

        while open_set:
            if self.expanded_nodes > nodes_limit:
                self.solution = []
                self.terminated = True
                break

            for i in range(1, len(open_set)):
                if open_set[shortest_solution_index][0] > open_set[i][0]:
                    shortest_solution_index = i

            self.solution = open_set[shortest_solution_index]
            open_set = open_set[:shortest_solution_index] + open_set[shortest_solution_index + 1:]
            current_path = self.solution[-1]
            if current_path == GOAL:
                break
            if current_path in expanded: continue
            for path in possible_moves(current_path, self.puzzle_size):
                if path in expanded: continue
                cost = self.solution[0] + self.heuristic.compute(path)
                new_path = [cost] + self.solution[1:] + [path]
                open_set.append(new_path)
                expanded.append(current_path)
            self.expanded_nodes += 1
