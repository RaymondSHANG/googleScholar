'''
This program further searches author names for 
the source papers using query results from pubmed database
'''
from pymed import PubMed
import pandas as pd
from difflib import SequenceMatcher
import json
import os

pubmed = PubMed(tool="PubMedSearcher", email="yshang@email.arizona.edu")
my_api_key = '5f2915a6f64423e63e34e3002b25f4f9bf08'
pubmed.parameters.update({'api_key': my_api_key})
pubmed._rateLimit = 10


def append_record(record):
    with open('pub_files.txt', 'a') as f:
        json.dump(record, f)
        f.write(os.linesep)


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
    "allcitation_merge.csv", header=0)  # ,nrows=2
## PUT YOUR SEARCH TERM HERE ##
# id_source,title_source,authors_source,url_source,cited_by_source,id_target,title,totalCitations,url,clusterid,authors

search_terms = allcitations['title_source'].values.tolist()
# allcitations.loc[:,'authors_source']
aus_terms = allcitations['authors_source'].values.tolist()
title_terms = allcitations['title_source'].values.tolist()
id_terms = allcitations['id_source'].values.tolist()
tip = 0
articleInfo = []
for i in range(len(search_terms)):
    search_term = search_terms[i]
    authors_source = str(aus_terms[i])
    authors_source = authors_source.split(",")
    authors_source_last = authors_source[0]
    authors_source_last = authors_source_last.split(" ")
    authors_source_last = authors_source_last[-1].strip()
    authors_source_last = authors_source_last.upper()
    title_source = title_terms[i]
    title_source = title_source.strip().upper()
    if i <= 990:
        # Set a number here, you may need to run this program multiple times
        continue

    #search_term = "Reconstituted postsynaptic density as a molecular platform for understanding synapse formation and plasticity"
    print(f"Pubmed search for {i}th article:\n#######################")
    print(search_term)
    print("#######################")
    results = pubmed.query(search_term, max_results=20)
    articleList = []
    #

    for article in results:
        # Print the type of object we've found (can be either PubMedBookArticle or PubMedArticle).
        # We need to convert it to dictionary with available function
        articleDict = article.toDict()
        articleList.append(articleDict)

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
            print("Find match for:")
            print(title_pubmed)
            # append df infomation
            au_pub = getpubaus(article['authors'])
            print(au_pub)
            print("-----------------------\n")
            my_dict = {u'index_source': i,
                       u'pubmed_id': pubmedId,
                       u'title_pub': article['title'],
                       u'title_source': title_terms[i],
                       u'authors_pub': au_pub,
                       u'clusterid_google': id_terms[i],
                       u'titleMatch': 'High'
                       }
            articleInfo.append(my_dict)
            append_record(my_dict)

            break
        if lastau_pubmed is not None and lastau_pubmed == authors_source_last:
            found = True
            print(f"Find potential match for:{title_source}")
            print(title_pubmed)
            # append
            au_pub = getpubaus(article['authors'])
            print(au_pub)
            print("-----------------------\n")
            my_dict = {u'index_source': i,
                       u'pubmed_id': pubmedId,
                       u'title_pub': article['title'],
                       u'title_source': title_terms[i],
                       u'authors_pub': au_pub,
                       u'clusterid_google': id_terms[i],
                       u'titleMatch': 'Low'
                       }
            articleInfo.append(my_dict)
            append_record(my_dict)
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
        my_dict = {u'index_source': i,
                   u'pubmed_id': "",
                   u'title_pub': "",
                   u'title_source': title_terms[i],
                   u'authors_pub': "",
                   u'clusterid_google': id_terms[i],
                   u'titleMatch': 'None'
                   }
        articleInfo.append(my_dict)
        append_record(my_dict)
    # Generate Pandas DataFrame from list of dictionaries
    #articlesPD = pd.DataFrame.from_dict(articleInfo)
    #export_csv = articlesPD.to_csv (r'pubtest.csv', index = None, header=True)
