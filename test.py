
import os
import io
import sys
import unittest
from unittest import TestCase
from unittest.mock import patch

import lrg_webservices as ws
import lrgparser as lrgp
import ui as ui
import bedgen as bg
import functions
import xml.etree.ElementTree as ET


class WebServicesTests(TestCase):
	"""Tests designed to test the functions contained within the
	lrg_webservices.py file.
	"""
	
	def setUp(self):
		self.this_directory_path = os.path.dirname(__file__)
		self.xml_path_relative = "testfiles/LRG_384.xml"
		self.xml_path_full = self.this_directory_path + self.xml_path_relative

	def test_hgnc_search(self):
		"""Checks that the LRG ID returned by the LRG website is correct """
		self.assertEqual(ws.search_by_hgnc("MYH7"), "LRG_384")

	def test_invalid_hgnc_search(self):
		"""Checks that a SystemExit is raised when invalid input is provided"""
		with self.assertRaises(SystemExit) as se:
			ws.search_by_hgnc("invalid_hgnc")

	def test_invalid_search_by_lrg(self):
		"""Checks that a SystemExit is raised when invalid input is provided"""
		with self.assertRaises(SystemExit) as se:
			ws.search_by_lrg("invalid_lrg")

	def test_lrg_xml_file(self):
		"""Checks that the LRG file returned by the LRG website has the 
		correct ID 
		"""
		test_xml = open(self.xml_path_full)
		test_xml_contents = test_xml.read()
		test_xml.close()
		self.assertIn("LRG_384", test_xml_contents)


class LRGParserTests(TestCase):
	"""Tests designed to test the functions contained within the
	lrgparser.py file.
	"""

	def setUp(self):
		self.this_directory_path = os.path.dirname(__file__)
		self.xml_path_relative = "testfiles/LRG_384.xml"
		self.xml_path_full = self.this_directory_path + self.xml_path_relative

	def test_get_tree_and_root_file(self):
		"""Tests that a file passed to the get_tree_and_root_file 
		function returns a root object with a single root tag - "lrg"
		"""
		root = lrgp.get_tree_and_root_file(str(self.xml_path_full))
		self.assertEqual(root.tag, "lrg")

	def test_invalid_get_tree_and_root_file(self):
		"""Tests that a file passed to the get_tree_and_root_file 
		function returns a root object with a single root tag - "lrg"
		"""
		with self.assertRaises(SystemExit) as se:
			lrgp.get_tree_and_root_file(str("fakefilepath"))

	def test_get_tree_and_root_string(self):
		"""Tests that a string passed to the get_tree_and_root_string
		function returns a root object with a single root tag - "lrg"
		"""
		try:
			lrg_xml = ws.search_by_lrg("LRG_384")
			root = lrgp.get_tree_and_root_string(lrg_xml)
			self.assertEqual(root.tag, "lrg")
		except Exception as e:
			self.fail("Error querying the LRG site:", e)

	def test_get_genome_builds(self):
		"""Tests that the correct genome build numbers are extracted from
		an LRG xml file
		"""
		test_xml = open(self.xml_path_full)
		root = lrgp.get_tree_and_root_file(test_xml)
		test_xml.close()
		genomebuilds = lrgp.get_genome_builds(root)
		expected_genomebuilds = ['GRCh37.p13', 'GRCh38.p12']
		self.assertEqual(genomebuilds, expected_genomebuilds)

	def test_get_transcript_ids(self):
		"""Tests that the correct transcript IDs are extracted from
		an LRG xml file
		"""
		test_xml = open(self.xml_path_full)
		root = lrgp.get_tree_and_root_file(test_xml)
		test_xml.close()
		transcripts = lrgp.get_transcript_ids(root)
		expected_transcripts = ['NM_000257.2',
								'NM_000257.3',
								'ENST00000355349.3']
		self.assertEqual(transcripts, expected_transcripts)		

	def test_lrg_object_creator(self):
		"""Tests that an 'lrg_object' is created properly when using the
		lrg_object_creator function and LRG_Object class
		"""
		test_xml = open(self.xml_path_full)
		root = lrgp.get_tree_and_root_file(test_xml)
		test_xml.close()
		genome_choice = 'GRCh37.p13'
		transcript_choice = 'NM_000257.2'
		flank = 0
		lrg_object = lrgp.lrg_object_creator(root,
										genome_choice,
										transcript_choice,
										flank)
		self.assertEqual(lrg_object.lrg_id, 'LRG_384')
		self.assertEqual(lrg_object.hgnc_id, '7577')
		self.assertEqual(lrg_object.seq_source, 'NG_007884.1')
		self.assertEqual(lrg_object.mol_type, 'dna')
		self.assertEqual(lrg_object.chromosome, '14')
		self.assertEqual(lrg_object.mapped_flanked_exon_coords.get(1),
						[23904870, 23904828])
		self.assertEqual(lrg_object.mapped_flanked_exon_coords.get(40),
						[23882080, 23881946])

	def test_arg_collection(self):
		"""Tests that arguments passed to the argument parsing function are
		correctly captured
		"""
		arguments = lrgp.arg_collection(['-l LRG_384'])
		self.assertEqual(arguments.get("lrgid"), " LRG_384")


	@patch('bedgen.write_bed_file', return_value=True)
	def test_automated_main(self, write_bed_file):
		"""Tests the lrgparser main() function using sufficient arguments
		for automated BED file generation. The writing of the physical file is
		prevented using the @patch decorator to avoid unwanted file generation
		"""
		arguments_full = lrgp.arg_collection(["-f", "testfiles/LRG_384.xml", 
											"-r", "GRCh37.p13", 
											"-t", "NM_000257.2"])
		arguments_full_introns = lrgp.arg_collection(["-f", "testfiles/LRG_384.xml",
													"-r", "GRCh37.p13",
													"-t", "NM_000257.2", 
													"-i"])
		arguments_full_flank = lrgp.arg_collection(["-f", "testfiles/LRG_384.xml",
													"-r", "GRCh37.p13",
													"-t", "NM_000257.2",
													"-fl", "200"])
		self.assertEqual(lrgp.main(arguments_full), True)
		self.assertEqual(lrgp.main(arguments_full_introns), True)
		self.assertEqual(lrgp.main(arguments_full_flank), True)


	@patch('ui.input', side_effect=["MYH7", "1", "1", "0", "y"])
	@patch('bedgen.write_bed_file', return_value=True)
	@patch('os.system', return_value="")
	def test_nonautomated_main(self, input, write_bed_file, system):
		"""Tests the lrgparser main() function using insufficient arguments
		for automated BED file generation. ui.input is patched to simulate
		user input for gene name, genome selection, transcript selection,
		flank size and intron inclusion. The writing of the physical file is
		prevented using the @patch decorator to avoid unwanted file generation
		"""
		arguments = lrgp.arg_collection([])
		self.assertEqual(lrgp.main(arguments), True)



