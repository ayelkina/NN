import datetime
import getopt
import sys

import pyximport
from prettytable import PrettyTable

from package.MachineLearning.NeuralNetwork import NeuralNetworkModel
from package.MachineLearning.RandomForest import RandomForestModel
from package.Utils.Helper import generate_goal

pyximport.install()
from package.Utils import Compare
from package.Algorithms.BLHF import BLHF


def main(argv):
    goal, mode = '', ''
    nn_name, rf_name = [], []
    number = 10

    try:
        opts, args = getopt.getopt(argv, "s:r:n:m:e:",
                                   ["size=", "randomforest=", "neuralnetwork=", "mode=", "elements="])
    except getopt.GetoptError:
        print('Error. Command line structure: Main.py -s <size> -r <random forest model> -n <neural network model>'
              '-m <[Learn, Compare]>, -e <number of elements to compare>]')
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-s', '-size'):
            goal = generate_goal(int(arg))
        elif opt == '-r':
            rf_name = arg.split(',')
        elif opt == '-n':
            nn_name = arg.split(',')
        elif opt in ('-m', '--mode'):
            mode = arg.lower()
        elif opt in ('-e', '-elements'):
            number = int(arg)

    if goal == '':
        goal = generate_goal(4)

    if not rf_name and not nn_name:
        print("Error. Please give the name for random forest model (rf <name>) or neural network model (nn <name>)")
        sys.exit(0)

    if mode in ('l', 'learn'):
        learn(nn_name, rf_name, goal)
    elif mode in ('c', 'compare'):
        compare(number, nn_name, rf_name, goal)
    else:
        print("Error. Mode can be L (Learn), or C (Compare)")
        sys.exit(0)


def compare(number, nn_name: list, rf_name: list, goal):
    learning_models = []
    for name in nn_name:
        learning_models.append(NeuralNetworkModel(name))
    for name in rf_name:
        learning_models.append(RandomForestModel(name))

    output = Compare.compare(number, learning_models, goal)
    table = PrettyTable()
    table.field_names = ["Heuristics", "Expanded nodes", "Suboptimality", "Time"]
    for result in output:
        table.add_row([result.heuristic, result.expanded_nodes, result.subopt, result.duration])

    print(table)
    print(datetime.datetime.now())


def learn(nn_name, rf_name, goal):
    learning_model = ''

    if nn_name:
        print("Learn neural network")
        learning_model = NeuralNetworkModel(nn_name[0])
    elif rf_name:
        learning_model = RandomForestModel(rf_name[0])
        print("Learn random forest")

    print(datetime.datetime.now())
    algorithm = BLHF(learning_model, goal)
    algorithm.execute()
    print(datetime.datetime.now())


if __name__ == "__main__":
    main(sys.argv[1:])
