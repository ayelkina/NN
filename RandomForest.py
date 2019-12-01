from sklearn.ensemble import RandomForestClassifier

from Helper import Helper

model = RandomForestClassifier(n_estimators=50)
input_train, output_train, input_test, output_test, input_dim = Helper.get_learning_data()

model.fit(input_train, output_train)
print(model.score(input_test, output_test))
predictions = model.predict(input_test)

num_predictions = len(input_test)
diff = 0
for i in range(num_predictions):
    val = predictions[i]
    absolute_diff = abs(val - output_test[i])
    print('Predicted:', val, ' Actual:', output_test[i], 'Difference:', absolute_diff)
    diff += absolute_diff

print("Error:", diff, "Mean:", diff / num_predictions)
