
import os
import io
import sys
import unittest
from unittest import TestCase
from unittest.mock import patch

import lrg_webservices as ws
import lrgparser as lrgp
import ui as ui
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
		"""Checks that the LRG ID returned by the LRG website is correct """
		self.assertEqual(ws.search_by_hgnc("invalid_hgnc"), None)

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
		test_xml = open(self.xml_path_full)
		root = lrgp.get_tree_and_root_file(test_xml)
		test_xml.close()
		self.assertEqual(root.tag, "lrg")

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
						[23904870, 23904829])
		self.assertEqual(lrg_object.mapped_flanked_exon_coords.get(40),
						[23882080, 23881947])

	def test_arg_collection(self):
		"""Tests that arguments passed to the argument parsing function are
		correctly captured
		"""
		arguments = lrgp.arg_collection(['-l LRG_384'])
		self.assertEqual(arguments.get("lrgid"), " LRG_384")


class UITests(TestCase):
	"""Tests designed to test the functions contained within the
	ui.py file. User input with input() is simulated using unittest.mock
	"""

	def setUp(self):
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

	def test_splashscreen(self):
		"""Checks that the splashscreen correctly returns. Functions without
		a return statement will return None if completed successfully.
		"""
		self.assertEqual(ui.splashscreen(True), None)

	@patch('ui.input', return_value='MYH7')
	def test_ask_what_gene(self, input):
		"""Check that the ask_what_gene() function correctly returns the
		string that the	user enters.
		"""
		self.assertEqual(ui.ask_what_gene(), "MYH7")

	@patch('ui.input', return_value="1")
	def test_ask_which_genome_build(self, input):
		"""Check that the ask_which_genome() function correctly returns the 
		string that the	user enters.
		"""
		availablebuilds = ['GRCh37.p13', 'GRCh38.p12']
		self.assertEqual(ui.ask_which_genome_build(availablebuilds),
													 "GRCh37.p13")

	@patch('ui.input', return_value="1")
	def test_ask_which_transcript(self, input):
		"""Check that the ask_which_transcript() function correctly returns 
		the string that the	user enters. 
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
		"""Check that the ask_which_transcript() function correctly handles 
		invalid input followed by valid input
		"""
		self.assertEqual(ui.ask_include_introns(), True)

	@patch('ui.input', return_value="n")
	def test_ask_include_introns_no(self, input):
		"""Check that the ask_include_introns() function correctly returns 
		False when chosen
		"""
		self.assertEqual(ui.ask_include_introns(), False)

	@patch('ui.input', side_effect=["badinput", "100000", "150"])
	def test_ask_flank_size(self, input):
		"""Check that the ask_flank_size() function correctly handles
		invalid input (string and then an int over the max allowed) 
		followed by returning a valid input value when provided (150) 
		"""
		self.assertEqual(ui.ask_flank_size(), "150")



if __name__ == '__main__':
	unittest.main(buffer=True)