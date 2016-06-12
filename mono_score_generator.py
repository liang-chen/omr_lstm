# this generate a music-xml filen, a svg file and a png file

import subprocess as sp
import shlex
from music21 import *
from bs4 import BeautifulSoup
import cairosvg
import random
import os
us = environment.UserSettings()
#us.create()
us['musicxmlPath'] = '/Applications/MuseScore 2.app'
#us['musicxmlPath'] = '/Applications/LilyPond.app'
def gen_chord():
	pitch_space = ["G3","A3","B3","C4","D4","E4","F4","G4","A4","B4","C5","D5","E5","A5","B5"]
	accid_space = ["#","-",""]
	notenum = random.randrange(1,2)
	pitchlist = []
	chordlist = []
	i = 0
	while(i<notenum):
		pitch = random.choice(pitch_space)
		if pitch not in pitchlist:
			pitchlist.append(pitch)
			accid = random.choice(accid_space)
			n = note.Note(pitch[0]+accid+pitch[1])
			chordlist.append(n)
			i += 1
	mychord = chord.Chord(chordlist)
	return mychord,chordlist

def gen_dur(meas_length,onsetlist):
	if meas_length == 4:
		onset_space = [i*0.25+0.25 for i in range(0,16)]
		for j in range(2):
			onset_space += [i*0.5+0.5 for i in range(0,8)]
		for j in range(4):
			onset_space += [i+1 for i in range(0,4)]
		baddur = [0,4,3.5,1.75,3.75]
	dur = 0
	while(True):
		onset = 0
		while(onset<=onsetlist[-1]):
			onset = random.choice(onset_space)
		dur = onset-onsetlist[-1]
		if dur not in baddur:
			break
	onsetlist.append(onset)
	return dur,onset

def gen_score(meas_num):
	s = stream.Score(id='mainScore')
	p0 = stream.Part(id='part0')
	meas_length = 4
	p0.insert(0, meter.TimeSignature('4/4'))
	for m in range(meas_num):#just one measure
		meas = stream.Measure(number=m)
		onsetlist = [0]
		durlist = []
		chordlist = []
		notenum = 4
		while(1):
			#pitch = random.choice(pitch_space)
			#accid = random.choice(accid_space)
			#n = note.Note(pitch+accid+"4")
			n,chord = gen_chord()
			chordlist.append(chord)
			dur,onset = gen_dur(meas_length,onsetlist)
			n.duration = duration.Duration(dur)
			durlist.append(dur)
			meas.repeatAppend(n,1)
			if(onset == meas_length):
				break
		p0.append(meas)
	s.insert(0,p0)
	return s,durlist,chordlist

def musescore_to_svg(filename):
	cmd = "/Applications/MuseScore\ 2.app/Contents/MacOS/mscore "+filename+".xml"+" -o "+filename+".svg"
	print cmd
	try:
		p = sp.Popen(shlex.split(cmd),stdout=sp.PIPE, stderr=sp.PIPE)
		pout,perr = p.communicate()
		if p.returncode:
			print "error running command"
			sys.exit(1)
	except OSERROR:
		print "MuseScore is not available"
		sys.exit(1)

def generate_score_files(num):
	for i in range(num):
		print "Generate page num",i,"\n"
		datadir = "./meas/"
		if not os.path.exists(datadir):
			os.makedirs(datadir)
		filename = "./meas/"+"mono_44_"+str(i)
		s,durlist,chordlist = gen_score(1)
		#d = s.show('musicxml.png')
		#s.show()
		#s.write("lily.svg", filename)
		s.write("musicxml",filename+".xml")
		musescore_to_svg(filename)
		svg_file = filename + ".svg"
		png_file = filename + ".png"
		cairosvg.svg2png(url=svg_file,write_to=png_file)

if __name__ == "__main__":
	generate_score_files(10)

