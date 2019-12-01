import tensorflow as tf

from Helper import Helper
from Parameters import BATCH_SIZE, EPOCHS, MODEL_NAME

input_train, output_train, input_test, output_test, input_dim = Helper.get_learning_data()

model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Dense(128, activation=tf.keras.activations.relu, input_dim=input_dim))
model.add(tf.keras.layers.Dense(128, activation=tf.keras.activations.relu))
model.add(tf.keras.layers.Dense(1, activation=tf.keras.activations.softplus))

model.compile(loss='mse',
              optimizer='adam',
              metrics=['accuracy'])

model.fit(input_train, output_train, epochs=EPOCHS, batch_size=BATCH_SIZE)

val_loss, val_acc = model.evaluate(input_train, output_train, batch_size=BATCH_SIZE)
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
model.save(MODEL_NAME)