class BedgenTests(TestCase):
	"""Tests to designed to test the functions contained within the
	bedgen.py file.
	"""
	def setUp(self):
		self.this_directory_path = os.path.dirname(__file__)
		self.xml_path_relative = "testfiles/LRG_384.xml"
		self.xml_path_full = self.this_directory_path + self.xml_path_relative
	

	def test_create_bed_contents(self):
		"""Tests that the contents of the BED file are correctly generated
		with accurate values
		"""
		test_xml = open(self.xml_path_full)
		root = lrgp.get_tree_and_root_file(test_xml)
		test_xml.close()
		genome_choice = 'GRCh37.p13'
		transcript_choice = 'NM_000257.2'
		flank = 0
		lrg_object = lrgp.lrg_object_creator(root,
										genome_choice,
										transcript_choice,
										flank)
		bedcontents_nointrons = bg.create_bed_contents(lrg_object, False)
		bedcontents_introns = bg.create_bed_contents(lrg_object, True)
		self.assertEqual(len(bedcontents_nointrons), 40)
		self.assertEqual(len(bedcontents_introns), 79)
		self.assertEqual(bedcontents_nointrons[0], 
						['chr14', 23904828, 23904870, "Exon_1"])
		self.assertEqual(bedcontents_nointrons[39], 
						['chr14', 23881946, 23882080, "Exon_40"])
		self.assertEqual(bedcontents_introns[40],
						['chr14', 23903459, 23904827, 'Intron_1'])
		self.assertEqual(bedcontents_introns[78],
						['chr14', 23882081, 23882966, 'Intron_39'])

	def test_write_bed_file(self):
		"""Tests that the BED file can be written to the local disk"""
		filepath = "testfilename"
		bedheader = ["header_item_1", "header_item_2"]
		bedcontents = [['chr14', 23881946, 23882080, "Exon_1"],
						['chr14', 23881946, 23882080, "Exon_40"]]
		success = bg.write_bed_file(filepath, bedheader, bedcontents)
		self.assertEqual(success, True)
		os.remove(filepath)
		with self.assertRaises(SystemExit) as se:
			bg.write_bed_file(None, bedheader, bedcontents)



