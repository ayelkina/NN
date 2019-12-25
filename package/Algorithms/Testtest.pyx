cdef class Rlass:
    def __init__(self):
        print("Init")

    cpdef int test_new(self):
        cdef int i = 0
        return i
