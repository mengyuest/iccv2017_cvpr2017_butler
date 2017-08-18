import csv
import os
import shutil
import errno

src_dir = "retrieves/papers/"
root_dir = "cvpr_lib@local/"
etc_dir = "Zi Other Files/"

f1 = open("retrieves/stat.csv",'r')
f2 = open("retrieves/3-cvpr2017-papers.csv",'r')
f3 = open("retrieves/cvpr2017.csv",'wb')

doc = f2.read()
doc = doc.replace("\,", "$")
doc = doc.replace("," , "\t")
doc = doc.replace("$" , ",")
doc = doc.replace("\\\"", "\"")
doc = doc.replace("--", "-")
doc = doc.replace("&", "and")

f3.write(doc)

f2.close()
f3.close()

f3 = open("retrieves/cvpr2017.csv",'r')

catalog = csv.reader(f1, delimiter='\t', quotechar="|")
mapping = csv.reader(f3, delimiter='\t', quotechar='|')

if not os.path.exists(root_dir):
	try:
		os.makedirs(root_dir)
	except OSError as exception:
		if exception.errno != errno.EEXIST:
			raise

count = 0
matched_count = 0
for row in enumerate(catalog):
	if count == 0:
		count = 1
		continue
	topic_name = row[1][0]
	topic_dir = root_dir + topic_name + "/"
	if not os.path.exists(topic_dir):
		try:
			os.makedirs(topic_dir)
		except OSError as exception:
			if exception.errno != errno.EEXIST:
				raise

	session_name = row[1][1]
	session_dir = topic_dir + session_name + "/"
	if not os.path.exists(session_dir):
		try:
			os.makedirs(session_dir)
		except OSError as exception:
			if exception.errno != errno.EEXIST:
				raise

	paper_name = row[1][3].strip()
	
	f3.seek(0)

	no_matched = True

	for sec_row in enumerate(mapping):
		if(sec_row[1][0][0] == paper_name[0] and sec_row[1][0][1] == paper_name[1]):
			if sec_row[1][0].strip()==paper_name:
				no_matched = False
				matched_count = matched_count+1
				paper_path = sec_row[1][2].split("/")[2]
				shutil.move(src_dir + paper_path, session_dir + paper_path)
				break

f1.close()
f3.close()

shutil.move(src_dir.split("/")[0], root_dir + etc_dir)

print
print("Successfuly received " + str(matched_count) + " papers from CVPR2017")





