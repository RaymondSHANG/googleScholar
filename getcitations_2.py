'''
input:data/allPapers_citationNumbers.csv
output1:data/allcitations.txt
output2:data/allcitationNumbers.csv
This program reads a set of goolge scholar papers(clusterid, url, etc)
goes to the url, extract all one to one citation records based on clusterid
The information of papers that cited your publications were also extracted, including citation numbers, authors, titles, etc
'''
import re

import time
import random

import requests_html
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from urllib.parse import urlparse, parse_qs

seen = set()
driver = None


def get_cluster_id(url):
    """
    Google assign a cluster identifier to a group of web documents
    that appear to be the same publication in different places on the web.
    How they do this is a bit of a mystery, but this identifier is 
    important since it uniquely identifies the publication.
    """
    vals = parse_qs(urlparse(url).query).get('cluster', [])
    if len(vals) == 1:
        return vals[0]
    else:
        vals = parse_qs(urlparse(url).query).get('cites', [])
        if len(vals) == 1:
            return vals[0]
    return None


def get_id(e):
    """
    Determining the publication id is tricky since it involves looking
    in the element for the various places a cluster id can show up.
    If it can't find one it will use the data-cid which should be 
    usable since it will be a dead end anyway: Scholar doesn't know of 
    anything that cites it.
    """
    for a in e.find('.gs_fl a'):
        if 'Cited by' in a.text:
            return get_cluster_id(a.attrs['href'])
        elif 'versions' in a.text:
            return get_cluster_id(a.attrs['href'])
    return e.attrs.get('data-cid')


def get_citations(url, depth=1, pages=1):
    """
    Given a page of citations it will return bibliographic information
    for the source, target of a citation.
    """
    if url in seen:
        return

    html = get_html(url)
    seen.add(url)

    # get the publication that these citations reference.
    # Note: this can be None when starting with generic search results
    a = html.find('#gs_res_ccl_top a', first=True)
    if a:
        to_pub = {
            'id': get_cluster_id(url),
            'title': a.text,
        }
    else:
        to_pub = None

    for e in html.find('#gs_res_ccl_mid .gs_r'):

        from_pub = get_metadata(e)
        if from_pub:
            yield from_pub, to_pub
        else:
            continue

        # depth first search if we need to go deeper
        if depth > 0 and from_pub['cited_by_url']:
            yield from get_citations(
                from_pub['cited_by_url'],
                depth=depth-1,
                pages=pages
            )

    # get the next page if that's what they wanted
    if pages > 1:
        for link in html.find('#gs_n a'):
            if link.text == 'Next':
                yield from get_citations(
                    'https://scholar.google.com' + link.attrs['href'],
                    depth=depth,
                    pages=pages-1
                )


def get_metadata(e):
    """
    Fetch the citation metadata from a citation element on the page.
    """
    article_id = get_id(e)
    if not article_id:
        return None

    a = e.find('.gs_rt a', first=True)
    if a:
        url = a.attrs['href']
        title = a.text
    else:
        url = None
        title = e.find('.gs_rt .gs_ctu', first=True).text

    authors = source = website = None
    meta = e.find('.gs_a', first=True).text
    meta_parts = [m.strip() for m in re.split(r'\W-\W', meta)]
    if len(meta_parts) == 3:
        authors, source, website = meta_parts
    elif len(meta_parts) == 2:
        authors, source = meta_parts

    if source and ',' in source:
        year = source.split(',')[-1].strip()
    else:
        year = source

    cited_by = cited_by_url = None
    for a in e.find('.gs_fl a'):
        if 'Cited by' in a.text:
            cited_by = a.search('Cited by {:d}')[0]
            cited_by_url = 'https://scholar.google.com' + a.attrs['href']

    return {
        'id': article_id,
        'url': url,
        'title': title,
        'authors': authors,
        'year': year,
        'cited_by': cited_by,
        'cited_by_url': cited_by_url
    }


