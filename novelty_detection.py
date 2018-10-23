from tensorflow.python.keras.layers import Input, Dense
from tensorflow.python.keras.models import Model

import numpy as np
import pandas

import matplotlib.pyplot as plt



import create_input
RANDOM_SEED = 9

# creating uniform points for training data
# 5500 uniformly distributed points in circle radius 4 centered at (0,0)
train_uniform_pts = create_input.create_train_data(100, 4, 5500)

# creating testing data
# 5000 uniform points, 500 gaussian-distributed points at (1,1)
test_uniform_pts = create_input.create_train_data(100, 4, 5000)
test_anomaly_pts = create_input.create_test_data(3, [1, 1], 0.3, 500)
test_pts = np.concatenate((test_uniform_pts, test_anomaly_pts))

train_pts = pandas.DataFrame(train_uniform_pts, columns=["x", "y", "label"])
test_pts  = pandas.DataFrame(test_pts, columns=["x", "y", "label"])

train_y = train_pts["label"].values
train_x = train_pts.drop(['label'], axis=1).values # drop the class column and make to np array
test_y  = test_pts["label"].values
test_x  = test_pts.drop(["label"], axis=1).values # drop the class column and make to np array

input_dim = train_x.shape[1]

# create model for neural network
input_data = Input(shape=(input_dim,))
hidden = Dense(1, activation='tanh')(input_data)
output = Dense(input_dim, activation='sigmoid')(hidden)

# build and fit/train neural network
autoencoder = Model(inputs=input_data, outputs=output)
autoencoder.compile(optimizer='sgd', loss='binary_crossentropy')
autoencoder.fit(train_x, train_x, shuffle=True, epochs=10, batch_size=2000, validation_data=(test_x, test_x), verbose=0)

# test neural network on data set with anomaly

predictions = autoencoder.predict(test_x)
mse = np.mean(np.power(test_x - predictions, 2), axis=1)
error_df = pandas.DataFrame({"Reconstruction_Error": mse, 'True_Class': test_y})

predicted_classes = []
threshold = 0.5

for row in mse:
    if row > threshold:
        predicted_classes.append(0)
    else:
        predicted_classes.append(1)

predicted_classes = np.asarray(predicted_classes)

false_pos = 0
false_neg = 0
correct_one = 0
correct_zero = 0

all_zero = np.count_nonzero(test_y == 0)
all_one = np.count_nonzero(test_y == 1)

for i in range(test_y.shape[0]):
    if test_y[i] == 0 and predicted_classes[i] == 1:
        false_pos +=1
    if test_y[i] == 1 and predicted_classes[i] == 0:
        false_neg +=1
    if test_y[i] == 1 and predicted_classes[i] == 1:
        correct_one += 1
    if test_y[i] == 0 and predicted_classes[i] == 0:
        correct_zero += 1

print("number of zeros", all_zero)
print("number of ones", all_one)
print("number of correct zeros", correct_zero)
print("number of correct ones", correct_one)
print("number of false positives", false_pos)
print("number of false negatives", false_neg)
print("accuracy", correct_zero/all_zero)
print("false positive rate", false_pos/all_zero)



# plot all of the data points
colors = {0: "b", 1: "r"}
plt.figure(1)
plt.title("Training data")
plt.scatter(train_x[:,0], train_x[:,1], c='blue') # training data
plt.figure(2)
plt.title("Testing Data")
plt.scatter(test_x[:,0], test_x[:,1], c=[colors[i] for i in test_y])
plt.figure(3)
plt.title("Testing data with predictions")
plt.scatter(test_x[:,0], test_x[:,1], c=[colors[i] for i in predicted_classes])

plt.show()



