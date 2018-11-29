


import argparse
import os
import sys

# Import of local python scripts. 
# bedgen contains the BED file generating functions
import bedgen 
# functions contains the exon extraction functions.
import functions
# ui contains the terminal UI functions.  
import ui 
# lrg_webservices contains the terminal UI functions.  
import lrg_webservices # Contains the 

# XML Related Imports
import xml.etree.ElementTree as ET


class LRG_Object:
	'''LRG object class containing LRG ID, HGNC ID etc'''
	def __init__(self, lrg_id, hgnc_id, seq_source, mol_type, nm_exon_coords, mapped_coords, chromosome):
		self.lrg_id = lrg_id
		self.hgnc_id = hgnc_id
		self.seq_source = seq_source
		self.mol_type = mol_type
		self.nm_exon_coords = nm_exon_coords
		self.mapped_coords = mapped_coords
		self.chromosome = chromosome


def main(arguments):
	'''Main function. Runs the UI and handles user choices. Calls appropriate
	external functions based on responses.
	'''
	ui.splashscreen()
	searchquery = ui.ask_what_gene()
	searchresults = lrg_webservices.search_by_hgnc(searchquery)
	if searchresults != None:
		lrg_xml = lrg_webservices.search_by_lrg(searchresults)
		root = get_tree_and_root_string(lrg_xml)

		#lrg_id = xml_file.rstrip('.xml')

		# Pick which Genome Build to use
		genomebuilds = get_genome_builds(root)
		genome_choice = ui.ask_which_genome_build(genomebuilds)

		# Pick which transcript id to use (NCBI and Ensembl transcripts)
		transcript_ids = get_transcript_ids(root)
		transcript_choice = ui.ask_which_transcript(transcript_ids)

		lrg_object = lrg_object_creator(root, genome_choice, transcript_choice)
		#check_lrg_object_contents(lrg_object)

		bed_filename = searchquery.upper()+"_"+lrg_object.lrg_id+"_"+transcript_choice+"_"+genome_choice+".tsv"
		bedheader = "Custom_Track_"+searchquery.upper()+"_"+lrg_object.lrg_id+"_"+transcript_choice+"_"+genome_choice
		bedcontents = bedgen.create_bed_contents(lrg_object)
		bed_file = bedgen.write_bed_file(bed_filename, bedheader, bedcontents)
	else:
		pass


def get_tree_and_root_file(xml_file):
	'''Returns the XML tree and root when provided with an XML file'''
	tree = ET.parse(xml_file)
	root = tree.getroot()
	return tree, root


def get_tree_and_root_string(xml_string):
	'''Returns the XML tree and root when provided with an XML string'''
	root = ET.fromstring(xml_string)
	return root


def get_genome_builds(root):
	'''Returns the different possible genome builds, pulled from the LRG xml file'''
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
	'''Returns the different possible transcripts, pulled from the LRG xml file'''
	transcripts = []
	for transcript_type in root.iter('annotation_set'):
		source = transcript_type.attrib["type"]
		if source == "ncbi" or source == "ensembl":
			for transcript in transcript_type:
				if transcript.tag == "mapping":
					transcript_id = transcript.attrib["coord_system"]
					transcripts.append(transcript_id)
	return transcripts


def lrg_object_creator(root, genome_choice, transcript_choice):
	'''Returns an LRG object when passed an LRG root. Object contains 
	lrg_id, hgnc_id, seq_source, mol_type, a dict of exons and locations.
	'''
	lrg_id = root.find('fixed_annotation/id').text
	hgnc_id = root.find('fixed_annotation/hgnc_id').text
	seq_source = root.find('fixed_annotation/sequence_source').text
	mol_type = root.find('fixed_annotation/mol_type').text
	exon_coords = functions.get_exon_coords(root, lrg_id)

	for transcript_type in root.iter('annotation_set'):
		source = transcript_type.attrib["type"]
		if source == "lrg":
			for transcript in transcript_type:
				if transcript.tag == "mapping":
					chromosome = transcript.attrib["other_name"]
					
	nm_exon_coords = functions.get_real_exon_coords(root, transcript_choice)
	mapped_coords = functions.get_chr_coordinates(root, genome_choice, transcript_choice)

	# Create an LRG Object using the LRG_Object class
	lrg_object = LRG_Object(lrg_id, hgnc_id, seq_source, mol_type, nm_exon_coords, mapped_coords, chromosome) 
	return lrg_object


def check_lrg_object_contents(lrg_object):
	print("LRG ID    : ", lrg_object.lrg_id)
	print("HGNC ID   : ", lrg_object.hgnc_id)
	print("SEQ SOURCE: ", lrg_object.seq_source)
	print("MOL TYPE  : ", lrg_object.mol_type)
	print("")
	for item in lrg_object.mapped_coords:
		print(lrg_object.mapped_coords[item])


def arg_collection():
	parser = argparse.ArgumentParser()
	# Main Arguments: 
	# Different routes to obtain an LRG XML file
	# Either by providing a file, a HGNC gene ID or an LRG ID.
	parser.add_argument('-f',
						'--file',
						help="ExistingLRG XML File location",
						type=str,
						dest='filearg')
	parser.add_argument('-g',
						'--geneid',
						help="Gene ID",
						type=str,
						dest='geneid')
	parser.add_argument('-l',
						'--lrgid',
						help="LRG ID",
						type=str,
						dest='lrgid')

	# Supplimentary Arguments:
	# Extra arguments necessary for automated BED file generation
	# If not provided, the UI will take over and prompt the user
	parser.add_argument('-r',
						'--referencegenome',
						help="Reference genome",
						type=str,
						dest='referencegenome')
	parser.add_argument('-t',
						'--transcript',
						help="Transcript",
						type=str,
						dest='transcript')
	args = parser.parse_args()
	arguments = {
				'filearg': args.filearg,
				'geneid': args.geneid,
				'lrgid': args.lrgid,
				'referencegenome': args.referencegenome,
				'transcript': args.transcript,
				}
	return arguments



if __name__ == "__main__":

	arguments = arg_collection()
	main(arguments)
