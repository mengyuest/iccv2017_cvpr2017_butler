#!/usr/bin/env python  
# -*- coding: utf-8 -*-  

from bs4 import BeautifulSoup
import csv

fi = open("retrieves/table_file0.schedule.html")
fo = open("retrieves/stat.csv",'w')

html_str = fi.read().replace("\n","")

soup = BeautifulSoup(html_str, 'html.parser')

cw = csv.writer(fo, delimiter = '\t', quotechar = '|', quoting = csv.QUOTE_MINIMAL)

last_topic = "NULL"
last_session = "NULL"

cw.writerow(['TOPIC','SESSION','ID','PAPER','AUTHOR'])

for row in soup.tbody.contents[3::2]:

   if len(row.contents[11].contents) > 0:

      if len(row.contents[11].contents[0]) > 1:
         last_topic = row.contents[11].contents[0].encode('utf8')

      elif len(row.contents[11].contents[0]) > 0 and len(row.contents[11].contents[0].contents[0]) > 1:
         last_topic = row.contents[11].contents[0].contents[0].encode('utf8')
      
      last_topic = last_topic.replace("“", "\"")
      last_topic = last_topic.replace("”", "\"")

   if len(row.contents[9].contents) > 0:

      if len(row.contents[9].contents[0]) > 1:
         last_session = row.contents[9].contents[0].encode('utf8')

      elif len(row.contents[9].contents[0]) > 0 and  len(row.contents[9].contents[0].contents[0]) > 1:
         last_session = row.contents[9].contents[0].contents[0].encode('utf8')

      last_session = last_session.replace("“", "\"")
      last_session = last_session.replace("”", "\"")

   if len(row.contents[15].contents[0].contents[0]) > 1:
      paper = row.contents[15].contents[0].contents[0].encode('utf8')
   elif len(row.contents[15].contents[0].contents[0].contents[0]) > 1:
      paper = row.contents[15].contents[0].contents[0].contents[0].encode('utf8')
   
   paper = paper.replace("“", "\"")
   paper = paper.replace("”", "\"")
   paper = paper.replace("—", "-")
   paper = paper.replace("°", "deg")
   paper = paper.replace("é", "e")
   paper = paper.replace("&", "and")

   author = row.contents[17].contents[0].contents[0].encode('utf8')
   paperid = row.contents[13].contents[0].contents[0].encode('utf8')

   cw.writerow([last_topic, last_session, paperid, paper, author]) 

