import pandas as pd

pubs = pd.read_csv('data/allPapers_citationNumbers.csv', header=0)

print(pubs)

tmp = pubs.loc[(pubs["clusterid"] != "['']")]
print(tmp)
