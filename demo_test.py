
import tensorflow as tf
from monodata import mono
from globv import model_path
from rhythmParser import rhythmParser
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
    #print testY[0:10,:,:]
    predict_prob = sess.run(model.prediction, {
            data: testX[0:1,:,:], target: testY[0:1,:,:], dropout: 0.5})

    prob = tf.transpose(predict_prob[0,:,:])

    print prob

    predict_label = sess.run(model.predict_label, {
        data: testX[0:1, :, :], target: testY[0:1, :, :], dropout: 0.5})

    print predict_label

    with sess.as_default():
        prob_ndarray = prob.eval()
    rp = rhythmParser(prob_ndarray)
    print rp.parse()
