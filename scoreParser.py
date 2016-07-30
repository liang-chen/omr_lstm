
from globalv import rhythm_label_num, pitch_max_num, dur_max_num, legitimate_dur, min_note_frames, pitch_shift, pitch_inverse_dict
from globalv import rhythmToDur, DurToRest, DurToRhythm

from math import log, isinf


class scoreState(object):
    def __init__(self, rhythm, pitch, type, index, total):
        self.rhythm = rhythm
        self.pitch = pitch
        self.type = type
        self.index = index
        self.total = total


class scoreParser(object):

    def __init__(self, pred_prob_pitch, pred_prob_rhythm):
        self._likelihood_pitch = pred_prob_pitch
        self._likelihood_rhythm = pred_prob_rhythm
        self._cols = pred_prob_pitch.shape[0]
        self._states = self._create_states()
        self._n_states = len(self._states)
        self._scores = [[-float("inf") for c in xrange(self._cols)] for r in xrange(self._n_states)]
        self._prev = [[-1 for c in xrange(self._cols)] for r in xrange(self._n_states)]

    def _create_states(self):
        states = []
        for t in xrange(dur_max_num + 1):
            states.append(scoreState(0, 0, "gap", 0, t))

        for r in legitimate_dur:
            for i in xrange(1, min_note_frames+1):
                for p in xrange(pitch_max_num):
                    for t in xrange(r, dur_max_num + 1):
                        states.append(scoreState(r, p, "note", i, t)) #actually this type corresponds to both notes and rests

        return states

    def _is_transition_okay(self, cur, next):
        #constraints
        if cur.type == "gap" and next.type == "gap" and cur.total == next.total:
            return True
        elif cur.type == "gap" and next.type == "note" and \
            cur.total + next.rhythm == next.total and \
            next.index == 1:
            return True
        elif cur.type == "note" and next.type == "gap" and \
            cur.total == next.total and cur.index == min_note_frames:
            return True
        elif cur.type == "note" and next.type == "note" and \
            cur.rhythm == next.rhythm and \
            cur.total == next.total and \
            cur.pitch == next.pitch and \
            (cur.index + 1 == next.index or \
            (cur.index == next.index and next.index == min_note_frames)): #same note
            return True
        elif cur.type == "note" and next.type == "note" and \
            cur.index == min_note_frames and next.index == 1 \
            and cur.total + next.rhythm == next.total: # different notes
            return True

        return False

    def _pitch_inverse_index(self, index):
        if index == 0:
            return "None"
        octave = (index + pitch_shift)/12
        pitch_class = index + pitch_shift - 12*octave

        if pitch_class in pitch_inverse_dict:
            return pitch_inverse_dict[pitch_class] + str(octave-2)
        elif pitch_class - 1 in pitch_inverse_dict:
            return pitch_inverse_dict[pitch_class - 1] + '#' + str(octave - 2)
        else:
            return pitch_inverse_dict[pitch_class + 1] + '-' + str(octave - 2)

    def parse(self):
        self._scores[0][0] = 0 #gap, total = 0

        ##forward pass
        for j in xrange(self._cols-1):
            print j
            for i in xrange(self._n_states):
                if isinf(self._scores[i][j]):
                    continue
                s = self._states[i]
                for ii in xrange(self._n_states):
                    ss = self._states[ii]
                    if not self._is_transition_okay(s,ss):
                        continue

                    r_index = 0
                    p_index = 0
                    if s.rhythm != 0: #note or rest
                        if s.pitch == 0:
                            r_index = DurToRest[s.rhythm]
                        else:
                            r_index = DurToRhythm[s.rhythm]
                            p_index = s.pitch

                    if(self._scores[i][j] + log(self._likelihood_rhythm[j][r_index] + 0.001) + \
                               log(self._likelihood_pitch[j][p_index] + 0.001) > self._scores[ii][j+1]):
                        self._scores[ii][j+1] = self._scores[i][j] + log(self._likelihood_rhythm[j][r_index] + 0.001) + \
                                                log(self._likelihood_pitch[j][p_index] + 0.001)
                        self._prev[ii][j+1] = i

        #backward pass
        cur_i = dur_max_num # the last gap state
        rhythms = []
        pitches = []
        total = []
        print "total = ", self._states[cur_i].total
        for j in xrange(self._cols - 1, 1, -1):
            s = self._states[cur_i]

            # if s.type == "note":
            #     rhythms = [s.rhythm] + rhythms
            #     pitches = [s.pitch] + pitches
            #     total = [s.total] + total

            if s.type == "note" and len(rhythms) == 0:
                rhythms = [s.rhythm] + rhythms
                pitches = [s.pitch] + pitches
                total = [s.total] + total
            if s.type == "note" and (s.rhythm != rhythms[0] or s.pitch != pitches[0] or s.total != total[0]):
                rhythms = [s.rhythm] + rhythms
                pitches = [s.pitch] + pitches
                total = [s.total] + total
            cur_i = self._prev[cur_i][j]
        pitches = [self._pitch_inverse_index(p) for p in pitches]
        print "total: ", total
        return rhythms, pitches