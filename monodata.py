
from globalv import const_rows, const_cols, rhythm_label_num, pitch_label_num, pitch_dict, pitch_shift
from sequenceLabelGenerator import sequenceLabelGenerator
import numpy as np


class mono(object):
    def __init__(self, frame_len, hop_size):
        self._frame_len = frame_len
        self._hop = hop_size

    def _parse_label(self, label):
        rhythmLabel = label[0]
        pitchLabel = [None]*label[3]

        if label[3] >= 2:
            print "Reading multiple pitches!"

        if label[3] == 0:
            return rhythmLabel, 0

        pitches = label[4:]
        cnt = 0
        for pitch in pitches:
            octave = pitch[-1]
            name = pitch[0]
            pitch_index = (int(octave)+2)*12 + pitch_dict[name]
            if len(pitch) == 2:
                acc_index = 0
            elif pitch[1] == '-':
                acc_index = -1
            else:
                acc_index = 1

            pitchLabel[cnt] = pitch_index + acc_index
            cnt += 1

        return rhythmLabel, pitchLabel[0] - pitch_shift


    def _load_sample(self, labelG):
        sample = np.empty((0, int(self._frame_len*const_rows)), dtype = 'float32')
        rhythmLabel = np.empty((0, 1), dtype='int16')
        pitchLabel = np.empty((0, 1), dtype='int16')
        i = 0

        while True:
            start = i
            end = i + self._frame_len
            if end > const_cols:
                break
            data, lab = labelG.slice(start, end) # label is in the format: rhythm, left, right, num_pitch, pitch names
            sample = np.vstack((sample, np.reshape(data, [1, -1])))
            if lab is None: ##background
                rhythmLabel = np.vstack((rhythmLabel, 0))
                pitchLabel = np.vstack((pitchLabel, 0))
            else:
                rl, pl = self._parse_label(lab)
                rhythmLabel = np.vstack((rhythmLabel, rl))
                pitchLabel = np.vstack((pitchLabel, pl)) # to make pitch label continous from 1 - n
            i += self._hop

        return sample, rhythmLabel, pitchLabel

    def load_data(self):
        X = None
        rhythmY = None
        pitchY = None
        testX = None
        testrhythmY = None
        testpitchY = None

        cnt_train = 0
        cnt_test = 0

        #load training data
        with open("train.txt", "r") as file:
            for line in file:
                print cnt_train
                cnt_train += 1

                [img_name, label_name] = line.strip().split()
                labelG = sequenceLabelGenerator(img_name, label_name)
                sample, rhythmLabel, pitchLabel = self._load_sample(labelG)
                if X is None:
                    X = sample[np.newaxis,...]
                else:
                    X = np.vstack([X, sample[np.newaxis,...]])

                if rhythmY is None:
                    rhythmY = rhythmLabel[np.newaxis, ...]
                else:
                    rhythmY = np.vstack((rhythmY, rhythmLabel[np.newaxis, ...]))

                if pitchY is None:
                    pitchY = pitchLabel[np.newaxis, ...]
                else:
                    pitchY = np.vstack((pitchY, pitchLabel[np.newaxis, ...]))
                break


        #load testing data
        with open("test.txt", "r") as file:
            for line in file:
                print cnt_test
                cnt_test += 1

                [img_name, label_name] = line.strip().split()
                labelG = sequenceLabelGenerator(img_name, label_name)
                sample, rhythmLabel, pitchLabel = self._load_sample(labelG)
                if  testX is None:
                    testX = sample[np.newaxis,...]
                else:
                    testX = np.vstack([testX, sample[np.newaxis, ...]])

                if testrhythmY is None:
                    testrhythmY = rhythmLabel[np.newaxis, ...]
                else:
                    testrhythmY = np.vstack((testrhythmY, rhythmLabel[np.newaxis, ...]))

                if testpitchY is None:
                    testpitchY = pitchLabel[np.newaxis, ...]
                else:
                    testpitchY = np.vstack((testpitchY, pitchLabel[np.newaxis, ...]))
                break

        print "Data loading done!"

        return X,rhythmY,pitchY, testX, testrhythmY, testpitchY
