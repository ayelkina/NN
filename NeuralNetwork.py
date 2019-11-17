import tensorflow as tf

import Heuristic
from Parameters import FILE_NAME, BATCH_SIZE, EPOCHS, MODEL_NAME

input_list = []
bootstrap_input = []
output_list = []
heuristics = []

input_size = ''
data_size = ''

file = open(FILE_NAME, "r")
training_data = file.read().splitlines()

line = 0
while line < len(training_data):
    inp = eval(training_data[line])
    input_data = Heuristic.NeuralNetwork().compute_input(inp)

    input_size = len(input_data)
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
out = output_list[-1]
inp = input_list[-1]
data_size = len(input_list)
# train_size = int(data_size * 2 / 3)
train_size = data_size
# Train features
input_train = input_list[:train_size]
output_train = output_list[:train_size]

# Test features
input_test = input_list[train_size:]
output_test = output_list[train_size:]

model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Dense(128, activation=tf.keras.activations.relu, input_dim=input_size))
model.add(tf.keras.layers.Dense(128, activation=tf.keras.activations.relu))
model.add(tf.keras.layers.Dense(1, activation=tf.keras.activations.softplus))

model.compile(loss='mse',
              optimizer='adam',
              metrics=['accuracy'])

model.fit(input_train, output_train, epochs=EPOCHS, batch_size=BATCH_SIZE)

val_loss, val_acc = model.evaluate(input_train, output_train, batch_size=BATCH_SIZE)
# predictions = model.predict(input_test)
#
# num_predictions = data_size - train_size
# diff = 0
# for i in range(num_predictions):
#     val = predictions[i]
#     result = int(round(val[0]))
#     absolute_diff = abs(result - output_test[i])
#     print('Predicted:', result, ' Actual:', output_test[i], 'Difference:', absolute_diff)
#     diff += absolute_diff
#
# print("Error:", diff, "Mean:", diff / num_predictions)
model.save(MODEL_NAME)
