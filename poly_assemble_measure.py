import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import matplotlib.image as mpimg
import numpy as np
#import cv2
from music21 import *
import random
import os
class primitive(object):
	def __init__(self,name,locbegin,locend,index):
		self.name = name
		self.locbegin = locbegin#a tuple
		self.locend = locend
		self.index = index
		self.width = 0
		self.height = 0
		self.edge = []
		self.partbeam = 0
		self.orderindex = 0#for stem or beam

def readprimlist(infile):
	f = open(infile,"r")
	data = f.readlines()
	primlist = []
	for d in data:
		symbol = d.split()
		name = symbol[0]
		locbegin = [float(symbol[1]),float(symbol[2])]
		locend = [float(symbol[3]),float(symbol[4])]
		width = float(symbol[5])
		height = float(symbol[6])
		p = primitive(name,locbegin,locend,len(primlist))
		p.width = width
		p.height = height
		primlist.append(p)
	return primlist

def svg2primlist(svg_file):
	soup = BeautifulSoup(open(svg_file),'xml')
	stafflist,barlist = findstaves(soup)
	primlist = []
	findnotes(soup,primlist)
	findstems(soup,primlist)
	findbeams(soup,primlist)
	findflags(soup,primlist)
	findaccid(soup,primlist)
	findmarkups(soup,primlist)
	findclefs(soup,primlist)
	findtimesigs(soup,primlist)
	#for i in primlist:
	#	print i.index,i.name,i.locbegin,i.locend
	return primlist,stafflist,barlist

def findstems(soup,primlist):
	stems = soup.find_all("polyline",{"class":"Stem"})
	for i in stems:
		locs = i["points"].split()
		begin = locs[0].split(",")
		end = locs[1].split(",")
		locbegin = [float(begin[0]),max(float(end[1]),float(begin[1]))]
		locend = [float(end[0]),min(float(begin[1]),float(end[1]))]
		primlist.append(primitive("stem",locbegin,locend,len(primlist)))

def findstaves(soup):
	stafflines = soup.find_all("polyline",{"class":"StaffLines"})
	stafflist = []
	barlist = []
	for i in stafflines:
		locs = i["points"].split()
		begin = locs[0].split(",")
		locbegin = [float(begin[0]),float(begin[1])]
		end = locs[1].split(",")
		locend = [float(end[0]),float(end[1])]
		if int(locbegin[0]) not in barlist:
			barlist.append(int(locbegin[0]))
		if int(locend[0]) not in barlist:
			barlist.append(int(locend[0]))
		stafflist.append(int(locbegin[1]))
	return stafflist,barlist

def findnotes(soup,primlist):
	notes = soup.find_all("path",{"class":"Note"})
	for i in notes:
		locs = i["d"].split()
		if len(locs)==25:
			name = "notesolid"
		elif len(locs)==56:
			name = "noteopen"
		else:
			name = "notewhole"
		locs = locs[0][1:]
		begin = locs.split(",")
		locbegin = [float(begin[0]),float(begin[1])]
		primlist.append(primitive(name,locbegin,locbegin,len(primlist)))

def findbeams(soup,primlist):
	beams = soup.find_all("path",{"class":"Beam"})
	for i in beams:
		locs = i["d"].split()
		begin = locs[1][1:].split(",")
		locbegin = [float(begin[0]),float(begin[1])]
		end = locs[3][1:].split(",")
		locend = [float(end[0]),float(end[1])]
		primlist.append(primitive("beam",locbegin,locend,len(primlist)))

def findflags(soup,primlist):
	hooks = soup.find_all("path",{"class":"Hook"})
	for i in hooks:
		locs = i["d"].split()
		begin = locs[1][1:].split(",")
		locbegin = [float(begin[0]),float(begin[1])]
		end = locs[3][1:].split(",")
		locend = [float(end[0]),float(end[1])]
		if len(locs)==44 or len(locs)==47:#flag down and flag up
			name = "1flag"
		elif len(locs)==82 or len(locs)==81:#flag down and flag up
			name = "2flag"
		else:
			print len(locs),"unknow hook\n"
			continue
		p = primitive(name,locbegin,locend,len(primlist))
		p.width = 8
		p.height = 16
		primlist.append(p)


