"""
Find the citation that citate more than one times
"""
from collections import Counter
import pandas as pd
import numpy as np
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

#d = {"one": [1.0, 2.0, 3.0, 4.0], "two": [4.0, 3.0, 2.0, 1.0]}

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
