import tensorflow as tf

from Utils import TrainingData
from Utils.Parameters import BATCH_SIZE, EPOCHS, NN_MODEL_NAME, INPUT_DIM


def learn_heuristic(training_set):
    input_list, output_list = TrainingData.get_training_data(training_set)
    input_train, output_train, input_test, output_test = TrainingData.split_data(input_list, output_list)

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
    print("/n Loss", val_loss, "ACC", val_acc)
    model.save(NN_MODEL_NAME)


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