def findclefs(soup,primlist):
    beams = soup.find_all("path",{"class":"Clef"})
    for i in beams:
        locs = i["d"].split()
        begin = locs[0][1:].split(",")
        locbegin = [float(begin[0]),float(begin[1])]
        locend = locbegin
        name = "treble"
        p = primitive(name,locbegin,locend,len(primlist))
        p.width = 20
        p.height = 40
        primlist.append(p)


def findtimesigs(soup,primlist):
    beams = soup.find_all("path",{"class":"TimeSig"})
    for i in beams:
        locs = i["d"].split()
        begin = locs[0][1:].split(",")
        locbegin = [float(begin[0]),float(begin[1])]
        locend = locbegin
        name = "TimeSig"
        p = primitive(name,locbegin,locend,len(primlist))
        p.width = 12
        p.height = 10
        primlist.append(p)

def findmarkups(soup,primlist):
    augdots = soup.find_all("path",{"class":"NoteDot"})
    for i in augdots:
        locs = i["d"].split()
        begin = locs[0][1:].split(",")
        locbegin = [float(begin[0]),float(begin[1])]
        locend = locbegin
        name = "augdot"
        p = primitive(name,locbegin,locend,len(primlist))
        p.width = 5
        p.height = 5
        primlist.append(p)

def findaccid(soup,primlist):
    beams = soup.find_all("path",{"class":"Accidental"})
    for i in beams:
        locs = i["d"].split()
        begin = locs[0][1:].split(",")
        locbegin = [float(begin[0]),float(begin[1])]
        locend = locbegin
        if len(locs)>10:
            if len(locs)==74:
                name = "flat"
            elif len(locs)==102:
                name = "sharp"
            elif len(locs)==32:
                name = "natural"
        p = primitive(name,locbegin,locend,len(primlist))
        p.width = 10
        p.height = 16
        primlist.append(p)

def write2file(outfile,primlist):
	f = open(outfile,"w")
	for i in primlist:
		mystr = i.name+" "+str(i.locbegin[0])+" "+str(i.locbegin[1])+" "+\
			str(i.locend[0])+" "+str(i.locend[1])+" "+\
			str(i.width)+" "+str(i.height)+"\n"
		f.write(mystr)
	f.close()



def linkStemEndNote(primlist):
	dx = 8
	dy = 5
	for i in primlist:
		if i.name!="stem":
			continue
		#find end head
		find = 0
		for j in primlist:
			if j.name!="notesolid" and j.name!="noteopen":
				continue
			if (abs(i.locbegin[0]-j.locbegin[0])<dx and\
					abs(i.locbegin[1]-j.locbegin[1])<dy):
				i.edge.append(j)
				j.edge.append(i)
				find = 1
				break
			if (abs(i.locend[0]-j.locbegin[0])<dx and\
					abs(i.locend[1]-j.locbegin[1])<dy):
				i.edge.append(j)
				j.edge.append(i)
				find = 1
				break
		if find == 0:
			print "link stem end note error\n"
			#print "aa",i.locbegin[0],
			#for j in primlist:
			#	if j.name=="noteopen":
			#		print "b",j.locbegin[0]


def linkStemFlag(primlist):
	d1 = 2
	for i in primlist:
		if i.name!="stem":
			continue
		#find flag
		for j in primlist:
			if j.name not in ["1flag","2flag"]:
				continue
			if (abs(i.locbegin[0]-j.locbegin[0])<d1 and\
					abs(i.locbegin[1]-j.locbegin[1])<d1):
				i.edge.append(j)
				j.edge.append(i)
				break
			if (abs(i.locend[0]-j.locbegin[0])<d1 and\
					abs(i.locend[1]-j.locbegin[1])<d1):
				i.edge.append(j)
				j.edge.append(i)
				break


