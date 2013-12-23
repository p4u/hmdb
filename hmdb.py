import imdb
import string
import os
import sys
import re
import time

execfile("hmdb.conf")

def print_help():
	print "hmdb | [Home Media Data Base]"
	print " use: %s <-n|-u|-c|-h>" %(sys.argv[0])
	print "    -n: Create a new database from scratch"
	print "    -u: Update an existing databse with only new files"
	print "    -c: Continue from previous session"
	print "    -h: Print this dirty help"

def gen_re():
	re_dirty = []
	for d in DIRTY:
		re_dirty.append(re.compile(d, re.IGNORECASE))
	return re_dirty

def is_movie(m):
	ms = m.split('.')
	if len(ms) == 0:
		return False
	if ms[len(ms)-1] in EXT:
		return True
	else:
		return False

def check_info(movie):
	try: movie["year"]
	except: movie["year"] = "desconegut"

	try: movie["genres"]
	except: movie["genres"] = "desconegut"

	try: movie["countries"][0]
	except: movie["countries"] = ["desconegut"]

	try: movie["director"][0]
	except: movie["director"] = [{"name":"desconegut"}]

	try: movie["full-size cover url"]
	except: movie["full-size cover url"] = "desconegut"

	try: movie["rating"]
	except: movie["rating"] = 0
	
	try: movie["plot"]
	except: movie["plot"] = [""]


	return movie

def get_cover(movie):
	global GENERIC_COVER
	global BASE_DIR
	global COVERS_DIR
	global GENERIC_COVER_THUMB

	img = COVERS_DIR + '/' + movie.getID() + '.jpg'
	thumb = COVERS_DIR + '/' + "thumb." + movie.getID() + '.jpg'

	if not os.path.exists(img):
		os.system("wget -q \"%s\" -O \"%s\"" %(movie["full-size cover url"],img))
		os.system("convert -thumbnail 150 %s %s" %(img,thumb))
		
	if not os.path.exists(img) or os.path.getsize(img) < 10000:
		print "Cover not found"
		img = GENERIC_COVER
		thumb = GENERIC_COVER_THUMB		
		
	img = img.replace(BASE_DIR,"")
	thumb = thumb.replace(BASE_DIR,"")

	return img,thumb

def set_last(f):
	global LAST_TMP
	last = open(LAST_TMP,'w')
	last.write(f)
	last.close()

def get_last():
	global LAST_TMP
	last = open(LAST_TMP,'r')
	l = last.read()
	last.close()
	return l
	
def clean_index():
	global INDEX_TMP
	html = open(INDEX_TMP,'w')
	html.write("")
	html.close()

def check_duplicate(movie):
	global MOVIES_ID
	offset = 0

	for m in MOVIES_ID:
		if m == movie.getID():
			offset += 1

	MOVIES_ID.append(movie.getID())		
	return offset		

def check_indexed(filename):
	global INDEXED_FILE
		
	index = open(INDEXED_FILE,'r')
	found = False
	for m in index.readlines():
		if m == filename + '\n':
			found = True
			break
	index.close()
	return found

def set_indexed(filename):
	global INDEXED_FILE

	index = open(INDEXED_FILE,'a')
	index.write(filename + '\n')
	index.close()

def clean_indexed():
	global INDEXED_FILE

	index = open(INDEXED_FILE,'w')
	index.write("")
	index.close()
	
def store_index(movie,thumb,offset):
	global OUTPUT_DIR
	global BASE_DIR
	global INDEX
	global INDEX_TMP

	link = OUTPUT_DIR.replace(BASE_DIR,"") + "/" +  movie.getID() + "_" + offset + ".html"
	content="<div id='movie'><img src='%s' height='150px' /><a href='%s'> %s </a></div>\n" %(thumb,link,movie["title"])
	
	index = open(INDEX_TMP,'a')
	index.write(str(int(movie["rating"])) + "|" + content.encode("iso-8859-1") )
	index.close()

