import numpy as np
import pyximport
import tensorflow as tf

from package.MachineLearning.AbstractMachineLearning import AbstractMachineLearning

pyximport.install()
from package.Model.Heuristic import MaximizingWithNN, NeuralNetwork

from package.Utils import TrainingData
from package.Utils.Parameters import BATCH_SIZE, EPOCHS, INPUT_DIM


class NeuralNetworkModel(AbstractMachineLearning):
    model_name = ''

    def __init__(self, name):
        self.model_name = name

    def learn_heuristic(self, training_set, maximizing_heuristic, goal):
        input_list, output_list = TrainingData.get_training_data(training_set, maximizing_heuristic, goal)
        input_train, output_train, input_test, output_test = TrainingData.split_data(input_list, output_list)

        model = tf.keras.models.Sequential()
        model.add(tf.keras.layers.Dense(128, activation=tf.keras.activations.sigmoid, input_dim=INPUT_DIM))
        model.add(tf.keras.layers.Dense(128, activation=tf.keras.activations.sigmoid))
        model.add(tf.keras.layers.Dense(1, activation=tf.keras.activations.softplus))

        model.compile(loss='mse',
                      optimizer='adam',
                      metrics=['accuracy'])

        model.fit(np.array(input_train), output_train, epochs=EPOCHS, batch_size=BATCH_SIZE)
        self.evaluate(model, input_test, output_test)
        model.save(self.model_name)
        return self.model_name

    def evaluate(self, model, input_test, output_test):
        if len(input_test) == 0:
            return

        predictions = model.predict(input_test)
        num_predictions = len(input_test)
        diff = 0
        for i in range(num_predictions):
            val = predictions[i]
            result = int(round(val[0]))
            absolute_diff = abs(result - output_test[i])
            diff += absolute_diff * absolute_diff

        print("Mean:", diff / num_predictions)

    def get_maximizing_heuristic(self):
        return MaximizingWithNN(self.model_name)

    def get_base_heuristic(self):
        return NeuralNetwork(self.model_name)