def linkNoteAccidAugdot(primlist):
	d1 = 10 #for augdot
	d2 = 20 #for accid
	for i in primlist:
		if i.name!="notesolid" and i.name!="noteopen" and i.name!="notewhole":
			continue
		#find end head
		for j in primlist:
			if j.name in ["flat","sharp","natural"]:
				if ((i.locbegin[0]-j.locbegin[0])>0 and\
						(i.locbegin[0]-j.locbegin[0])<d2 and\
						abs(i.locbegin[1]-j.locbegin[1])<10):
					i.edge.append(j)
					j.edge.append(i)
			elif j.name == "augdot":
				if ((i.locbegin[0]-j.locbegin[0])<0 and\
						(j.locbegin[0]-i.locbegin[0])<d1 and\
						abs(i.locbegin[1]-j.locbegin[1])<10):
					i.edge.append(j)
					j.edge.append(i)

def linkStemRestNote(primlist):
	d1 = 5
	head_wid = 5#3#half_wid
	for i in primlist:
		if i.name!="notesolid" and i.name!="noteopen":
			continue
		find = 0
		connect = 0
		for j in i.edge:
			if j.name=="stem":
				connect = 1
				break
		if connect == 1:
			continue
		#find end head
		#print "h",i.locbegin[0]
		for j in primlist:
			if j.name!="stem":
				continue
			#print "l",j.locbegin[0],j.locbegin[1],j.locend[1]
			if ((abs(i.locbegin[0]-head_wid-j.locbegin[0])<d1 or\
					(abs(i.locbegin[0]+head_wid-j.locbegin[0])<d1)) and\
					(i.locbegin[1]<j.locbegin[1]+d1) and\
					(i.locbegin[1]>j.locend[1]-d1)):
				i.edge.append(j)
				j.edge.append(i)
				find = 1
				break
		if find==0:
			print "link stem rest note error\n"

def linkBeamEndStem(primlist):
	d1 = 2
	d2 = 5
	for i in primlist:
		if i.name!="beam":
			continue
		#find end head
		stemnum = 0
		for j in primlist:
			if j.name!="stem":
				continue
			if (abs(i.locbegin[0]-j.locbegin[0])<d1 and\
					abs(i.locbegin[1]-j.locbegin[1])<d2):
				i.edge.append(j)
				j.edge.append(i)
				stemnum += 1
			if (abs(i.locend[0]-j.locbegin[0])<d1 and\
					abs(i.locend[1]-j.locbegin[1])<d2):
				i.edge.append(j)
				j.edge.append(i)
				stemnum += 1
			if (abs(i.locbegin[0]-j.locbegin[0])<d1 and\
					abs(i.locbegin[1]-j.locend[1])<d2):
				i.edge.append(j)
				j.edge.append(i)
				stemnum += 1
			if (abs(i.locend[0]-j.locbegin[0])<d1 and\
					abs(i.locend[1]-j.locend[1])<d2):
				i.edge.append(j)
				j.edge.append(i)
				stemnum += 1
		if stemnum == 2:
			i.partbeam = 0
		elif stemnum == 1:
			i.partbeam = 1
		else:
			print "link beam end stem error,find ",stemnum,"stems\n"
			for j in i.edge:
				print j.locbegin

def linkBeamRestStem(primlist):
	d1 = 2
	d2 = 5
	for i in primlist:
		if i.name!="stem":
			continue
		for j in primlist:
			if j.name!="beam":
				continue
			if j in i.edge:
				continue
			if ((i.locbegin[0]>j.locend[0]) and\
					(i.locbegin[0]<j.locbegin[0])):
				midy = 0.5*(j.locend[1]+j.locbegin[1])
				if(abs(i.locbegin[1]-midy)<10):
					i.edge.append(j)
					j.edge.append(i)
				elif(abs(i.locend[1]-midy)<10):
					i.edge.append(j)
					j.edge.append(i)


def linkBeamBeam(primlist):
	d1 = 2
	d2 = 5
	for i in primlist:
		if i.name!="beam":
			continue
		for j in primlist:
			if j==i or j.name!="beam" or j in i.edge:
				continue
			#only look for overlap shorter beam
			if (i.locbegin[0]>=j.locend[0] and i.locbegin[0]<=j.locbegin[0] and\
				i.locend[0]>=j.locend[0] and i.locbegin[0]<=j.locbegin[0]):
				hi = 0.5*(i.locbegin[1]+i.locend[1])
				hj = 0.5*(j.locbegin[1]+j.locend[1])
				if(abs(hi-hj)<10):
					i.edge.append(j)
					j.edge.append(i)
					i.orderindex = j.orderindex + 1

