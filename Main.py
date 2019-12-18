import matplotlib.pyplot as plt

from Model.Heuristic import *
from Utils import CompareHeuristics

if __name__ == "__main__":
    # input = CompareHeuristics.generate_input_list(1)
    # algorithm = Astar(MaximizingWithNN())
    # algorithm.solve(input[0], 100)
    # print(len(algorithm.solution) -2)

    # Bootstrap.run()
    print("Finish bootstrap")
    x, y = CompareHeuristics.compare(10)
    x_pos = np.arange(len(x))

    plt.barh(x_pos, y, align='center', alpha=1)
    plt.yticks(x_pos, x)
    plt.xlabel('Expanded nodes')
    plt.title('15-puzzle')

    plt.savefig('puzzle_15.png')
    plt.show()
