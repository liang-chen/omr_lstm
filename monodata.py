
from globv import const_rows, const_cols, label_num
from rhythmMap import rhythmMap
import numpy as np

class mono(object):

    def __init__(self, frame_len, hop_size):
        self._frame_len = frame_len
        self._hop = hop_size

    def _load_sample(self, rmap, one_hot):
        sample = np.empty((0, int(self._frame_len*const_rows)), dtype = 'float32')
        if one_hot == 0:
            label = np.empty((1, 0), dtype='int16')
        else:
            label = np.empty((0, label_num), dtype='int16')
        i = 0

        while True:
            start = i
            end = i + self._frame_len
            if end > const_cols:
                break
            data, lab = rmap.slice(start, end)
            sample = np.vstack((sample, np.reshape(data, [1, -1])))
            if one_hot == 0:
                label = np.append(label, lab)
            else:
                temp = np.zeros((1, label_num), dtype='int16')
                temp[0, lab] = 1
                label = np.vstack((label, temp))
            i += self._hop
        return sample, label

    def load_data(self, one_hot = 0):
        X = None
        Y = None
        testX = None
        testY = None

        #load training data
        with open("train.txt", "r") as file:
            for line in file:
                [img_name, label_name] = line.strip().split()
                rmap = rhythmMap(img_name, label_name)
                sample, label = self._load_sample(rmap, one_hot)
                if X is None:
                    X = sample[np.newaxis,...]
                else:
                    X = np.vstack([X, sample[np.newaxis,...]])

                if Y is None:
                    Y = label[np.newaxis, ...]
                else:
                    Y = np.vstack((Y, label[np.newaxis, ...]))

        #load testing data
        with open("test.txt", "r") as file:
            for line in file:
                [img_name, label_name] = line.strip().split()
                rmap = rhythmMap(img_name, label_name)
                sample, label = self._load_sample(rmap, one_hot)
                if testX is None:
                    testX = sample[np.newaxis,...]
                else:
                    testX = np.vstack([testX, sample[np.newaxis, ...]])

                if testY is None:
                    testY = label[np.newaxis, ...]
                else:
                    testY = np.vstack((testY, label[np.newaxis, ...]))

        return X,Y,testX,testY