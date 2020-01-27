from abc import abstractmethod


class AbstractMachineLearning:

    @abstractmethod
    def learn_heuristic(self, training_set, maximizing_heuristic, goal):
        ...

    @abstractmethod
    def evaluate(self, model, input_test, output_test):
        ...

    @abstractmethod
    def get_maximizing_heuristic(self):
        ...

    @abstractmethod
    def get_base_heuristic(self):
        ...
