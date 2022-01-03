'''
Merge authors from pubmed search
'''
from pymed import PubMed
import pandas as pd
from difflib import SequenceMatcher
import json
import os


allcitations = pd.read_csv("allcitation_merge.csv", header=0)  # ,nrows=2
print(allcitations.shape)
tmp1 = allcitations.id_source
tmp1_set = set(tmp1)
print(len(tmp1_set))
# 803, although we have 990 total citations,
# only corresponding to 803 unique papers
# Some papers cites more than one of my publications


ausPubmed = pd.read_json('pub_files.txt', orient='records', lines=True)
ausPubmed.to_csv("pub_files.csv", index=False)
ausPubmed2 = ausPubmed.drop_duplicates(
    subset=ausPubmed.columns.difference(['index_source']))
print(ausPubmed.shape)
tmp1 = ausPubmed.clusterid_google
tmp1_set = set(tmp1)
print(len(tmp1_set))  # 803

print(ausPubmed2.shape)
tmp1 = ausPubmed2.clusterid_google
tmp1_set = set(tmp1)
print(len(tmp1_set))  # 803


df_all = allcitations.merge(ausPubmed2, how="left",
                            left_on="id_source", right_on="clusterid_google")

print(df_all.shape)
df_all.to_csv("allcitation_pubMerge.csv", index=False)
