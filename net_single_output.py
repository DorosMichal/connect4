from tensorflow.keras.layers import Input, Dense, Conv2D, Flatten, Softmax, concatenate
from tensorflow.keras import Model

input_board = Input(shape=(7, 7, 3))
x = Conv2D(64, 4, activation="relu")(input_board)
x = Conv2D(64, 4, activation="relu")(x)
after_conv = Flatten()(x)

# input player to move
input_info = Input(shape=(2,))

x = concatenate([input_info, after_conv])
x = Dense(128, activation="relu")(after_conv)
x = Dense(64, activation="relu")(x)
x = Dense(64, activation="relu")(x)

output_move = Dense(7, activation=Softmax())(x)
# output_score = Dense(1, activation="linear")(x)
output_score = Dense(11, activation=Softmax())(x)

inputs = [input_board, input_info]
outputs = [output_move, output_score]

model = Model(inputs=inputs, outputs=outputs)
