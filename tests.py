
import os
import unittest

import lrg_webservices as ws


class WebServicesTests(unittest.TestCase):
	""" Tests designed to test the functions contained within the
	lrg_webservices.py file.
	"""

	def test_hgnc_search(self):
		""" Checks that the LRG ID returned by the LRG website is correct """
		self.assertEqual(ws.search_by_hgnc("MYH7"), "LRG_384")

	def test_lrg_xml_file(self):
		""" Checks that the LRG file returned by the LRG website is correct """
		this_directory_path = os.path.dirname(__file__)
		test_xml_path = "testfiles/LRG_384.xml"
		test_xml = open(this_directory_path + test_xml_path)
		test_xml_contents = test_xml.read()
		self.assertIn("LRG_384", test_xml_contents)



if __name__ == '__main__':
	unittest.main()