class FunctionsTests(TestCase):
	""" Tests that the functions that handle exon and intron coordinates
	create dictionaries containing the correct values.
	"""
	
	def setUp(self):
		self.this_directory_path = os.path.dirname(__file__)
		self.xml_path_relative = "testfiles/LRG_384.xml"
		self.xml_path_full = self.this_directory_path + self.xml_path_relative
		self.xml_path_relative_pos = "testfiles/LRG_155.xml"
		self.xml_path_full_pos = self.this_directory_path + self.xml_path_relative_pos

	def test_get_exon_coords(self):
		""" Tests that assess the creation of the exon_coords dictionary
		"""
		test_xml = open(self.xml_path_full)
		root = lrgp.get_tree_and_root_file(test_xml)
		test_xml.close()

		test_xml_pos = open(self.xml_path_full_pos)
		root_pos = lrgp.get_tree_and_root_file(test_xml_pos)
		test_xml_pos.close()

		genome_choice = 'GRCh37.p13'
		transcript_choice = 'NM_000257.2'
		pos_transcript_choice = 'NM_002389.4'

		exon_coordinates = functions.get_exon_coords(root,
													genome_choice,
													transcript_choice)
		pos_exon_coordinates = functions.get_exon_coords(root_pos,
														genome_choice,
														pos_transcript_choice)

		self.assertEqual(type(exon_coordinates),dict)
		self.assertEqual(len(exon_coordinates), 40)
		self.assertEqual(exon_coordinates[1],[23904870,23904828])
		self.assertEqual(exon_coordinates[40],[23882080,23881946])

		self.assertEqual(type(pos_exon_coordinates),dict)
		self.assertEqual(len(pos_exon_coordinates), 14)

	def test_get_intron_coords(self):
		""" Tests that assess the creation of the intron_coords dictionary
		"""
		test_xml = open(self.xml_path_full)
		root = lrgp.get_tree_and_root_file(test_xml)
		test_xml.close()

		test_xml_pos = open(self.xml_path_full_pos)
		root_pos = lrgp.get_tree_and_root_file(test_xml_pos)
		test_xml_pos.close()

		genome_choice = 'GRCh37.p13'
		transcript_choice = 'NM_000257.2'
		pos_transcript_choice = 'NM_002389.4'
		
		
		exon_coordinates = functions.get_exon_coords(root,
													genome_choice,
													transcript_choice)
		intron_coordinates = functions.get_intron_coords(exon_coordinates)
		
		self.assertEqual(type(intron_coordinates),dict)
		self.assertEqual(len(intron_coordinates), 39)
		self.assertEqual(intron_coordinates[1],[23904827,23903459])
		self.assertEqual(intron_coordinates[39],[23882966,23882081])
	
		pos_exon_coordinates = functions.get_exon_coords(root_pos,
														genome_choice,
														pos_transcript_choice)
		pos_intron_coordinates = functions.get_intron_coords(pos_exon_coordinates)
		
		self.assertEqual(type(pos_intron_coordinates),dict)
		self.assertEqual(len(pos_intron_coordinates), 13)

	def test_get_flanked_coords(self):
		""" Tests that asses the creation of the exon_coords dictionary when
		flanking regions are used.
		"""
		test_xml = open(self.xml_path_full)
		root = lrgp.get_tree_and_root_file(test_xml)
		test_xml.close()
		
		test_xml_pos = open(self.xml_path_full_pos)
		root_pos = lrgp.get_tree_and_root_file(test_xml_pos)
		test_xml_pos.close()

		genome_choice = 'GRCh37.p13'
		transcript_choice = 'NM_000257.2'
		pos_transcript_choice = 'NM_002389.4'
		
		exon_coordinates = functions.get_exon_coords(root,
													genome_choice,
													transcript_choice)
		flanked_coordinates = functions.get_flanked_coords(exon_coordinates,
															100)

		self.assertEqual(type(flanked_coordinates),dict)
		self.assertEqual(len(flanked_coordinates), 40)
		
		pos_exon_coordinates = functions.get_exon_coords(root_pos,
														genome_choice,
														pos_transcript_choice)
		pos_flanked_coordinates = functions.get_flanked_coords(pos_exon_coordinates,
																100)

		self.assertEqual(type(pos_flanked_coordinates),dict)
		self.assertEqual(len(pos_flanked_coordinates), 14)
		self.assertEqual(pos_flanked_coordinates[1],[207925282,207925754])
		self.assertEqual(pos_flanked_coordinates[14],[207966763,207968961])
		

