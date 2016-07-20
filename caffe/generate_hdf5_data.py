
from __future__ import print_function
import h5py
import numpy as np
from globalv import const_cols, const_rows
from monodata import mono


m = mono(1,1) #frame length, hop size
X, Y , testX, testY = m.load_data(one_hot=1)

batch_train = 10
N_train = batch_train*const_cols
shape_train = (N_train, 1, const_rows, 1) #one channel, width = 1, height = const_rows

batch_test = 3
N_test = batch_test*const_cols
shape_test = (N_test, 1, const_rows, 1) #one channel, width = 1, height = const_rows

DIR = "/N/dc2/projects/omrdl/data/hdf5/" #dir on bigred2

#prepare training data
cnt = 0

train_fn = "train_music.txt"
test_fn = "test_music.txt"

open(train_fn, "w").close()
open(test_fn, "w").close()

while cnt < X.shape[0]:
    h5_fn = str(cnt) + "_train" + ".h5"
    with h5py.File(h5_fn, 'w') as f:
        data = np.empty(shape_train)
        label = np.empty([N_train, ])
        clip_markers = np.empty([N_train, ])

        for i in xrange(const_cols):
            for ii in xrange(batch_train):
                idx = i*batch_train + ii
                print(idx)
                data[idx] = X[cnt+ii][i][np.newaxis, ..., np.newaxis]
                label[idx] = np.where(Y[cnt+ii][i] == 1)[0]
                clip_markers[idx] = 0 if i == 0 else 1
        print("here")
        print(data.shape)
        f['label'] = label
        f['data'] = data
        f['clip_markers'] = clip_markers

    with open(train_fn, "a") as f:
        print(DIR + h5_fn, file = f)

    cnt += batch_train

#prepare testing data
cnt = 0
while cnt < testX.shape[0]:
    h5_fn = str(cnt) + "_test" + ".h5"
    with h5py.File(h5_fn, 'w') as f:
        data = np.empty(shape_test)
        label = np.empty([N_test, ])
        clip_markers = np.empty([N_test, ])

        for i in xrange(const_cols):
            for ii in xrange(batch_test):
                idx = i * batch_test + ii
                data[idx] = testX[cnt + ii][i][np.newaxis, ..., np.newaxis]
                label[idx] = np.where(testY[cnt + ii][i] == 1)[0]
                clip_markers[idx] = 0 if i == 0 else 1
        f['label'] = label
        f['data'] = data
        f['clip_markers'] = clip_markers

    with open(test_fn, "a") as f:
        print(DIR + h5_fn, file = f)

    cnt += batch_test

