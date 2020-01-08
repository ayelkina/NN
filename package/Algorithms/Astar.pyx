from package.Model.Path import Path
from package.Utils.Tiles import possible_moves

cdef class Astar:
    cdef public:
        object heuristic
        cdef int expanded_nodes
        object solution
        terminated

    def __init__(self, heuristic):
        self.heuristic = heuristic

    cpdef void solve(self, list input, int nodes_limit, list goal):
        self.expanded_nodes = 0
        self.terminated = False
        cdef int puzzle_size = len(input[0]) - 1
        cdef int i, cost = 0
        cdef list current_path, path, new_path,  expanded = []
        cdef list open_set = [Path(0, 0, [input])]

        while open_set:
            if self.expanded_nodes > nodes_limit:
                self.solution.path = []
                self.terminated = True
                break

            self.solution = self.minimal_solution(open_set)
            current_path = self.solution.path[-1]
            if current_path == goal:
                break
            if current_path in expanded: continue
            for path in possible_moves(current_path, puzzle_size):
                if path in expanded: continue
                cost = self.solution.cost + 1
                new_path = self.solution.path + [path]
                open_set.append(Path(cost, self.heuristic.compute(path, goal), new_path))
            expanded.append(current_path)
            self.expanded_nodes += 1


    def minimal_solution(self, list open_set):
        cdef int min_cost = 9999999
        solution = ''
        for state in open_set:
            if state.goal < min_cost:
                min_cost = state.goal
                solution = state
        open_set.remove(solution)
        return solution