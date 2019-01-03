#!/usr/bin/python3
# -*- coding: utf-8 -*-

import urllib.request
import lrgparser


def search_by_hgnc(searchterm):
	"""Searches the lrg-sequence database for the provided HGNC ID searchterm 
	using the REST API. Returns a matching LRG ID extracted from the search
	results XML file (Note: Not an LRG XML file)
	"""
	url = "https://www.ebi.ac.uk/ebisearch/ws/rest/lrg?query=name:"+searchterm
	queryresults = urllib.request.urlopen(url)
	xml_file = queryresults.read()
	root = lrgparser.get_tree_and_root_string(xml_file)
	try:
		lrg_id = root.find('entries/entry').attrib['id']
	except:
		print("No LRG results for the search term: " + searchterm)
		raise SystemExit
	return lrg_id


def search_by_lrg(searchterm):
	"""Searches the lrg-sequence database for the provided LRG ID searchterm 
	using the REST API. Returns the matching LRG XML file.
	"""
	url = "http://ftp.ebi.ac.uk/pub/databases/lrgex/"+searchterm+".xml"
	queryresults = urllib.request.urlopen(url)
	xml_file = queryresults.read()
	return(xml_file)
