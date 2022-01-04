'''
input:  data/allcitation_final2_reformat_modify.csv
output: data/allcitations_summary.csv
This program re-analyzed the citations after mannual inspections, and get the final results including
1. allcitations_summary.csv
'''
import pandas as pd

allcitations = pd.read_csv(
    "data/allcitation_final2_reformat_modify.csv", header=0)
print(allcitations.shape)
print(len(list(allcitations.titleMatch)))
print(allcitations.columns)
# ['id_source', 'title_source_x', 'authors_source', 'url_source',
#       'cited_by_source', 'id_target', 'title', 'totalCitations', 'url',
#       'clusterid', 'authors', 'index_source', 'pubmed_id', 'title_pub',
#       'title_source_y', 'authors_pub', 'clusterid_google', 'titleMatch',
#       'authoerOverlaps', 'selfcitations']

df1 = allcitations[[
    'id_target', 'title', 'authors', 'totalCitations',
    'url']]
df1 = df1.drop_duplicates()
print(df1)
df2 = allcitations[['id_target', 'selfcitations']]
df2.loc[df2['selfcitations'] == -1, "selfcitations"] = 0
df2 = df2.groupby('id_target')['selfcitations'].agg(
    selfcitations='sum', total='count').reset_index()
print(df2.shape)
print(df2.columns)

allcitations_summary = df1.merge(
    df2, how="left", left_on="id_target", right_on="id_target")
# print(allcitations_summary)
allcitations_summary['selfcitationrate'] = allcitations_summary['selfcitations'] / \
    allcitations_summary['total']

print(allcitations_summary[['title', 'selfcitationrate']])
print("total citation rate:")
print(sum(allcitations_summary['selfcitations']) /
      sum(allcitations_summary['total']))
allcitations_summary.to_csv("data/allcitations_summary.csv", index=False)
'''
grouper = df2.groupby('id_target')
print(grouper)
res = grouper.count()
res['totalcitations'] = grouper.selfcitations.count()
res['selfcitations'] = grouper.selfcitations.sum()
print(res)
'''
