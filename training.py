from functional_net import Output, create_model
import numpy as np
from keras.metrics import CategoricalCrossentropy as CCmetric
from keras.losses import CategoricalCrossentropy as CCloss

with open("boards", "r") as file:
    data = np.fromfile(file, dtype=np.int32, sep=" ")

NUM_OF_VALUES = 11
data = data.reshape(-1, 49 * 3 + 10)
np.random.shuffle(data)
input1 = data[:, : 49 * 3].reshape(-1, 7, 7, 3)
input2 = data[:, 49 * 3 : 49 * 3 + 2]
# output1 = data[:, -8:-1]
output2 = np.eye(NUM_OF_VALUES)[data[:, -1]]

TRAIN = 35 * 10 ** 4
train_in = (input1[:TRAIN, :], input2[:TRAIN, :])
train_out = output2[:TRAIN]
# train_out = (output1[:TRAIN, :], output2[:TRAIN])

test_in = (input1[TRAIN:, :], input2[TRAIN:, :])
test_out = output2[TRAIN:]
# test_out = (output1[TRAIN:, :], output2[TRAIN:])

model = create_model(Output.value)
model.compile(
    loss=CCloss(),
    optimizer="adam",
    metrics=["accuracy", CCmetric()],
)
model.fit(x=train_in, y=train_out, epochs=30, validation_data=(test_in, test_out))

model.save("trained_model_values")
del model
