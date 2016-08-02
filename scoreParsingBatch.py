
from __future__ import print_function
import numpy as np
from scoreParser import scoreParser
from globalv import rhythm_label_num, pitch_max_num

fpitch = open('test_pitch_prob.txt', 'r')
frhythm = open('test_rhythm_prob.txt', 'r')

cnt_all = 0
cnt_pitch_match = 0
cnt_rhythm_match = 0

for i in xrange(3000):
    for j in xrange(3):
        #print j
        pitch_prob = np.empty((0, pitch_max_num), dtype = 'float32')
        rhythm_prob = np.empty((0, rhythm_label_num), dtype = 'float32')
        for k in xrange(39):
            cmp_pitch = fpitch.readline()
            #print(cmp_pitch.replace(':', ' '))
            cmp_pitch = [x.strip() for x in cmp_pitch.replace(':', ' ').replace('.', ' ').split()]


            line_pitch = fpitch.readline()

            cmp_rhythm = frhythm.readline()
            cmp_rhythm = [x.strip() for x in cmp_rhythm.replace(':', ' ').replace('.', ' ').split()]

            if (int(cmp_pitch[2]) == int(cmp_pitch[5]) and int(cmp_rhythm[2]) != 0):
                cnt_pitch_match += 1

            if (int(cmp_rhythm[2]) == int(cmp_rhythm[5]) and int(cmp_rhythm[2]) != 0):
                cnt_rhythm_match += 1

            if(int(cmp_rhythm[2]) != 0):
                cnt_all += 1

            line_rhythm = frhythm.readline()
            #pitch_prob = np.vstack((pitch_prob, np.array([float(f) for f in line_pitch.strip().split()])))
            #rhythm_prob = np.vstack((rhythm_prob, np.array([float(f) for f in line_rhythm.strip().split()])))
        # parser = scoreParser(pitch_prob, rhythm_prob)
        # rhythms, pitches = parser.parse()
        #
        # r_and_p = zip(rhythms, pitches)
        # with open('hmm_parsed_'+str(i*3+j) + '.txt', 'w') as f:
        #     for item in r_and_p:
        #         print(str(item[0]) + '\t' + item[1] , file = f)

print(cnt_pitch_match)
print(cnt_rhythm_match)
print(cnt_all)

fpitch.close()
frhythm.close()
