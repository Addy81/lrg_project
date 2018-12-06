


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
	def __init__(self, lrg_id, hgnc_id, seq_source, mol_type, 
				mapped_flanked_exon_coords, mapped_intron_coords, chromosome):
		self.lrg_id = lrg_id
		self.hgnc_id = hgnc_id
		self.seq_source = seq_source
		self.mol_type = mol_type
		self.mapped_flanked_exon_coords = mapped_flanked_exon_coords
		self.mapped_intron_coords = mapped_intron_coords
		self.chromosome = chromosome


def main(args):
	'''Main function. Runs the UI and handles user choices. Calls appropriate
	external functions based on responses.
	'''
	if (args['file'] == None and 
		args['lrgid'] == None and 
		args['geneid'] == None):
		show_ui = True
	else:
		show_ui = False


	# If a file is provided, check whether it is valid
	if args['file'] != None:
		# TODO add some file checking stuff
		# Obtain the root from the XML file
		root = get_tree_and_root_file(args['file'])

	# If no file is provided using the file flag, XML is obtained using
	# the 'geneid' or 'lrgid' flag or asking the user with the UI.
	else:
		# Obtain a Gene ID when no LRG or Gene ID given
		if args['geneid'] == None and args['lrgid'] == None:
			ui.splashscreen()
			searchquery = ui.ask_what_gene()
			args['geneid'] = searchquery


		# Obtain an LRG ID using Gene ID, only if no LRG ID has been provided
		if 	args['geneid'] != None and args['lrgid'] == None:
			searchresults = lrg_webservices.search_by_hgnc(args['geneid'])
			if searchresults != None:
				# TODO does this always only return 1 result?
				args['lrgid'] =  searchresults 


		# At this point, the program has an LRG ID and can use this to obtain
		# an XML from the LRG-sequence.org site
		lrg_xml = lrg_webservices.search_by_lrg(args['lrgid'])
		# Obtain the root from the XML string provided by the webservices
		root = get_tree_and_root_string(lrg_xml)


	# At this point in the program, whether a file, LRG ID or Gene ID has been
	# provided, the program now has an XML root, from which it can obtain 
	# genome build, transcript, exon location and mapping information.


	# Pick which Genome Build to use if none has been provided with a flag
	if args['referencegenome'] == None:
		genomebuilds = get_genome_builds(root)
		genome_choice = ui.ask_which_genome_build(genomebuilds)
		args['referencegenome'] = genome_choice


	# Pick which Transcript to use if none has been provided with a flag
	if args['transcript'] == None:
		transcript_ids = get_transcript_ids(root)
		transcript_choice = ui.ask_which_transcript(transcript_ids)
		args['transcript'] = transcript_choice
	

	# Pick the flank size to use if none has been provided with a flag
	if args['flank'] == None:
		if show_ui == True:
			args['flank'] = ui.ask_flank_size()
		else:
			args['flank'] = 0
	args['flank'] = int(args['flank'])


	# Choose whether to include intronic regions in the BED file
	if args['introns'] == False:
		if show_ui == True:
			args['introns'] = ui.ask_include_introns()


	# Create an LRG_Object, which contains LRG ID, HGNC ID, mapped exon 
	# coordinates etc. This information is extracted from the XML root by
	# lrg_object_creator()
	lrg_object = lrg_object_creator(root, 
									args['referencegenome'],
									args['transcript'],
									args['introns'],
									args['flank'])

	# BED file filename creation
	bed_filename = "_".join([lrg_object.hgnc_id,
							lrg_object.lrg_id,
							args['transcript'],
							args['referencegenome'],
							"flank"+str(args['flank'])
							]) + ".tsv"
					
	# BED file header creation
	bedheader_name = "LRG_Parser_Custom_Track"
	bedheader_desc = "_".join([lrg_object.hgnc_id,
								lrg_object.lrg_id,
								args['transcript'],
								args['referencegenome']])
	bedheader = [bedheader_name, bedheader_desc]


	# Create the contents of the BED file.
	bedcontents = bedgen.create_bed_contents(lrg_object, args['introns'])


	# Write the BED contents to disk
	bed_file = bedgen.write_bed_file(bed_filename, bedheader, bedcontents)


def get_tree_and_root_file(xml_file):
	'''Returns the XML tree and root when provided with an XML file'''
	tree = ET.parse(xml_file)
	root = tree.getroot()
	return root


def get_tree_and_root_string(xml_string):
	'''Returns the XML tree and root when provided with an XML string'''
	root = ET.fromstring(xml_string)
	return root


