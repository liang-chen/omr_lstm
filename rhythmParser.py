
from globalv import label_num, min_note_frames
from math import log, isinf


class rhythmState(object):
    def __init__(self, rhythm, type, index, total):
        self.rhythm = rhythm
        self.type = type
        self.index = index
        self.total = total


class rhythmParser(object):

    def __init__(self, pred_prob):
        self._likelihood = pred_prob
        self._cols = pred_prob.shape[1]
        self._states = self._create_states()
        self._n_states = len(self._states)
        self._scores = [[-float("inf") for c in xrange(self._cols)] for r in xrange(self._n_states)]
        self._prev = [[-1 for c in xrange(self._cols)] for r in xrange(self._n_states)]

    def _create_states(self):
        states = []
        for t in xrange(label_num):
            states.append(rhythmState(0, "gap", 0, t))

        for r in xrange(1, label_num):
            for i in xrange(1, min_note_frames+1):
                for t in xrange(r, label_num):
                    states.append(rhythmState(r, "note", i, t))

        return states

    def _is_transition_okay(self, cur, next):
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
            cur.total == next.total and \
            (cur.index + 1 == next.index or \
            (cur.index == next.index and next.index == min_note_frames)):
            return True
        elif cur.type == "note" and next.type == "note" and \
            cur.index == min_note_frames and next.index == 1 \
            and cur.total + next.rhythm == next.total:
            return True

        return False

    def parse(self):
        self._scores[0][0] = 0 #gap, total = 0

        ##forward pass
        for j in xrange(self._cols-1):
            for i in xrange(self._n_states):
                if isinf(self._scores[i][j]):
                    continue
                s = self._states[i]
                for ii in xrange(self._n_states):
                    ss = self._states[ii]
                    if not self._is_transition_okay(s,ss):
                        continue
                    if(self._scores[i][j] + log(self._likelihood[s.rhythm][j]) >
                       self._scores[ii][j+1]):
                        self._scores[ii][j+1] = self._scores[i][j] + log(self._likelihood[s.rhythm][j])
                        self._prev[ii][j+1] = i

        #backward pass
        cur_i = label_num - 1
        rhythms = []
        for j in xrange(self._cols - 1, 1, -1):
            s = self._states[cur_i]
            if s.type == "note" and s.index == 1:
                rhythms = [s.rhythm] + rhythms
            cur_i = self._prev[cur_i][j]

        return rhythms