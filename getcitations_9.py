'''
input:data/allcitation_final2.csv
output1:data/allcitation_final2_reformat.csv
output2(after mannual inspection):data/allcitation_final2_reformat_modify.csv
After this round, final check of allcitation_final2_reformat.csv, especiall the author overlaps, 
correct "selfcitations" values if nessesary.
This program summarize the results from getcitations_8.py:
1. reformat the citation results, making it more convenitent for mannual inspections
#2. get a summary citation results from each paper
'''
import pandas as pd

allcitations = pd.read_csv("data/allcitation_final2.csv", header=0)
print(allcitations.shape)
print(len(list(allcitations.titleMatch)))
print(allcitations.columns)
# ['id_source', 'title_source_x', 'authors_source', 'url_source',
#       'cited_by_source', 'id_target', 'title', 'totalCitations', 'url',
#       'clusterid', 'authors', 'index_source', 'pubmed_id', 'title_pub',
#       'title_source_y', 'authors_pub', 'clusterid_google', 'titleMatch',
#       'authoerOverlaps', 'selfcitations']
allcitations_reformat = allcitations[[
    'index_source', 'id_source', 'title_source_x', 'authors_source',
    'authors_pub', 'title_pub', 'titleMatch', 'url_source',
    'cited_by_source', 'id_target', 'title', 'authors', 'totalCitations',
    'url', 'authoerOverlaps', 'selfcitations']]
allcitations_reformat.columns = [
    'index_source', 'id_source', 'title_source', 'authors_source',
    'authors_pub', 'title_pub', 'titleMatch', 'url_source',
    'cited_by_source', 'id_target', 'title', 'authors', 'totalCitations',
    'url', 'authoerOverlaps', 'selfcitations']
print(sum(allcitations['id_source'] != allcitations['clusterid_google']))
allcitations_reformat.to_csv(
    "data/allcitation_final2_reformat.csv", index=False)

#allcitations_summary.to_csv("data/allcitations_summary.csv", index=False)
'''
grouper = df2.groupby('id_target')
print(grouper)
res = grouper.count()
res['totalcitations'] = grouper.selfcitations.count()
res['selfcitations'] = grouper.selfcitations.sum()
print(res)
'''
