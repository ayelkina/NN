from pylab import *

from Utils import CompareHeuristics

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

if __name__ == "__main__":
    # Bootstrap.run()
    print("Finish bootstrap")

    x, y = CompareHeuristics.compare(20)
    x_pos = np.arange(len(x))

    plt.barh(x_pos, y, align='center', alpha=1)
    plt.yticks(x_pos, x)
    plt.xlabel('Expanded nodes')
    plt.title('15-puzzle')

    plt.savefig('puzzle_15.png')
    plt.show()
