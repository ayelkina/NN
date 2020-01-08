import datetime
import getopt
import sys
import matplotlib.pyplot as plt
import numpy as np
import pyximport

from prettytable import PrettyTable
from package.Model.NeuralNetwork import NeuralNetworkModel
from package.Model.RandomForest import RandomForestModel

pyximport.install()
from package.Utils import CompareHeuristics
from package.Algorithms import Bootstrap
from package.Utils.Parameters import goal_15, goal_24


def main(argv):
    goal, mode, rf_name, nn_name = '', '', '', ''
    number = 10

    try:
        opts, args = getopt.getopt(argv, "s:r:n:m:e:",
                                   ["size=", "randomforest=", "neuralnetwork=", "mode=", "elements="])
    except getopt.GetoptError:
        print('Error. Command line structure: Main.py -s <size> -rn <random forest model> -nn <neural network model>'
              '-m <[Learn, Compare]>, -e <number of elements to compare>]')
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-s', '-size'):
            if arg == '24':
                goal = goal_24
            else:
                goal = goal_15
        elif opt == '-r':
            rf_name = arg
        elif opt == '-n':
            nn_name = arg
        elif opt in ('-m', '--mode'):
            mode = arg.lower()
        elif opt in ('-e', '-elements'):
            number = int(arg)

    if rf_name == '' and nn_name == '':
        print("Error. Please give the name for random forest model (rf <name>) or neural network model (nn <name>)")
        sys.exit(0)

    if mode in ('l', 'learn'):
        learn(nn_name, rf_name, goal)
    elif mode in ('c', 'compare'):
        compare(number, nn_name, rf_name, goal)
    else:
        print("Error. Mode can be L (Learn), or C (Compare)")
        sys.exit(0)


def draw_bar_spot(x, y, goal):
    x_pos = np.arange(len(x))
    plt.barh(x_pos, y, align='center', alpha=1)
    plt.yticks(x_pos, x)
    plt.xlabel('Expanded nodes')
    size = len(goal[0])
    puzzle_type = str(size * size - 1)
    title = puzzle_type + '-puzzle'
    plt.title(title)

    plt.savefig(puzzle_type + '.png')
    plt.show()


def compare(number, nn_name, rf_name, goal):
    learning_models = []
    if nn_name != '':
        learning_models.append(NeuralNetworkModel(nn_name))
    if rf_name != '':
        learning_models.append(RandomForestModel(rf_name))

    output = CompareHeuristics.compare_with_subopt(number, learning_models, goal)
    table = PrettyTable()
    table.field_names = ["Heuristics", "Expanded nodes", "Suboptimality", "Time"]
    for result in output:
        table.add_row([result.heuristic, result.expanded_nodes, result.subopt, result.duration])

    print(table)


def learn(nn_name, rf_name, goal):
    learning_model = ''

    if nn_name != '':
        print("Learn neural network")
        learning_model = NeuralNetworkModel(nn_name)
    elif rf_name != '':
        learning_model = RandomForestModel(rf_name)
        print("Learn random forest")

    print(datetime.datetime.now())
    Bootstrap.run(learning_model, goal)
    print(datetime.datetime.now())


if __name__ == "__main__":
    main(sys.argv[1:])
