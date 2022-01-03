from collections import Counter
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from pymed import PubMed
from difflib import SequenceMatcher
import json
import os
import requests
import re
pubmed = PubMed(tool="PubMedSearcher", email="yshang@email.arizona.edu")
my_api_key = '5f2915a6f64423e63e34e3002b25f4f9bf08'
pubmed.parameters.update({'api_key': my_api_key})
pubmed._rateLimit = 10

search_term = "Functional interplay between protein domains in a supramodular structure involving the postsynaptic density protein PSD-95"
#results = pubmed.query(search_term, max_results=20)
# print(results)
# print(len(list(results)))

#results2 = pubmed._getArticleIds(query=search_term, max_results=10)
# print(results2)
# print(len(list(results2)))
#pubmed.parameters["db"] = "pmc"
#results3 = pubmed._getArticleIds(query=search_term, max_results=10)
# if len(list(results3)) > 0:
#    pubmed.parameters["db"] = "pubmed"
#    results4 = pubmed._getArticles(article_ids=results3)
#    for result in results4:
#        tmp = result.toDict()
#        print(tmp['title'])  # title_pubmed = article['title']

# for result in results3:
#    print(result)
# print(len(list(results3)))

BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
# https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi
# esearch.fcgi?db=pubmed&term=asthma
# /entrez/eutils/esearch.fcgi
# esearch.fcgi?db=pubmed&term=asthma

response = requests.get(f"{BASE_URL}?db=pubmed&term={search_term}")
# print(response.text)

search_term2 = "Protein Phase Separation: A New Phase in Cell Biology"
# response1 = requests.get(
#    f"https://pubmed.ncbi.nlm.nih.gov/?format=abstract&term={search_term}")
# response2 = requests.get(
#    f"https://pubmed.ncbi.nlm.nih.gov/?format=pmid&term={search_term2}")

search_term3 = "The protein complex crystallography beamline (BL19U1) at the Shanghai Synchrotron Radiation Facility"
response3 = requests.get(
    f"https://pubmed.ncbi.nlm.nih.gov/?format=pmid&term={search_term2}")
# print(response2.text)

# <title>Not found - PubMed</title>

# with open('pubmed_results3.txt', 'w') as f:
#    f.write(response3.text)
# <meta name="citation_pmid" content="31831623">
soup = BeautifulSoup(response3.text, "html.parser")
aa = soup.find_all('pre')
print(aa)
if aa != []:

    cc = aa[0].contents[0]
    print("AA")
    print(cc)
    bb = cc.splitlines()
    for line in bb:
        line = line.strip()
        if line == "":
            continue
        print(line)


#PMID- 29602697
#OWN - NLM
# TI  - Protein Phase Separation: A New Phase in Cell Biology.
# AU  - Boeynaems S

# class="single-result-redirect-message"
# <div class="multiple-results-actions "
#PMID: 31831623
# soup.find(class_="abstract").find("h1").text

results3 = []
for article in results3:
    # Print the type of object we've found (can be either PubMedBookArticle or PubMedArticle).
    # We need to convert it to dictionary with available function
    print(article)