def get_html(url):
    """
    get_html uses selenium to drive a browser to fetch a URL, and return a
    requests_html.HTML object for it.

    If there is a captcha challenge it will alert the user and wait until 
    it has been completed.
    """
    global driver

    time.sleep(random.randint(1, 5))
    driver.get(url)
    while True:
        try:
            recap = driver.find_element_by_css_selector(
                '#gs_captcha_ccl,#recaptcha')
        except NoSuchElementException:

            try:
                html = driver.find_element_by_css_selector(
                    '#gs_top').get_attribute('innerHTML')
                return requests_html.HTML(html=html)
            except NoSuchElementException:
                print("google has blocked this browser, reopening")
                driver.close()
                driver = webdriver.Chrome()
                return get_html(url)

        print("... it's CAPTCHA time!\a ...")
        time.sleep(5)


def remove_nones(d):
    new_d = {}
    for k, v in d.items():
        if v is not None:
            new_d[k] = v
    return new_d


#getcite_onepaper(url='https://scholar.google.com/scholar?oi=bibs&hl=en&cites=7601154960238900186',pages = 2, depth = 0, outputfile = "test",citation_file="citation.txt")
#getcite_onepaper(url='https://scholar.google.com/scholar?oi=bibs&hl=en&oe=ASCII&cites=5823750366366098033',pages = 2, depth = 0, outputfile = "test2",citation_file="citation.txt")
# Using readlines()
driver = webdriver.Chrome()

pubs = pd.read_csv('data/allPapers_citationNumbers.csv', header=0, nrows=23)
print(pubs.columns)
print(pubs['url'])
citation_file = "data/allcitations.txt"
#file2 = 'allpapers_summary.txt'
count = 0
# Index(['title', 'totalCitations', 'url', 'clusterid', 'authors'], dtype='object')
'''
({'id': 'RUBFYN1GWeMJ', 'url': 'https://www.thieme-connect.com/products/ejournals/html/10.1055/s-0041-1727144', 'title': 'SYNGAP1 and Its Related Epileptic Syndromes', 'authors': 'MT Garozzo, D Caruso…', 'year': '2021', 'cited_by': None, 'cited_by_url': None},
 {'id': '7601154960238900186', 'title': 'Phase transition in postsynaptic densities underlies formation of synaptic complexes and...'})
'''
column_names = ["id_source", "title_source", "authors_source",
                "url_source", "cited_by_source", "id_target"]

df = pd.DataFrame(columns=column_names)
#df = pd.DataFrame([[1, 2], [3, 4]], columns=list('AB'), index=['x', 'y'])
#df = df.append({'A': i}, ignore_index=True)
count = 0
for i in range(pubs.shape[0]):  # pubs.shape[0]
    #i = 15
    currentcount = pubs.loc[i, "totalCitations"]
    if pd.isna(currentcount):
        continue
    currentcount = int(currentcount)
    print("###################\n")
    print(pubs.loc[i, "title"])
    url_current = pubs.loc[i, "url"]
    citations_onepaper = get_citations(url=url_current, depth=0, pages=50)
    for from_pub, to_pub in citations_onepaper:
        if to_pub:
            print('%s -> %s' % (from_pub['id'], to_pub['title']))
            current_authors = from_pub['authors']
            current_cite = from_pub['cited_by']
            if current_authors is not None:
                if current_authors.find("…") >= 0:
                    if current_cite is not None:
                        pass

            #df = df.append({'A': i}, ignore_index=True)
            df.loc[count] = [from_pub['id'], from_pub['title'], from_pub['authors'],
                             from_pub['url'], from_pub['cited_by'], to_pub['id']]
            count = count + 1
            with open(citation_file, 'a+') as f:
                f.write('%s -> %s\n' % (from_pub['id'], to_pub['id']))

    print("****\n\n")
    # print(citations_onepaper)
    #    getcite_onepaper(url=currenturl,pages = math.ceil(currentcount/10), depth = 0, outputfile = f"paper{currentcluster}",citation_file="citation.txt")

    #print("Line{}: {}".format(count, line[0:1]))
driver.close()
df.to_csv("data/allcitationNumbers.csv", index=False)