class UITests(TestCase):
	"""Tests designed to test the functions contained within the
	ui.py file. User input with input() is simulated using the @patch
	decorator from unittest.mock
	"""

	def setUp(self):
		"""Create some dictionaries to be used as arguments in the tests.
		"""
		self.args_none = {'file': None, 'geneid': None, 'lrgid': None}
		self.args = {'file': "test", 'geneid': "7577", 'lrgid': "LRG_384"}

	def test_determine_if_show_ui_true(self):
		"""Check that the UI will be shown if no file, geneid or lrgid is
		provided
		"""
		self.assertEqual(ui.determine_if_show_ui(self.args_none), True)

	def test_determine_if_show_ui_false(self):
		"""Check that the UI will not be shown if a file, geneid or lrgid is
		provided
		"""
		self.assertEqual(ui.determine_if_show_ui(self.args), False)

	@patch('ui.os.system', return_value=None)
	def test_splashscreen(self, systemreplace):
		"""Checks that the splashscreen correctly returns. Functions without
		a return statement will return None if completed successfully.
		"""
		self.assertEqual(ui.splashscreen(), None)

	@patch('ui.input', return_value='MYH7')
	def test_ask_what_gene(self, input):
		"""Check that the ask_what_gene() function correctly returns the
		string that the	user enters.
		"""
		self.assertEqual(ui.ask_what_gene(), "MYH7")

	@patch('ui.input', side_effect=["badinput", "10", "1"])
	def test_ask_which_genome_build(self, input):
		"""Check that the ask_which_genome() function correctly returns the 
		string that the	user enters.
		"""
		availablebuilds = ['GRCh37.p13', 'GRCh38.p12']
		self.assertEqual(ui.ask_which_genome_build(availablebuilds),
													 "GRCh37.p13")

	@patch('ui.input', side_effect=["badinput", "10", "1"])
	def test_ask_which_transcript(self, input):
		"""Check that the ask_which_transcript() function correctly handles 
		invalid input (string then number choice that is too large)
		followed by a valid transcript. 
		"""
		availabletranscripts = ["NM_000257.2", 
								"NM_000257.4",
								"ENST00000355349.3"]
		self.assertEqual(ui.ask_which_transcript(availabletranscripts),
													 "NM_000257.2")

	@patch('ui.input', return_value="y")
	def test_ask_include_introns_yes(self, input):
		"""Check that the ask_include_introns() function correctly returns 
		True when chosen
		"""
		self.assertEqual(ui.ask_include_introns(), True)

	@patch('ui.input', side_effect=["badinput", "y"])
	def test_ask_include_introns_invalid(self, input):
		"""Check that the ask_include_introns() function correctly handles 
		invalid input followed by valid input
		"""
		self.assertEqual(ui.ask_include_introns(), True)

	@patch('ui.input', return_value="n")
	def test_ask_include_introns_no(self, input):
		"""Check that the ask_include_introns() function correctly returns 
		False when chosen
		"""
		self.assertEqual(ui.ask_include_introns(), False)

	@patch('ui.input', side_effect=["badinput", "-10", "150"])
	def test_ask_flank_size(self, input):
		"""Check that the ask_flank_size() function correctly handles
		invalid input (string and then an int over the max allowed) 
		followed by returning a valid input value when provided (150) 
		"""
		self.assertEqual(ui.ask_flank_size(), "150")



if __name__ == '__main__':
	unittest.main(buffer=True)