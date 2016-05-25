from music21 import *
import random
#us = environment.UserSettings()
#us.create()
#us['musicxmlPath'] = '/Applications/MuseScore 2.app'
onset_space = [i*0.25+0.25 for i in range(0,16)]
onset_space += [i*0.5+0.5 for i in range(0,8)]
onset_space += [i+1 for i in range(0,4)]
pitch_space = ["C","D","E","F","G","A","B"]
accid_space = ["#","-",""]
#print onset_space
s = stream.Score(id='mainScore')
p0 = stream.Part(id='part0')
p0.insert(0, meter.TimeSignature('4/4'))
for m in range(20):
	meas = stream.Measure(number=m)
	onsetlist = [0]
	notenum = 4
	while(1):
		pitch = random.choice(pitch_space)
		accid = random.choice(accid_space)
		n = note.Note(pitch+accid+"4")
		onset = 0
		while(onset<=onsetlist[-1]):
			onset = random.choice(onset_space)
		#onset = onsetlist[-1]+0.25
		dur = onset-onsetlist[-1]
		onsetlist.append(onset)
		n.duration = duration.Duration(dur)
		meas.repeatAppend(n,1)
		if(onset == onset_space[-1]):
			break
	p0.append(meas)
s.insert(0,p0)
s.show()
