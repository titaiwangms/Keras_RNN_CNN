from typing import Tuple, List, Dict

import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.layers import Embedding
from keras.layers import SimpleRNN, GRU, LSTM
from keras.layers import Conv1D, GlobalAveragePooling1D, MaxPooling1D
from keras.layers import Conv2D, MaxPooling2D, Flatten, Bidirectional, GlobalMaxPooling1D
from keras import optimizers
from keras.callbacks import EarlyStopping

def create_toy_rnn(input_shape: tuple,
                   n_outputs: int) -> Tuple[keras.Model, Dict]:
    """Creates a recurrent neural network for a toy problem.

    The network will take as input a sequence of number pairs, (x_{t}, y_{t}),
    where t is the time step. It must learn to produce x_{t-3} - y{t} as the
    output of time step t.

    This method does not call Model.fit, but the dictionary it returns alongside
    the model will be passed as extra arguments whenever Model.fit is called.
    This can be used to, for example, set the batch size or use early stopping.

    :param input_shape: The shape of the inputs to the model.
    :param n_outputs: The number of outputs from the model.
    :return: A tuple of (neural network, Model.fit keyword arguments)
    """
    model = Sequential()
    model.add(SimpleRNN(256, input_shape=input_shape, return_sequences=True, activation = 'tanh'))
    model.add(Dense(1, activation="linear"))

    model.compile(loss='mse',
                optimizer='adam')

    return (model, {}) 


def create_mnist_cnn(input_shape: tuple,
                     n_outputs: int) -> Tuple[keras.Model, Dict]:
    """Creates a convolutional neural network for digit classification.

    The network will take as input a 28x28 grayscale image, and produce as
    output one of the digits 0 through 9. The network will be trained and tested
    on a fraction of the MNIST data: http://yann.lecun.com/exdb/mnist/

    This method does not call Model.fit, but the dictionary it returns alongside
    the model will be passed as extra arguments whenever Model.fit is called.
    This can be used to, for example, set the batch size or use early stopping.

    :param input_shape: The shape of the inputs to the model.
    :param n_outputs: The number of outputs from the model.
    :return: A tuple of (neural network, Model.fit keyword arguments)
    """
    model = Sequential()
    model.add(Conv2D(64, 3, activation='relu', input_shape=input_shape))
    model.add(Conv2D(64, 3, activation='relu'))
    model.add(MaxPooling2D(3))
    model.add(Dropout(0.25))
    model.add(Conv2D(128, 3, activation='relu'))
    model.add(MaxPooling2D(3))
    model.add(Flatten())
    model.add(Dense(n_outputs, activation='softmax'))

    model.compile(loss='categorical_crossentropy',
                optimizer='adam',
                metrics=['accuracy'])

    return (model, {})


def create_youtube_comment_rnn(vocabulary: List[str],
                               n_outputs: int) -> Tuple[keras.Model, Dict]:
    """Creates a recurrent neural network for spam classification.

    This network will take as input a YouTube comment, and produce as output
    either 1, for spam, or 0, for ham (non-spam). The network will be trained
    and tested on data from:
    https://archive.ics.uci.edu/ml/datasets/YouTube+Spam+Collection

    Each comment is represented as a series of tokens, with each token
    represented by a number, which is its index in the vocabulary. Note that
    comments may be of variable length, so in the input matrix, comments with
    fewer tokens than the matrix width will be right-padded with zeros.

    This method does not call Model.fit, but the dictionary it returns alongside
    the model will be passed as extra arguments whenever Model.fit is called.
    This can be used to, for example, set the batch size or use early stopping.

    :param vocabulary: The vocabulary defining token indexes.
    :param n_outputs: The number of outputs from the model.
    :return: A tuple of (neural network, Model.fit keyword arguments)
    """

    max_features = len(vocabulary)

    model = Sequential()
    model.add(Embedding(max_features, 200))
    model.add(Bidirectional(GRU(64, activation='linear', dropout=0.5)))
    model.add(Dense(n_outputs, activation='sigmoid'))
    adam = optimizers.Adam(lr=0.01) 

    model.compile(loss='binary_crossentropy',
                optimizer=adam,
                metrics=['accuracy'])

    return (model, {})

def create_youtube_comment_cnn(vocabulary: List[str],
                               n_outputs: int) -> Tuple[keras.Model, Dict]:
    """Creates a convolutional neural network for spam classification.

    This network will take as input a YouTube comment, and produce as output
    either 1, for spam, or 0, for ham (non-spam). The network will be trained
    and tested on data from:
    https://archive.ics.uci.edu/ml/datasets/YouTube+Spam+Collection

    Each comment is represented as a series of tokens, with each token
    represented by a number, which is its index in the vocabulary. Note that
    comments may be of variable length, so in the input matrix, comments with
    fewer tokens than the matrix width will be right-padded with zeros.

    This method does not call Model.fit, but the dictionary it returns alongside
    the model will be passed as extra arguments whenever Model.fit is called.
    This can be used to, for example, set the batch size or use early stopping.

    :param vocabulary: The vocabulary defining token indexes.
    :param n_outputs: The number of outputs from the model.
    :return: A tuple of (neural network, Model.fit keyword arguments)
    """

    max_features = len(vocabulary)

    model = Sequential()
    model.add(Embedding(max_features, 200))
    model.add(Conv1D(64, 3, activation='relu'))
    model.add(GlobalMaxPooling1D())
    model.add(Dropout(0.25))
    model.add(Dense(n_outputs, activation='sigmoid'))

    adam = optimizers.Adam(lr=0.01)
    model.compile(loss='binary_crossentropy',
                optimizer=adam,
                metrics=['accuracy'])

    return (model, {})


