import pandas as pd

allcitations = pd.read_csv("allcitation_final2.csv", header=0)
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
allcitations_reformat.to_csv("allcitation_final2_reformat.csv", index=False)

df1 = allcitations_reformat[[
    'id_target', 'title', 'authors', 'totalCitations',
    'url']]
df1 = df1.drop_duplicates()
print(df1)
df2 = allcitations_reformat[['id_target', 'selfcitations']]
df2.loc[df2['selfcitations'] == -1, "selfcitations"] = 0
df2 = df2.groupby('id_target')['selfcitations'].agg(
    selfcitation='sum', total='count').reset_index()
print(df2.shape)
print(df2.columns)

allcitations_summary = df1.merge(
    df2, how="left", left_on="id_target", right_on="id_target")
print(allcitations_summary)
allcitations_summary.to_csv("allcitations_summary.csv", index=False)
'''
grouper = df2.groupby('id_target')
print(grouper)
res = grouper.count()
res['totalcitations'] = grouper.selfcitations.count()
res['selfcitations'] = grouper.selfcitations.sum()
print(res)
'''
