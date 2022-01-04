'''
input1: pubmed email and api_key
input2:data/allcitation_selfcitations.csv
output:data/allcitation_final.csv
output2(mannual inspection):data/allcitation_final_modify.csv

I found the results from eutilies pubmed is different from pubmed web search.
This program re-queries the results from getitations_4.py. 
For those low/none matched results, re-query from pubmed websearch.
After this round of running, you need to manual inspect all your results, mainly for those "none" and "low" titleMatch results
Making any corrections if nessesary.
'''
from collections import Counter
import pandas as pd
import numpy as np
from pymed import PubMed
from difflib import SequenceMatcher
import json
import os
import requests
import re
from bs4 import BeautifulSoup

parameters_user = pd.read_json(
    'data/parameters.txt', orient='records', lines=True)
pubemail = str(parameters_user.loc[0, 'pubemail']).strip()
my_api_key = str(parameters_user.loc[0, 'api_key']).strip()

pubmed = PubMed(tool="PubMedSearcher", email=pubemail)
pubmed.parameters.update({'api_key': my_api_key})
pubmed._rateLimit = 10


def getpubaus(authos_pub):
    '''
    get lastname and initials from pubmed author dicts
    '''
    aus = list()
    for oneau in authos_pub:
        onename = oneau['initials']
        if onename is None:
            onename = oneau['lastname']
        else:
            onename = oneau['initials']
            if onename is None:
                continue
            else:
                onename = oneau['initials'] + " " + oneau['lastname'].upper()
            # oneau['initials']+" "+
        if onename is None:
            # print(authos_pub)
            continue
        aus.append(onename)
    return ",".join(aus)


allcitations = pd.read_csv(
    "data/allcitation_selfcitations.csv", header=0)  # ,nrows=2
print(allcitations.shape)
print(allcitations.columns)
'''
['id_source', 'title_source_x', 'authors_source', 'url_source',
       'cited_by_source', 'id_target', 'title', 'totalCitations', 'url',
       'clusterid', 'authors', 'index_source', 'pubmed_id', 'title_pub',
       'title_source_y', 'authors_pub', 'clusterid_google', 'titleMatch',
       'authoerOverlaps', 'selfcitations']
'''

#titleMatch == "None"

