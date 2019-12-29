import datetime

import pyximport

pyximport.install()
from package.Algorithms import Bootstrap

if __name__ == "__main__":
    # training_set = []
    # input = CompareHeuristics.generate_input_list(1)
    # print(input[0])
    # training_set.append([input[0], 19])
    # heur = MaximizingWithNN()
    # NeuralNetwork.learn_heuristic(training_set, heur)
    # get_predicted_values_with_maximum(input[0], heur)
    # algorithm = Astar(MaximizingWithNN())
    # algorithm.solve(input[0], 100)
    # print(len(algorithm.solution) -2)

    print(datetime.datetime.now())
    Bootstrap.run()
    print(datetime.datetime.now())
    #
    # print("Finish bootstrap")
    # x, y = CompareHeuristics.compare(10)
    # x_pos = np.arange(len(x))
    # #
    # plt.barh(x_pos, y, align='center', alpha=1)
    # plt.yticks(x_pos, x)
    # plt.xlabel('Expanded nodes')
    # plt.title('15-puzzle')
    # #
    # plt.savefig('puzzle_15_3.png')
    # plt.show()
