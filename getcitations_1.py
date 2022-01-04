'''
input: your google profile id: user=APooktAAAAAJ
output:data/allPapers_citationNumbers.csv
This is the first step of my google scholar analytics
This program gets your google-scholar profile, extract all your publications:
"title": title_all, 
"totalCitations": citation_all,
"url": citationUrl_all, 
"clusterid": clusterid_all, 
"authors": authors_all
'''
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
import random
from bs4 import BeautifulSoup
import pandas as pd

parameters_user = pd.read_json(
    'data/parameters.txt', orient='records', lines=True)
gid = str(parameters_user.loc[0, 'gid']).strip()

driver = webdriver.Chrome("/usr/local/bin/chromedriver")
# &cstart=100&pagesize=100
driver.get(
    f'https://scholar.google.com/citations?hl=en&user={gid}&hl=en&cstart=0&pagesize=100')

try:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(20)
    # Wait up to 10s until the element is loaded on the page
    element = WebDriverWait(driver, 10).until(
        # Locate element by id
        EC.presence_of_element_located((By.ID, 'gsc_bpf_more'))
    )
finally:
    element.click()

html_source = driver.page_source
soup = BeautifulSoup(html_source, 'html.parser')
driver.close()
# with open("allpubs.html") as fp:
#    soup = BeautifulSoup(fp, 'html.parser')
#   <tr class="gsc_a_tr">
#       <td class="gsc_a_t">
#           <a href="/citations?view_op=view_citation&amp;hl=en&amp;user=APooktAAAAAJ&amp;citation_for_view=APooktAAAAAJ:YsMSGLbcyi4C" class="gsc_a_at">Phase transition in postsynaptic densities underlies formation of synaptic complexes and synaptic plasticity</a>
#           <div class="gs_gray">M Zeng, Y Shang, Y Araki, T Guo, RL Huganir, M Zhang</div>
#           <div class="gs_gray">Cell 166 (5), 1163-1175. e12<span class="gs_oph">, 2016</span></div>
#       </td><td class="gsc_a_c">
#           <a href="https://scholar.google.com/scholar?oi=bibs&amp;hl=en&amp;cites=7601154960238900186" class="gsc_a_ac gs_ibl">245</a></td><td class="gsc_a_y"><span class="gsc_a_h gsc_a_hc gs_ibl">2016</span>
#       </td>
#   </tr>

title_all = list()
citation_all = list()
citationUrl_all = list()
clusterid_all = list()
authors_all = list()
driver = webdriver.Chrome()
paper_records = soup("tr", {"class": 'gsc_a_tr'})
for p in paper_records:
    paper_title = p.find('a', {"class": "gsc_a_at"}).getText()
    print(paper_title)
    citations_anchor = p.find('a', {"class": 'gsc_a_ac'})
    citations = citations_anchor.getText()
    citationUrl = citations_anchor['href']
    clusterid = citationUrl.split("cites=")
    if len(clusterid) > 1:
        clusterid = clusterid[1]
    print(clusterid)
    if clusterid == '':
        continue
    authors = p.find('div', {'class': 'gs_gray'}).getText()
    print(authors)
    if authors.find(", ...") >= 0:
        print(authors)
        paper_url = p.find('a', {"class": "gsc_a_at"})['href']
        paper_url = "https://scholar.google.com"+paper_url
        print(paper_url)
        time.sleep(random.randint(1, 5))
        driver.get(paper_url)
        while True:
            try:
                recap = driver.find_element_by_css_selector(
                    '#gs_captcha_ccl,#recaptcha')
            except NoSuchElementException:
                try:
                    html2 = driver.find_element_by_css_selector(
                        '#gs_top').get_attribute('innerHTML')
                    html2 = driver.page_source
                    break
                except NoSuchElementException:
                    print("google has blocked this browser, reopening")
                    driver.close()
                    driver = webdriver.Chrome()
                    break
            print("... it's CAPTCHA time!\a ...")
            time.sleep(5)
        soup2 = BeautifulSoup(html2, 'html.parser')
        # <div class="gsc_oci_value">Ilona Christy Unarta, Jianchao Xu, Yuan Shang, Carina Hey Pui Cheung, Ruichi Zhu, Xudong Chen, Siqin Cao, Peter Pak-Hang Cheung, Donald Bierer, Mingjie Zhang, Xuhui Huang, Xuechen Li</div></div>
        p2 = soup2("div", {"class": 'gsc_oci_value'})
        authors = p2[0].getText()
        print("New Detailed Authors:\t", authors)

    print(f"######{clusterid}\n")

    title_all.append(paper_title)
    citation_all.append(citations)
    citationUrl_all.append(citationUrl)
    clusterid_all.append(clusterid)
    authors_all.append(authors)

driver.close()
#citation_all = [int(a) for a in citation_all]
df1 = pd.DataFrame({"title": title_all, "totalCitations": citation_all,
                   "url": citationUrl_all, "clusterid": clusterid_all, "authors": authors_all})
print(df1.shape, "df1 shape")
df1.to_csv("data/allPapers_citationNumbers.csv", index=False)
