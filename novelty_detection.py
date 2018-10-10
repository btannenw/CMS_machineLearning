import tensorflow as tf
from tensorflow.python.keras.layers import Input, Dense
from tensorflow.python.keras.models import Model, load_model
from tensorflow.python.keras.callbacks import ModelCheckpoint, TensorBoard
from tensorflow.python.keras import regularizers

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import create_input

pts = create_input.create_train_data(9, 4, 5500)

uniform_pts = create_input.create_train_data(100, 4, 5000)
anomaly = create_input.create_test_data(3, [1, 1], 0.3, 500)

full_test = np.concatenate((uniform_pts, anomaly))

input_data = Input(shape=(2,))
hidden1 = Dense(30, activation='tanh')(input_data)
hidden2 = Dense(30, activation='tanh')(hidden1)
hidden3 = Dense(10, activation='tanh')(hidden2)
output = Dense(2, activation='sigmoid')(hidden3)


autoencoder = Model(input_data, output)
autoencoder.compile(optimizer='adam', loss='binary_crossentropy')
autoencoder.fit(pts, pts, epochs=5, verbose=0)

predictions = autoencoder.predict(full_test)

mse = np.mean(np.power(full_test - predictions, 2), axis=1)
labels = np.concatenate((np.zeros(5000,), np.ones(500,)))

df_error = pd.DataFrame({'reco_error': mse, 'Label': labels})
df_error.describe()

outliers = df_error.index[df_error.reco_error > 0.1].tolist()

print("anomalous points", len(outliers))