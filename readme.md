## Readme
This program sets extract your google scholar profile and analyze your citations
Before runing,you also need to creat a folder "data", and a "parameters.txt" file in data
An example of parameters.txt, which stores your google scholar id:gid, your pubmed email address, and you pubmed api_key
```
{"gid":"xxxx"
"pubemail":"x@xxxx.edu"
"api_key":"xxxxxx"}
```

## Filelist
- getcitations_1.py: extract your google scholar profile, get all your publications, including titles, authors, citationNumbers, google_clusterids, url.
- getcitations_2.py: extract all informations of the papers that cited your work, including titles,authors, citationNumbers, etc
- getcitations_3.py: merges the matching source-target(results of getcitations_2.py) with target information(results of getcitations_1.py)
- getcitations_4.py: authorlist from googlescholar is not complete, this program search them from pubmed using E-utilities
- getcitations_5.py: Merge authors results from pubmed search with googlescholar main results
- getcitations_6.py: This program analyzes the self-citations to get a first glance
- getcitations_7.py: Further update authors information by pubmed websearch since E-utilities did not return the best matching results
- getcitations_8.py: Re-analyze the self-citations after pubmed websearch
- getcitations_9.py: Format the results form 8.py. After this, we need mannual inspections
- getcitations_10.py: Get the summary results