def prim2sym(primlist):
	linkBeamBeam(primlist)
	linkStemEndNote(primlist)
	linkStemFlag(primlist)
	linkStemRestNote(primlist)
	linkBeamEndStem(primlist)
	linkBeamRestStem(primlist)
	linkNoteAccidAugdot(primlist)

def beamloc(beambegin,beamend,x):
	slope = 1.0*(beamend[1]-beambegin[1])/(beamend[0]-beambegin[0])
	#print slope
	#print x-beambegin[0]
	y = beambegin[1] + (x-beambegin[0])*slope
	return y

def segmentBeamStem(primlist):
	for i in primlist:
		if i.name!="beam" or i.orderindex!=0:
			continue
		stemlist = []
		for j in i.edge:
			if j.name=="stem":
				stemlist.append(j)
		stemlist = sorted(stemlist, key=lambda x: x.locbegin[0])
		#print len(stemlist)
		left = stemlist[0]
		for j in range(1,len(stemlist)):
			right = stemlist[j]
			beamnum = 0
			miny = 1000
			maxy = 0
			for k in left.edge:
				if k.name=="beam" and k.partbeam==0:
					#beam end on left, not consider
					if(abs(k.locbegin[0]-left.locbegin[0])<2):
						continue
					else:
						if k.locbegin[1]<miny:
							miny = k.locbegin[1]
						if k.locend[1]<miny:
							miny = k.locend[1]
						if k.locbegin[1]>maxy:
							maxy = k.locbegin[1]
						if k.locend[1]>maxy:
							maxy = k.locend[1]
						beamnum += 1
			name = str(beamnum)+"beam"
			locbegin = [0,0]
			locbegin[0] = left.locbegin[0]
			locbegin[1] = miny
			locend = [0,0]
			locend[0] = right.locbegin[0]
			locend[1] = beamloc(i.locend,i.locbegin,locend[0])
			p = primitive(name,locbegin,locend,len(primlist))
			primlist.append(p)
			left = right

def generateSample(myimg,x,x2,y,y2):
	cur = np.zeros((y2-y,x2-x),dtype='uint8')
	print x,x2,y,y2
	print myimg.shape
	for j in range(y,y2):
		for i in range(x,x2):
			cur[j-y][i-x] = myimg[j][i]
			print myimg[i][j],
		print
	return cur

