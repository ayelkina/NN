import datetime

import pyximport

pyximport.install()
from package.Algorithms import Bootstrap

if __name__ == "__main__":
    # input = CompareHeuristics.generate_input_list(1)
    # heur = MaximizingWithNN()
    # get_predicted_values_with_maximum(input[0], heur)
    # algorithm = Astar(MaximizingWithNN())
    # algorithm.solve(input[0], 100)
    # print(len(algorithm.solution) -2)

    print(datetime.datetime.now())
    Bootstrap.run()
    print(datetime.datetime.now())

    # print("Finish bootstrap")
    # x, y = CompareHeuristics.compare(10)
    # x_pos = np.arange(len(x))
    #
    # plt.barh(x_pos, y, align='center', alpha=1)
    # plt.yticks(x_pos, x)
    # plt.xlabel('Expanded nodes')
    # plt.title('15-puzzle')
    #
    # plt.savefig('puzzle_15.png')
    # plt.show()
