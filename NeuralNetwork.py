import tensorflow as tf

import Heuristic
from Parameters import BATCH_SIZE, EPOCHS, MODEL_NAME, INPUT_DIM


def get_input_list_from_file(file_name):
    input_list = []
    output_list = []

    file = open(file_name, "r")
    training_data = file.read().splitlines()

    line = 0
    while line < len(training_data):
        solution_path = eval(training_data[line + 2])
        solution_length = int(training_data[line + 1])

        i = 1
        for path in solution_path[:-1]:
            input_data = Heuristic.NeuralNetwork().compute_input(path)
            input_list.append(input_data)
            output_list.append(solution_length - i)
            i += 1

        line += 3

    file.close()

    return input_list, output_list


def get_training_data(training_set):
    input_list = []
    output_list = []

    for line in training_set:
        input_data = Heuristic.NeuralNetwork.compute_input(line[0])
        input_list.append(input_data)
        output_list.append(line[1])

    return input_list, output_list


def split_data(input_list, output_list):
    data_size = len(input_list)
    # train_size = int(data_size * 2 / 3)
    train_size = data_size

    input_train = input_list[:train_size]
    output_train = output_list[:train_size]

    input_test = input_list[train_size:]
    output_test = output_list[train_size:]

    return input_train, output_train, input_test, output_test


def learn_heuristic(training_set):
    input_list, output_list = get_training_data(training_set)
    input_train, output_train, input_test, output_test = split_data(input_list, output_list)

    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Dense(128, activation=tf.keras.activations.relu, input_dim=INPUT_DIM))
    model.add(tf.keras.layers.Dense(128, activation=tf.keras.activations.relu))
    model.add(tf.keras.layers.Dense(1, activation=tf.keras.activations.softplus))

    model.compile(loss='mse',
                  optimizer='adam',
                  metrics=['accuracy'])

    model.fit(input_train, output_train, epochs=EPOCHS, batch_size=BATCH_SIZE)

    val_loss, val_acc = model.evaluate(input_train, output_train, batch_size=BATCH_SIZE)
    evaluate(model, input_test, output_test)
    print("Loss", val_loss, "ACC", val_acc)
    model.save(MODEL_NAME)


def evaluate(model, input_test, output_test):
    if len(input_test) == 0:
        return

    predictions = model.predict(input_test)

    num_predictions = len(input_test)
    diff = 0
    for i in range(num_predictions):
        val = predictions[i]
        result = int(round(val[0]))
        absolute_diff = abs(result - output_test[i])
        print('Predicted:', result, ' Actual:', output_test[i], 'Difference:', absolute_diff)
        diff += absolute_diff

    print("Error:", diff, "Mean:", diff / num_predictions)
