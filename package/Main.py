import datetime
import matplotlib.pyplot as plt
import pyximport
import numpy as np

from package.Model.NeuralNetwork import NeuralNetworkModel
from package.Model.RandomForest import RandomForestModel

pyximport.install()
from package.Utils import CompareHeuristics
from package.Algorithms import Bootstrap
from package.Algorithms import Astar
from package.Model import NeuralNetwork
from package.Model import RandomForest
from package.Utils import TrainingData
from package.Utils.Parameters import FILE_NAME
from package.Utils.Tiles import possible_moves

if __name__ == "__main__":
    training_set = []
    input = CompareHeuristics.generate_input_list(1)
    # print(input[0])
    # training_set.append([input[0], 19])
    # heur = MaximizingWithNN()
    # NeuralNetwork.learn_heuristic(training_set, heur)
    # get_predicted_values_with_maximum(input[0], heur)
    # algorithm = Astar(MaximizingWithNN())
    # algorithm.solve(input[0], 100)
    # print(len(algorithm.solution) -2)

    print(datetime.datetime.now())
    learning_model = RandomForestModel()
    Bootstrap.run(learning_model)
    print(datetime.datetime.now())
    #
    # print("Finish bootstrap")
    x, y = CompareHeuristics.compare(2, learning_model)
    x_pos = np.arange(len(x))
    #
    plt.barh(x_pos, y, align='center', alpha=1)
    plt.yticks(x_pos, x)
    plt.xlabel('Expanded nodes')
    plt.title('15-puzzle')
    #
    plt.savefig('forest.png')
    plt.show()