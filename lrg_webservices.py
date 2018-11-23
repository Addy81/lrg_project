

import urllib.request
import lrgparser

# XML Related Imports
import xml.etree.ElementTree as ET


def search_by_hgnc(searchterm):
	url = "https://www.ebi.ac.uk/ebisearch/ws/rest/lrg?query=name:"+searchterm
	queryresults = urllib.request.urlopen(url)
	xml_file = queryresults.read()
	root = lrgparser.get_tree_and_root_string(xml_file)
	try:
		lrg_id = root.find('entries/entry').attrib['id']
	except:
		print("No results for that search term")
		lrg_id = None

	return lrg_id


def search_by_lrg(searchterm):
	url = "http://ftp.ebi.ac.uk/pub/databases/lrgex/"+searchterm+".xml"
	queryresults = urllib.request.urlopen(url)
	xml_file = queryresults.read()
	return(xml_file)
