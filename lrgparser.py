


import argparse
import os
import sys

# Import of other local python scripts. 'bedgen' contains the BED file
# generating functions. 'functions' contains the exon extraction functions.
import bedgen
import functions
import ui

# XML Related Imports
import xml.etree.ElementTree as ET


class LRG_Object:
	'''LRG object class containing LRG ID, HGNC ID etc'''
	def __init__(self, lrg_id, hgnc_id, seq_source, mol_type, nm_exon_coords):
		self.lrg_id = lrg_id
		self.hgnc_id = hgnc_id
		self.seq_source = seq_source
		self.mol_type = mol_type
		self.nm_exon_coords = nm_exon_coords


def main(xml_file):
	'''Main function'''
	ui.splashscreen(xml_file)
	tree, root = get_tree_and_root(xml_file)
	lrg_id = xml_file.rstrip('.xml')

	# Pick which Genome Build to use
	genomebuilds = get_genome_builds(root)
	genome_choice = ui.ask_which_genome_build(genomebuilds)

	# Pick which transcript id to use (NCBI and Ensembl transcripts)
	transcript_ids = get_transcript_ids(root)
	transcript_choice = ui.ask_which_transcript(transcript_ids)

	lrg_object = lrg_object_creator(root, lrg_id, transcript_choice)
	check_lrg_object_contents(lrg_object)
	#bed_file = bedgen.generate_bed(lrg_object)



def get_tree_and_root(xml_file):
	'''Returns the XML tree and root when provided with an XML file'''
	tree = ET.parse(xml_file)
	root = tree.getroot()
	return tree, root

def get_genome_builds(root):
	genomebuilds = []
	for transcript_type in root.iter('annotation_set'):
		source = transcript_type.attrib["type"]
		if source == "lrg":
			for transcript in transcript_type:
				if transcript.tag == "mapping":
					genomebuild = transcript.attrib["coord_system"]
					genomebuilds.append(genomebuild)
	return genomebuilds

def get_transcript_ids(root):
	transcripts = []
	for transcript_type in root.iter('annotation_set'):
		source = transcript_type.attrib["type"]
		if source == "ncbi" or source == "ensembl":
			for transcript in transcript_type:
				if transcript.tag == "mapping":
					transcript_id = transcript.attrib["coord_system"]
					transcripts.append(transcript_id)
	return transcripts




def lrg_object_creator(root, xml_id, transcript_choice):
	'''Returns an LRG object when passed an LRG root. Object contains 
	lrg_id, hgnc_id, seq_source, mol_type, a dict of exons and locations.
	'''
	lrg_id = root.find('fixed_annotation/id').text
	hgnc_id = root.find('fixed_annotation/hgnc_id').text
	seq_source = root.find('fixed_annotation/sequence_source').text
	mol_type = root.find('fixed_annotation/mol_type').text
	exon_coords = functions.get_exon_coords(root, lrg_id)
	nm_exon_coords = functions.get_real_exon_coords(root, transcript_choice)

	# Create an LRG Object using the LRG_Object class
	lrg_object = LRG_Object(lrg_id, hgnc_id, seq_source, mol_type, nm_exon_coords) 
	return lrg_object


def check_lrg_object_contents(lrg_object):
	print("LRG ID    : ", lrg_object.lrg_id)
	print("HGNC ID   : ", lrg_object.hgnc_id)
	print("SEQ SOURCE: ", lrg_object.seq_source)
	print("MOL TYPE  : ", lrg_object.mol_type)
	print("")
	for item in lrg_object.nm_exon_coords:
		print(lrg_object.nm_exon_coords[item])





if __name__ == "__main__":
	main('LRG_384.xml')
