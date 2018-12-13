
import os
import unittest

import lrg_webservices as ws
import lrgparser as lrgp
import xml.etree.ElementTree as ET


class WebServicesTests(unittest.TestCase):
	""" Tests designed to test the functions contained within the
	lrg_webservices.py file.
	"""

	def test_hgnc_search(self):
		""" Checks that the LRG ID returned by the LRG website is correct """
		self.assertEqual(ws.search_by_hgnc("MYH7"), "LRG_384")

	def test_lrg_xml_file(self):
		""" Checks that the LRG file returned by the LRG website has the 
		correct ID 
		"""
		this_directory_path = os.path.dirname(__file__)
		test_xml_path = "testfiles/LRG_384.xml"
		test_xml = open(this_directory_path + test_xml_path)
		test_xml_contents = test_xml.read()
		self.assertIn("LRG_384", test_xml_contents)



class LRGParserTests(unittest.TestCase):
	""" Tests designed to test the functions contained within the
	lrgparser.py file.
	"""

	def test_get_tree_and_root_file(self):
		""" Tests that a file passed to the get_tree_and_root_file function
		returns a root object with a single root tag - "lrg"
		"""
		this_directory_path = os.path.dirname(__file__)
		test_xml_path = "testfiles/LRG_384.xml"
		test_xml = open(this_directory_path + test_xml_path)
		root = lrgp.get_tree_and_root_file(test_xml)
		self.assertEqual(root.tag, "lrg")



if __name__ == '__main__':
	unittest.main()