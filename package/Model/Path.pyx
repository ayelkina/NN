cdef class Path:
    cdef public:
        cdef int cost
        cdef int heuristic
        cdef int goal
        cdef list path

    def __init__(self, int cost, int heuristic, list path):
        self.cost = cost
        self.heuristic = heuristic
        self.path = path
        self.goal = cost + heuristic