def get_genome_builds(root):
	'''Returns the different possible genome builds extracted from the LRG 
	xml file
	'''
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
	'''Returns the different possible transcripts extracted from the LRG 
	xml file
	'''
	transcripts = []
	for transcript_type in root.iter('annotation_set'):
		source = transcript_type.attrib["type"]
		if source == "ncbi" or source == "ensembl":
			for transcript in transcript_type:
				if transcript.tag == "mapping":
					transcript_id = transcript.attrib["coord_system"]
					transcripts.append(transcript_id)
	return transcripts


def lrg_object_creator(root, genome_choice, transcript_choice, 
						intron_choice, flank):
	'''Returns an LRG object when passed an LRG root. Object contains 
	lrg_id, hgnc_id, seq_source, mol_type, a dict of exons and locations.
	'''
	lrg_id = root.find('fixed_annotation/id').text
	hgnc_id = root.find('fixed_annotation/hgnc_id').text
	seq_source = root.find('fixed_annotation/sequence_source').text
	mol_type = root.find('fixed_annotation/mol_type').text

	# Get the chromosome number
	for transcript_type in root.iter('annotation_set'):
		source = transcript_type.attrib["type"]
		if source == "lrg":
			for transcript in transcript_type:
				if transcript.tag == "mapping":
					chromosome = transcript.attrib["other_name"]
	
	# LRG exon coordinates mapped to the given genome build and transcript
	mapped_exon_coords = functions.get_exon_coords(root, genome_choice,
												transcript_choice)
	
	# Intron coordinates obtained using the gaps between the mapped exons
	mapped_intron_coords = functions.get_intron_coords(mapped_exon_coords)

	# Mapped exon coordinated with flanking regions added
	mapped_flanked_exon_coords = functions.get_flanked_coords(
												mapped_exon_coords, flank)

	# Create an LRG Object using the LRG_Object class
	lrg_object = LRG_Object(lrg_id, 
							hgnc_id, 
							seq_source, 
							mol_type, 
							mapped_flanked_exon_coords, 
							mapped_intron_coords, 
							chromosome) 
	return lrg_object


def check_lrg_object_contents(lrg_object):
	"""Can be used to check what is present in an lrg_object"""
	print("LRG ID    : ", lrg_object.lrg_id)
	print("HGNC ID   : ", lrg_object.hgnc_id)
	print("SEQ SOURCE: ", lrg_object.seq_source)
	print("MOL TYPE  : ", lrg_object.mol_type)
	print("")
	for item in lrg_object.mapped_flanked_exon_coords:
		print(lrg_object.mapped_flanked_exon_coords[item])


def arg_collection():
	"""Perfoms the inital collection of arguments when the program starts"""
	parser = argparse.ArgumentParser()
	# Main Arguments: 
	# Different routes to obtain an LRG XML file
	# Either by providing a file, a HGNC gene ID or an LRG ID.
	parser.add_argument('-f', '--file',
						help="ExistingLRG XML File location",
						type=str,
						dest='file')
	parser.add_argument('-g', '--geneid',
						help="Gene ID",
						type=str,
						dest='geneid')
	parser.add_argument('-l', '--lrgid',
						help="LRG ID",
						type=str,
						dest='lrgid')

	# Supplimentary Arguments:
	# Extra arguments necessary for automated BED file generation
	# If not provided, the UI will take over and prompt the user
	parser.add_argument('-r', '--referencegenome',
						help="Reference genome",
						type=str,
						dest='referencegenome')
	parser.add_argument('-t', '--transcript',
						help="Transcript",
						type=str,
						dest='transcript')
	
	# Optional Arguments:
	# Extra arguments that are not necessary for automated BED file generation
	# If not provided, it is assumed that they are not desired. Their presence
	# or absence will be displayed in the BED filename for audit purposes
	parser.add_argument('-i', '--introns',
						action='store_true', 
						help="If present, the BED file  will include introns")
	parser.add_argument('-fl', '--flank', 
						type=int,
						help="If present, exon coords include flanking regions")


	args = parser.parse_args()
	arguments = {
				'file': args.file,
				'geneid': args.geneid,
				'lrgid': args.lrgid,
				'referencegenome': args.referencegenome,
				'transcript': args.transcript,
				'flank': args.flank,
				'introns': args.introns,
				}
	return arguments



if __name__ == "__main__":
	# Get all the arguments that have been provided
	arguments = arg_collection()
	# Run the main program
	main(arguments)

