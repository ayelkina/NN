import os

import Bootstrap
from Helper import Helper

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

if __name__ == "__main__":
    Bootstrap.run()
    print("Finish bootstrap")
    Helper.compare_heuristics(20)
