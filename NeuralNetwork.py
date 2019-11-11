import tensorflow as tf

import Heuristic

input_list = []
bootstrap_input = []
output_list = []
heuristics = []


def get_output_by_number(output):
    if output == 'LinearConflict':
        return 0
    elif output == 'Manhattan':
        return 1
    elif output == 'Misplaced':
        return 2
    elif output == 'ColumnsMisplaced':
        return 3
    elif output == 'RowsMisplaced':
        return 4
    return 5


# def get_training_data():
file = open("training_data_2.txt", "r")

training_data = file.read().splitlines()
line = 0

while line < len(training_data):
    inp = eval(training_data[line])
    input_data = []
    input_data.append(Heuristic.Manhattan().compute(inp))
    input_data.append(Heuristic.LinearConflict().compute(inp))
    input_data.append(Heuristic.Misplaced().compute(inp))
    input_data.append(Heuristic.ColumnsMisplaced().compute(inp))
    input_data.append(Heuristic.RowsMisplaced().compute(inp))
    input_data.append(Heuristic.Gasching().compute(inp))
    input_list.append(input_data)
    heuristics.append(get_output_by_number(training_data[line + 2]))
    solution_path = eval(training_data[line + 3])
    bootstrap_input.append(solution_path)
    output_list.append(len(solution_path))
    line += 4

file.close()

train_size = 150
# Train features
input_train = input_list[:train_size]
output_train = output_list[:train_size]

# Test features
input_test = input_list[train_size:]
output_test = output_list[train_size:]

input_count = 6
data_count = 245
x = tf.placeholder(tf.float32, [data_count, input_count])
y = tf.placeholder(tf.float32, [data_count, None])

model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Dense(64, activation=tf.keras.activations.sigmoid, input_dim=input_count))
model.add(tf.keras.layers.Dense(64, activation=tf.keras.activations.sigmoid))
model.add(tf.keras.layers.Dense(1))

model.compile(loss='mse',
              optimizer='adam',
              metrics=['accuracy'])

model.fit(input_train, output_train, epochs=500, batch_size=10)

val_loss, val_acc = model.evaluate(input_train, output_train, batch_size=10)
predictions = model.predict(input_train)

num_predictions = data_count - train_size
diff = 0

for i in range(num_predictions):
    val = predictions[i]
    # print(description_test.iloc[i])
    print('Predicted: ', val[0], 'Actual: ', output_test[i], '\n')
    # diff += abs(val[0] - labels_test.iloc[i])

model.save('heuristic.model')
