import pickle

from sklearn.ensemble import RandomForestClassifier

from package.Model.Heuristic import MaximizingWithRF, RandomForest
from package.Utils import TrainingData


class RandomForestModel:
    model_name = ''

    def __init__(self, name):
        self.model_name = name

    def learn_heuristic(self, training_set, maximizing_heuristic, goal):
        input_list, output_list = TrainingData.get_training_data(training_set, maximizing_heuristic, goal)
        input_train, output_train, input_test, output_test = TrainingData.split_data(input_list, output_list)

        model = RandomForestClassifier(n_estimators=200)
        model.fit(input_train, output_train)
        model.score(input_train, output_train)

        self.evaluate(model, input_test, output_test)
        pickle.dump(model, open(self.model_name, 'wb'))

        return model

    @staticmethod
    def evaluate(model, input_test, output_test):
        if len(input_test) == 0:
            return

        predictions = model.predict(input_test)
        num_predictions = len(input_test)
        diff = 0
        for i in range(num_predictions):
            val = predictions[i]
            absolute_diff = abs(val - output_test[i])
            diff += absolute_diff * absolute_diff

        print("Mean:", diff / num_predictions)

    def get_maximizing_heuristic(self):
        return MaximizingWithRF(self.model_name)

    def get_base_heuristic(self):
        return RandomForest(self.model_name)
