


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
	def __init__(self, lrg_id, hgnc_id, seq_source, mol_type, mapped_flanked_exon_coords, mapped_intron_coords, chromosome):
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
		#TODO add some file checking stuff
		# Obtain the root from the XML file
		root = get_tree_and_root_file(args['file'])

	# If no file is provided using the file flag, XML is obtained using
	# the 'geneid' or 'lrgid' flag, whichever is provided
	else:
		# Obtain a Gene ID when no LRG or Gene ID given
		if args['geneid'] == None and args['lrgid'] == None:
			ui.splashscreen()
			searchquery = ui.ask_what_gene()
			args['geneid'] = searchquery
		else:
			pass

		# Obtain an LRG ID using Gene ID, only if no LRG ID has been provided
		if 	args['geneid'] != None and args['lrgid'] == None:
			searchresults = lrg_webservices.search_by_hgnc(args['geneid'])
			if searchresults != None:
				args['lrgid'] =  searchresults # TODO does it always only return 1 result?
			else:
				pass
		else:
			pass

		# At this point, the program has an LRG ID and can use this to obtain
		# an XML from the LRG-sequence.org site
		lrg_xml = lrg_webservices.search_by_lrg(args['lrgid'])
		# Obtain the root from the XML string provided by the webservices
		root = get_tree_and_root_string(lrg_xml)


	# At this point, whether a file, LRG ID or Gene ID has been provided, the
	# program has an XML root, from which it can obtain genome build,
	# transcript, exon location and mapping information

	if args['referencegenome'] == None:
		# Pick which Genome Build to use if none given
		genomebuilds = get_genome_builds(root)
		genome_choice = ui.ask_which_genome_build(genomebuilds)
		args['referencegenome'] = genome_choice
	else:
		pass

	if args['transcript'] == None:
		# Pick which transcript id to use if none given
		transcript_ids = get_transcript_ids(root)
		transcript_choice = ui.ask_which_transcript(transcript_ids)
		args['transcript'] = transcript_choice
	else:
		pass
	


	if args['flank'] == None:
		
		if show_ui == True:
			args['flank'] = ui.ask_flank_size()
		else:
			args['flank'] = 0
		pass
	else:
		pass
	args['flank'] = int(args['flank'])

	if args['introns'] == False:
		if show_ui == True:
			args['introns'] = ui.ask_include_introns()
		else:
			pass
	else:
		pass






	# Create an LRG_Object, which contains LRG ID, HGNC ID, mapped exon 
	# coordinates etc. This information is extracted from the root.
	lrg_object = lrg_object_creator(root, 
									args['referencegenome'],
									args['transcript'],
									args['introns'],
									args['flank'])

	# To create the BED file, the filename and header row are generated
	bed_filename = "_".join([lrg_object.hgnc_id,
							lrg_object.lrg_id,
							args['transcript'],
							args['referencegenome'],
							"flank"+str(args['flank'])
							]) + ".tsv"
					
	bedheader_name = "LRG_Parser_Custom_Track"
	bedheader_desc = "_".join([lrg_object.hgnc_id,
								lrg_object.lrg_id,
								args['transcript'],
								args['referencegenome']])

	bedheader = [bedheader_name, bedheader_desc]

	# Create the contents of the BED file. This will be a nested list  
	# containing [Chromosome, start, end]
	bedcontents = bedgen.create_bed_contents(lrg_object, args['introns'])

	# Write these BED contents to disk
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


def lrg_object_creator(root, genome_choice, transcript_choice, intron_choice, flank):
	'''Returns an LRG object when passed an LRG root. Object contains 
	lrg_id, hgnc_id, seq_source, mol_type, a dict of exons and locations.
	'''
	lrg_id = root.find('fixed_annotation/id').text
	hgnc_id = root.find('fixed_annotation/hgnc_id').text
	seq_source = root.find('fixed_annotation/sequence_source').text
	mol_type = root.find('fixed_annotation/mol_type').text

	for transcript_type in root.iter('annotation_set'):
		source = transcript_type.attrib["type"]
		if source == "lrg":
			for transcript in transcript_type:
				if transcript.tag == "mapping":
					chromosome = transcript.attrib["other_name"]
					

	
	mapped_exon_coords = functions.get_exon_coords(root, genome_choice, transcript_choice)
	mapped_intron_coords = functions.get_intron_coords(mapped_exon_coords)
	mapped_flanked_exon_coords = functions.get_flanked_coords(mapped_exon_coords, flank)


	# Create an LRG Object using the LRG_Object class
	lrg_object = LRG_Object(lrg_id, hgnc_id, seq_source, mol_type, mapped_flanked_exon_coords, mapped_intron_coords, chromosome) 
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
						dest='file')
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
	parser.add_argument('-i',
						'--introns',
						action='store_true', 
						help="If present, outputs intron coordinates instead of exon coordinates")
	parser.add_argument('-fl',
						'--flank', 
						type=int,
						help="If present, output coordinates include flanking regions")

						
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

	arguments = arg_collection()
	main(arguments)



# REMOVED
#lrg_id = xml_file.rstrip('.xml')
#check_lrg_object_contents(lrg_object)

