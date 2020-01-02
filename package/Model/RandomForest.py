import pickle

from sklearn.ensemble import RandomForestClassifier

from package.Model.Heuristic import MaximizingWithRF, RandomForest
from package.Utils import TrainingData
from package.Utils.Parameters import RF_MODEL_NAME


class RandomForestModel:
    def learn_heuristic(self, training_set, maximizing_heuristic):
        input_list, output_list = TrainingData.get_training_data(training_set, maximizing_heuristic)
        input_train, output_train, input_test, output_test = TrainingData.split_data(input_list, output_list)

        model = RandomForestClassifier(n_estimators=150)
        model.fit(input_train, output_train)
        model.score(input_train, output_train)

        self.evaluate(model, input_test, output_test)
        pickle.dump(model, open(RF_MODEL_NAME, 'wb'))

        return model

    def evaluate(self, model, input_test, output_test):
        if len(input_test) == 0:
            return

        predictions = model.predict(input_test)
        num_predictions = len(input_test)
        diff = 0
        for i in range(num_predictions):
            val = predictions[i]
            absolute_diff = abs(val - output_test[i])
            print('Predicted:', val, ' Actual:', output_test[i], 'Difference:', absolute_diff)
            diff += absolute_diff

        print("Error:", diff, "Mean:", diff / num_predictions)

    @staticmethod
    def get_maximizing_heuristic():
        return MaximizingWithRF()

    @staticmethod
    def get_base_heuristic():
        return RandomForest()
