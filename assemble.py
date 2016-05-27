class primitive(object):
	def __init__(self,name,locbegin,locend,index):
		self.name = name
		self.locbegin = locbegin#a tuple
		self.locend = locend
		self.index = index
		self.width = 0
		self.height = 0
		self.refloc = [0,0]
		self.edge = []
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
		primlist.append(primitive(name,locbegin,locend,len(primlist)))
	return primlist

def linkStemEndNote(primlist):
	d1 = 2
	for i in primlist:
		if i.name!="stem":
			continue
		#find end head
		for j in primlist:
			if j.name!="note":
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


def linkStemRestNote(primlist):
	d1 = 5
	head_wid = 3#half_wid
	for i in primlist:
		if i.name!="note":
			continue
		connect = 0
		for j in i.edge:
			if j.name=="stem":
				connect = 1
				break
		if connect == 1:
			continue
		#find end head
		for j in primlist:
			if j.name!="stem":
				continue
			if (abs(i.locbegin[0]-head_wid-j.locbegin[0])<d1 and\
					(i.locbegin[1]<j.locbegin[1]+d1) and\
					(i.locbegin[1]>j.locend[1]-d1)):
				i.edge.append(j)
				j.edge.append(i)
				break

def linkBeamEndStem(primlist):
	d1 = 2
	d2 = 5
	for i in primlist:
		if i.name!="beam":
			continue
		#find end head
		for j in primlist:
			if j.name!="stem":
				continue
			if (abs(i.locbegin[0]-j.locbegin[0])<d1 and\
					abs(i.locbegin[1]-j.locbegin[1])<d2):
				i.edge.append(j)
				j.edge.append(i)
			if (abs(i.locend[0]-j.locbegin[0])<d1 and\
					abs(i.locend[1]-j.locbegin[1])<d2):
				i.edge.append(j)
				j.edge.append(i)
			if (abs(i.locbegin[0]-j.locend[0])<d1 and\
					abs(i.locbegin[1]-j.locend[1])<d2):
				i.edge.append(j)
				j.edge.append(i)
			if (abs(i.locend[0]-j.locend[0])<d1 and\
					abs(i.locend[1]-j.locend[1])<d2):
				i.edge.append(j)
				j.edge.append(i)

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
					j.orderindex = i.orderindex + 1
		print i.index,i.name,
		for j in i.edge:
			print j.index,j.name,
		print

def prim2sym(primlist):
	linkBeamBeam(primlist)
	linkStemEndNote(primlist)
	linkStemRestNote(primlist)
	linkBeamEndStem(primlist)
	linkBeamRestStem(primlist)
	#linkNoteAccid(primlist)

class TreeNode(object):
	def __init__(self):
		self.label = ""
		self.primindex = 0
		self.left = None
		self.right = None
	def __str__(self):
		if self.label == "prim":
			reply = str(self.primindex)
		else:
			reply = self.label
		if self.left:
			reply += " "+self.left.__str__()
		if self.right:
			reply += " "+self.right.__str__()
		return reply

def PrimTree(cur):
	node = TreeNode()
	node.label = "prim"
	node.primindex = cur.index
	return node

def NoteTree(primlist,cur):
	node = TreeNode()
	node.label = "Note"
	return node

def StemTree(primlist,cur):
	node = TreeNode()
	node.label = "StemHead"
	leftnode = PrimTree(cur)
	for i in cur.edge:
		if i.name=="note":
			rightnode = NoteTree(primlist,i)
	node.left = leftnode
	node.right = rightnode
	return node

def BeamTree(primlist,cur):
	node = TreeNode()
	node.label = "BeamStem"
	for i in cur.edge:
		if i.name=="stem":
			leftnode = StemTree(primlist,i)
	rightnode = PrimTree(cur)
	node.left = leftnode
	node.right = rightnode
	return node

infile = "./measures/01.txt"
primlist = readprimlist(infile)
prim2sym(primlist)
for i in primlist:
	if i.name=="beam":
		print i.index,"#",
		for j in i.edge:
			print j.name,j.index,
		print
#segmentBeamStem()

for i in primlist:
	if i.name=="stem":
		node = StemTree(primlist,i)
		print node

for i in primlist:
	if i.name == "beam":
		node = BeamTree(primlist,i)
		print node