def generateTrain(primlist,myimg,pagenum):
	count = 0
	#cur = np.zeros((96,96),dtype='uint8')
	for i in primlist:
		#plt.imshow(white)
		if i.name == "treble":
			x = int(i.locbegin[0]-0.5*i.width)
			y = int(i.locbegin[1]-0.5*i.height)
			x2 = int(i.locbegin[0]+0.5*i.width)
			y2 = int(i.locbegin[1]+0.5*i.height)
			cur = myimg[y:y2,x:x2]
			#cur = generateSample(myimg,x,x2,y,y2)
			#cv2.imwrite(str(count)+i.name+".png",cur)
			#plt.imshow(cur)
			#plt.savefig(str(count)+i.name+".png")
		elif i.name == "flat":
			x = int(i.locbegin[0]-0.5*i.width)
			y = int(i.locbegin[1]-0.5*i.height)
			x2 = int(i.locbegin[0]+0.5*i.width)
			y2 = int(i.locbegin[1]+0.5*i.height)
			cur = myimg[y:y2,x:x2]
		elif i.name == "sharp":
			x = int(i.locbegin[0]-0.6*i.width)
			y = int(i.locbegin[1]-0.7*i.height)
			x2 = int(i.locbegin[0]+0.4*i.width)
			y2 = int(i.locbegin[1]+0.3*i.height)
			cur = myimg[y:y2,x:x2]
		elif i.name in ["1flag","2flag"]:
			print "haha"
			x = int(i.locbegin[0]-0*i.width)
			y = int(i.locbegin[1]-0*i.height)
			x2 = int(i.locbegin[0]+1*i.width)
			y2 = int(i.locbegin[1]+1*i.height)
			cur = myimg[y:y2,x:x2]
		elif i.name == "notesolid":
			x = int(i.locbegin[0]-5)
			y = int(i.locbegin[1]-2)
			x2 = int(i.locbegin[0]+5)
			y2 = int(i.locbegin[1]+8)
			cur = myimg[y:y2,x:x2]
		elif i.name == "noteopen":
			x = int(i.locbegin[0]-7)
			y = int(i.locbegin[1]-3)
			x2 = int(i.locbegin[0]+3)
			y2 = int(i.locbegin[1]+7)
			cur = myimg[y:y2,x:x2]
		elif i.name == "stem":
			x = int(i.locbegin[0]-5)
			y = min(int(i.locbegin[1]),int(i.locend[1]))
			y2 = max(int(i.locbegin[1]),int(i.locend[1]))+1
			x2 = int(i.locend[0]+5)
			if (y2-y<5 or y2-y>40):
				continue
			cur = myimg[y:y2,x:x2]
		elif i.name in ["1beam","2beam"]:
			#print i.name
			x = int(i.locbegin[0])-2
			y = min(int(i.locbegin[1]),int(i.locend[1]))-5
			y2 = max(int(i.locbegin[1]),int(i.locend[1]))+5
			x2 = int(i.locend[0])+2
			#print x,y,x2,y2
			if y2-y<20:
				y2 = y +20
			if x2-x<5:
				continue
			cur = myimg[y:y2,x:x2]
		else:
			continue
		name = "./training/"+pagenum+"_"+i.name+str(count)+".png"
		mpimg.imsave(name,cur)

		count += 1

def get_stem_box(stem):
	left = stem.locbegin[0]-1
	right = stem.locbegin[0]
	up = min(stem.locbegin[1],stem.locend[1])-5
	down = max(stem.locbegin[1],stem.locend[1])+5
	if(down-up<10):
		print "stem height error"
		return 0,0,0,0
	notenum = 0
	for i in stem.edge:
		if i.name=="notesolid" or i.name=="noteopen":
			notenum += 1
			#print i.name,i.locbegin
			if i.locbegin[0]-5<left:
				left = min(left,i.locbegin[0]-5)
			if i.locbegin[0]+5>right:
				right = max(right,i.locbegin[0]+5)
			for j in i.edge:
				if j.name in ["sharp","flat","natural"]:
					#print j.name
					if j.locbegin[0]-5<left:
						left = min(left,j.locbegin[0]-5)
				if j.name == "augdot":
					#print j.name
					if j.locend[0]+5>right:
						right = max(right,j.locend[0]+5)
		elif i.name in ["1flag","2flag"]:
			#print i.name
			if i.locbegin[0]+5>right:
				right = max(right,i.locbegin[0]+8)
		elif i.name == "beam":
			#print i.name
			if i.locbegin[0]>right:
				right = max(right,stem.locbegin[0]+5)
			if i.locend[0]<left:
				left = min(left,stem.locbegin[0]-5)
	if right-left==1:
		print "stem range error"
		return 0,0,0,0
	return left,right,up,down

def primitive_assemble(primlist):
	prim2sym(primlist)
	segmentBeamStem(primlist)#break beam and add beam1,beam2 to primlist
	#generateTrain(primlist,myimg,pagenum)

def dur2durlabel(dur):
	if dur==1:
		return 1
	elif dur ==2:
		return 2
	elif dur ==3:
		return 3
	elif dur == 4:
		return 4
	elif dur==6:
		return 5
	elif dur==8:
		return 6
	elif dur==12:
		return 7

