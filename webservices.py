

import urllib.request




def search_by_hgnc(searchterm):
	url = "https://www.ebi.ac.uk/ebisearch/ws/rest/lrg?query=name:"+searchterm
	queryresults = urllib.request.urlopen(url)
	print(queryresults.read())