from tensorflow.keras.layers import Input, Dense, Conv2D, Flatten, Softmax, concatenate
from tensorflow.keras import Model


class Output:
    move = 1
    value = 2
    both = 3


def create_model(output):
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

    outputs = []
    if output & Output.move:
        output_move = Dense(7, activation=Softmax())(x)
        outputs.append(output_move)
    if output & Output.value:
        output_score = Dense(11, activation=Softmax())(x)
        outputs.append(output_score)

    inputs = [input_board, input_info]
    return Model(inputs=inputs, outputs=outputs)
