"""
generate dict for each paper
title1, id1, url1, authors, title2,id2

"""
from collections import Counter
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup

#citation.txt
file1 = open('citation.txt', 'r')
Lines = file1.readlines()

c1 = []
c2 = []
# Strips the newline character
for line in Lines:
	cites = line.split(" ")
	c1.append(cites[0])
	c2.append(cites[2].strip())
df1 = pd.DataFrame({"source":c1,"target":c2})
a = dict(Counter(c1))
b = {k: v for k, v in sorted(a.items(), key=lambda item: item[1],reverse=True)}
df2 = pd.DataFrame({"source":k,"count":v} for (k,v) in b.items())
df1 = pd.merge(df1,df2,on='source')
print(df1.shape,"df1 shape")

c2unique = set(c2)
id_all = []
label_all = []
url_all = []
authors_all = []
year_all = []
target_all = []

for currentpaper in c2unique:
	#print(currentpaper)
	target_current = currentpaper
	jsoncurrent = ""
	with open(f"paper{currentpaper}.html", 'r') as f2:
                Lines2 = f2.readlines()
                tip = 0
                finished = 1
                for line2 in Lines2:
                	if '  "nodes":' in line2:
                		tip = 1
                		#print(line2)
                		continue
                	if tip==1 and '],' in line2:
                		tip = 2
                		#with open(f"json{currentpaper}.txt", 'w+') as f3:
                		#	f2.write(jsoncurrent)
                		break

                	if tip == 1:
                		if '},' in line2:
                			finished = 1
                			#if authors == "":
                			#	continue
                			id_all.append(id_current)
                			label_all.append(label)
                			url_all.append(url_current)
                			authors_all.append(authors)
                			year_all.append(year_current)
                			target_all.append(target_current)
                			continue
                		if '  {' in line2:
                			finished = 0
                			id_current = ""
                			label = ""
                			url_current = ""
                			authors = ""
                			year_current = ""
                			continue
                		if finished == 0:
                			aa=1
                			if '"label"' in line2:
                				line2list = line2.split('"')
                				label = line2list[-2]
                				#print(label)
                				continue
                			if '"id"' in line2:
                				line2list = line2.split('"')
                				id_current = line2list[-2]
                				#print(id_current)
                				continue
                			if '"url"' in line2:
                				line2list = line2.split('"')
                				url_current = line2list[-2]
                				#print(id_current)
                				continue
                			if '"authors"' in line2:
                				line2list = line2.split('"')
                				authors = line2list[-2]
                				#print(id_current)
                				continue
                			if '"year"' in line2:
                				line2list = line2.split('"')
                				year_current = line2list[-2]
                				#print(id_current)
                				continue

                		jsoncurrent += (line2)

#print(c2unique)

df2 = pd.DataFrame({"source":id_all,"title_source":label_all,"yearl_source":year_all,"authors_source":authors_all,"url_source":url_all})
#df2.to_csv("citation_details.csv",index=False)
print(df2.shape,"df2 shape")
source_df2 = df2["source"]
source_df1 = df1["source"]
print(len(list(set(source_df1) & set(source_df2))))
df3 = pd.merge(df1,df2,on='source',how="left")
print(df3.shape,"df3 shape")
#allpapers_summary.txt

file3 = open('allpapers_summary.txt', 'r')
Lines3 = file3.readlines()

c3 = []
c4 = []
# Strips the newline character
for line in Lines3:
	cites = line.split("###")
	c3.append(cites[0])
	c4.append(cites[-1].strip())

df4 = pd.DataFrame({"target":c4,"title_target":c3})
#print(df4)
#print(df3.head(10))
#print(df3.columns)
print(df4.shape,"df4 shape")

df5 = pd.merge(df3,df4,on='target')

df5 = df5.sort_values(by=['count','source'],ascending=False)
print(df5.shape,"df5 shape")

df5 = df5.drop_duplicates(subset=['source', 'target'], keep='first',ignore_index=True)
print(df5.shape,"df5 shape drop")
print(df5[["source","target"]].head(2))
test1 = df5["source"]
print(len(test1),"test1 len")
test2 = list(set(test1))
print(len(test2),"test1 set len")
#test2 = df5["target"][1:2]
#df2.columns = ("source","count")
df5.to_csv("citation_details2.csv",index=False)
#d = {"one": [1.0, 2.0, 3.0, 4.0], "two": [4.0, 3.0, 2.0, 1.0]}

"""
#In [45]: pd.DataFrame(d)
df1 = pd.DataFrame({"source":c1,"target":c2})
a = dict(Counter(c1))
b = {k: v for k, v in sorted(a.items(), key=lambda item: item[1],reverse=True)}
df2 = pd.DataFrame({"source":k,"count":v} for (k,v) in b.items())

df3 = pd.merge(df1,df2,on='source')
df3 = df3.sort_values(by=['count','source'],ascending=False)

#df2.columns = ("source","count")
df3.to_csv("citation_stat.csv",index=False)
#a_dict = collections.OrderedDict(a)

#print(b)
"""
