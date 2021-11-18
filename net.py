from keras.models import Sequential
from tensorflow.keras.utils import to_categorical
from keras.layers import Dense, Input, Conv2D, Flatten
import numpy as np
from numpy import float32, int32

TRAIN = 9 * 10**4

model = Sequential()
model.add(Input(shape=(7, 7, 3)))
model.add(Conv2D(64, 4, activation='relu'))
# model.add(Conv2D(64, 3, activation='relu'))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(3, activation='relu'))

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

with open('squashed', 'r') as file:
    data = np.fromfile(file, sep=' ')

data = data.reshape(-1, 49*3+3)
np.random.shuffle(data)
train_data = data[:TRAIN]
test_data = data[TRAIN:]

train_data, train_labels = train_data[:,:-3], train_data[:,-3:]
test_data, test_labels = test_data[:,:-3], test_data[:,-3:]

# train_labels = to_categorical(train_labels[:,-1]+1)
# test_labels = to_categorical(test_labels[:,-1]+1)
train_data = train_data.reshape(-1, 7, 7, 3)
test_data = test_data.reshape(-1, 7, 7, 3)


model.fit(train_data, train_labels, epochs=100, validation_data=(test_data, test_labels))