
from globv import const_rows, const_cols, label_num
from rhythmMap import rhythmMap
import numpy as np

class mono(object):

    def __init__(self, frame_len, hop_size):
        self._frame_len = frame_len
        self._hop = hop_size

    def _load_sample(self, rmap):
        sample = np.empty((0, const_rows, self._frame_len), dtype = 'float32')
        label = np.empty((0, label_num), dtype = 'float32')
        i = 0
        while True:
            start = i
            end = i + self._hop
            if end >= const_cols:
                break
            data, lab = rmap.slice(start, end)
            sample = np.vstack([sample, ])
            label = np.append(label, lab)
        return sample, label

    def load_data(self):
        X = np.empty((0, const_rows, self._frame_len), dtype = 'float32')
        Y = np.empty((0, const_rows, label_num), dtype = 'float32')
        testX = np.empty((0, const_rows, self._frame_len), dtype = 'float32')
        testY = np.empty((0, const_rows, label_num), dtype = 'float32')

        #load training data
        with open("train.txt", "r") as file:
            for line in file:
                [img_name, label_name] = line.strip().split()
                rmap = rhythmMap(img_name, label_name)
                sample, label = self._load_sample(rmap)
                X = np.append(X, sample, axis = 0)
                Y = np.append(Y, label)

        #load testing data
        with open("test.txt", "r") as file:
            for line in file:
                [img_name, label_name] = line.strip().split()
                rmap = rhythmMap(img_name, label_name)
                sample, label = self._load_sample(rmap)
                testX = np.append(X, sample, axis=0)
                testY = np.append(Y, label)

        return X,Y,testX,testY