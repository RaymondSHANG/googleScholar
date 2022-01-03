'''
This program is to re-analyze the self-citations,after all those works done by pubmed websearch and mannual corrections
For each paper id, we hava a dict with clusterid:authors
we also have the citations for each paper.
The output will be a dataframe:
paperid papertitle totalCitation selfcitation
'''

from collections import Counter
import pandas as pd
import numpy as np


#url_all = pubs.loc[:,'url']
#url_all = url_all.tolist()

#url_all = pubs.loc[:,'url']
#url_all = url_all.tolist()
allcitations = pd.read_csv(
    "allcitation_final_modify.csv", header=0)  # ,nrows=2
print(allcitations.shape)
# print(allcitations.columns)
# ['id_source', 'title_source', 'authors_source', 'url_source',
#       'cited_by_source', 'id_target', 'title', 'totalCitations', 'url',
#       'clusterid', 'authors']
# allcitation_merge.csv


def formatAuthors(authors):
    '''
    authors:'SF Banani, HO Lee, AA Hyman…' or 'RAW Frank, SGN Grant'
    return a list containing all authors with "A Surname" format
    '''
    authorlist = authors.split(",")
    authorlist = [s.strip() for s in authorlist]
    notcomplete = False

    for i in range(len(authorlist)):
        currentauthor = authorlist[i].strip().split(" ")
        # print(currentauthor)
        currentlen = len(currentauthor)
        lastname = currentauthor[currentlen-1]
        lastname = lastname.strip()
        lastname = lastname.upper()
        if lastname.find("…") > 0:
            notcomplete = True
            lastname = lastname[0:(len(lastname)-1)]
        firstname = ""
        if currentlen == 1:
            continue
        elif currentlen == 2:
            if currentauthor[0].strip().isupper():
                firstname = currentauthor[0].strip()
            else:
                firstname = currentauthor[0].strip()
                firstname = firstname.upper()
        else:
            for j in range(currentlen - 1):
                tmp = currentauthor[j]
                tmp = tmp.strip()
                firstname = firstname + tmp[0].upper()
        authorlist[i] = firstname + " " + lastname
        #print("Newname:\t" + authorlist[i])
    if notcomplete:
        authorlist.append("…")
    # print("\n\n")
    # print(authorlist)
    return authorlist


def checkOverlap(aulist1, aulist2):
    '''
    receive to list, check if there is any element overlaps
    '''
    overlaps = 0
    for au1 in aulist1:
        for au2 in aulist2:
            if au1 == au2:
                overlaps = overlaps + 1
    return overlaps


# id_source,title_source_x,authors_source,url_source,cited_by_source,id_target,title,totalCitations,url,clusterid,authors,index_source,pubmed_id,title_pub,title_source_y,authors_pub,clusterid_google,titleMatch,authoerOverlaps,selfcitations
pre_target = ""
i = 407
currentcount = allcitations.loc[i, 'totalCitations']

current_au_source = str(allcitations.loc[i, 'authors_source'])
current_au_source = formatAuthors(current_au_source)
current_au_sourcePubmed = str(allcitations.loc[i, 'authors_pub'])
current_au_sourcePubmed = formatAuthors(current_au_sourcePubmed)
print(current_au_source)
current_au_sourceNew = current_au_source
if str(allcitations.loc[i, "titleMatch"]) == "High":
    current_au_sourceNew = current_au_sourcePubmed

current_target = allcitations.loc[i, 'clusterid']
if current_target != pre_target:
    current_au_target = allcitations.loc[i, 'authors']
    current_au_target = formatAuthors(current_au_target)
    pre_target = current_target

currentoverlaps = checkOverlap(current_au_sourceNew, current_au_target)
print('source:')
print(current_au_sourceNew)
print('target:')
print(current_au_target)
print('overlap:')
print(currentoverlaps)

'''
allcitations['authoerOverlaps'] = citationmarker1
allcitations['selfcitations'] = citationmarker2
allcitations.to_csv("allcitation_final2.csv", index=False)
'''
