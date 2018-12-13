
import unittest

import lrg_webservices as ws

class WebServicesTests(unittest.TestCase):
	
	def test_hgnc_search(self):
		self.assertEqual(ws.search_by_hgnc("MYH7"), "LRG_384")


if __name__ == '__main__':
	unittest.main()