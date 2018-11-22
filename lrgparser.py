

import bedgen
import functions
import argparse
import os
import sys

# XML Related Imports
import xml.etree.ElementTree as ET


class lrgobject:
	'''LRG object class containing LRG ID, HGNC ID etc'''
	def __init__(self, lrg_id, hgnc_id, seq_source, mol_type):
		self.lrg_id = lrg_id
		self.hgnc_id = hgnc_id
		self.seq_source = seq_source
		self.mol_type = mol_type
		self.


def main(xml_file):
	'''Main function'''
	lrg_object = lrg_object_creator(xml_file)
	bed_file = bedgen.generate_bed(lrg_object)


def lrg_object_creator(xml_file):
	'''Returns an LRG object when passed an LRG XML file. Object contains 
	lrg_id, hgnc_id, seq_source, mol_type, a dict of exons and locations.
	'''
	tree = ET.parse(xml_file)
	root = tree.getroot()
	lrg_id = root.find('fixed_annotation/id').text
	hgnc_id = root.find('fixed_annotation/hgnc_id').text
	seq_source = root.find('fixed_annotation/sequence_source').text
	mol_type = root.find('fixed_annotation/mol_type').text
	#exons = functions.get_exon_locs(root)


in __name__ == "__main__":
	main('LRG_384.xml')
