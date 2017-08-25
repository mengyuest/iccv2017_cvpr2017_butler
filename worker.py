#!/usr/bin/env python  
# -*- coding: utf-8 -*-  

import csv
import os
import shutil
import errno
from multiprocessing import Process, Pool, Value, Manager
from datetime import datetime
import urllib2

def download(todoitem):
	paper_dir = todoitem[0]
	session_dir = todoitem[1]
	paper_path = todoitem[2]
	dtype = todoitem[3]
	if dtype == "paper":

		os.system("mwget -d \""+paper_dir+"\" -n " + str(connect_num.value) + \
			" -t 90 http://openaccess.thecvf.com/content_cvpr_2017/papers/"+paper_path)
	if dtype == "appendix":

		os.system("mwget -d \""+paper_dir+"\" -n " + str(connect_num.value) + \
			" -t 90 http://openaccess.thecvf.com/content_cvpr_2017/supplemental/"+paper_path)

	shutil.move(paper_dir+paper_path, session_dir+paper_path)

	file_size.value = file_size.value+os.path.getsize(session_dir+paper_path)
	file_downloaded.value = file_downloaded.value + 1
	os.system("echo \"\\033[1;32m[GET] " + paper_path + "\\033[0m \"")
	os.system("echo \"\\033[1;32m[NOW] " + str(file_downloaded.value) + \
		"/" + str(file_todo.value) + " files downloaded" + \
		"\\033[0m \"")


def standarize_html(doc):
	doc = doc.replace("“", "\"")
	doc = doc.replace("”", "\"")
	doc = doc.replace("—", "-")
	doc = doc.replace("°", "deg")
	doc = doc.replace("é", "e")
	doc = doc.replace("&", "and")
	return doc

def standarize_csv(doc):

	doc = doc.replace("\,", "$")
	doc = doc.replace("," , "\t")
	doc = doc.replace("$" , ",")
	doc = doc.replace("\\\"", "\"")
	doc = doc.replace("--", "-")
	doc = doc.replace("&", "and")
	return doc

if __name__ == "__main__":

	dt_start = datetime.now()

	server = Manager()
	process_num = 50
	connect_num = server.Value('i', 4)

	file_size = server.Value('d', 0)

	file_sum = server.Value('i', 0)
	file_saved = server.Value('i',0)
	file_downloaded = server.Value('i', 0) 
	file_todo = server.Value('i', 0)

	root_path = "cvpr_lib@local/" #server.Value(c_char_p, "cvpr_lib@local/")
	src_path = root_path+"Zi Other Files/" #server.Value(c_char_p, root_path+"Zi Other Files/")
	paper_dir = root_path+"papers/" #server.Value(c_char_p, root_path+"papers/")

	if not os.path.exists(root_path):
		try:
			os.makedirs(root_path)
		except OSError as exception:
			if exception.errno != errno.EEXIST:
				raise

	if not os.path.exists(src_path):
		try:
			os.makedirs(src_path)
		except OSError as exception:
			if exception.errno != errno.EEXIST:
				raise

	os.system("mwget -d \""+src_path+"\" -n 4 "  + \
			"-t 90 http://openaccess.thecvf.com/content_cvpr_2017/3-cvpr2017-papers.csv")

	print("Downloading schedule csv files ...")
	stat_csv = urllib2.urlopen('http://cvpr2017.thecvf.com/program/main_conference')
	w1 = open(src_path + "origin_stat.html", 'wb') 
	w1.write(stat_csv.read())
	w1.close()

	w1 = open(src_path + "origin_stat.html", 'r') 
	w2 = open(src_path + "stat.csv", 'wb')

	pencil = csv.writer(w2, delimiter = '\t', quotechar = '|', quoting = csv.QUOTE_MINIMAL)
	pencil.writerow(['TOPIC',	'SESSION',	'ID',	'PAPER',	'AUTHOR'])

	csv_content =   ['NULL','NULL','NULL','NULL','NULL','NULL','NULL','NULL','NULL']

	lines = w1.readlines()

	col_id=0
	start_trim = False

	for line in lines:
		if start_trim == True:
			if  "</table>" in line:
				break
			else:	
				if "</tr" in line and csv_content[5] != "NULL":
					col_id = 0
					pencil.writerow([csv_content[5],csv_content[4],csv_content[6],csv_content[7],csv_content[8]])

				elif "<td " in line:
					#print("@@  "+line)
					strs = line.strip().split('>')
					for item in strs:
						#print("\""+item+"\"")
						item = item.strip()
						if item != "" and item[0] != '<':
							csv_content[col_id] = standarize_html(item.strip().split('<')[0].strip())
							break
					#print("id="+str(col_id))
					col_id = col_id + 1

		elif "\"program_schedule\"" in line:
			start_trim = True

		else:
			continue

	w2.close()
	w1.close()

	f1 = open(src_path + "stat.csv",'r')
	f2 = open(src_path + "3-cvpr2017-papers.csv",'r')
	f3 = open(src_path + "cvpr2017.csv",'wb')

	doc = f2.read()
	doc = standarize_csv(doc)

	f3.write(doc)

	f2.close()
	f3.close()

	f3 = open(src_path + "cvpr2017.csv",'r')

	catalog = csv.reader(f1, delimiter='\t', quotechar="|")
	mapping = csv.reader(f3, delimiter='\t', quotechar='|')

	if not os.path.exists(paper_dir):
		try:
			os.makedirs(paper_dir)
		except OSError as exception:
			if exception.errno != errno.EEXIST:
				raise

	todolist=[]

	count = 0
	matched_count = 0
	for row in enumerate(catalog):
		if count == 0:
			count = 1
			continue
		topic_name = row[1][0]
		topic_dir = paper_dir + topic_name + "/"
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
					
					if(sec_row[1][3]!="None"):
						appendix_path = sec_row[1][3].split("/")[2]
						matched_count = matched_count+1
					else:
						appendix_path = "None"
					isPaperFound = False
					isAppendixFound = False
					for root, dirs, files in os.walk(session_dir):
						if paper_path in files:
							isPaperFound = True
							os.system("echo \"\\033[1;32m[FOUND] paper: " + paper_path + "\\033[0m \"")
							break
						if appendix_path in files:
							isAppendixFound = True
							os.system("echo \"\\033[1;32m[FOUND] appendix: " + appendix_path + "\\033[0m \"")
							break

					if isPaperFound != True:
						dtype = "paper"
						todolist.append([paper_dir, session_dir, paper_path, dtype])

					if appendix_path != "None" and isAppendixFound != True:
						dtype = "appendix"
						todolist.append([paper_dir, session_dir, appendix_path, dtype])
					
					break

	f1.close()
	f3.close()

	file_sum.value = matched_count
	file_todo.value = len(todolist)
	pool = Pool(process_num)
	pool.map(download, todolist)

	print
	os.system("echo \"\\033[1;32mSuccessfuly received " + str(file_sum.value) +\
	 " files from CVPR2017, " + "\\033[0m \"")
	os.system("echo \"\\033[1;32mwith "+str(file_downloaded.value)+" files downloaded and " +\
	 str(file_sum.value-file_downloaded.value) + " files that already had"+ "\\033[0m \"")

	dt_end=datetime.now()
	time_interval = (dt_end - dt_start).seconds
	download_speed = file_size.value/1024/time_interval
	os.system("echo \"\\033[1;32mElapse time: "+(str)(time_interval)+"s"+ "\\033[0m \"")
	os.system("echo \"\\033[1;32mDownload speeds: "+ (str)(download_speed) +"KB/s"+ "\\033[0m \"")
	