from package.Model.Path import Path
from package.Utils.Parameters import GOAL
from package.Utils.Tiles import possible_moves

cdef class Astar:
    cdef public:
        object heuristic
        cdef int puzzle_size
        cdef int expanded_nodes
        object solution
        terminated

    def __init__(self, heuristic):
        self.heuristic = heuristic

    cpdef void solve(self, list input, int nodes_limit):
        self.expanded_nodes = 0
        self.terminated = False
        self.puzzle_size = len(input[0]) - 1
        cdef list expanded = []
        cdef list open_set = [Path(0, 0, [input])]
        cdef int min_cost = 0
        cdef int i, cost
        cdef list current_path
        cdef list path, new_path

        while open_set:
            if self.expanded_nodes > nodes_limit:
                self.solution.path = []
                self.terminated = True
                break

            min_cost = 9999999
            for state in open_set:
                if state.goal < min_cost:
                    min_cost = state.goal
                    self.solution = state

            open_set.remove(self.solution)
            current_path = self.solution.path[-1]
            if current_path == GOAL:
                break
            if current_path in expanded: continue
            for path in possible_moves(current_path, self.puzzle_size):
                if path in expanded: continue
                cost = self.solution.cost + 1
                new_path = self.solution.path + [path]
                open_set.append(Path(cost, self.heuristic.compute(path), new_path))
            expanded.append(current_path)
            self.expanded_nodes += 1
