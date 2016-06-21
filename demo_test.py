
import tensorflow as tf
from monodata import mono
from globv import model_path
from demo_train import SequenceLabelling


if __name__ == '__main__':
    m = mono(1,1) #frame length, hop size
    X, Y , testX, testY = m.load_data(one_hot=1)
    _, length, image_size = X.shape
    num_classes = Y.shape[2]
    data = tf.placeholder(tf.float32, [None, length, image_size])
    target = tf.placeholder(tf.float32, [None, length, num_classes])
    dropout = tf.placeholder(tf.float32)
    model = SequenceLabelling(data, target, dropout)

    saver = tf.train.Saver()
    sess = tf.Session()
    sess.run(tf.initialize_all_variables())

    ckpt = tf.train.get_checkpoint_state(model_path)
    saver.restore(sess, ckpt.model_checkpoint_path)
    error = sess.run(model.error, {
        data: testX, target: testY, dropout: 0.5})
    print('testing error {:3.1f}%'.format(100 * error))
