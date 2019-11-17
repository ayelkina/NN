import os

from Helper import Helper

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

if __name__ == "__main__":
    Helper.compare_heuristics(100)
