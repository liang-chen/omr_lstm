from bs4 import BeautifulSoup
import cairosvg

class primitive(object):
	def __init__(self,name,locbegin,locend,index):
		self.name = name
		self.locbegin = locbegin#a tuple
		self.locend = locend
		self.index = index
		self.width = 0
		self.height = 0
		self.refloc = [0,0]

def svg2primlist(svg_file):
	soup = BeautifulSoup(open(svg_file),'xml')
	primlist = []
	findnotes(soup,primlist)
	findstems(soup,primlist)
	findbeams(soup,primlist)
	for i in primlist:
		print i.index,i.name,i.locbegin,i.locend
	return primlist

def findstems(soup,primlist):
	stems = soup.find_all("polyline",{"class":"Stem"})
	for i in stems:
		locs = i["points"].split()
		begin = locs[0].split(",")
		locbegin = (float(begin[0]),float(begin[1]))
		end = locs[1].split(",")
		locend = (float(end[0]),float(end[1]))
		primlist.append(primitive("stem",locbegin,locend,len(primlist)))

def findstaves(soup):
	stafflines = soup.find_all("polyline",{"class":"StaffLines"})
	for i in stafflines:
		locs = i["points"].split()
		begin = locs[0].split(",")
		locbegin = (float(begin[0]),float(begin[1]))
		end = locs[1].split(",")
		locend = (float(end[0]),float(end[1]))
		print locbegin,locend

def findnotes(soup,primlist):
	notes = soup.find_all("path",{"class":"Note"})
	for i in notes:
		locs = i["d"].split()[0][1:]
		begin = locs.split(",")
		locbegin = (float(begin[0]),float(begin[1]))
		primlist.append(primitive("note",locbegin,locbegin,len(primlist)))

def findbeams(soup,primlist):
	beams = soup.find_all("path",{"class":"Beam"})
	for i in beams:
		locs = i["d"].split()
		begin = locs[1][1:].split(",")
		locbegin = (float(begin[0]),float(begin[1]))
		end = locs[3][1:].split(",")
		locend = (float(end[0]),float(end[1]))
		primlist.append(primitive("beam",locbegin,locend,len(primlist)))

def write2file(outfile,primlist):
	f = open(outfile,"w")
	for i in primlist:
		mystr = i.name+" "+str(i.locbegin[0])+" "+str(i.locbegin[1])+" "+\
				str(i.locend[0])+" "+str(i.locend[1])+"\n"
		f.write(mystr)
	f.close()

svg_file = "./measures/01.svg"
png_file = "./measures/01.png"
primlist = svg2primlist(svg_file)
cairosvg.svg2png(url=svg_file,write_to=png_file)
write2file("./measures/01.txt",primlist)