for i in range(allcitations.shape[0]):
    if allcitations.loc[i, 'titleMatch'] == "None":
        print(f"##    {i}    ##\n",
              allcitations.loc[i, 'title_source_x'])

        search_term = allcitations.loc[i, 'title_source_x']
        authors_source = str(allcitations.loc[i, 'authors_source'])
        authors_source = authors_source.split(",")
        authors_source_last = authors_source[0]
        authors_source_last = authors_source_last.split(" ")
        authors_source_last = authors_source_last[-1].strip()
        authors_source_last = authors_source_last.upper()
        title_source = search_term
        title_source = title_source.strip().upper()
        if i <= 990:
            # Set a number here, you may need to run this program multiple times
            # continue
            pass

        #search_term = "Reconstituted postsynaptic density as a molecular platform for understanding synapse formation and plasticity"
        # print(f"Pubmed search for {i}th article:\n#######################")
        # print(search_term)
        # print("#######################")
        # First try pubmed websearch:
        # class="single-result-redirect-message"
        articleList = []

        response2 = requests.get(
            f"https://pubmed.ncbi.nlm.nih.gov/?format=abstract&term={search_term}")
        if re.search('<span class="single-result-redirect-message">', response2.text, re.MULTILINE):
            pubid_search = re.search(
                '<meta name="citation_pmid" content="(.*)">', response2.text)
            pubid = pubid_search.groups()[0]
            # print(pubid)
            results = pubmed._getArticles(article_ids=pubid)
            for article in results:
                articleList.append(article.toDict())

        else:
            response1 = requests.get(
                f"https://pubmed.ncbi.nlm.nih.gov/?format=pmid&term={search_term}")
            soup = BeautifulSoup(response1.text, "html.parser")
            aa = soup.find_all('pre')
            if aa == []:
                continue
            pubid = aa[0].contents[0]
            results = pubmed._getArticles(article_ids=pubid)
            for article in results:
                articleList.append(article.toDict())
        # Generate list of dict records which will hold all article details that could be fetch from PUBMED API
        found = False
        for article in articleList:
            # Sometimes article['pubmed_id'] contains list separated with comma - take first pubmedId in that list - thats article pubmedId
            # {'lastname': 'Emperador-Melero', 'firstname':
            # {'lastname': 'Tse', 'firstname': 'Wai-Pui', '...
            # 'lastname': 'Oliva', 'firstname': 'Rosario', 'initials': 'R',
            authors_pubmed = article['authors']
            if len(authors_pubmed) == 0:
                continue
            # print(authors_pubmed)
            # print(authors_pubmed[0]['lastname'])
            lastau_pubmed = authors_pubmed[0]['lastname']
            if lastau_pubmed is None:
                lastau_pubmed = ""
            lastau_pubmed = lastau_pubmed.upper()
            #initau_pubmed = authors_pubmed[0]['initials']
            # if initau_pubmed is None:
            #    initau_pubmed = " "
            #initau_pubmed = initau_pubmed.strip()
            title_pubmed = article['title']
            pubmedId = article['pubmed_id'].partition('\n')[0]
            #print("Current search result:")
            # print(title_pubmed)
            # print("authors")
            au_pub = getpubaus(article['authors'])
            # print(au_pub)
            # print("---------------------")
            if SequenceMatcher(None, title_pubmed.upper(), title_source).ratio() > 0.8:
                found = True
                print("*****Find match for:*****")
                print(title_pubmed)
                # append df infomation
                au_pub = getpubaus(article['authors'])
                print(au_pub)
                print("-----------------------\n")
                #'pubmed_id', 'title_pub',
                #'title_source_y', 'authors_pub', 'clusterid_google', 'titleMatch',
                #'authoerOverlaps', 'selfcitations'

                allcitations.loc[i, 'pubmed_id'] = pubmedId
                allcitations.loc[i, 'title_pub'] = article['title']
                allcitations.loc[i, 'title_source_y'] = search_term.strip()
                allcitations.loc[i, 'authors_pub'] = au_pub
                allcitations.loc[i, 'titleMatch'] = 'High'
                break
            if lastau_pubmed is not None and lastau_pubmed == authors_source_last:
                found = True
                print(f"###Find potential match for:{title_source}")
                print(title_pubmed)
                # append
                au_pub = getpubaus(article['authors'])
                print(au_pub)
                print("-----------------------\n")
                allcitations.loc[i, 'pubmed_id'] = pubmedId
                allcitations.loc[i, 'title_pub'] = article['title']
                allcitations.loc[i, 'title_source_y'] = search_term.strip()
                allcitations.loc[i, 'authors_pub'] = au_pub
                allcitations.loc[i, 'titleMatch'] = 'Low'
                break
            '''
            pubmedId = article['pubmed_id'].partition('\n')[0]
            # Append article info to dictionary 
            articleInfo.append({u'pubmed_id':pubmedId,
                            u'title':article['title'],
                            u'keywords':article['keywords'],
                            u'journal':article['journal'],
                            u'abstract':article['abstract'],
                            u'conclusions':article['conclusions'],
                            u'methods':article['methods'],
                            u'results': article['results'],
                            u'copyrights':article['copyrights'],
                            u'doi':article['doi'],
                            u'publication_date':article['publication_date'], 
                            u'authors':article['authors']})
            '''
        if found == False:
            # appendNone
            # print(len(id_terms))
            allcitations.loc[i, 'pubmed_id'] = ""
            allcitations.loc[i, 'title_pub'] = ""
            allcitations.loc[i, 'title_source_y'] = search_term.strip()
            allcitations.loc[i, 'authors_pub'] = ""
            allcitations.loc[i, 'titleMatch'] = 'None'

allcitations.to_csv("data/allcitation_final.csv", index=False)
