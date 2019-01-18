

"""
This module contains functions for interacting with the API for
lrg-sequence.org
"""


import urllib.request
import lrgparser


def search_by_hgnc(searchterm):
	"""Searches the lrg-sequence database for the provided HGNC searchterm 
	using the REST API. Returns a matching LRG ID extracted from the search
	results XML file (Note: Not an LRG XML file)
	
	Args:
		searchterm (str): HGNC name search term to query the ebi.ac.uk site
	Returns:
		lrg_id (str): LRG ID that matches the HGNC gene input

	"""
	url = "https://www.ebi.ac.uk/ebisearch/ws/rest/lrg?query=name:"+searchterm
	queryresults = urllib.request.urlopen(url)
	xml_file = queryresults.read()
	root = lrgparser.get_tree_and_root_string(xml_file)
	# Looks to see whether the returned XML file contains a match for the
	# search term
	try:
		lrg_id = root.find('entries/entry').attrib['id']
	except:
		print("No LRG is available for: " + searchterm)
		raise SystemExit
	return lrg_id


def search_by_lrg(searchterm):
	"""Searches the lrg-sequence database for the provided LRG ID searchterm 
	using the REST API. Returns the matching LRG XML file.
	
	Args:
		searchterm (str): LRG ID in the format 'LRG_123'
	Returns:
		xml_file (str): Contents of the returned XML file

	"""
	url = "http://ftp.ebi.ac.uk/pub/databases/lrgex/"+searchterm+".xml"
	try:
		queryresults = urllib.request.urlopen(url)
		xml_file = queryresults.read()
	except urllib.error.HTTPError:
		print("No LRG is available for the search term: " + searchterm)
		raise SystemExit
	return(xml_file)
