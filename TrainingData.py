class TrainingData:
    input = []
    heuristic = ''
    solution_path = []
    solution_length = ''

    def __init__(self, Astar):
        self.input = Astar.input
        self.heuristic = Astar.heuristic
        self.solution_path = Astar.solution[1:]
        self.solution_length = Astar.expanded_nodes