def draw_index():
	global TEMPLATE_INDEX
	global INDEX
	global OUTPUT_DIR

	index = open(INDEX_TMP,'r')
	for i in index.readlines():
		n = int(i.split("|")[0])
		c = i.split("|")[1]
		INDEX[n].append(c)
	index.close()

	template = open(TEMPLATE_INDEX,'r').read()	
	for i in range(1,10):
		movies = ""
		for m in INDEX[i]:
			try:
				movies += m.encode("iso-8859-1")
			except:
				print "Unicode problem"

		template = template.replace("MDB_INDEX"+str(i),movies)
	
	html = open(OUTPUT_DIR + "/index.html",'w')
	html.write(template.encode("iso-8859-1"))
	html.close()

def draw_movie(movie,file_url,template,cover,offset):
	global OUTPUT_DIR
	html = open(OUTPUT_DIR + "/" + movie.getID() + "_" + offset + ".html",'w')

	template = template.replace("MDB_TITLE",movie["title"])
	template = template.replace("MDB_RATING",str(movie["rating"]))
	template = template.replace("MDB_COVER",cover)
	template = template.replace("MDB_YEAR",str(movie["year"]))
	template = template.replace("MDB_GENERES",str(movie["genres"]).replace("u\'","").replace("\'",""))
	template = template.replace("MDB_KIND",movie["kind"])
	template = template.replace("MDB_COUNTRY",movie["countries"][0])
	template = template.replace("MDB_DIRECTOR",movie["director"][0]["name"])

	try:
		template = template.replace("MDB_DOWNLOAD",file_url)
	except:
		print "Warning, you have a problem with codification. Please rename the file"
		template = template.replace("MDB_DOWNLOAD","Codificacion_problem_with_filename")

	template = template.replace("MDB_PLOT",movie["plot"][0])

	html.write(template.encode("iso-8859-1"))
	html.close()

###############################
########### Main ##############
###############################
INDEX = [[],[],[],[],[],[],[],[],[],[]]
MOVIES_ID = []
RE_DIRTY = gen_re()
mdb = imdb.IMDb()
mtemplate = open(TEMPLATE_MOVIE,'r').read()
new = False
cont = False

if len(sys.argv) > 1 and sys.argv[1] == "-c": 
	print "[Continuing from previous season...]"
	cont = True
	last = get_last()

if len(sys.argv) > 1 and sys.argv[1] == "-n":
	print "[Regenerating new index...]"
	clean_index()
	clean_indexed()
	new = True

if len(sys.argv) > 1 and sys.argv[1] == "-u":
	print "[Updating the home media data base...]"

if len(sys.argv) == 1 or sys.argv[1] == "-h":
	print_help()
	sys.exit(0)

follow = False

for movie_dir in MOVIES_DIR:
	print "Scanning dir: " + movie_dir

	for r,d,f in os.walk(movie_dir):
		for file in f:
			if not(cont and file != last):
				follow = True
			if is_movie(file) and follow:
				set_last(file)
				print "Original: " + file
				file_url = r.replace(BASE_DIR,"") + "/" + file
				
				indexed = check_indexed(file_url)

				if not new and indexed: 
					print "This movie is yet indexed"

					print "------------------------------------------------------"
					continue
				
				for d in RE_DIRTY:
				 	file = re.sub(d,"",file)
				file = re.sub("\."," ",file)	
				file = re.sub("_"," ",file)
				file = re.sub("-"," ",file)
				file = file.strip()
				file = unicode(file,'iso-8859-1')
				#print "Clean: " + file
				
				results = mdb.search_movie(file)
	
				if len(results) == 0: 
					try:
						print "NOT FOUND: " + file
		
					except:
						print "NOT FOUND, and there is a problem with codification. Please rename file"
					print "------------------------------------------------------"
					continue
							
				movie = results[0]
				mdb.update(movie)
				movie = check_info(movie)
				offset = check_duplicate(movie)
				if not indexed: set_indexed(file_url)
				print "imdb ==> " + results[0]["title"].encode("iso-8859-1")
				cover,thumb = get_cover(movie)
				draw_movie(movie,file_url,mtemplate,cover,str(offset))
				store_index(movie,thumb,str(offset))
				print "------------------------------------------------------"
draw_index()
