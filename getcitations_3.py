'''
input1: data/allPapers_citationNumbers.csv
input2:data/allcitationNumbers.csv
output:data/allcitation_merge.csv
This program merges the matching source-target with target information
the source-target matching is : allcitationNumbers.csv
the target info is: allPapers_citationNumbers.csv
'''
import pandas as pd


pubs = pd.read_csv('data/allPapers_citationNumbers.csv', header=0, nrows=23)
print(pubs.columns)
# print(pubs['url'])
df = pd.read_csv("data/allcitationNumbers.csv", header=0)
print(df.columns)
df_all = df.merge(pubs, how="left", left_on="id_target", right_on="clusterid")
df_all.to_csv("data/allcitation_merge.csv", index=False)