def match_score2prim(score,primlist,stafflist,barlist,myimg,extraspace):
	notelist = score.getElementsByClass('Part')[0].getElementsByClass('Measure')[0].getElementsByClass('Chord')
	alllist = score.getElementsByClass('Part')[0].getElementsByClass('Measure')[0].elements
	print len(alllist)
	#read all stem primitives
	stemlist = []
	for i in primlist:
		if i.name == "stem":
			stemlist.append(i)
	stemlist.sort(key=lambda x:x.locbegin[0],reverse=False)
	#for i in stemlist:
	#	print i.locbegin[0]
	note_range = []
	cols = range(barlist[1]-barlist[0])#10 pixels per column, overlap by 5
	column_labels = [0 for i in range(len(cols))]
	reply2 = ""
	if len(alllist)-1!=len(stemlist):
		print "alllist doesn't match stemlist"
		return
	for i in range(len(alllist)):
		if i == 0:
			continue
		chord = alllist[i]
		isnote = chord.isNote
		ischord = chord.isChord
		if isnote==True:
			pitch_label = [chord.pitch.name+str(chord.pitch.octave)]
		elif ischord==True:
			pitch_label = []
			chord = chord.sortAscending()
			for j in chord.pitches:
				pitch_label.append(j.name+str(j.octave))
		#print pitch_label
		dur_label = int(4*chord.duration.quarterLength)
		dur_label = dur2durlabel(dur_label)
		left,right,up,down = get_stem_box(stemlist[i-1])#alllist has a time signature
		if left == right:
			continue
		#up = stafflist[0]-20
		#down = stafflist[4]+20
		up = max(stafflist[0]-extraspace,int(up))
		down = min(stafflist[4]+extraspace,int(down))
		if(int(down)-int(up)<20):
			print "sample height error"
			continue
		cur = myimg[int(up):int(down),int(left):int(right)]
		debugdir = "./debug/"
		if not os.path.exists(debugdir):
			os.makedirs(debugdir)
		pngname = "./debug/"+str(dur_label)+"_"+str(int(left))+".png"
		xratio = 1.0*(0.5*(left+right)-barlist[0])/(barlist[1]-barlist[0])
		yratio = 1.0*(0.5*(up+down)-stafflist[0]+20)/(40+stafflist[4]-stafflist[0])
		wratio = 1.0*(right-left)/(barlist[1]-barlist[0])
		hratio = 1.0*(down-up)/(40+stafflist[4]-stafflist[0])
		reply2 += str(dur_label)+" "+\
				str(int(left)-int(barlist[0]))+" "+\
				str(int(right)-int(barlist[0]))+" "
		#reply2 += str(dur_label)+" "+\
		#		str(xratio)+" "+str(yratio)+" "+\
		#		str(wratio)+" "+str(hratio)+ " "
		reply2 += str(len(pitch_label)) + " "
		for j in pitch_label:
			reply2 += j + " "
		reply2 += "\n"
		mpimg.imsave(pngname,cur)
		for j in range(int(left)-barlist[0],int(right)-barlist[0]):
			column_labels[j] = dur_label
	reply = ""
	for i in column_labels:
		reply += str(i) + " "
	reply += "\n"
	return reply,reply2

def generate_label(num):
	for i in range(num):
		pagenum = i
		print "Label page num",pagenum
		infile = "./meas/"+"poly_44_"+str(pagenum)
		#read svg file and assemble
		svg_file = infile + ".svg"
		primlist,stafflist,barlist= svg2primlist(svg_file)
		primitive_assemble(primlist)
		#read xml file
		xml_file = infile + ".xml"
		score = converter.parse(xml_file)
		#score.show('text')
		#cut out png, and write out label for each column
		myimg = mpimg.imread(infile+'.png')
		extraspace = 30
		cur = myimg[stafflist[0]-extraspace:stafflist[4]+extraspace,barlist[0]:barlist[1]]
		pngname = infile+"_s"+".png"
		mpimg.imsave(pngname,cur)
		column_labels,range_labels = match_score2prim(score,primlist,stafflist,barlist,myimg,extraspace)
		labelfile = infile+"_col.txt"
		f = open(labelfile,"w")
		f.write(column_labels)
		f.close()
		rangefile = infile+"_s.txt"
		f2 = open(rangefile,"w")
		f2.write(range_labels)
		f2.close()


if __name__ == "__main__":
	generate_label(2000)
