
"""
    A toy model stacking bidirectional rnn over cnn
"""

#from __future__ import division, print_function, absolute_import

import tensorflow as tf
import numpy as np
import tflearn
from tflearn.layers.recurrent import bidirectional_rnn, BasicLSTMCell
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.normalization import local_response_normalization
from tflearn.layers.estimator import regression

import tflearn.datasets.mnist as mnist
X, Y, testX, testY = mnist.load_data(one_hot=True)
Y = np.zeros([55000/20, 10])
X = X.reshape([-1, 28, 28, 1])
testX = testX.reshape([-1, 28, 28, 1])

# mnist net
network = input_data(shape=[None, 28, 28, 1], name = "input")
network = conv_2d(network, 32, 3, activation='relu', regularizer="L2")
network = max_pool_2d(network, 2)
network = local_response_normalization(network)
network = conv_2d(network, 64, 3, activation='relu', regularizer="L2")
network = max_pool_2d(network, 2)
network = local_response_normalization(network)
network = fully_connected(network, 128, activation='tanh')
# network = dropout(network, 0.8)

nframes = 20
network = tf.reshape(network, [-1, nframes, 128])
network = bidirectional_rnn(network, BasicLSTMCell(128), BasicLSTMCell(128))#, return_seq = True)
# network = bidirectional_rnn(network, BasicLSTMCell(256), BasicLSTMCell(256), return_seq = True)
# network = dropout(network, 0.5)

network = fully_connected(network, 10, activation='softmax') #what's the number of output?
network = regression(network, optimizer='adam', learning_rate=0.01,
                     loss='categorical_crossentropy', name='target')


# Training
model = tflearn.DNN(network, tensorboard_verbose=1)
model.fit({'input': X}, {'target': Y}, n_epoch=20,
           validation_set=({'input': testX}, {'target': testY}),
           snapshot_step=100, show_metric=True, run_id='convnet_birnn')









