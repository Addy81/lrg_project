
import os
import unittest

import lrg_webservices as ws
import lrgparser as lrgp
import xml.etree.ElementTree as ET


class WebServicesTests(unittest.TestCase):
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

	def test_lrg_xml_file(self):
		"""Checks that the LRG file returned by the LRG website has the 
		correct ID 
		"""
		test_xml = open(self.xml_path_full)
		test_xml_contents = test_xml.read()
		test_xml.close()
		self.assertIn("LRG_384", test_xml_contents)



class LRGParserTests(unittest.TestCase):
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
		lrg_xml = ws.search_by_lrg("LRG_384")
		root = lrgp.get_tree_and_root_string(lrg_xml)
		self.assertEqual(root.tag, "lrg")

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
		self.assertEqual(lrg_object.mapped_flanked_exon_coords.get(1), [23904870, 23904829])
		self.assertEqual(lrg_object.mapped_flanked_exon_coords.get(40), [23882080, 23881947])

if __name__ == '__main__':
	unittest.main()