import functools
import tensorflow as tf
from tensorflow.models.rnn import rnn_cell
from tensorflow.models.rnn import rnn
from monodata import mono
import numpy as np

def lazy_property(function):
    attribute = '_' + function.__name__

    @property
    @functools.wraps(function)
    def wrapper(self):
        if not hasattr(self, attribute):
            setattr(self, attribute, function(self))
        return getattr(self, attribute)
    return wrapper


class SequenceLabelling:

    def __init__(self, data, target, dropout, num_hidden=200, num_layers=3):
        self.data = data
        self.target = target
        self.dropout = dropout
        self._num_hidden = num_hidden
        self._num_layers = num_layers
        self.prediction
        self.error
        self.optimize

    @lazy_property
    def prediction(self):
        # Recurrent network.
        network = rnn_cell.LSTMCell(self._num_hidden)
        network = rnn_cell.DropoutWrapper(
            network, output_keep_prob=self.dropout)
        network = rnn_cell.MultiRNNCell([network] * self._num_layers)
        output, _ = rnn.dynamic_rnn(network, data, dtype=tf.float32)
        # Softmax layer.
        max_length = int(self.target.get_shape()[1])
        num_classes = int(self.target.get_shape()[2])
        weight, bias = self._weight_and_bias(self._num_hidden, num_classes)
        # Flatten to apply same weights to all time steps.
        output = tf.reshape(output, [-1, self._num_hidden])
        prediction = tf.nn.softmax(tf.matmul(output, weight) + bias)
        prediction = tf.reshape(prediction, [-1, max_length, num_classes])
        return prediction

    @lazy_property
    def cost(self):
        cross_entropy = -tf.reduce_sum(
            self.target * tf.log(self.prediction), reduction_indices=1)
        cross_entropy = tf.reduce_mean(cross_entropy)
        return cross_entropy

    @lazy_property
    def optimize(self):
        learning_rate = 0.01
        optimizer = tf.train.AdagradOptimizer(learning_rate)
        return optimizer.minimize(self.cost)

    @lazy_property
    def error(self):
        mistakes = tf.not_equal(
            tf.argmax(self.target, 2), tf.argmax(self.prediction, 2))
        return tf.reduce_mean(tf.cast(mistakes, tf.float32))

    @staticmethod
    def _weight_and_bias(in_size, out_size):
        weight = tf.truncated_normal([in_size, out_size], stddev=0.01)
        bias = tf.constant(0.1, shape=[out_size])
        return tf.Variable(weight), tf.Variable(bias)


if __name__ == '__main__':
    m = mono(1,1) #frame length, hop size
    X, Y , testX, testY = m.load_data(one_hot=1)
    nsamples, length, image_size = X.shape
    num_classes = Y.shape[2]
    data = tf.placeholder(tf.float32, [None, length, image_size])
    target = tf.placeholder(tf.float32, [None, length, num_classes])
    dropout = tf.placeholder(tf.float32)
    model = SequenceLabelling(data, target, dropout)
    sess = tf.Session()
    sess.run(tf.initialize_all_variables())
    for epoch in range(10):
        for run in range(100):
            print run
            indices = np.random.randint(0, nsamples, size = 10)
            batchX = X[indices, :, :]
            batchY = Y[indices, :, :]
            print batchX.shape
            print batchY.shape
            sess.run(model.optimize, {
                data: batchX, target: batchY, dropout: 0.5})
        error = sess.run(model.error, {
            data: testX, target: testY, dropout: 0.5})
        print('Epoch {:2d} error {:3.1f}%'.format(epoch + 1, 100 * error))
