


import argparse
import os
import sys

# Import of other local python scripts. 'bedgen' contains the BED file
# generating functions. 'functions' contains the exon extraction functions.
import bedgen
import functions

# XML Related Imports
import xml.etree.ElementTree as ET


class LRG_Object:
	'''LRG object class containing LRG ID, HGNC ID etc'''
	def __init__(self, lrg_id, hgnc_id, seq_source, mol_type, exon_coords):
		self.lrg_id = lrg_id
		self.hgnc_id = hgnc_id
		self.seq_source = seq_source
		self.mol_type = mol_type
		self.exon_coords = exon_coords


def main(xml_file):
	'''Main function'''
	tree, root = get_tree_and_root(xmlfile)
	lrg_object = lrg_object_creator(root)
	bed_file = bedgen.generate_bed(lrg_object)


def get_tree_and_root(xmlfile):
	'''Returns the XML tree and root when provided with an XML file'''
	tree = ET.parse(xml_file)
	root = tree.getroot()
	return tree, root


def lrg_object_creator(xml_file):
	'''Returns an LRG object when passed an LRG root. Object contains 
	lrg_id, hgnc_id, seq_source, mol_type, a dict of exons and locations.
	'''
	lrg_id = root.find('fixed_annotation/id').text
	hgnc_id = root.find('fixed_annotation/hgnc_id').text
	seq_source = root.find('fixed_annotation/sequence_source').text
	mol_type = root.find('fixed_annotation/mol_type').text
	exon_coords = functions.get_exon_coords(root)

	# Create an LRG Object using the LRG_Object class
	lrg_object = LRG_Object(lrg_id, hgnc_id, seq_source, mol_type, exon_coords) 
	return lrg_object




in __name__ == "__main__":
	main('LRG_384.xml')
